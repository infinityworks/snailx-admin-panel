import unittest
from globals.globals import app
from unittest import mock
from unittest.mock import MagicMock
import datetime
from routes.races.add_snail_to_race import (validate_snail_in_inflight_round,
                                            validate_snail_in_same_round,
                                            flash_redirect,
                                            validate_snail_in_same_race,
                                            commit_snail_to_race)
from dateutil import parser


class MockRace:
    def __init__(self, id, date):
        self.id = id
        self.date = date
        self.status = "TEST PLAYED"
        self.id_round = 1


class MockRound:
    def __init__(self, start_date, end_date):
        self.id = 1
        self.name = "Test Round"
        self.start_date = start_date
        self.end_date = end_date


class MockRaceParticipants():
    def __init__(self, id, id_snail, id_race):
        self.id = id
        self.id_snail = id_snail
        self.id_race = id_race


class MockSnail():
    def __init__(self, id, name, trainer_id):
        self.id = id
        self.name = name
        self.trainer_id = trainer_id


class TestAddSnailToRace(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    @mock.patch('flask_login.utils._get_user')
    def test_snail_to_race_page_response_is_200(self, current_user):
        with self.client as client:
            current_user.is_authenticated = True
            response = client.get("/rounds/1/races/1/add")
            self.assertEqual(200, response.status_code)