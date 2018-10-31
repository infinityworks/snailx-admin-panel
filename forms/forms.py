from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, BooleanField, SubmitField, 
                     IntegerField, DateField, SelectField)
from wtforms.validators import DataRequired
from wtforms.widgets import HiddenInput


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RaceResultsForm(FlaskForm):
    time_to_finish = IntegerField('Time to Finish', 
                                  validators=[DataRequired()])
    position = IntegerField('Position', validators=[DataRequired()])
    id_race_participants = IntegerField('Participant ID', widget=HiddenInput())
    did_not_finish = BooleanField('Did Not Finish')
    submit = SubmitField('Submit Result')


class AddRaceForm(FlaskForm):
    race_date = StringField('Date', validators=[DataRequired()])
    race_status = StringField('Status', validators=[DataRequired()])
    submit = SubmitField('Add Race')


class AddRoundForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    start_date = StringField('Start Date', validators=[DataRequired()])
    end_date = StringField('End Date', validators=[DataRequired()])
    submit = SubmitField('Create Round')


class AddSnailToRace(FlaskForm):
    snail_id = SelectField('Name')
    submit = SubmitField('Add Snail')

    
class AddSnailForm(FlaskForm):
    snail_name = StringField('Snail Name', validators=[DataRequired()])
    trainer_name = SelectField('Trainer Name')
    submit = SubmitField('Add Snail')


class AddTrainerForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Add Trainer')
