# coding: utf-8

"""   
    unittest base
    ~~~~~~~~~~~~~
    
    :copyleft: 2009 by the django-dbpreferences team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""

import os
import sys
import unittest

from django.core import management
from django.utils.encoding import smart_str
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType

from BrowserDebug import debug_response



class BaseTestCase(unittest.TestCase):
    # Should we open a bwoser traceback?
    browser_traceback = True

    TEST_USERS = {
        "superuser": {
            "username": "superuser",
            "email": "superuser@example.org",
            "password": "superuser_password",
            "is_staff": True,
            "is_superuser": True,
        },
        "staff": {
            "username": "staff test user",
            "email": "staff_test_user@example.org",
            "password": "staff_test_user_password",
            "is_staff": True,
            "is_superuser": False,
        },
        "normal": {
            "username": "normal test user",
            "email": "normal_test_user@example.org",
            "password": "normal_test_user_password",
            "is_staff": False,
            "is_superuser": False,
        },
    }

    def _pre_setup(self):
        super(BaseTestCase, self)._pre_setup()

    def login(self, usertype):
        """
        Login the user defined in self.TEST_USERS
        return User model instance
        """
        test_user = self._get_userdata(usertype)

        ok = self.client.login(username=test_user["username"],
                               password=test_user["password"])
        self.failUnless(ok, "Can't login test user '%s'!" % usertype)
        return self._get_user(usertype)

    def add_user_permissions(self, user, permissions):
        """
        add permissions to the given user instance.
        permissions e.g.: ("AppLabel.add_Modelname", "auth.change_user")
        """
        assert(permissions, (list, tuple))
        for permission in permissions:
            # permission, e.g: blog.add_blogentry
            app_label, permission_codename = permission.split(".", 1)
            model_name = permission_codename.split("_", 1)[1]

            try:
                content_type = ContentType.objects.get(app_label=app_label, model=model_name)
            except ContentType.DoesNotExist:
                etype, evalue, etb = sys.exc_info()
                evalue = etype("Can't get ContentType for app %r and model %r: %s" % (
                    app_label, model_name, evalue
                ))
                raise etype, evalue, etb


            perm = Permission.objects.get(content_type=content_type, codename=permission_codename)
            user.user_permissions.add(perm)
            user.save()

        self.assertTrue(user.has_perms(permissions))

    def _get_userdata(self, usertype):
        """ return userdata from self.TEST_USERS for the given usertype """
        try:
            return self.TEST_USERS[usertype]
        except KeyError, err:
            etype, evalue, etb = sys.exc_info()
            evalue = etype(
                "Wrong usetype %s! Existing usertypes are: %s" % (err, ", ".join(self.TEST_USERS.keys()))
            )
            raise etype, evalue, etb

    def _get_user(self, usertype):
        """ return User model instance for the goven usertype"""
        test_user = self._get_userdata(usertype)
        return User.objects.get(username=test_user["username"])

    def _create_testusers(self):
        """ Create all available testusers. """
        def create_user(username, password, email, is_staff, is_superuser):
            """
            Create a user and return the instance.
            """
            defaults = {'password':password, 'email':email}
            user, created = User.objects.get_or_create(
                username=username, defaults=defaults
            )
            if not created:
                user.email = email
            user.set_password(password)
            user.is_staff = is_staff
            user.is_superuser = is_superuser
            user.save()
        for usertype, userdata in self.TEST_USERS.iteritems():
            create_user(**userdata)

    def raise_browser_traceback(self, response, msg):
        debug_response(
            response, self.browser_traceback, msg, display_tb=False
        )
        msg += " (url: %r)" % response.request.get("PATH_INFO", "???")
        raise self.failureException, msg

    def assertStatusCode(self, response, excepted_code=200):
        """
        assert response status code, if wrong, do a browser traceback.
        """
        if response.status_code == excepted_code:
            return # Status code is ok.
        msg = "assertStatusCode error: %r != %r" % (response.status_code, excepted_code)
        self.raise_browser_traceback(response, msg)

    def assertRedirect(self, response, url, status_code=302):
        """
        assert than response is a redirect to the right destination, if wrong, do a browser traceback.
        """
        self.assertStatusCode(response, excepted_code=status_code)
        try:
            location = response['Location']
        except KeyError, err:
            self.raise_browser_traceback(response, "No 'Location' in response: %s" % err)
        else:
            if location != url:
                self.raise_browser_traceback(response, "Wrong destination url: %r != %r" % (location, url))

    def assertResponse(self, response, must_contain=(), must_not_contain=()):
        """
        Check the content of the response
        must_contain - a list with string how must be exists in the response.
        must_not_contain - a list of string how should not exists.
        """
        for txt in must_contain:
            txt = smart_str(txt, response._charset)
            if not txt in response.content:
                self.raise_browser_traceback(response, "Text not in response: '%s'" % txt)

        for txt in must_not_contain:
            txt = smart_str(txt, response._charset)
            if txt in response.content:
                self.raise_browser_traceback(response, "Text should not be in response: '%s'" % txt)


def direct_run(raw_filename):
    """
    Run a test direct from a unittest file.
    A unittest file should add something like this:
    
    if __name__ == "__main__":
        # Run this unitest directly
        direct_run(__file__)
    """
    appname = os.path.splitext(os.path.basename(raw_filename))[0]
    print "direct run %r" % appname
    management.call_command('test', appname)
