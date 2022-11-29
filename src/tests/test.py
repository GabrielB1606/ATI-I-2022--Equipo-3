from . import BaseTestClass
from flask import url_for, request
# python -m unittest

class TestHello(BaseTestClass):

    def test_hello(self):
        rv = self.app.get('/login')
        self.assertEqual(rv.status, '200 OK')
        # self.assertEqual(rv.data, b'Hello World!\n')

    def test_loginFacebook(self):
        rv = self.app.get('/facebook')
        self.assertEqual(rv.status, '308 PERMANENT REDIRECT')

