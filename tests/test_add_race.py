import unittest
from globals.globals import app
from unittest import mock
from unittest.mock import MagicMock


class TestAddRace(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_add_race_response_is_200(self):
        with self.client as client:
            response = client.get("/rounds/1/races/add")
            self.assertEqual(200, response.status_code)

    @mock.patch("")
    def test_add_race_form_redirects_to_rounds(self):
        with self.client as client:
            response = client.post('/rounds/1/race/add', data={"status": "TEST STATUS", "date": "10/25/2018 12:00 AM"})
            self.assertIn("TEST STATUS", response.data)