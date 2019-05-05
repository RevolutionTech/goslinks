import google.oauth2.credentials
import googleapiclient.discovery
from flask import current_app, session

from goslinks.db.models import UserModel
from .constants import ACCESS_TOKEN_URI, AUTH_EMAIL, AUTH_TOKEN_KEY


def logged_in_user():
    email = session.get(AUTH_EMAIL)
    if email:
        return UserModel.get(email)


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
