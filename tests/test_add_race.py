import unittest
from globals.globals import app
from unittest import mock
from unittest.mock import MagicMock
import datetime


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
    @mock.patch('db.models.Race.get_races_by_round', MagicMock(return_value=[MockRace(1, datetime.datetime.now()),
                                                                             MockRace(2, datetime.datetime.now())]))
    @mock.patch('db.models.Round.get_round', MagicMock(return_value=MockRound(datetime.datetime(2017, 10, 5, 18, 00),
                                                                               datetime.datetime(2019, 10, 5, 18, 00))))
    @mock.patch('routes.add_race.add_race.add_race_to_db', MagicMock(return_value=None))
    @mock.patch('routes.login.login.redirect_to', MagicMock(return_value="rounds.rounds"))
    def test_add_race_form_redirects_to_rounds(self, username):
        with self.client as client:
            username.is_authenticated = True
            response = client.post('/rounds/1/races/add', data=dict(race_status="TEST STATUS",
                                                                    race_date="10/25/2018 12:00 AM"),
                                                follow_redirects=True)
            self.assertIn(b"Start Date", response.data)

    @mock.patch('flask_login.utils._get_user')
    @mock.patch('db.models.Race.get_races_by_round', MagicMock(return_value=[MockRace(1, datetime.datetime.now()),
                                                                             MockRace(2, datetime.datetime.now()),
                                                                             MockRace(2, datetime.datetime.now()),
                                                                             MockRace(2, datetime.datetime.now()),
                                                                             MockRace(2, datetime.datetime.now())]))
    @mock.patch('db.models.Round.get_round', MagicMock(return_value=MockRound(datetime.datetime(2017, 10, 5, 18, 00),
                                                                              datetime.datetime(2019, 10, 5, 18, 00))))
    @mock.patch('routes.add_race.add_race.add_race_to_db', MagicMock(return_value=None))
    def test_add_race_form_too_many_races(self, username):
        with self.client as client:
            username.is_authenticated = True
            client.post('/rounds/1/races/add', data=dict(race_status="TEST STATUS", race_date="10/25/2018 12:00 AM"))

            with client.session_transaction() as session:
                flash_message = session['_flashes'][0][1]
                self.assertEqual(flash_message, "Can't add race to round with 5 or more races.")

    @mock.patch('flask_login.utils._get_user')
    @mock.patch('db.models.Race.get_races_by_round', MagicMock(return_value=[MockRace(1, datetime.datetime(2016, 10, 5, 18, 00))]))
    @mock.patch('db.models.Round.get_round', MagicMock(return_value=MockRound(datetime.datetime(2017, 10, 5, 18, 00),
                                                                              datetime.datetime(2019, 10, 5, 18, 00))))
    @mock.patch('routes.add_race.add_race.add_race_to_db', MagicMock(return_value=None))
    def test_add_race_form_too_early(self, username):
        with self.client as client:
            username.is_authenticated = True
            client.post('/rounds/1/races/add', data=dict(race_status="TEST STATUS", race_date="10/25/2016 12:00 AM"))

            with client.session_transaction() as session:
                flash_message = session['_flashes'][0][1]
                self.assertEqual(flash_message, "Can't add race that doesn't take place within round dates.")

    @mock.patch('flask_login.utils._get_user')
    @mock.patch('db.models.Race.get_races_by_round',
                MagicMock(return_value=[MockRace(1, datetime.datetime(2020, 10, 5, 18, 00))]))
    @mock.patch('db.models.Round.get_round', MagicMock(return_value=MockRound(datetime.datetime(2017, 10, 5, 18, 00),
                                                                              datetime.datetime(2019, 10, 5, 18, 00))))
    @mock.patch('routes.add_race.add_race.add_race_to_db', MagicMock(return_value=None))
    def test_add_race_form_too_late(self, username):
        with self.client as client:
            username.is_authenticated = True
            client.post('/rounds/1/races/add', data=dict(race_status="TEST STATUS", race_date="10/25/2020 12:00 AM"))

            with client.session_transaction() as session:
                flash_message = session['_flashes'][0][1]
                self.assertEqual(flash_message, "Can't add race that doesn't take place within round dates.")
