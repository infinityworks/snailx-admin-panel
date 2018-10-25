from flask import render_template, Blueprint, url_for, redirect
from flask_login import current_user
from db.models import RaceResult, Race, RaceParticipants


result_blueprint = Blueprint('result', __name__)


@result_blueprint.route('/rounds/<int:round_id>/races/<int:race_id>', methods=['GET'])
def race(round_id, race_id):
    if not current_user.is_authenticated:
        return redirect(url_for('login.login'))

    race = Race().get_race(race_id)
    participants = RaceParticipants().get_race_participants_race_id(race_id)

    return render_template('results.html', race=race, participants=participants)

