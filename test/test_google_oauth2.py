from unittest import mock

from flask import session

from goslinks.google_oauth2.decorators import no_cache
from goslinks.google_oauth2.utils import (
    logged_in_user,
    build_credentials,
    get_user_info,
)
from test.app_test_case import AppTestCase, SimpleTestCase


class NoCacheDecoratorTestCase(SimpleTestCase):

    CACHE_HEADERS = ("Cache-Control", "Pragma", "Expires")

    def test_view_without_decorator_missing_cache_headers(self):
        @self.app.route("/hello/")
        def hello():
            return "Hello World!"

        response = self.client.get("/hello/")

        for header in self.CACHE_HEADERS:
            self.assertNotIn(header, response.headers)

    def test_decorator_adds_cache_headers(self):
        @self.app.route("/hello/")
        @no_cache
        def hello():
            return "Hello World!"

        response = self.client.get("/hello/")

        for header in self.CACHE_HEADERS:
            self.assertIn(header, response.headers)


class LoggedInUserTestCase(AppTestCase):
    def test_logged_in_user(self):
        created_user = self.create_user()
        session["auth_email"] = created_user.email

        authenticated_user = logged_in_user()
        self.assertEqual(authenticated_user.email, created_user.email)

    def test_logged_in_user_returns_none_if_unauthenticated(self):
        self.assertIsNone(logged_in_user())


class BuildCredentialsTestCase(AppTestCase):
    @mock.patch("goslinks.google_oauth2.utils.google.oauth2.credentials.Credentials")
    def test_build_credentials(self, mock_google_oauth2_credentials):
        access_token = "OAUTH2_ACCESS_TOKEN"
        refresh_token = "OAUTH2_REFRESH_TOKEN"
        session["auth_token"] = {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }

        build_credentials()
        mock_google_oauth2_credentials.assert_called_once_with(
            access_token,
            refresh_token=refresh_token,
            client_id="GOOGLE_OAUTH2_CLIENT_ID",
            client_secret="GOOGLE_OAUTH2_CLIENT_SECRET",
            token_uri="https://www.googleapis.com/oauth2/v4/token",
        )

    def test_build_credentials_fails_without_authenticated_user(self):
        with self.assertRaises(AssertionError):
            build_credentials()


class GetUserInfoTestCase(AppTestCase):
    @mock.patch("goslinks.google_oauth2.utils.googleapiclient.discovery.build")
    @mock.patch(
        "goslinks.google_oauth2.utils.build_credentials", return_value="CREDENTIALS"
    )
    def test_get_user_info(self, mock_build_credentials, mock_build_oauth2_client):
        mock_build_oauth2_client.return_value = mock.Mock(
            userinfo=lambda: mock.Mock(
                get=lambda: mock.Mock(execute=lambda: self.ORIGINAL_USER_INFO)
            )
        )

        result = get_user_info()
        mock_build_oauth2_client.assert_called_with(
            "oauth2", "v2", credentials="CREDENTIALS"
        )
        self.assertEqual(result, self.ORIGINAL_USER_INFO)
