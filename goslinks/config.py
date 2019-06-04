import os

from dotenv import load_dotenv

load_dotenv()


class Config(object):
    SECRET_KEY = os.environ["GOSLINKS_SECRET_KEY"]

    MODEL_BASE_CLASS = "pynamodb.models.Model"
    MODEL_DYNAMODB_HOST = os.environ["GOSLINKS_MODEL_DYNAMODB_HOST"]

    GOOGLE_OAUTH2_CLIENT_ID = os.environ["GOSLINKS_GOOGLE_OAUTH2_CLIENT_ID"]
    GOOGLE_OAUTH2_CLIENT_SECRET = os.environ["GOSLINKS_GOOGLE_OAUTH2_CLIENT_SECRET"]


class TestingConfig(Config):
    TESTING = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False

    MODEL_BASE_CLASS = "test.fake_pynamodb.FakeModel"

    WTF_CSRF_ENABLED = False

    GOOGLE_OAUTH2_CLIENT_ID = "GOOGLE_OAUTH2_CLIENT_ID"
    GOOGLE_OAUTH2_CLIENT_SECRET = "GOOGLE_OAUTH2_CLIENT_SECRET"
