from flask import Flask, render_template

from .db import LinkModel


app = Flask(__name__)


@app.route("/")
def links():
    return render_template("links.html", links=LinkModel.scan())
