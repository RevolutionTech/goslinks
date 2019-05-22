from flask import Blueprint, current_app, make_response, redirect, request, session

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
    uri, state = oauth2_session.authorization_url(AUTHORIZATION_URL)

    session[AUTH_STATE_KEY] = state
    session.permanent = True

    return redirect(uri, code=302)


@bp.route("/login/google/complete")
@no_cache
def google_auth_redirect():
    req_state = request.args.get("state", default=None, type=None)

    if AUTH_STATE_KEY not in session or req_state != session[AUTH_STATE_KEY]:
        response = make_response("Invalid state parameter", 401)
        return response

    oauth2_session = build_oauth2_session(state=session[AUTH_STATE_KEY])
    oauth2_tokens = oauth2_session.fetch_access_token(
        ACCESS_TOKEN_URI, authorization_response=request.url
    )
    session[AUTH_TOKEN_KEY] = oauth2_tokens

    user_info = get_user_info()
    is_email_verified = user_info.get("verified_email", False)
    if not is_email_verified:
        response = make_response(
            "Cannot authenticate a user without a verified email address.", 401
        )
        return response

    user = get_model("user").update_or_create_user(user_info)
    session[AUTH_EMAIL] = user.email
    return redirect(current_app.config["GOOGLE_OAUTH2_BASE_URI"], code=302)


@bp.route("/logout/google")
@no_cache
def logout():
    session.pop(AUTH_EMAIL, None)
    session.pop(AUTH_TOKEN_KEY, None)
    session.pop(AUTH_STATE_KEY, None)

    config = current_app.config
    return redirect(config["GOOGLE_OAUTH2_BASE_URI"], code=302)
