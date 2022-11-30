import unittest

from app import app

class BaseTestClass(unittest.TestCase):

    def setUp(self):
        app.testing = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()