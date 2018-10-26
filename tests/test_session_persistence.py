import unittest
from unittest import TestCase
from unittest import mock 
from unittest.mock import MagicMock
from globals.globals import app, login_manager

from flask import url_for
from flask_login import login_user, current_user

from db.models import User
from routes.login.login import login, is_authenticated



class TestSessionPersistence(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
    @mock.patch('routes.login.login.redirect_to', return_value="")
    @mock.patch('routes.login.login.is_authenticated', MagicMock(return_value=True))
    def test_current_user_is_authenticated(self, redirectMock):
        with self.client as client:
            client.get("/login")
        redirectMock.assert_called_once_with("rounds.rounds")

    @mock.patch('routes.login.login.redirect_to', return_value="")
    @mock.patch('routes.login.login.is_authenticated', MagicMock(return_value=False))
    def test_current_user_is_not_authenticated(self, redirectMock):
        with self.client as client:
            client.get("/login")
        redirectMock.assert_not_called()
            

if __name__ == '__main__':
    unittest.main()
