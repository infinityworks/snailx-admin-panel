import unittest
from globals.globals import app
from unittest import mock
from unittest.mock import MagicMock
import datetime
from routes.rounds.add_round import validate_date_interval, validate_dates, validate_start_before_end, validate_name_length, validate_unique_name
from dateutil import parser


# class MockRound():
#     def __init__(self, name="test", start_date=datetime.datetime.now(), end_date=datetime.datetime.now() + datetime.timedelta(days=1)):
#         self.id = 1
#         self.name = name
#         self.start_date = start_date
#         self.end_date = end_date


class TestAddRound(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    @mock.patch("db.models.Round.get_num_rounds_between_dates", MagicMock(return_value=(0,)))
    def test_add_round_date_interval_validation_valid_date_interval(self):
        self.assertTrue(validate_date_interval(
            datetime.datetime.utcnow(), datetime.datetime.now() + datetime.timedelta(days=1)))

    @mock.patch("db.models.Round.get_num_rounds_between_dates", MagicMock(return_value=(1,)))
    def test_add_round_date_interval_validation_invalid_date_interval(self):
        self.assertFalse(validate_date_interval(
            datetime.datetime.utcnow(), datetime.datetime.now() + datetime.timedelta(days=1)))

    def test_add_round_date_in_past_validation_dates_in_future(self):
        fake_date = parser.parse("01/01/1999 12:00 PM")
        self.assertTrue(validate_dates(
            "01/01/2000 11:00 AM", "02/02/2000 12:00 PM", fake_date))

    def test_add_round_date_in_past_validation_dates_in_past(self):
        fake_date = parser.parse("01/01/2010 4:00 PM")
        self.assertFalse(validate_dates(
            "01/01/2010 3:30 PM", "02/02/2010 12:00 PM", fake_date))

    def test_add_round_start_date_after_end_date_validation(self):
        self.assertFalse(validate_start_before_end(
            "01/01/2003 12:00 PM", "02/02/2002 12:00 PM"))

    def test_add_round_name_length_greater_than_max_validation(self):
        self.assertFalse(validate_name_length("12345678910111213"))

    @mock.patch("db.models.Round.get_round_by_name", MagicMock(return_value=True))
    def test_add_round_name_unique_validation(self):
        self.assertFalse(validate_unique_name("unqiuename"))

    @mock.patch('flask_login.utils._get_user')
    @mock.patch('routes.rounds.add_round.db.session.add', MagicMock(return_value=None))
    @mock.patch('routes.rounds.add_round.db.session.commit', MagicMock(return_value=None))
    @mock.patch('routes.rounds.add_round.validate_date_interval', MagicMock(return_value=True))
    @mock.patch('routes.rounds.add_round.validate_dates', MagicMock(return_value=True))
    @mock.patch('routes.rounds.add_round.validate_start_before_end', MagicMock(return_value=True))
    @mock.patch('routes.rounds.add_round.validate_name_length', MagicMock(return_value=True))
    @mock.patch('routes.rounds.add_round.validate_unique_name', MagicMock(return_value=True))
    def test_add_round_valid_round_logged_in(self, current_user):
        current_user.is_authenticated = True
        with self.client as client:
            response = client.post(
                '/rounds/add', data=dict(name="test", start_date="01/01/2001 12:00 AM", end_date="02/02/2002 12:00 PM"), follow_redirects=True)
            self.assertIn(b'All Rounds', response.data)

    @mock.patch('routes.rounds.add_round.db.session.add', MagicMock(return_value=None))
    @mock.patch('routes.rounds.add_round.db.session.commit', MagicMock(return_value=None))
    @mock.patch('routes.rounds.add_round.validate_date_interval', MagicMock(return_value=True))
    @mock.patch('routes.rounds.add_round.validate_dates', MagicMock(return_value=True))
    @mock.patch('routes.rounds.add_round.validate_start_before_end', MagicMock(return_value=True))
    @mock.patch('routes.rounds.add_round.validate_name_length', MagicMock(return_value=True))
    @mock.patch('routes.rounds.add_round.validate_unique_name', MagicMock(return_value=True))
    def test_add_round_valid_round_not_logged_in(self):
        with self.client as client:
            response = client.post(
                '/rounds/add', data=dict(name="test", start_date="01/01/2001 12:00 AM", end_date="02/02/2002 12:00 PM"), follow_redirects=True)
            self.assertIn(b'Sign In', response.data)

    @mock.patch('flask_login.utils._get_user')
    @mock.patch('routes.rounds.add_round.validate_date_interval', MagicMock(return_value=False))
    @mock.patch('routes.rounds.add_round.validate_dates', MagicMock(return_value=True))
    @mock.patch('routes.rounds.add_round.validate_start_before_end', MagicMock(return_value=True))
    @mock.patch('routes.rounds.add_round.validate_name_length', MagicMock(return_value=True))
    @mock.patch('routes.rounds.add_round.validate_unique_name', MagicMock(return_value=True))
    def test_add_round_date_interval_validation_invalid_date_interval_flash(self, current_user):
        current_user.is_authenticated = True
        with self.client as client:
            response = client.post(
                '/rounds/add', data=dict(name="test", start_date="01/01/2001 12:00 AM", end_date="02/02/2002 12:00 PM"))
            self.assertIn(
                b'Failed to create new round. A round already exists between the given dates, please enter valid dates.', response.data)

    @mock.patch('flask_login.utils._get_user')
    @mock.patch('routes.rounds.add_round.validate_date_interval', MagicMock(return_value=True))
    @mock.patch('routes.rounds.add_round.validate_dates', MagicMock(return_value=False))
    @mock.patch('routes.rounds.add_round.validate_start_before_end', MagicMock(return_value=True))
    @mock.patch('routes.rounds.add_round.validate_name_length', MagicMock(return_value=True))
    @mock.patch('routes.rounds.add_round.validate_unique_name', MagicMock(return_value=True))
    def test_add_round_date_in_past_validation_dates_in_past_flash(self, current_user):
        current_user.is_authenticated = True
        with self.client as client:
            response = client.post(
                '/rounds/add', data=dict(name="test", start_date="01/01/2001 12:00 AM", end_date="02/02/2002 12:00 PM"))
            self.assertIn(
                b'Failed to create new round. One or more of the supplied dates are in the past, please enter valid dates.', response.data)

    @mock.patch('flask_login.utils._get_user')
    @mock.patch('routes.rounds.add_round.validate_date_interval', MagicMock(return_value=True))
    @mock.patch('routes.rounds.add_round.validate_dates', MagicMock(return_value=True))
    @mock.patch('routes.rounds.add_round.validate_start_before_end', MagicMock(return_value=False))
    @mock.patch('routes.rounds.add_round.validate_name_length', MagicMock(return_value=True))
    @mock.patch('routes.rounds.add_round.validate_unique_name', MagicMock(return_value=True))
    def test_add_round_start_date_after_end_date_validation_flash(self, current_user):
        current_user.is_authenticated = True
        with self.client as client:
            response = client.post(
                '/rounds/add', data=dict(name="test", start_date="01/01/2001 12:00 AM", end_date="02/02/2002 12:00 PM"))
            self.assertIn(
                b'Failed to create new round. A round cannot be created with an end date before the start date, please enter valid dates.', response.data)

    @mock.patch('flask_login.utils._get_user')
    @mock.patch('routes.rounds.add_round.validate_date_interval', MagicMock(return_value=True))
    @mock.patch('routes.rounds.add_round.validate_dates', MagicMock(return_value=True))
    @mock.patch('routes.rounds.add_round.validate_start_before_end', MagicMock(return_value=True))
    @mock.patch('routes.rounds.add_round.validate_name_length', MagicMock(return_value=False))
    @mock.patch('routes.rounds.add_round.validate_unique_name', MagicMock(return_value=True))
    def test_add_round_name_length_greater_than_max_validation_flash(self, current_user):
        current_user.is_authenticated = True
        with self.client as client:
            response = client.post(
                '/rounds/add', data=dict(name="test", start_date="01/01/2001 12:00 AM", end_date="02/02/2002 12:00 PM"))
            self.assertIn(
                b'Failed to create new round. The maximum name length is 12 characters.', response.data)

    @mock.patch('flask_login.utils._get_user')
    @mock.patch('routes.rounds.add_round.validate_date_interval', MagicMock(return_value=True))
    @mock.patch('routes.rounds.add_round.validate_dates', MagicMock(return_value=True))
    @mock.patch('routes.rounds.add_round.validate_start_before_end', MagicMock(return_value=True))
    @mock.patch('routes.rounds.add_round.validate_name_length', MagicMock(return_value=True))
    @mock.patch('routes.rounds.add_round.validate_unique_name', MagicMock(return_value=False))
    def test_add_round_unique_name_validation_flash(self, current_user):
        current_user.is_authenticated = True
        with self.client as client:
            response = client.post(
                '/rounds/add', data=dict(name="test", start_date="01/01/2001 12:00 AM", end_date="02/02/2002 12:00 PM"))
            self.assertIn(
                b'Failed to create new round. Round name already exists.', response.data)
