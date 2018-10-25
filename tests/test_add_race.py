import unittest
from globals.globals import app
from unittest import mock
from unittest.mock import MagicMock


class TestAddRace(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_add_race_response_is_200(self):
        with self.client as client:
            response = client.get("/rounds/1/race/add")
            self.assertEqual(200, response.status_code)

    def test_add_race_form_redirects_to_rounds(self):
        with self.client as client:
            response = client.post('')