from flask import render_template, Blueprint, redirect, url_for, flash, request
from forms.forms import AddRoundForm
from db.models import Round
from globals.globals import db
import datetime

add_round_blueprint = Blueprint('add_round', __name__)


@add_round_blueprint.route("/rounds/add", methods=["GET", "POST"])
def add_round():
    form = AddRoundForm()

    if form.validate_on_submit():
        start = form.start_date.data
        end = form.end_date.data

        if not validate_dates(start, end):
            flash(
                'Failed to create new round. One or more of the supplied dates are in the past, please enter valid dates.', 'danger')
            return render_template('add_round.html', title='Add Round', form=form)

        if not validate_start_before_end(start, end):
            flash(
                'Failed to create new round. A round cannot be created with an end date before the start date, please enter valid dates.', 'danger')
            return render_template('add_round.html', title='Add Round', form=form)

        if not validate_date_interval(start, end):
            flash(
                'Failed to create new round. A round already exists between the given dates, please enter valid dates.', 'danger')
            return render_template('add_round.html', title='Add Round', form=form)

        try:
            new_round = Round(
                name=form.name.data, start_date=start, end_date=end)
            db.session.add(new_round)
            db.session.commit()
            return redirect(url_for('rounds.rounds'))
        except:
            flash(
                'Failed to create new round. Check that round details are valid and try again.', 'error')

    return render_template('add_round.html', title='Add Round', form=form)


def validate_date_interval(start_date, end_date):
    return not Round().get_num_rounds_between_dates(start_date, end_date)[0]


def validate_dates(start_date, end_date):
    cur_datetime = datetime.datetime.now()
    return (not datetime.datetime.strptime(start_date, '%m/%d/%Y %H:%M %p') < cur_datetime
            or not datetime.datetime.strptime(end_date, '%m/%d/%Y %H:%M %p') < cur_datetime)


def validate_start_before_end(start_date, end_date):
    return datetime.datetime.strptime(start_date, '%m/%d/%Y %H:%M %p') < datetime.datetime.strptime(end_date, '%m/%d/%Y %H:%M %p')