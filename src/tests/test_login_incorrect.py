from . import BaseTestClass
from config import database_hook

# python -m unittest

class TestLogin(BaseTestClass):


    def test_login_incorrect(self):
        response = self.app.post('/login', data={
            'email':'chachy.drs@gmail.com',
            'password':'281267423',
        }, follow_redirects = True)

        self.assertEqual(response.request.path, '/login')