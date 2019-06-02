from http import HTTPStatus

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

    LINK_SLUG = "wiki"
    LINK_NAME = f"{ORGANIZATION_NAME}|{LINK_SLUG}"
    LINK_URL = "https://acme.atlassian.net/wiki"

    def assertFormErrors(self, response):
        self.assertStatus(response, HTTPStatus.OK)
        self.assertEqual(response.content_type, "text/html; charset=utf-8")
        self.assertIn('<ul class="errors">', response.get_data().decode("utf-8"))

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

    def login(self, email=None):
        if not email:
            user = self.create_user()
            email = user.email

        with self.client.session_transaction() as sess:
            sess["auth_email"] = email

        return email

    def create_link(self):
        user = self.create_user()
        link_model = get_model("link")
        link = link_model(name=self.LINK_NAME, url=self.LINK_URL, owner=user.email)
        link.save()
        return link
