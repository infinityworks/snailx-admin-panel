from flask import render_template, Blueprint, redirect, url_for, flash, request
from forms.forms import AddRoundForm
from db.models import Round
from globals.globals import db

add_round_blueprint = Blueprint('add_round', __name__)


@add_round_blueprint.route("/rounds/add", methods=["GET", "POST"])
def add_round():
    form = AddRoundForm()

    if form.validate_on_submit():
        start = form.start_date.data
        end = form.end_date.data

        if not validate_round_dates(start, end):
            flash(
                'A round already exists between the given dates. Please select a different start and end date.', 'danger')
            return render_template('add_round.html', title='Add Round', form=form)

        try:
            new_round = Round(
                name=form.name.data, start_date=start, end_date=end)
            db.session.add(new_round)
            db.session.commit()
            return redirect(url_for('rounds.rounds'))
        except:
            flash(
                'Failed to create new round. Check that round details are valid and try again.', 'danger')

    return render_template('add_round.html', title='Add Round', form=form)


def validate_round_dates(start_date, end_date):
    return not Round().get_num_rounds_between_dates(start_date, end_date)[0]
