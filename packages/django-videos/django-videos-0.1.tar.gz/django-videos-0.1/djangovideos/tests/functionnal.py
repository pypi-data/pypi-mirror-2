# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django_webtest import WebTest
from webtest import Form
from djangovideos import models

__all__ = ('WebTest', 'UserWebTest', 'models', 'reverse')

class UserWebTest(WebTest):

    login = 'user1'
    extra_environ = {'REMOTE_USER': login}
    user = None

    def setUp(self):
        super(UserWebTest, self).setUp()
        user = models.User.objects.create_user(self.login, '%s@example.com' % self.login)
        user.is_superuser = True
        user.save()
        self.user = user

