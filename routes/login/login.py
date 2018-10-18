from flask import render_template, Blueprint, redirect, url_for, flash, request
from forms.forms import LoginForm
from db.models import User, Snail
from flask_login import login_user, current_user, logout_user, login_required
from globals.globals import bcrypt, login_manager, db


login_blueprint = Blueprint('login', __name__)


@login_blueprint.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)