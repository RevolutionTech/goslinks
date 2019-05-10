from flask import Blueprint, render_template

from goslinks.db.models import LinkModel
from goslinks.google_oauth2.utils import logged_in_user

bp = Blueprint("goslinks", __name__)


@bp.route("/")
def links():
    user = logged_in_user()
    return render_template("links.html", user=user, links=LinkModel.scan())
