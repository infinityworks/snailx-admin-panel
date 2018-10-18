from flask import render_template, Blueprint, redirect
from forms.forms import LoginForm
from db.models import User, Snail

login_blueprint = Blueprint('login', __name__)


@login_blueprint.route("/login", methods=["GET", "POST"])
def index():
    form = LoginForm()

    if form.validate_on_submit():
        snails = Snail()
        return str(snails.get_all_snails())

        # user = User.query.filter_by(username=form.username.data).first()
        #
        # if current_user.is_authenticated:
        #     flash('You are already logged in')
        #     return redirect('/login')
        #
        # if user is None or not user.check_password(form.password.data):
        #     flash('Invalid username or password')
        #     return redirect('/login')
        #
        # login_user(user, remember=form.remember_me.data)

        return redirect('/')

    return render_template('login.html', title='Sign In', form=form)