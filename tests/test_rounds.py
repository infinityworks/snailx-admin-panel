import unittest
from globals.globals import app
from unittest import mock
from unittest.mock import MagicMock
import datetime


class MockRound():
    def __init__(self):
        self.id = 1
        self.name = "Mike Round"
        self.start_date = datetime.datetime.now()
        self.end_date = datetime.datetime.now()


class TestRounds(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    @mock.patch('flask_login.utils._get_user')
    def test_rounds_page_response_is_200(self, current_user):
        with self.client as client:
            current_user.is_authenticated = True
            response = client.get("/rounds")
            self.assertEqual(200, response.status_code)

    @mock.patch("db.models.Round.get_all_rounds", MagicMock(return_value=[MockRound(), MockRound()]))
    @mock.patch('flask_login.utils._get_user')
    def test_rounds_are_displayed(self, current_user):
        with self.client as client:
            current_user.is_authenticated = True
            response = client.get('/rounds')
            self.assertIn(b"Mike Round", response.data)
