from flask import Blueprint, render_template
from flask_login import current_user
from db.models import Race


add_race_blueprint = Blueprint('add_race', __name__)

@add_race_blueprint.route('/rounds/<int:round_id>/add_race', methods=['GET', 'POST'])
def add_race(round_id):
    if current_user.is_authenticated: