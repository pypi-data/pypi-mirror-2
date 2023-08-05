# -*- coding: utf-8 -*-
from djangovideos.tests.functionnal import *
from djangovideos.models import Video

class TestFlashUrl(UserWebTest):

    value = "http://www.youtube.com/watch?v=ZFeHUdEQ1Zs"

    def test_index(self):
        resp = self.app.get(reverse('index'), user='user1')
        resp.mustcontain('submit')
        form = resp.form
        form['url'] = self.value
        resp = form.submit()
        resp = resp.follow()
        resp.mustcontain('<param name="movie" value="http://www.youtube.com/v/ZFeHUdEQ1Zs')

class TestObject(TestFlashUrl):

    value = '<object width="640" height="505"><param name="movie" value="http://www.youtube.com/v/ZFeHUdEQ1Zs&hl=fr_FR&fs=1&"></param><param name="allowFullScreen" value="true"></param><param name="allowscriptaccess" value="always"></param><embed src="http://www.youtube.com/v/ZFeHUdEQ1Zs&hl=fr_FR&fs=1&" type="application/x-shockwave-flash" allowscriptaccess="always" allowfullscreen="true" width="640" height="505"></embed></object>'
