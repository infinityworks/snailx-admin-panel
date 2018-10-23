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


from routes.index import index_blueprint, home_blueprint
from routes.login.login import login_blueprint
from routes.rounds.rounds import rounds_blueprint
from routes.races.races import races_blueprint


app.register_blueprint(index_blueprint)
app.register_blueprint(login_blueprint)
app.register_blueprint(home_blueprint)
app.register_blueprint(rounds_blueprint)
app.register_blueprint(races_blueprint)
