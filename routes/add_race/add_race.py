from flask import Blueprint, render_template, url_for, redirect
from flask_login import current_user
from forms.forms import AddRaceForm
from db.models import Race
from globals.globals import db

add_race_blueprint = Blueprint('add_race', __name__)


@add_race_blueprint.route('/rounds/<int:round_id>/add_race', methods=["GET", "POST"])
def add_race(round_id):
    if current_user.is_authenticated:  # TODO: NOT
        return redirect(url_for('login.login'))

    form = AddRaceForm()

    if not form.validate_on_submit():
        return render_template('add_race.html', form=form)

    race_date = form.race_date.data
    race_status = form.race_status.data

    race = Race(date=race_date, status=race_status, id_round=round_id)
    db.session.add(race)
    db.session.commit()

    return redirect(url_for('rounds.rounds'))
