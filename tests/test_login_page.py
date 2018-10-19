import unittest
from globals.globals import app


class TestLoginPage(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    def test_login_page_response(self):
        with self.client as client:
            response = client.get("/login")
            self.assertEqual(200, response.status_code)

    def test_login_page_contents(self):
        with self.client as client:
            response = client.get("/login")
            self.assertIn(b'Sign In', response.data)


if __name__ == '__main__':
    unittest.main()
