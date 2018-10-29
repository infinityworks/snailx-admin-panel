from flask import render_template, Blueprint, url_for, redirect, flash
from flask_login import current_user
from db.models import Snail
from forms.forms import RaceResultsForm, AddSnailToRace
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

    return render_template('add_snail_to_race.html', all_snails=all_snails,
                           form=form)


def validation(form):
    return form.validate()
