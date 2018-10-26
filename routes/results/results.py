from flask import render_template, Blueprint, url_for, redirect, request, flash
from flask_login import current_user
from db.models import RaceResult, Race, RaceParticipants
from forms.forms import RaceResultsForm
from globals.globals import db

result_blueprint = Blueprint('result', __name__)


@result_blueprint.route('/rounds/<int:round_id>/races/<int:race_id>', methods=['GET', 'POST'])
def race(round_id, race_id):
    if not current_user.is_authenticated:
        return redirect(url_for('login.login'))

    race_results_form = RaceResultsForm()
    race = Race().get_race(race_id)
    participants = RaceParticipants().get_race_participants_race_id(race_id)
    if race_results_form.validate_on_submit():
        result_row = RaceResult().get_race_result(race_results_form.id_race_participants.data)
        if not result_row:
            db.session.add(RaceResult(position=race_results_form.position.data, time_to_finish=race_results_form.time_to_finish.data, did_not_finish=race_results_form.did_not_finish.data, id_race_participants=race_results_form.id_race_participants.data ))
            db.session.commit()
            flash("Race Result recorded for Race Participant ID {}.".format(race_results_form.id_race_participants.data))
        else:
            flash("Race Result Failed. Race Result already exists for for Race Participant ID {}.".format(race_results_form.id_race_participants.data))
        return redirect(url_for('result.race', round_id=round_id, race_id=race_id))  
    elif race_results_form.errors.items():
        flash("Form submission not valid. Please resubmit.")
        return redirect(url_for('result.race', round_id=round_id, race_id=race_id))
    return render_template('results.html', race=race, participants=participants, race_results_form=race_results_form)


def validation(form):
    return form.validate()