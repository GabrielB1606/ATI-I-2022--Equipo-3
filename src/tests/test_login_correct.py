from . import BaseTestClass
from config import database_hook

# python -m unittest

class TestLogin(BaseTestClass):


    # Test 1. Login Correct: Correct redirect to home
    def test_login_correct(self):
        response = self.app.post('/login', data={
            'email':'chachy.drs@gmail.com',
            'password':'28126743',
        }, follow_redirects = True)

        self.assertEqual(response.request.path, '/')
