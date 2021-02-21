from config import config
from flask import Flask
from flask_bootstrap import Bootstrap
# from flask_wtf.csrf import CSRFProtect
from routes import *


app = Flask("__name__")

# app.secret_key = "numberforsecret1234509876"
# csrf_token = CSRFProtect(app)
app.register_blueprint(routes)
Bootstrap(app)

if __name__ == "__main__":
    app.run(debug=True)

