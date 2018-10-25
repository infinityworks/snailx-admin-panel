import unittest
from globals.globals import app
from unittest import mock
from unittest.mock import MagicMock


class TestAddRace(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    @mock.patch('flask_login.utils._get_user')
    def test_add_race_response_is_200(self, username):
        with self.client as client:
            username.is_authenticated = True
            response = client.get("/rounds/1/races/add")
            self.assertEqual(200, response.status_code)

    @mock.patch('flask_login.utils._get_user')
    def test_add_race_form_redirects_to_rounds(self, username):
        with self.client as client:
            username.is_authenticated = True
            response = client.post('/rounds/1/races/add', data=dict(status="TEST STATUS", date="10/25/2018 12:00 AM"),
                                   follow_redirects=True)
            self.assertIn("Start Date", str(response.data))
