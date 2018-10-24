from flask import Blueprint, render_template, url_for, redirect
from flask_login import current_user
from forms.forms import AddRaceForm
from db.models import Race


add_race_blueprint = Blueprint('add_race', __name__)

@add_race_blueprint.route('/rounds/<int:round_id>/add_race', methods=['GET', 'POST'])
def add_race(round_id):
    if current_user.is_authenticated:  # TODO: NOT
        return redirect(url_for('login.login'))

    form = AddRaceForm()

    if form.validate_on_submit():
        race_date = form.date.data
        race_status = form.status.data

        return redirect(url_for('rounds.rounds'))

    return render_template('add_race.html', form=form)
