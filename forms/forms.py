from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RaceResultsForm(FlaskForm):
    time_to_finish = IntegerField('Time to Finish', validators=[DataRequired()])
    position = IntegerField('Position', validators=[DataRequired()])
    did_not_finish = BooleanField('Did Not Finish', validators=[DataRequired()])
    submit = SubmitField('Submit Result')