from flask import Blueprint, render_template, url_for, redirect, flash
from forms.forms import AddTrainerForm
from flask_login import current_user
from db.models import Trainer
from globals.globals import db
from routes.login.login import redirect_to

add_trainer_blueprint = Blueprint('add_trainer', __name__)


@add_trainer_blueprint.route('/trainer/add', methods=["GET", "POST"])
def add_trainer():

    if not current_user.is_authenticated:
        return redirect_to('login.login')

    form = AddTrainerForm()

    if form.validate_on_submit():
        trainer_name = form.name.data
        trainer_exists_in_db = Trainer().get_trainer_by_name(trainer_name)

        if trainer_exists_in_db >= 1:
            flash("This trainer name already exists")
            return redirect(url_for('add_trainer.add_trainer'))

        flash("Successfully added trainer")
        add_race_to_db(trainer_name)
        return redirect(url_for('add_trainer.add_trainer'))

    return render_template('add_trainer.html', form=form)


def add_race_to_db(trainer_name):
    trainer = Trainer(name=trainer_name)

    db.session.add(trainer)
    db.session.commit()
