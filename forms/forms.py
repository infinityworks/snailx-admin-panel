from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class AddRaceForm(FlaskForm):
    race_date = StringField('Date', validators=[DataRequired()])
    race_status = StringField('Status', validators=[DataRequired()])
    submit = SubmitField('Add Race')
