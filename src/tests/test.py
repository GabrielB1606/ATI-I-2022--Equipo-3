from . import BaseTestClass
from config import database_hook

# python -m unittest

class TestHello(BaseTestClass):

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

    # Test 2. Register Correct: EMAIL, PASSWORD, CONFIRM were given
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

        database_hook["usuarios"].delete_one({'email':'test@mail.com'})

    # Test 3. Correct redirect to Facebook Login in 
    def test_loginFacebook(self):
        rv = self.app.get('/facebook')
        self.assertEqual(rv.status, '308 PERMANENT REDIRECT')