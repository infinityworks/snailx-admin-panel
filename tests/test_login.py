import unittest
from globals.globals import app


class TestLogin(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    def test_index_page_response(self):
        with self.client as client:
            response = client.get("/login")
            self.assertEqual(200, response.status_code)
    
    def test_successful_login(self):
        with self.client as client:
            response = self.client.post("/login", data=dict(username="sandeep", password="yes"), follow_redirects=True)
            self.assertIn(b"Hello World", response.data)

    def test_unsuccessful_login(self):
        with self.client as client:
            response = self.client.post("/login", data=dict(username="bob", password="no"), follow_redirects=True)
            self.assertIn(b"Login Unsuccessful", response.data)
           
            


if __name__ == '__main__':
    unittest.main()
