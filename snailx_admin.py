from flask import Flask, render_template

# ------------------------------------------------ FLASK ---------------------------------------------------------------

app = Flask(__name__)


@app.route("/")
def html_home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)