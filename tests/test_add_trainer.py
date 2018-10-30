import unittest
from globals.globals import app
from unittest import mock
from unittest.mock import MagicMock


class TestAddTrainer(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    @mock.patch('flask_login.utils._get_user')
    def test_add_trainer_returns_200(self, current_user):
        current_user.is_authenticated = True
        with self.client as client:
            response = client.get('/trainer/add', follow_redirects=True)
            self.assertEqual(response.status_code, 200)

    @mock.patch('flask_login.utils._get_user')
    @mock.patch('db.models.Trainer.get_trainer_by_name', MagicMock(return_value=0))
    @mock.patch('routes.add_trainer.add_trainer.add_race_to_db', MagicMock(return_value=None))
    def test_add_trainer_to_db(self, current_user):
        current_user.is_authenticated = True
        with self.client as client:
            response = client.post('/trainer/add', data=dict(name='test'), follow_redirects=True)
            self.assertIn(b'Successfully added trainer', response.data)

    @mock.patch('flask_login.utils._get_user')
    @mock.patch('db.models.Trainer.get_trainer_by_name', MagicMock(return_value=1))
    @mock.patch('routes.add_trainer.add_trainer.add_race_to_db', MagicMock(return_value=None))
    def test_add_trainer_to_db_if_exists(self, current_user):
        current_user.is_authenticated = True
        with self.client as client:
            response = client.post('/trainer/add', data=dict(name='test'), follow_redirects=True)
            self.assertIn(b'This trainer name already exists', response.data)