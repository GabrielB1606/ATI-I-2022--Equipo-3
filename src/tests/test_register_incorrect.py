from . import BaseTestClass
from config import database_hook

# python -m unittest

class TestRegister(BaseTestClass):

    # Test 1. Register Incorrect: NAME missing
    def test_register_incorrect(self):
        response = self.app.post('/sign_in', data={
            'email':'test@mail.com',
            'password':'12345678',
            'confirm':'12345678',
            'name':''
        }, follow_redirects = True)

        user = database_hook["usuarios"].find_one({'email':'test@mail.com'})

        self.assertEqual(user, None)
        self.assertEqual(response.request.path, '/sign_in')