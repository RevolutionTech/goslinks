from authlib.client import OAuth2Session
from flask import Blueprint, current_app, make_response, redirect, request, session

from goslinks.db.factory import model_factory
from goslinks.google_oauth2.constants import (
    ACCESS_TOKEN_URI,
    AUTHORIZATION_URL,
    AUTHORIZATION_SCOPE,
    AUTH_EMAIL,
    AUTH_TOKEN_KEY,
    AUTH_STATE_KEY,
)
from goslinks.google_oauth2.decorators import no_cache
from goslinks.google_oauth2.utils import get_user_info

bp = Blueprint("google_oauth2", __name__)


@bp.route("/login/google")
@no_cache
def login():
    config = current_app.config
    oauth2_session = OAuth2Session(
        config["GOOGLE_OAUTH2_CLIENT_ID"],
        config["GOOGLE_OAUTH2_CLIENT_SECRET"],
        scope=AUTHORIZATION_SCOPE,
        redirect_uri=config["GOOGLE_OAUTH2_AUTH_REDIRECT_URI"],
    )

    uri, state = oauth2_session.authorization_url(AUTHORIZATION_URL)

    session[AUTH_STATE_KEY] = state
    session.permanent = True

    return redirect(uri, code=302)


@bp.route("/login/google/complete")
@no_cache
def google_auth_redirect():
    req_state = request.args.get("state", default=None, type=None)

    if req_state != session[AUTH_STATE_KEY]:
        response = make_response("Invalid state parameter", 401)
        return response

    config = current_app.config
    oauth2_session = OAuth2Session(
        config["GOOGLE_OAUTH2_CLIENT_ID"],
        config["GOOGLE_OAUTH2_CLIENT_SECRET"],
        scope=AUTHORIZATION_SCOPE,
        state=session[AUTH_STATE_KEY],
        redirect_uri=config["GOOGLE_OAUTH2_AUTH_REDIRECT_URI"],
    )

    oauth2_tokens = oauth2_session.fetch_access_token(
        ACCESS_TOKEN_URI, authorization_response=request.url
    )
    session[AUTH_TOKEN_KEY] = oauth2_tokens

    user_info = get_user_info()
    is_email_verified = user_info["verified_email"]
    if not is_email_verified:
        response = make_response(
            "Cannot authenticate a user without a verified email address.", 401
        )
        return response

    user = model_factory("user").update_or_create_user(user_info)
    session[AUTH_EMAIL] = user.email
    return redirect(config["GOOGLE_OAUTH2_BASE_URI"], code=302)


@bp.route("/logout/google")
@no_cache
def logout():
    session.pop(AUTH_EMAIL, None)
    session.pop(AUTH_TOKEN_KEY, None)
    session.pop(AUTH_STATE_KEY, None)

    config = current_app.config
    return redirect(config["GOOGLE_OAUTH2_BASE_URI"], code=302)
