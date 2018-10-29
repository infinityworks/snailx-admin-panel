import unittest
from globals.globals import app
from unittest import mock
from unittest.mock import MagicMock
from flask_login import current_user


class TestLogout(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    def test_logout_page_response(self):
        with self.client as client:
            response = client.get("/")
            self.assertEqual(200, response.status_code)
    
    @mock.patch('routes.login.logout.is_active', MagicMock(return_value=True))
    def test_successful_logout(self):  
        with self.client as client:
            client.post("/", follow_redirects=True)
            response = client.get("/logout", follow_redirects=True)
            self.assertFalse(current_user.is_active)
            self.assertIn(b"Logout successful.", response.data)

    def test_login_required_for_logout(self):  
        with self.client as client:
            response = client.get("/logout", follow_redirects=True)
            self.assertIn(b"No user currently logged in.", response.data)


if __name__ == '__main__':
    unittest.main()
