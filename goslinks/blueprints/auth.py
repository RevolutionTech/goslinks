from flask import Blueprint, redirect, session

from goslinks.auth.constants import AUTH_EMAIL_KEY, AUTH_NEXT_URL_KEY
from goslinks.auth.decorators import no_cache

bp = Blueprint("auth", __name__)


@bp.route("/logout/")
@no_cache
def logout():
    # Deprecated session variables, to be removed after 2020/10/13
    session.pop("auth_token", None)
    session.pop("auth_state", None)

    session.pop(AUTH_NEXT_URL_KEY, None)
    session.pop(AUTH_EMAIL_KEY, None)
    return redirect("/", code=302)
