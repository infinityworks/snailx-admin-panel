from flask import render_template, Blueprint, redirect, url_for, flash, request
from forms.forms import AddSnailForm
from flask_login import current_user
from db.models import Trainer, Snail
from globals.globals import db

add_snail_blueprint = Blueprint('add_snail', __name__)


@add_snail_blueprint.route("/snails/add", methods=["GET", "POST"])
def add_snail():
    if not current_user.is_authenticated:
        return redirect(url_for('login.login'))

    trainer_model = Trainer()
    form = AddSnailForm()
    form.trainer_name.choices = [(str(t.id), t.name) for t in trainer_model.get_all_trainers()]
    if form.validate_on_submit():
        if validate_snail_not_in_db(form.snail_name.data):
            flash('Snail already exists')
            return redirect(url_for('add_snail.add_snail'))

        if len(form.snail_name.data) > 12:
            flash('Snail name cannot be longer than 12 characters.')
            return redirect(url_for('add_snail.add_snail'))

        try:
            add_snail_to_db(form.snail_name.data.capitalize(), int(form.trainer_name.data))

        except:
            flash('Failed to create new snail, please check provided details are correct and try again.', 'error')
            return redirect(url_for('add_snail.add_snail'))

        flash('Snail successfully added.')
        return redirect(url_for('rounds.rounds'))

    return render_template('add_snail.html', title='Add Snail', form=form)


def validate_snail_not_in_db(name):
    return Snail().get_snail_by_name(name.capitalize())


def add_snail_to_db(snail_name, trainer_id):
    new_snail = Snail(name=snail_name, trainer_id=trainer_id)
    db.session.add(new_snail)
    db.session.commit()
