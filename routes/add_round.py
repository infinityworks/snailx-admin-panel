from flask import render_template, Blueprint, redirect, url_for, flash, request
from forms.forms import AddRoundForm
from db.models import Round
from globals.globals import db

add_round_blueprint = Blueprint('add_round', __name__)


@add_round_blueprint.route("/rounds/add", methods=["GET", "POST"])
def add_round():
    form = AddRoundForm()
    print("POSTED")
    if form.validate_on_submit():
        print("VALIDATED FORM")
        try:
            new_round = Round(
                name=form.name.data, start_date=form.start_date.data, end_date=form.end_date.data)
            db.session.add(new_round)
            db.session.commit()
            return redirect(url_for('index.index'))
        except:
            flash(
                'Failed to create new round. Check that round details are valid and try again.', 'danger')

    return render_template('add_round.html', title='Add Round', form=form)
