from flask import render_template, Blueprint, url_for, redirect
from flask_login import current_user
from db.models import Race, Round
import datetime


races_blueprint = Blueprint('races', __name__)


@races_blueprint.route('/rounds/<int:round_id>/races', methods=['GET', 'POST'])
def races(round_id):
    if not current_user.is_authenticated:
        return redirect(url_for('login.login'))

    races = Race().get_races_by_round(round_id)
    current_round_toggle = validate_current_round_not_started(round_id)
    return render_template('races.html', races=races, round_id=round_id, current_round_toggle=current_round_toggle, now=time_now())


def validate_current_round_not_started(round_id):
    current_round = Round().get_round(round_id)
    if current_round.start_date >= datetime.datetime.utcnow():
        return True
    else:
        return False


def time_now():
    return datetime.datetime.utcnow()
