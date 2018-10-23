from flask import render_template, Blueprint, redirect, url_for, flash
from flask_login import logout_user, login_required
from globals.globals import login_manager
from db.models import User


logout_blueprint = Blueprint('logout', __name__)



@logout_blueprint.route("/logout")
@login_required
def logout():
    logout_user()
    flash('Logout successful.')
    return redirect(url_for('login.login'))