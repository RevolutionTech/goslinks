from http import HTTPStatus
from unittest import mock

from test.app_test_case import AppTestCase


class GoogleOAuth2LoginTestCase(AppTestCase):
    @mock.patch("goslinks.blueprints.google_oauth2.build_oauth2_session")
    def test_login(self, mock_build_oauth2_session):
        google_oauth2_signin_url = "https://accounts.google.com/o/oauth2/v2/auth"
        google_oauth2_state = "GOOGLE_OAUTH2_STATE"
        mock_build_oauth2_session.return_value = mock.Mock(
            authorization_url=lambda url: (
                google_oauth2_signin_url,
                google_oauth2_state,
            )
        )

        response = self.client.get("/login/google")
        with self.client.session_transaction() as sess:
            self.assertEqual(sess["auth_state"], google_oauth2_state)
            self.assertTrue(sess.permanent)
        self.assertStatus(response, HTTPStatus.FOUND)
        self.assertRedirects(response, google_oauth2_signin_url)


class GoogleOAuth2RedirectTestCase(AppTestCase):
    def setUp(self):
        self.google_oauth2_state = "GOOGLE_OAUTH2_STATE"
        with self.client.session_transaction() as sess:
            sess["auth_state"] = self.google_oauth2_state

    @mock.patch("goslinks.blueprints.google_oauth2.get_model")
    @mock.patch(
        "goslinks.blueprints.google_oauth2.get_user_info",
        return_value={"verified_email": True},
    )
    @mock.patch("goslinks.blueprints.google_oauth2.build_oauth2_session")
    def test_google_auth_redirect(
        self, mock_build_oauth2_session, mock_get_user_info, mock_get_model
    ):
        oauth2_tokens = {
            "access_token": "OAUTH2_ACCESS_TOKEN",
            "refresh_token": "OAUTH2_REFRESH_TOKEN",
        }
        mock_build_oauth2_session.return_value = mock.Mock(
            fetch_access_token=lambda url, authorization_response: oauth2_tokens
        )
        mock_get_model.return_value = mock.Mock(
            update_or_create_user=lambda d: mock.Mock(email=self.USER_EMAIL)
        )

        response = self.client.get(
            f"/login/google/complete?state={self.google_oauth2_state}"
        )
        mock_build_oauth2_session.assert_called_once_with(
            state=self.google_oauth2_state
        )
        mock_get_user_info.assert_called_once()
        with self.client.session_transaction() as sess:
            self.assertEqual(sess["auth_token"], oauth2_tokens)
            self.assertEqual(sess["auth_email"], self.USER_EMAIL)
        self.assertStatus(response, HTTPStatus.FOUND)
        self.assertRedirects(response, "http://GOOGLE_OAUTH2_BASE_URI")

    def test_google_auth_redirect_requires_state_in_session(self):
        with self.client.session_transaction() as sess:
            del sess["auth_state"]

        response = self.client.get(
            f"/login/google/complete?state={self.google_oauth2_state}"
        )
        self.assertStatus(response, HTTPStatus.UNAUTHORIZED)

    def test_google_auth_redirect_requires_state_query_param(self):
        response = self.client.get("/login/google/complete")
        self.assertStatus(response, HTTPStatus.UNAUTHORIZED)

    def test_google_auth_redirect_requires_matching_state(self):
        response = self.client.get("/login/google/complete?state=WRONGSTATE")
        self.assertStatus(response, HTTPStatus.UNAUTHORIZED)

    @mock.patch("goslinks.blueprints.google_oauth2.get_user_info")
    @mock.patch("goslinks.blueprints.google_oauth2.build_oauth2_session")
    def test_google_auth_redirect_requires_verified_email(
        self, mock_build_oauth2_session, mock_get_user_info
    ):
        oauth2_tokens = {
            "access_token": "OAUTH2_ACCESS_TOKEN",
            "refresh_token": "OAUTH2_REFRESH_TOKEN",
        }
        mock_build_oauth2_session.return_value = mock.Mock(
            fetch_access_token=lambda url, authorization_response: oauth2_tokens
        )
        mock_get_user_info.return_value = self.ORIGINAL_USER_INFO

        response = self.client.get(
            f"/login/google/complete?state={self.google_oauth2_state}"
        )
        self.assertStatus(response, HTTPStatus.UNAUTHORIZED)


class GoogleOAuth2LogoutTestCase(AppTestCase):
    def test_logout(self):
        with self.client.session_transaction() as sess:
            sess["auth_email"] = self.USER_EMAIL
            sess["auth_token"] = {
                "access_token": "OAUTH2_ACCESS_TOKEN",
                "refresh_token": "OAUTH2_REFRESH_TOKEN",
            }
            sess["auth_state"] = "GOOGLE_OAUTH2_STATE"

        response = self.client.get("/logout/google")
        with self.client.session_transaction() as sess:
            self.assertNotIn("auth_email", sess)
            self.assertNotIn("auth_token", sess)
            self.assertNotIn("auth_state", sess)
        self.assertStatus(response, HTTPStatus.FOUND)
        self.assertRedirects(response, "http://GOOGLE_OAUTH2_BASE_URI")
