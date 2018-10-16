import os
from flask import render_template
from globals.globals import app



if __name__ == "__main__":
    port = os.getenv('PORT') or 5001
    app.run(host='0.0.0.0', port=port, debug=True)
