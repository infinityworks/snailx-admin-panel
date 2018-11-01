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

    @mock.patch('flask_login.utils._get_user')
    def test_rounds_races_page_response_is_200(self, current_user):
        with self.client as client:
            current_user.is_authenticated = True
            response = client.get("/rounds/1/races")
            self.assertEqual(200, response.status_code)

    @mock.patch("db.models.Race.get_races_by_round", MagicMock(return_value=[
        MockRace(1, datetime.datetime.now(), 'TEST_STATUS', 1),
        MockRace(2, datetime.datetime.now(), 'TEST_STATUS', 1),
        MockRace(3, datetime.datetime.now(), 'TEST_STATUS', 1)]))
    @mock.patch('flask_login.utils._get_user')
    def test_races_are_displayed(self, current_user):
        with self.client as client:
            current_user.is_authenticated = True
            response = client.get("/rounds/1/races")
            self.assertIn(b"TEST_STATUS", response.data)

    @mock.patch("db.models.Race.get_races_by_round",
                MagicMock(return_value=[]))
    @mock.patch('flask_login.utils._get_user')
    def test_no_races_are_displayed(self, current_user):
        with self.client as client:
            current_user.is_authenticated = True
            response = client.get('/round/5/races')
            self.assertNotIn(b"TEST_STATUS", response.data)

    @mock.patch("routes.races.races.validate_current_round_not_started",
                MagicMock(return_value=False))
    @mock.patch("db.models.Race.get_races_by_round", MagicMock(return_value=[
        MockRace(1, datetime.datetime.now(), 'TEST_STATUS', 1),
        MockRace(2, datetime.datetime.now(), 'TEST_STATUS', 1),
        MockRace(3, datetime.datetime.now(), 'TEST_STATUS', 1)]))
    @mock.patch('flask_login.utils._get_user')
    def test_add_race_button_started_round(self, current_user):
        with self.client as client:
            current_user.is_authenticated = True
            response = self.client.get("/rounds/1/races")
            self.assertIn(b"add-race-disabled", response.data)

    @mock.patch("routes.races.races.validate_current_round_not_started",
                MagicMock(return_value=True))
    @mock.patch("db.models.Race.get_races_by_round", MagicMock(return_value=[
        MockRace(1, datetime.datetime.now(), 'TEST_STATUS', 1),
        MockRace(2, datetime.datetime.now(), 'TEST_STATUS', 1),
        MockRace(3, datetime.datetime.now(), 'TEST_STATUS', 1)]))
    @mock.patch('flask_login.utils._get_user')
    def test_add_race_button_future_round(self, current_user):
        with self.client as client:
            current_user.is_authenticated = True
            response = self.client.get("/rounds/1/races")
            self.assertIn(b"add-race-enabled", response.data)

    @mock.patch("routes.races.races.validate_current_round_not_started",
                MagicMock(return_value=False))
    @mock.patch("db.models.Race.get_races_by_round", MagicMock(return_value=[
        MockRace(1, datetime.datetime.now(), 'TEST_STATUS', 1),
        MockRace(2, datetime.datetime.now(), 'TEST_STATUS', 1),
        MockRace(3, datetime.datetime.now(), 'TEST_STATUS', 1)]))
    @mock.patch('flask_login.utils._get_user')
    def test_add_snail_button_started_round(self, current_user):
        with self.client as client:
            current_user.is_authenticated = True
            response = self.client.get("/rounds/1/races")
            self.assertIn(b"add-snail-disabled", response.data)

    @mock.patch("routes.races.races.validate_current_round_not_started",
                MagicMock(return_value=True))
    @mock.patch("db.models.Race.get_races_by_round", MagicMock(return_value=[
        MockRace(1, datetime.datetime.now(), 'TEST_STATUS', 1),
        MockRace(2, datetime.datetime.now(), 'TEST_STATUS', 1),
        MockRace(3, datetime.datetime.now(), 'TEST_STATUS', 1)]))
    @mock.patch('flask_login.utils._get_user')
    def test_add_snail_button_future_round(self, current_user):
        with self.client as client:
            current_user.is_authenticated = True
            response = self.client.get("/rounds/1/races")
            self.assertIn(b"add-snail-enabled", response.data)
            self.assertIn(b"add-results-disabled", response.data)

    @mock.patch("routes.races.races.time_now",
                MagicMock(return_value=datetime.datetime(2018, 10, 1, 14, 10,
                                                         58, 00000)))
    @mock.patch("db.models.Race.get_races_by_round", MagicMock(return_value=[
        MockRace(1, datetime.datetime(2018, 11, 1, 14, 10, 58, 00000),
                 'TEST_STATUS', 1)]))
    @mock.patch('flask_login.utils._get_user')
    def test_add_results_button_disabled(self, current_user):
        with self.client as client:
            current_user.is_authenticated = True
            response = self.client.get("/rounds/1/races")
            self.assertIn(b"add-results-disabled", response.data)

    @mock.patch("routes.races.races.time_now",
                MagicMock(return_value=datetime.datetime(2018, 11, 1, 14, 10,
                                                         58, 00000)))
    @mock.patch("db.models.Race.get_races_by_round", MagicMock(return_value=[
        MockRace(1, datetime.datetime(2018, 10, 1, 14, 10, 58, 00000),
                'TEST_STATUS', 1)]))
    @mock.patch('flask_login.utils._get_user')
    def test_add_results_button_enabled(self, current_user):
        with self.client as client:
            current_user.is_authenticated = True
            response = self.client.get("/rounds/1/races")
            self.assertIn(b"add-results-enabled", response.data)
