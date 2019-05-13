from goslinks.db.factory import get_model
from test.app_test_case import AppTestCase


class UserModelTestCase(AppTestCase):

    UPDATED_USER_INFO = {
        **AppTestCase.ORIGINAL_USER_INFO,
        "picture": "https://googleusercontent.com/abc123/photo.jpg",
    }

    def test_update_or_create_user_creates_nonexistent_user(self):
        user_model = get_model("user")
        self.assertEqual(user_model.count(self.USER_EMAIL), 0)
        user_model.update_or_create_user(self.UPDATED_USER_INFO)
        self.assertEqual(user_model.count(self.USER_EMAIL), 1)

    def test_update_or_create_user_updates_existing_user(self):
        user = self.create_user()
        user_model = get_model("user")
        self.assertEqual(user_model.count(self.USER_EMAIL), 1)

        user_model.update_or_create_user(self.UPDATED_USER_INFO)
        self.assertEqual(user_model.count(self.USER_EMAIL), 1)
        self.assertTrue(user_model.get(user.email).photo)


class LinkModelTestCase(AppTestCase):

    LINK_SLUG = "wiki"
    LINK_NAME = f"{AppTestCase.ORGANIZATION_NAME}|{LINK_SLUG}"

    def create_link(self):
        user = self.create_user()
        link_model = get_model("link")
        link = link_model(
            name=self.LINK_NAME, url="https://acme.atlassian.net/wiki", owner=user.email
        )
        link.save()
        return link

    def test_organization(self):
        link = self.create_link()
        self.assertEqual(link.organization, self.ORGANIZATION_NAME)

    def test_slug(self):
        link = self.create_link()
        self.assertEqual(link.slug, self.LINK_SLUG)

    def test_owner_user(self):
        link = self.create_link()
        self.assertEqual(link.owner_user.email, self.USER_EMAIL)
