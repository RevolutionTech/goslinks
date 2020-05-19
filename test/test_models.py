from test.app_test_case import AppTestCase

from goslinks.db.factory import get_model


class UserModelTestCase(AppTestCase):

    UPDATED_USER_INFO = {
        **AppTestCase.ORIGINAL_USER_INFO,
        "picture": "https://googleusercontent.com/abc123/photo.jpg",
    }

    def test_organization(self):
        user = self.create_user()
        self.assertEqual(user.organization, self.ORGANIZATION_NAME)

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
    def test_organization(self):
        link = self.create_link()
        self.assertEqual(link.organization, self.ORGANIZATION_NAME)

    def test_slug(self):
        link = self.create_link()
        self.assertEqual(link.slug, self.LINK_SLUG)

    def test_owner_user(self):
        link = self.create_link()
        self.assertEqual(link.owner_user.email, self.USER_EMAIL)

    def test_get_from_organization_and_slug(self):
        created_link = self.create_link()
        retrieved_link = get_model("link").get_from_organization_and_slug(
            created_link.organization, created_link.slug
        )
        self.assertEqual(retrieved_link, created_link)

    def test_get_or_init_new_link(self):
        user = self.create_user()
        link = get_model("link").get_or_init(user=user, slug=self.LINK_SLUG)
        self.assertEqual(link.name, self.LINK_NAME)
        self.assertEqual(link.owner, user.email)

    def test_get_or_init_existing_link(self):
        link = self.create_link()
        user = link.owner_user

        existing_link = get_model("link").get_or_init(user=user, slug=link.slug)
        self.assertEqual(existing_link.name, link.name)
        self.assertEqual(existing_link.owner, user.email)
