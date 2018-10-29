from flask import Blueprint, redirect, url_for, flash
from flask_login import logout_user, current_user


logout_blueprint = Blueprint('logout', __name__)


@logout_blueprint.route("/logout")
def logout():
    if is_active():
        logout_user()
        flash('Logout successful.')
        return redirect(url_for('login.login')) 
    else:
        flash('No user currently logged in.')
        return redirect(url_for('login.login'))


def is_active():
    return current_user.is_active