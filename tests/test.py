import unittest
from globals.globals import app


class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
