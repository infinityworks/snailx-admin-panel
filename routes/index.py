from flask import render_template, Blueprint
from globals.globals import app

index_blueprint = Blueprint('index', __name__)


@index_blueprint.route("/")
def index():
    return render_template("index.html")