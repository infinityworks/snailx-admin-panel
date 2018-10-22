from flask import render_template, Blueprint

index_blueprint = Blueprint('index', __name__)
home_blueprint = Blueprint('home', __name__)

@index_blueprint.route("/")
def index():
    return render_template("index.html")

@home_blueprint.route("/home")
def home():
    return render_template("index.html")