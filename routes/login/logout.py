from flask import render_template, Blueprint, redirect, url_for, flash
from flask_login import logout_user, login_required, current_user
from globals.globals import login_manager
from db.models import User


logout_blueprint = Blueprint('logout', __name__)


@logout_blueprint.route("/logout")
def logout():
    if is_authenticated():
        logout_user()
        flash('Logout successful.')
        return redirect(url_for('login.login')) 
    else:
        flash('No user currently logged in.')
        return redirect(url_for('login.login'))

def is_authenticated():
    return current_user.is_authenticated