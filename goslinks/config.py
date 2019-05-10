import os

from dotenv import load_dotenv

load_dotenv()


class Config(object):
    SECRET_KEY = os.environ["GOSLINKS_SECRET_KEY"]

    MODEL_REGISTRY = "goslinks.db.models.MODEL_REGISTRY"

    GOOGLE_OAUTH2_BASE_URI = os.environ["GOSLINKS_GOOGLE_OAUTH2_BASE_URI"]
    GOOGLE_OAUTH2_AUTH_REDIRECT_URI = f"{GOOGLE_OAUTH2_BASE_URI}/login/google/complete"
    GOOGLE_OAUTH2_CLIENT_ID = os.environ["GOSLINKS_GOOGLE_OAUTH2_CLIENT_ID"]
    GOOGLE_OAUTH2_CLIENT_SECRET = os.environ["GOSLINKS_GOOGLE_OAUTH2_CLIENT_SECRET"]
