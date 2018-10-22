from flask import render_template, Blueprint, url_for, redirect
from flask_login import current_user
from db.models import Round
from datetime import datetime, timedelta


rounds_blueprint = Blueprint('rounds', __name__)


@rounds_blueprint.route('/rounds', methods=['GET'])
def rounds():
    if current_user.is_authenticated:  # TODO: not
        return redirect(url_for('login.login'))

    all_rounds = Round().get_all_rounds()
    present = datetime.now()

    for curr_round in all_rounds:
        if present > curr_round.start_date and present < curr_round.end_date:
            print("test")
            curr_round.active_round = True
            print("test2")
            break

    print(all_rounds)
    return render_template('rounds.html', title='Rounds', rounds=all_rounds)
