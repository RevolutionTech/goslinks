import unittest

from goslinks.helpers.slug import clean_to_slug


class CleanToSlugTestCase(unittest.TestCase):
    def test_clean_to_slug_keeps_valid_slug(self):
        self.assertEqual(clean_to_slug("foo"), "foo")

    def test_clean_to_slug_lowercases(self):
        self.assertEqual(clean_to_slug("FOO"), "foo")

    def test_clean_to_slug_removes_spaces(self):
        self.assertEqual(clean_to_slug("foo bar"), "foobar")

    def test_clean_to_slug_removes_underscores(self):
        self.assertEqual(clean_to_slug("foo_bar"), "foobar")

    def test_clean_to_slug_removes_dashes(self):
        self.assertEqual(clean_to_slug("foo-bar"), "foobar")

    def test_clean_to_slug_removes_pipes(self):
        self.assertEqual(clean_to_slug("foo|bar"), "foobar")

    def test_clean_to_slug_removes_misc_special_characters(self):
        special_chars = "`~!@#$%^&*()=+[]{};:'\"<>,./?\\"
        self.assertEqual(clean_to_slug(f"foo{special_chars}bar"), "foobar")
