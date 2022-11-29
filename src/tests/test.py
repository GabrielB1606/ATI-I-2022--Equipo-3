from . import BaseTestClass

# python -m unittest

class TestHello(BaseTestClass):

    def test_hello(self):
        rv = self.app.get('/login')
        self.assertEqual(rv.status, '200 OK')
        # self.assertEqual(rv.data, b'Hello World!\n')