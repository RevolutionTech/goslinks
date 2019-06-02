from http import HTTPStatus

from goslinks.db.factory import get_model
from test.app_test_case import AppTestCase


class GoslinkEditTestCase(AppTestCase):
    def test_edit_requires_authentication(self):
        response = self.client.get("/edit/foo")
        self.assertStatus(response, HTTPStatus.FOUND)
        self.assertRedirects(response, "/login/google")

    def test_edit_form_requires_url(self):
        self.login()

        response = self.client.post("/edit/foo", data={"slug": "foo"})
        self.assertFormErrors(response)

    def test_edit_form_url_must_be_valid(self):
        self.login()

        response = self.client.post(
            "/edit/foo", data={"slug": "foo", "url": "invalid-url"}
        )
        self.assertFormErrors(response)

    def test_create_new_link(self):
        email = self.login()

        response = self.client.post(
            "/edit/foo", data={"slug": "foo", "url": self.LINK_URL}
        )
        self.assertStatus(response, HTTPStatus.FOUND)

        _, organization = email.split("@")
        link = get_model("link").get_from_organization_and_slug(organization, "foo")
        self.assertEqual(link.url, self.LINK_URL)

    def test_create_new_link_with_different_slug(self):
        email = self.login()

        response = self.client.post(
            "/edit/foo", data={"slug": "bar", "url": self.LINK_URL}
        )
        self.assertStatus(response, HTTPStatus.FOUND)

        _, organization = email.split("@")
        link = get_model("link").get_from_organization_and_slug(organization, "bar")
        self.assertEqual(link.url, self.LINK_URL)

    def test_update_existing_link(self):
        link = self.create_link()
        self.login(link.owner)

        new_url = "https://example.com"
        response = self.client.post(
            f"/edit/{link.slug}", data={"slug": link.slug, "url": new_url}
        )
        self.assertStatus(response, HTTPStatus.FOUND)

        retrieved_link = get_model("link").get(link.name)
        self.assertEqual(retrieved_link.url, new_url)


class GoslinkRedirectTestCase(AppTestCase):
    def test_goslink_redirect_requires_authentication(self):
        response = self.client.get("/foo")
        self.assertStatus(response, HTTPStatus.FOUND)
        self.assertRedirects(response, "/login/google")

    def test_goslink_redirect_to_edit_page_with_new_slug(self):
        self.login()

        response = self.client.get("/foo")
        self.assertStatus(response, HTTPStatus.FOUND)
        self.assertRedirects(response, "/edit/foo")

    def test_goslink_redirect_to_link_url(self):
        link = self.create_link()
        self.login(link.owner)

        response = self.client.get(f"/{link.slug}")
        self.assertStatus(response, HTTPStatus.FOUND)
        self.assertRedirects(response, link.url)
