import unittest
from globals.globals import app
from unittest import mock
from unittest.mock import MagicMock
import datetime


class MockRaceParticipants():
    def __init__(self, id, id_snail, id_race):
        self.id = id
        self.id_snail = id_snail
        self.id_race = id_race


class MockRace:
    def __init__(self, id, date, status, id_round):
        self.id = id
        self.date = date
        self.status = status
        self.id_round = id_round


class TestResult(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    @mock.patch('flask_login.utils._get_user')
    def test_results_page_response_is_200(self, current_user):
        with self.client as client:
            current_user.is_authenticated = True
            response = client.get("/rounds/1/races/1")
            self.assertEqual(200, response.status_code)

    
    @mock.patch('flask_login.utils._get_user')
    def test_results_page_displayed(self, current_user):
        with self.client as client:
            current_user.is_authenticated = True
            response = client.get("/rounds/1/races/1")
            self.assertIn(b"Time to Finish", response.data)

    @mock.patch("db.models.RaceParticipants.get_race_participants_race_id", MagicMock(return_value=[MockRaceParticipants(1,1,1), MockRaceParticipants(2,2,1)]))
    @mock.patch("db.models.Race.get_race", MagicMock(return_value=MockRace(1, datetime.datetime.now(), 'TEST_STATUS', 1)))
    @mock.patch('flask_login.utils._get_user')
    def test_results_participant_listed(self, current_user):
        with self.client as client:
            current_user.is_authenticated = True
            response = client.get("/rounds/1/races/1")
            self.assertIn(b"\"id_race_participants\" type=\"hidden\" value=\"2", response.data)

    @mock.patch("db.models.RaceParticipants.get_race_participants_race_id", MagicMock(return_value=[MockRaceParticipants(1,1,1), MockRaceParticipants(3,3,1)]))
    @mock.patch("db.models.Race.get_race", MagicMock(return_value=MockRace(1, datetime.datetime.now(), 'TEST_STATUS', 1)))
    @mock.patch('flask_login.utils._get_user')
    def test_results_participant_not_listed(self, current_user):
        with self.client as client:
            current_user.is_authenticated = True
            response = client.get("/rounds/1/races/1")
            self.assertNotIn(b"\"id_race_participants\" type=\"hidden\" value=\"2", response.data)
    
    @mock.patch("wtforms.form.validate", MagicMock(return_value=True))
    @mock.patch("db.models.RaceResult.get_race_result",MagicMock(return_value=False))
    @mock.patch("forms.forms.RaceResultsForm.submit",MagicMock(return_value=True))
    @mock.patch("db.models.RaceParticipants.get_race_participants_race_id", MagicMock(return_value=[MockRaceParticipants(1,1,1), MockRaceParticipants(3,3,1)]))
    @mock.patch("db.models.Race.get_race", MagicMock(return_value=MockRace(1, datetime.datetime.now(), 'TEST_STATUS', 1)))
    @mock.patch('flask_login.utils._get_user')
    def test_results_valid_data_posted(self, current_user):
        with self.client as client:
            current_user.is_authenticated = True
            response = client.post("/rounds/1/races/1", 
                data=dict(id=1, id_race_participants=1, position=1, time_to_finish=200, did_not_finish=False), follow_redirects=False)
            self.assertIn(b"Race Result recorded for Race Participant ID 1.", response.data)
