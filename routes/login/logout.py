from flask import render_template, Blueprint, redirect, url_for, flash, request
from forms.forms import LoginForm
from flask_login import logout_user, login_required
from globals.globals import login_manager, db
from db.models import User



logout_blueprint = Blueprint('logout', __name__)

@logout_blueprint.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login.login'))