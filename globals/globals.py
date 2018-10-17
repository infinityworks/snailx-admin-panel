from flask import Flask
from config.config import Config

app = Flask(__name__)
app.config.from_object(Config)

from routes.index import index_blueprint
from routes.login.login import login_blueprint


app.register_blueprint(index_blueprint)
app.register_blueprint(login_blueprint)