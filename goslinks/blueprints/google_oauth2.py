import urllib

from flask import Blueprint, make_response, redirect, render_template, request, session

from goslinks.db.factory import get_model
from goslinks.google_oauth2.constants import (
    ACCESS_TOKEN_URI,
    AUTHORIZATION_URL,
    AUTH_EMAIL,
    AUTH_TOKEN_KEY,
    AUTH_STATE_KEY,
)
from goslinks.google_oauth2.decorators import no_cache
from goslinks.google_oauth2.utils import build_oauth2_session, get_user_info

bp = Blueprint("google_oauth2", __name__)


@bp.route("/login/google")
@no_cache
def login():
    oauth2_session = build_oauth2_session()
    uri, state_token = oauth2_session.create_authorization_url(AUTHORIZATION_URL)

    state_params = {"token": state_token}
    if "next" in request.args:
        state_params["next"] = request.args["next"]
    state = urllib.parse.urlencode(state_params)

    session[AUTH_STATE_KEY] = state
    session.permanent = True

    return redirect(uri, code=302)


@bp.route("/login/google/complete")
@no_cache
def google_auth_redirect():
    req_state_token = request.args.get("state", default=None, type=None)

    if AUTH_STATE_KEY not in session:
        return make_response("Missing state parameter", 401)

    state_params = dict(urllib.parse.parse_qsl(session[AUTH_STATE_KEY]))
    if not req_state_token or req_state_token != state_params.get("token"):
        return make_response("Invalid state parameter", 401)

    oauth2_session = build_oauth2_session(state=state_params["token"])
    oauth2_tokens = oauth2_session.fetch_access_token(
        ACCESS_TOKEN_URI, authorization_response=request.url
    )
    session[AUTH_TOKEN_KEY] = oauth2_tokens

    user_info = get_user_info()
    is_email_verified = user_info.get("verified_email", False)
    if "hd" not in user_info or not is_email_verified:
        return render_template("google_oauth2_error.html"), 401

    user = get_model("user").update_or_create_user(user_info)
    session[AUTH_EMAIL] = user.email

    next_url = state_params.get("next", "/")
    return redirect(next_url, code=302)


@bp.route("/logout/google")
@no_cache
def logout():
    session.pop(AUTH_EMAIL, None)
    session.pop(AUTH_TOKEN_KEY, None)
    session.pop(AUTH_STATE_KEY, None)
    return redirect("/", code=302)
