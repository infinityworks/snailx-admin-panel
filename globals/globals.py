from flask import Flask


app = Flask(__name__)


from routes.index import index_blueprint

app.register_blueprint(index_blueprint)
