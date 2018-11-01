from flask import Blueprint, render_template, url_for, redirect, flash
from flask_login import current_user
from forms.forms import AddRaceForm
from db.models import Race, Round
from globals.globals import db
from dateutil import parser
from routes.login.login import redirect_to

add_race_blueprint = Blueprint('add_race', __name__)


@add_race_blueprint.route('/rounds/<int:round_id>/races/add', methods=["GET", "POST"])
def add_race(round_id):
    if not current_user.is_authenticated:
        return redirect_to('login.login')

    form = AddRaceForm()

    round_ = Round().get_round(round_id)

    if form.validate_on_submit():
        races = Race().get_races_by_round(round_id)

        if len(races) >= 5:
            flash("Can't add race to round with 5 or more races.")
            return redirect_to('rounds.rounds')

        race_date, race_status = form.race_date.data, form.race_status.data
        current_round = Round().get_round(round_id)

        if parser.parse(race_date) < current_round.start_date or parser.parse(race_date) > current_round.end_date:
            flash("Can't add race that doesn't take place within round dates.")
            return redirect_to('rounds.rounds')

        add_race_to_db(race_date, race_status, round_id)

        return redirect_to('rounds.rounds')

    return render_template('add_race.html', form=form, round_=round_)


def add_race_to_db(race_date, race_status, round_id):
    race = Race(date=race_date, status=race_status, id_round=round_id)

    db.session.add(race)
    db.session.commit()
