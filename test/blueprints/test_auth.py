from http import HTTPStatus
from test.app_test_case import AppTestCase


class AuthLogoutTestCase(AppTestCase):
    def test_logout(self):
        with self.client.session_transaction() as sess:
            sess["auth_next_url"] = "/foo"
            sess["auth_email"] = self.USER_EMAIL
            sess["auth_token"] = {
                "access_token": "OAUTH2_ACCESS_TOKEN",
                "refresh_token": "OAUTH2_REFRESH_TOKEN",
            }
            sess["auth_state"] = "GOOGLE_OAUTH2_STATE"

        response = self.client.get("/logout/")
        with self.client.session_transaction() as sess:
            self.assertNotIn("auth_next_url", sess)
            self.assertNotIn("auth_email", sess)
            self.assertNotIn("auth_token", sess)
            self.assertNotIn("auth_state", sess)
        self.assertStatus(response, HTTPStatus.FOUND)
        self.assertRedirects(response, "/")
