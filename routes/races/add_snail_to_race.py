from flask import render_template, Blueprint, url_for, redirect, flash
from flask_login import current_user
from db.models import Snail, RaceParticipants, Race, Round
from forms.forms import AddSnailToRace
from globals.globals import db

add_snail_to_race_blueprint = Blueprint('add_snail_to_race', __name__)


@add_snail_to_race_blueprint.route('/rounds/<int:round_id>/races/'
                                   '<int:race_id>/add',
                                   methods=['GET', 'POST'])
def add_snail_to_race(round_id, race_id):

    if not current_user.is_authenticated:
        return redirect(url_for('login.login'))

    all_snails = Snail().get_all_snails()
    form = AddSnailToRace()
    form.snail_id.choices = [(str(snail.id), snail.name) for snail in all_snails]

    if form.validate_on_submit():
        if validate_snail_in_same_race(race_id, form.snail_id.data):
            flash_redirect("This snail is already in the selected race", 
                           "add_snail_to_race.add_snail_to_race", 
                           race_id, round_id)

        elif validate_snail_in_same_round(round_id, race_id, form.snail_id.data):
            flash_redirect("This snail is already racing in the selected round", 
                           "add_snail_to_race.add_snail_to_race", race_id, 
                           round_id)

        elif validate_snail_in_inflight_round(round_id):
            flash_redirect("This round in ineligible for snails to be added, "
                           "please check the times and try again", 
                           "add_snail_to_race.add_snail_to_race", 
                           race_id, 
                           round_id)

        else:
            flash("Snail has been added to this race")
            commit_snail_to_race(race_id, form.snail_id.data)

    return render_template('add_snail_to_race.html', all_snails=all_snails,
                           form=form, race_id=race_id)


def commit_snail_to_race(id_race, id_snail):
    race_participant = RaceParticipants(id_race=id_race, id_snail=id_snail)
    db.session.add(race_participant)
    db.session.commit()


def validate_snail_in_same_race(race_id, snail_id):
    race_participants = RaceParticipants().get_race_participants_race_id(race_id)
    for snail in race_participants:
        if int(snail.id_snail) == int(snail_id):
            return True
    return False


def flash_redirect(message, path, race_id, round_id):
    flash(message)
    return redirect(url_for(path, race_id=race_id, round_id=round_id))


def validate_snail_in_same_round(round_id, race_id, snail_id):
    races_in_round = Race().get_races_by_round(round_id)
    for race in races_in_round:
        race_participants = RaceParticipants().get_race_participants_race_id(race.id)
        for snail in race_participants:
            if int(snail.id_snail) == int(snail_id):
                return True
    return False


def validate_snail_in_inflight_round(round_id):
    future_rounds = Round().get_future_round_times()
    for rounds in future_rounds:
        if not int(rounds.id) == int(round_id):
            return True
    return False
