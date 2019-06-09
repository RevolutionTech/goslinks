import unittest

from wtforms import Form

from goslinks.forms import SlugField


class SlugFieldTestCase(unittest.TestCase):
    class F(Form):
        slug = SlugField()

    def test_slug_field(self):
        form = self.F(slug="foo")
        self.assertTrue(form.validate())

    def test_slug_field_cleans_special_characters(self):
        form = self.F(slug="foo!bar")
        self.assertTrue(form.validate())
        self.assertEqual(form.data["slug"], "foobar")
