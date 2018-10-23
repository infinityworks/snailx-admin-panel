from flask import render_template, Blueprint, redirect, url_for, flash
from forms.forms import LoginForm
from db.models import User
from flask_login import current_user
from globals.globals import bcrypt, login_manager, db


login_blueprint = Blueprint('login', __name__)


@login_blueprint.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = get_username(form.username.data)
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            return redirect(url_for('index.index'))
        else:
            flash('Login Unsuccessful. Invalid Credentials.', 'danger')
    return render_template('login.html', title='Login', form=form)

def get_username(username):
    return User().get_user_by_username(username)
