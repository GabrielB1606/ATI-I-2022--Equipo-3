from . import BaseTestClass
from config import database_hook

# python -m unittest
class TestRegister(BaseTestClass):
    # Test Register Correct: EMAIL, PASSWORD, CONFIRM were given
    def test_register_correct(self):
        response = self.app.post('/sign_in', data={
            'email':'test@mail.com',
            'password':'12345678',
            'confirm':'12345678',
            'name':'Johny Test'
        }, follow_redirects = True)

        user = database_hook["usuarios"].find_one({'email':'test@mail.com'})

        self.assertNotEqual(user, None)
        self.assertEqual(user['email'], 'test@mail.com')
        self.assertEqual(response.request.path, '/')

class TestLoginFacebook(BaseTestClass):
    # Test Correct redirect to Facebook Login in 
    def test_loginFacebook(self):
        rv = self.app.get('/facebook')
        self.assertEqual(rv.status, '308 PERMANENT REDIRECT')
