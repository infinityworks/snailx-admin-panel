from flask import render_template, Blueprint, redirect, url_for, flash, request
from forms.forms import LoginForm
from db.models import User, Snail
from flask_login import login_user, current_user, logout_user, login_required
from globals.globals import bcrypt, login_manager, db

@login_blueprint.route("/logout")
def logout():
    logout_user()
    return redirect_to('login.logout')