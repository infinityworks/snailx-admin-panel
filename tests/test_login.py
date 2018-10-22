import unittest
from globals.globals import app
from unittest import mock
from unittest.mock import MagicMock
from routes.login.login import get_username

class MockUser:
    def __init__(self, id, username, email, password):
        self.id = id
        self.username = username
        self.email = email
        self.password = password

#TODO mock a login form here!

class TestLogin(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    def test_login_page_response(self):
        with self.client as client:
            response = client.get("/login")
            self.assertEqual(200, response.status_code)
    
    # def test_successful_login(self):
    #     with self.client as client:
    #         response = self.client.post("/login", data=dict(username="sandeep", password="yes"), follow_redirects=True)
    #         self.assertIn(b"Hello World", response.data)

    @mock.patch("routes.login.login.get_username", MagicMock(return_value=MockUser(1, "Bob", "bob@bob.com", "bob")))
    def test_successful_login(self):  
        with self.client as client:
            response = self.client.post("/login", follow_redirects=True)
            self.assertIn(b"Hello World", response.data)



    # def test_unsuccessful_login(self):
    #     with self.client as client:
    #         response = self.client.post("/login", data=dict(username="bob", password="no"), follow_redirects=True)
    #         self.assertIn(b"Login Unsuccessful", response.data)
           
    # def test_authenticated_user(self):
    #     with self.client as client:
    #         response = self.client.get("/", data=dict(username="sandeep"), follows_redirect=True)


if __name__ == '__main__':
    unittest.main()
