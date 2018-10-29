import unittest
from globals.globals import app
from unittest import mock
from unittest.mock import MagicMock


class MockTrainer:
    def __init__(self, id, name):
        self.id = id
        self.name = name


class TestAddSnail(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    @mock.patch('flask_login.utils._get_user')
    def test_add_snail_returns_200(self, current_user):
        current_user.is_authenticated = True
        with self.client as client:
            response = client.get('/snails/add', follow_redirects=True)
            self.assertEqual(response.status_code, 200)

    @mock.patch('flask_login.utils._get_user')
    @mock.patch('db.models.Trainer.get_all_trainers',
                MagicMock(return_value=[MockTrainer(1, 'Terry'), MockTrainer(1, 'Gary')]))
    @mock.patch('routes.add_snail.add_snail.validate_snail_not_in_db', MagicMock(return_value=False))
    @mock.patch('routes.add_snail.add_snail.add_snail_to_db', MagicMock(return_value=None))
    def test_add_snail_creates_snail(self, current_user):
        current_user.is_authenticated = True
        with self.client as client:
            response = client.post('snails/add',
                                   data=dict(snail_name="test snail", trainer_name="test_trainer"),
                                   follow_redirects=True)
            self.assertIn(b'test snail', response.data)

    @mock.patch('flask_login.utils._get_user')
    @mock.patch('db.models.Trainer.get_all_trainers',
                MagicMock(return_value=[MockTrainer(1, 'Terry'), MockTrainer(1, 'Gary')]))
    @mock.patch('routes.add_snail.add_snail.validate_snail_not_in_db', MagicMock(return_value=True))
    @mock.patch('routes.add_snail.add_snail.add_snail_to_db', MagicMock(return_value=None))
    def test_add_snail_name_too_long(self, current_user):
        current_user.is_authenticated = True
        with self.client as client:
            client.post('snails/add',
                                   data=dict(snail_name="Test Snail", trainer_name="test_trainer"),
                        follow_redirects=True)


