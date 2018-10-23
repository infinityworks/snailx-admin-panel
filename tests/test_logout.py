import unittest
from globals.globals import app
from unittest import mock
from unittest.mock import MagicMock
from globals.globals import bcrypt
from flask_login import logout_user, current_user, UserMixin

class MockUser(UserMixin):
    def __init__(self, id, username, email, password):
        self.id = id
        self.username = username
        self.email = email
        self.password = password

class TestLogout(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()


    @mock.patch("flask_login.logout_user", MagicMock(return_value=True))
    def test_logout_page_response(self):
        with self.client as client:
            response = client.get("/login")
            self.assertEqual(200, response.status_code)
    
    @mock.patch("routes.login.login.get_username", MagicMock(return_value=MockUser(1, "Bob", "bob@bob.com", bcrypt.generate_password_hash("bob").decode("utf-8"))))
    @mock.patch("routes.login.login.login_user", MagicMock(return_value=True))    
    @mock.patch("flask_login.login_user", MagicMock(return_value=True))
    def test_successful_logout(self):  
        with self.client as client:
            response = client.get("/logout", follow_redirects=True)
            self.assertIn(b"Logout successful.", response.data)


    @mock.patch("flask_login.login_user", MagicMock(return_value=False))
    def test_login_required_for_logout(self):  
        with self.client as client:
            response = client.get("/logout", follow_redirects=True)
            self.assertIn(b"Unauthorized", response.data)


if __name__ == '__main__':
    unittest.main()
