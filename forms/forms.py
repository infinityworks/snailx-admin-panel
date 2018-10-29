from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class AddRaceForm(FlaskForm):
    race_date = StringField('Date', validators=[DataRequired()])
    race_status = StringField('Status', validators=[DataRequired()])
    submit = SubmitField('Add Race')


class AddRoundForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    start_date = StringField('Start Date', validators=[DataRequired()])
    end_date = StringField('End Date', validators=[DataRequired()])
    submit = SubmitField('Create Round')
