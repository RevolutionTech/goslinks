from flask import Flask, render_template

from .db import LinkModel
from .google_oauth2.app import app as google_auth_app
from .google_oauth2.utils import logged_in_user

app = Flask(__name__)
app.config.from_object("goslinks.config.Config")
app.register_blueprint(google_auth_app)


@app.route("/")
def links():
    user = logged_in_user()
    return render_template("links.html", user=user, links=LinkModel.scan())
