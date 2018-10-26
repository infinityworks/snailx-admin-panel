import unittest
from globals.globals import app
from unittest import mock
from unittest.mock import MagicMock
import datetime
from routes.rounds.add_round import validate_date_interval, validate_dates, validate_start_before_end, validate_name_length


class MockRound():
    def __init__(self, name="test", start_date=datetime.datetime.now(), end_date=datetime.datetime.now() + datetime.timedelta(days=1)):
        self.id = 1
        self.name = name
        self.start_date = start_date
        self.end_date = end_date


class TestAddRound(unittest.TestCase):

    @mock.patch('flask_login.utils._get_user')
    def setUp(self, current_user):
        current_user.is_authenticated = True
        self.client = app.test_client()

    @mock.patch("db.models.Round.get_num_rounds_between_dates", MagicMock(return_value=(0,)))
    def test_add_round_date_interval_validation_valid_date_interval(self):
        new_round = MockRound()
        self.assertTrue(validate_date_interval(
            new_round.start_date, new_round.end_date))

    @mock.patch("db.models.Round.get_num_rounds_between_dates", MagicMock(return_value=(1,)))
    def test_add_round_date_interval_validation_invalid_date_interval(self):
        new_round = MockRound()
        self.assertFalse(validate_date_interval(
            new_round.start_date, new_round.end_date))

    def test_add_round_date_in_past_validation_dates_in_past(self):
        fake_date = datetime.datetime(2010, 10, 10, 10, 10, 0)
        new_round = MockRound(start_date="01/01/2001 12:00 AM",
                              end_date="02/02/2002 12:00 PM")
        self.assertFalse(validate_dates(
            new_round.start_date, new_round.end_date, fake_date))

    def test_add_round_date_in_past_validation_dates_in_future(self):
        fake_cur_date = datetime.datetime(2000, 10, 10, 10, 10, 0)
        self.assertTrue(validate_dates(
            "01/01/2001 12:00 AM", "02/02/2002 12:00 PM", fake_cur_date))

    def test_add_round_start_date_after_end_date_validation(self):
        self.assertFalse(validate_start_before_end(
            "01/01/2003 12:00 AM", "02/02/2002 12:00 PM"))

    def test_add_round_name_length_greater_than_max_validation(self):
        self.assertFalse(validate_name_length("12345678910111213"))

    def test_add_round_data_required_validation(self):
        pass

    def test_add_round_success(self):
        pass

    def test_add_round_not_logged_in(self):
        pass

    def test_add_round_logged_in(self):
        pass
