from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
print("############# CURRENT CONFIG: " + os.environ['APP_SETTINGS'] + " #############")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


from routes.index import index_blueprint
from routes.login.login import login_blueprint


app.register_blueprint(index_blueprint)
app.register_blueprint(login_blueprint)