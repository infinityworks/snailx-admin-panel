from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from wtforms.widgets import HiddenInput


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RaceResultsForm(FlaskForm):
    time_to_finish = IntegerField('Time to Finish', validators=[DataRequired()])
    position = IntegerField('Position', validators=[DataRequired()])
    id_race_participants = IntegerField('Participant ID', widget=HiddenInput())
    did_not_finish = BooleanField('Did Not Finish')
    submit = SubmitField('Submit Result')