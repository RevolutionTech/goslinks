from http import HTTPStatus
from test.app_test_case import AppTestCase, SimpleTestCase
from unittest import mock

from flask import session

from goslinks.auth.decorators import login_required, no_cache
from goslinks.auth.loginpass import handle_authorize
from goslinks.auth.utils import logged_in_user


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
        with self.client.session_transaction() as sess:
            self.assertEqual(sess["auth_next_url"], "/hello/")
        self.assertStatus(response, HTTPStatus.FOUND)
        self.assertRedirects(response, "/login/google")

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


class HandleAuthorizeTestCase(AppTestCase):
    @mock.patch("goslinks.auth.loginpass.get_model")
    def test_handle_authorize(self, mock_get_model):
        mock_get_model.return_value = mock.Mock(
            update_or_create_user=lambda d: mock.Mock(email=self.USER_EMAIL)
        )

        user_info = {
            "email_verified": True,
            "hd": self.ORGANIZATION_NAME,
        }

        with self.app.test_request_context():
            response = handle_authorize(mock.Mock(), mock.Mock(), user_info)
            self.assertEqual(session["auth_email"], self.USER_EMAIL)
        self.assertStatus(response, HTTPStatus.FOUND)
        self.assertEqual(response.location, "/")

    @mock.patch("goslinks.auth.loginpass.get_model")
    def test_handle_authorize_with_next(self, mock_get_model):
        mock_get_model.return_value = mock.Mock(
            update_or_create_user=lambda d: mock.Mock(email=self.USER_EMAIL)
        )

        user_info = {
            "email_verified": True,
            "hd": self.ORGANIZATION_NAME,
        }
        next_url = "/foo"

        with self.app.test_request_context():
            session["auth_next_url"] = next_url
            response = handle_authorize(mock.Mock(), mock.Mock(), user_info)
        self.assertStatus(response, HTTPStatus.FOUND)
        self.assertEqual(response.location, next_url)

    def test_handle_authorize_requires_hosted_domain(self):
        user_info = {"email_verified": True}

        response_html, status_code = handle_authorize(
            mock.Mock(), mock.Mock(), user_info
        )
        self.assertEqual(
            response_html,
            "You must use a verified GSuite email address to authenticate.\n"
            'Try <a href="/login/google">logging in</a> again with your work account.',
        )
        self.assertEqual(status_code, HTTPStatus.UNAUTHORIZED)

    def test_handle_authorize_requires_verified_email(self):
        user_info = {"hd": self.ORGANIZATION_NAME}

        response_html, status_code = handle_authorize(
            mock.Mock(), mock.Mock(), user_info
        )
        self.assertEqual(
            response_html,
            "You must use a verified GSuite email address to authenticate.\n"
            'Try <a href="/login/google">logging in</a> again with your work account.',
        )
        self.assertEqual(status_code, HTTPStatus.UNAUTHORIZED)


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
