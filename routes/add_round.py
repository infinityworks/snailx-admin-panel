from flask import render_template, Blueprint, redirect, url_for, flash, request
from forms.forms import AddRoundForm

add_round_blueprint = Blueprint('add_round', __name__)


@add_round_blueprint.route("/rounds/add", methods=["GET", "POST"])
def add_round():
    form = AddRoundForm()

    if form.validate_on_submit():
        flash('Add Round Flash.', 'danger')

    return render_template('add_round.html', title='Add Round', form=form)
