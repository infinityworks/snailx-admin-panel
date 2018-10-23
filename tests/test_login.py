import unittest
from globals.globals import app
from unittest import mock
from unittest.mock import MagicMock
from globals.globals import bcrypt

class MockUser:
    def __init__(self, id, username, email, password):
        self.id = id
        self.username = username
        self.email = email
        self.password = password

class TestLogin(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    def test_login_page_response(self):
        with self.client as client:
            response = client.get("/login")
            self.assertEqual(200, response.status_code)
    
    @mock.patch("routes.login.login.get_username", MagicMock(return_value=MockUser(1, "Bob", "bob@bob.com", "bob")))
    @mock.patch("routes.login.login.bcrypt.check_password_hash", MagicMock(return_value=True))
    @mock.patch("routes.login.login.login_user", MagicMock(return_value=False))
    def test_successful_login(self):  
        with self.client as client:
            response = self.client.post("/login", data=dict(username="Bob", password="bob"), follow_redirects=True)
            self.assertIn(b"Hello World", response.data)

    @mock.patch("routes.login.login.get_username", MagicMock(return_value=MockUser(1, "Bob", "bob@bob.com", "bob")))
    @mock.patch("routes.login.login.bcrypt.check_password_hash", MagicMock(return_value=False))
    def test_unsuccessful_login(self):
        with self.client as client:
            response = self.client.post("/login", data=dict(username="Jon", password="bob"))
            self.assertIn(b"Login Unsuccessful", response.data)
           
    @mock.patch("routes.login.login.get_username", MagicMock(return_value=MockUser(1, "Bob", "bob@bob.com", bcrypt.generate_password_hash("bob").decode("utf-8"))))
    @mock.patch("routes.login.login.login_user", MagicMock(return_value=False))    
    def test_check_login_with_password(self):
        with self.client as client:
            response = self.client.post("/login", data=dict(username="Bob", password="bob"), follow_redirects=True)
            self.assertIn(b"Hello World", response.data)

    @mock.patch("routes.login.login.get_username", MagicMock(return_value=MockUser(1, "Bob", "bob@bob.com", bcrypt.generate_password_hash("fish").decode("utf-8"))))
    def test_check_login_with_incorrect_password(self):
        with self.client as client:
            response = self.client.post("/login", data=dict(username="Bob", password="bob"), follow_redirects=False)
            self.assertIn(b"Login Unsuccessful", response.data)


if __name__ == '__main__':
    unittest.main()
