import unittest
from globals.globals import app
from unittest import mock
from unittest.mock import MagicMock
import datetime
from routes.races.add_snail_to_race import (validate_snail_in_same_race,
                                            flash_redirect,
                                            validate_snail_in_same_round,
                                            validate_snail_in_inflight_round)


class MockRace:
    def __init__(self, id):
        self.id = id
        self.date = datetime.datetime.now()
        self.status = "TEST PLAYED"
        self.id_round = 1


class MockRound:
    def __init__(self, start_date, end_date):
        self.id = 1
        self.name = "Test Round"
        self.start_date = start_date
        self.end_date = end_date


class MockRaceParticipants:
    def __init__(self, id, id_snail, id_race):
        self.id = id
        self.id_snail = id_snail
        self.id_race = id_race


class MockSnail:
    def __init__(self, id, name, trainer_id):
        self.id = id
        self.name = name
        self.trainer_id = trainer_id


class TestAddSnailToRace(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    @mock.patch('db.models.RaceParticipants.get_race_participants_race_id', MagicMock(return_value=[MockRaceParticipants(1,1,1)]))
    def test_validate_snail_in_same_race_true(self):
        self.assertTrue(validate_snail_in_same_race(1, 1))

    @mock.patch('db.models.RaceParticipants.get_race_participants_race_id', MagicMock(return_value=[MockRaceParticipants(1,1,1)]))
    def test_validate_snail_in_same_race_false(self):
        self.assertFalse(validate_snail_in_same_race(1, 2))

    @mock.patch('db.models.Race.get_races_by_round', MagicMock(return_value=[MockRace(1)]))
    @mock.patch('db.models.RaceParticipants.get_race_participants_race_id', MagicMock(return_value=[MockRaceParticipants(1,1,1)]))
    def test_validate_snail_in_same_round_true(self):
        self.assertTrue(validate_snail_in_same_round(1, 1, 1))

    @mock.patch('db.models.Race.get_races_by_round', MagicMock(return_value=[MockRace(1)]))
    @mock.patch('db.models.RaceParticipants.get_race_participants_race_id', MagicMock(return_value=[MockRaceParticipants(1,1,1)]))
    def test_validate_snail_in_same_round_false(self):
        self.assertFalse(validate_snail_in_same_round(1, 2, 2))

    @mock.patch("db.models.Round.get_future_round_times", MagicMock(return_value=[MockRound(1, "date")]))
    def test_validate_snail_in_inflight_round_false(self):
        self.assertFalse(validate_snail_in_inflight_round(1))

    @mock.patch('flask_login.utils._get_user')
    def test_snail_to_race_page_response_is_200(self, current_user):
        with self.client as client:
            current_user.is_authenticated = True
            response = client.get("/rounds/1/races/1/add")
            self.assertEqual(200, response.status_code)

    @mock.patch('flask_login.utils._get_user')
    @mock.patch('db.models.Snail.get_all_snails', MagicMock(
        return_value=[MockSnail(id=1, name="test1", trainer_id=1),
                      MockSnail(id=2, name="test2", trainer_id=1)]))
    @mock.patch('routes.races.add_snail_to_race.validate_snail_in_same_race',
                MagicMock(return_value=False))
    @mock.patch('routes.races.add_snail_to_race.validate_snail_in_same_round',
                MagicMock(return_value=False))
    @mock.patch('routes.races.add_snail_to_race.validate_snail_in_inflight_round',
                MagicMock(return_value=False))
    @mock.patch('routes.races.add_snail_to_race.commit_snail_to_race',
                MagicMock(return_value=None))
    def test_snail_adds_snail_to_race(self, current_user):
        with self.client as client:
            current_user.is_authenticated = True
            response = client.post("/rounds/1/races/1/add",
                                   data=dict(snail_id=1), follow_redirects=True)
            self.assertIn(b"Snail has been added to this race", response.data)

    @mock.patch('flask_login.utils._get_user')
    @mock.patch('db.models.Snail.get_all_snails', MagicMock(
        return_value=[MockSnail(id=1, name="test1", trainer_id=1),
                      MockSnail(id=2, name="test2", trainer_id=1)]))
    @mock.patch('routes.races.add_snail_to_race.validate_snail_in_same_race',
                MagicMock(return_value=True))
    @mock.patch('routes.races.add_snail_to_race.validate_snail_in_same_round',
                MagicMock(return_value=False))
    @mock.patch('routes.races.add_snail_to_race.validate_snail_in_inflight_round',
                MagicMock(return_value=True))
    @mock.patch('routes.races.add_snail_to_race.commit_snail_to_race',
                MagicMock(return_value=None))
    def test_snail_already_in_race(self, current_user):
        with self.client as client:
            current_user.is_authenticated = True
            response = client.post("/rounds/1/races/1/add",
                                   data=dict(snail_id=1), follow_redirects=True)
            self.assertIn(b"This snail is already in the selected race",
                          response.data)

    @mock.patch('flask_login.utils._get_user')
    @mock.patch('db.models.Snail.get_all_snails', MagicMock(
        return_value=[MockSnail(id=1, name="test1", trainer_id=1),
                      MockSnail(id=2, name="test2", trainer_id=1)]))
    @mock.patch('routes.races.add_snail_to_race.validate_snail_in_same_race',
                MagicMock(return_value=False))
    @mock.patch('routes.races.add_snail_to_race.validate_snail_in_same_round',
                MagicMock(return_value=True))
    @mock.patch('routes.races.add_snail_to_race.validate_snail_in_inflight_round',
                MagicMock(return_value=True))
    @mock.patch('routes.races.add_snail_to_race.commit_snail_to_race',
                MagicMock(return_value=None))
    def test_snail_already_in_round(self, current_user):
        with self.client as client:
            current_user.is_authenticated = True
            response = client.post("/rounds/1/races/1/add",
                                   data=dict(snail_id=1), follow_redirects=True)
            self.assertIn(b"This snail is already racing in the selected round",
                          response.data)

    @mock.patch('flask_login.utils._get_user')
    @mock.patch('db.models.Snail.get_all_snails', MagicMock(
        return_value=[MockSnail(id=1, name="test1", trainer_id=1),
                      MockSnail(id=2, name="test2", trainer_id=1)]))
    @mock.patch('routes.races.add_snail_to_race.validate_snail_in_same_race',
                MagicMock(return_value=False))
    @mock.patch('routes.races.add_snail_to_race.validate_snail_in_same_round',
                MagicMock(return_value=False))
    @mock.patch('routes.races.add_snail_to_race.validate_snail_in_inflight_round',
                MagicMock(return_value=True))
    @mock.patch('routes.races.add_snail_to_race.commit_snail_to_race',
                MagicMock(return_value=None))
    def test_snail_already_in_inflight_round(self, current_user):
        with self.client as client:
            current_user.is_authenticated = True
            response = client.post("/rounds/1/races/1/add",
                                   data=dict(snail_id=1), follow_redirects=True)
            self.assertIn(
                b"This round in ineligible for snails to be added, please check the times and try again",
                response.data)
