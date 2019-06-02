import unittest

from wtforms import Form

from goslinks.forms import SlugField


class SlugFieldTestCase(unittest.TestCase):
    class F(Form):
        slug = SlugField()

    def test_slug_field(self):
        form = self.F(slug="foo")
        self.assertTrue(form.validate())

    def test_slug_field_requires_value(self):
        form = self.F()
        self.assertFalse(form.validate())

    def test_slug_field_rejects_special_characters(self):
        form = self.F(slug="foo!bar")
        self.assertFalse(form.validate())
        self.assertIn("slug", form.errors)
        self.assertEqual(
            form.errors["slug"],
            ["Only lowercase letters, numbers, and dashes (-) are allowed."],
        )

    def test_slug_field_lowercases(self):
        form = self.F(slug="FOO")
        self.assertTrue(form.validate())
        self.assertEqual(form.data["slug"], "foo")

    def test_slug_field_converts_spaces(self):
        form = self.F(slug="foo bar")
        self.assertTrue(form.validate())
        self.assertEqual(form.data["slug"], "foo-bar")

    def test_slug_field_converts_underscores(self):
        form = self.F(slug="foo_bar")
        self.assertTrue(form.validate())
        self.assertEqual(form.data["slug"], "foo-bar")
