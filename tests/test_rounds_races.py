import unittest
from globals.globals import app
from unittest import mock
from unittest.mock import MagicMock
import datetime


class MockRace:
    def __init__(self, id, date, status, id_round):
        self.id = id
        self.date = date
        self.status = status
        self.id_round = id_round


class TestRoundsRaces(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_rounds_races_page_response_is_200(self):
        with self.client as client:
            response = client.get("/rounds/1/races")
            self.assertEqual(200, response.status_code)

    @mock.patch("db.models.Race.get_races_by_round", MagicMock(return_value=[
        MockRace(1, datetime.datetime.now(), 'TEST_STATUS', 1),
        MockRace(2, datetime.datetime.now(), 'TEST_STATUS', 1),
        MockRace(3, datetime.datetime.now(), 'TEST_STATUS', 1)]))
    def test_races_are_displayed(self):
        with self.client as client:
            response = client.get("/rounds/1/races")
            self.assertIn(b"TEST_STATUS", response.data)

    @mock.patch("db.models.Race.get_races_by_round", MagicMock(return_value=[]))
    def test_no_races_are_displayed(self):
        with self.client as client:
            response = client.get('/round/5/races')
            self.assertNotIn(b"TEST_STATUS", response.data)