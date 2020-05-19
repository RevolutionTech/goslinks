from http import HTTPStatus
from test.app_test_case import AppTestCase, SimpleTestCase
from unittest import mock

from flask import session

from goslinks.google_oauth2.decorators import login_required, no_cache
from goslinks.google_oauth2.utils import (
    build_credentials,
    build_oauth2_session,
    get_user_info,
    logged_in_user,
)


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


class LoginRequiredDecoratorTestCase(AppTestCase):
    def test_login_required_redirects_unauthenticated_user(self):
        @self.app.route("/hello/")
        @login_required
        def hello():
            return "Hello World!"

        response = self.client.get("/hello/")
        self.assertStatus(response, HTTPStatus.FOUND)
        self.assertRedirects(response, "/login/google?next=/hello/")

    def test_login_required_allows_authenticated_user(self):
        @self.app.route("/hello/")
        @login_required
        def hello():
            return "Hello World!"

        user = self.create_user()
        with self.client.session_transaction() as sess:
            sess["auth_email"] = user.email

        response = self.client.get("/hello/")
        self.assertStatus(response, HTTPStatus.OK)


class LoggedInUserTestCase(AppTestCase):
    def test_logged_in_user(self):
        created_user = self.create_user()
        session["auth_email"] = created_user.email

        authenticated_user = logged_in_user()
        self.assertEqual(authenticated_user.email, created_user.email)

    def test_logged_in_user_returns_none_if_unauthenticated(self):
        self.assertIsNone(logged_in_user())

    def test_logged_in_user_returns_none_if_does_not_exist(self):
        session["auth_email"] = self.USER_EMAIL
        self.assertIsNone(logged_in_user())
        self.assertNotIn("auth_email", session)


class BuildOAuth2SessionTestCase(AppTestCase):
    @mock.patch("goslinks.google_oauth2.utils.OAuth2Session")
    def test_build_oauth2_session(self, mock_oauth2_session):
        google_oauth2_state = "GOOGLE_OAUTH2_STATE"
        oauth2_session_mock = mock.Mock()
        mock_oauth2_session.return_value = oauth2_session_mock

        self.assertEqual(build_oauth2_session(google_oauth2_state), oauth2_session_mock)
        mock_oauth2_session.assert_called_once_with(
            "GOOGLE_OAUTH2_CLIENT_ID",
            "GOOGLE_OAUTH2_CLIENT_SECRET",
            scope="openid email profile",
            state=google_oauth2_state,
            redirect_uri="http://localhost/login/google/complete",
        )

    @mock.patch("goslinks.google_oauth2.utils.OAuth2Session")
    def test_build_oauth2_session_without_scope(self, mock_oauth2_session):
        build_oauth2_session()
        mock_oauth2_session.assert_called_once_with(
            "GOOGLE_OAUTH2_CLIENT_ID",
            "GOOGLE_OAUTH2_CLIENT_SECRET",
            scope="openid email profile",
            state=None,
            redirect_uri="http://localhost/login/google/complete",
        )


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
