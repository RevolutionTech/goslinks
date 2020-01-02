import google.oauth2.credentials
import googleapiclient.discovery
from authlib.integrations.requests_client import OAuth2Session
from flask import current_app, request, session, url_for

from goslinks.db.factory import get_model
from goslinks.google_oauth2.constants import (
    ACCESS_TOKEN_URI,
    AUTHORIZATION_SCOPE,
    AUTH_EMAIL,
    AUTH_TOKEN_KEY,
)


def logged_in_user():
    email = session.get(AUTH_EMAIL)
    if email:
        user_model = get_model("user")
        try:
            return user_model.get(email)
        except user_model.DoesNotExist:
            # User has been deleted, remove from session
            session.pop(AUTH_EMAIL, None)


def build_oauth2_session(state=None):
    config = current_app.config
    return OAuth2Session(
        config["GOOGLE_OAUTH2_CLIENT_ID"],
        config["GOOGLE_OAUTH2_CLIENT_SECRET"],
        scope=AUTHORIZATION_SCOPE,
        state=state,
        redirect_uri=url_for("google_oauth2.google_auth_redirect", _external=True),
    )


def build_credentials():
    try:
        oauth2_tokens = session[AUTH_TOKEN_KEY]
    except KeyError:
        raise AssertionError("User must be logged in")

    config = current_app.config
    return google.oauth2.credentials.Credentials(
        oauth2_tokens["access_token"],
        refresh_token=oauth2_tokens["refresh_token"],
        client_id=config["GOOGLE_OAUTH2_CLIENT_ID"],
        client_secret=config["GOOGLE_OAUTH2_CLIENT_SECRET"],
        token_uri=ACCESS_TOKEN_URI,
    )


def get_user_info():
    credentials = build_credentials()
    oauth2_client = googleapiclient.discovery.build(
        "oauth2", "v2", credentials=credentials
    )
    return oauth2_client.userinfo().get().execute()
