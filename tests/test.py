import app as app
import unittest


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.app

    def test_home(self):
        self.app.get('/')
        # Make your assertions
        
