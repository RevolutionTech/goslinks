from flask_testing import TestCase

from goslinks.app import create_flask_app
from goslinks.config import TestingConfig
from goslinks.db.factory import get_model, get_models


class SimpleTestCase(TestCase):
    def create_app(self):
        return create_flask_app(TestingConfig)


class AppTestCase(SimpleTestCase):

    ORGANIZATION_NAME = "acme.com"
    USER_EMAIL = f"jsmith@{ORGANIZATION_NAME}"
    ORIGINAL_USER_INFO = {"email": USER_EMAIL, "name": "John Smith"}

    def setUp(self):
        for model in get_models():
            model.create_table()

    def tearDown(self):
        for model in get_models():
            model.delete_table()

    def create_user(self):
        user_model = get_model("user")
        user = user_model(**self.ORIGINAL_USER_INFO)
        user.save()
        return user
