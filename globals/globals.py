from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)


from routes.login.login import login_blueprint
from routes.rounds.add_round import add_round_blueprint
from routes.login.logout import logout_blueprint
from routes.rounds.rounds import rounds_blueprint
from routes.races.races import races_blueprint
from routes.add_race.add_race import add_race_blueprint


app.register_blueprint(login_blueprint)
app.register_blueprint(add_round_blueprint)
app.register_blueprint(logout_blueprint)
app.register_blueprint(rounds_blueprint)
app.register_blueprint(races_blueprint)
app.register_blueprint(add_race_blueprint)