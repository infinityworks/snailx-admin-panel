from flask import render_template, Blueprint, url_for, redirect, flash
from flask_login import current_user
from db.models import RaceResult, Race, RaceParticipants, Snail
from forms.forms import RaceResultsForm
from globals.globals import db

result_blueprint = Blueprint('result', __name__)


@result_blueprint.route('/rounds/<int:round_id>/races/<int:race_id>',
                        methods=['GET', 'POST'])
def race(round_id, race_id):

    if not current_user.is_authenticated:
        return redirect(url_for('login.login'))

    race_results_form = RaceResultsForm()
    race = Race().get_race(race_id)
    participants = RaceParticipants().get_participants_snails_race_id(race_id)

    unresulted_participants = [
        participant for participant, snail, result in participants if not result]

    if race_results_form.validate_on_submit():
        result_row = RaceResult().get_race_result(
            race_results_form.id_race_participants.data)

        if not result_row:

            times = []
            for participant, snail, result in participants:
                time = RaceResult().get_time_to_finish(participant.id)
                if time:
                    times.append(time[0])

            time_to_finish = race_results_form.time_to_finish.data
            new_times = calc_new_positions(times, time_to_finish)
            new_result_position = update_existing_positions(
                participants, new_times, time_to_finish)

            db.session.add(
                RaceResult(position=new_result_position,
                           time_to_finish=race_results_form.time_to_finish.
                           data,
                           did_not_finish=race_results_form.did_not_finish.
                           data,
                           id_race_participants=race_results_form.
                           id_race_participants.data))

            db.session.commit()
            flash("Race Result recorded for Race Participant ID {}.".format(
                race_results_form.id_race_participants.data))

        else:
            flash("Race Result Failed. Race Result already exists for Race "
                  "Participant ID {}.".format(race_results_form.
                                              id_race_participants.data))
        return redirect(url_for('result.race',
                                round_id=round_id,
                                race_id=race_id))

    elif race_results_form.errors.items():
        flash("Form submission not valid. Please resubmit.")
        return redirect(url_for('result.race',
                                round_id=round_id,
                                race_id=race_id))

    return render_template('results.html',
                           race=race,
                           participants=participants,
                           unresulted_participants=unresulted_participants,
                           race_results_form=race_results_form)


def validation(form):
    return form.validate()


def calc_new_positions(times, time_to_finish):
    times.append(time_to_finish)
    return sorted(times)


def update_existing_positions(participants, new_times, new_time_to_finish):
    for participant, snail, result in participants:
        result = RaceResult().get_race_result(participant.id)
        if result:
            result.position = new_times.index(result.time_to_finish) + 1

    return new_times.index(new_time_to_finish) + 1
