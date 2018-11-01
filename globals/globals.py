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
from routes.add_round.add_round import add_round_blueprint
from routes.login.logout import logout_blueprint
from routes.rounds.rounds import rounds_blueprint
from routes.races.races import races_blueprint
from routes.add_snail.add_snail import add_snail_blueprint
from routes.results.results import result_blueprint
from routes.add_race.add_race import add_race_blueprint
from routes.races.add_snail_to_race import add_snail_to_race_blueprint
from routes.add_trainer.add_trainer import add_trainer_blueprint


app.register_blueprint(login_blueprint)
app.register_blueprint(add_round_blueprint)
app.register_blueprint(logout_blueprint)
app.register_blueprint(rounds_blueprint)
app.register_blueprint(races_blueprint)
app.register_blueprint(add_snail_blueprint)
app.register_blueprint(result_blueprint)
app.register_blueprint(add_race_blueprint)
app.register_blueprint(add_snail_to_race_blueprint)
app.register_blueprint(add_trainer_blueprint)
