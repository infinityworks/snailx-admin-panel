from flask import render_template, Blueprint, url_for, redirect
from flask_login import current_user
from db.models import Race


races_blueprint = Blueprint('races', __name__)


@races_blueprint.route('/races/<int:round_id>', methods=['GET'])
def races(round_id):
    if current_user.is_authenticated:  # TODO: not
        return redirect(url_for('login.login'))

    races = Race().get_races_by_round(round_id)

    return render_template('races.html', races=races)
