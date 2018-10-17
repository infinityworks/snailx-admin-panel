from flask import Flask
import os


app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
print("############# CURRENT CONFIG: " +
      os.environ['APP_SETTINGS'] + " #############")


from routes.index import index_blueprint

app.register_blueprint(index_blueprint)
