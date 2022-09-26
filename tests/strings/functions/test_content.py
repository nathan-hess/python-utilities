import unittest

from pyxx.strings import (
    str_excludes_chars,
    str_includes_only,
)


class Test_StrExcludesChars(unittest.TestCase):
    def test_no_prohibited_chars(self):
        # Verifies that `True` is returned when no "prohibited" characters
        # are present
        self.assertTrue(str_excludes_chars('abcd12345*()', 'efg6'))
        self.assertTrue(str_excludes_chars('abcd12345*()', 'e'))

    def test_prohibited_chars(self):
        # Verifies that `False` is returned when "prohibited" characters
        # are present
        self.assertFalse(str_excludes_chars('abcd12345*()', 'def'))
        self.assertFalse(str_excludes_chars('abcd12345*()', '('))


class Test_StrIncludesOnly(unittest.TestCase):
    def test_all_allowed_chars(self):
        # Verifies that `True` is returned when only "allowed" characters
        # are present
        self.assertTrue(str_includes_only('abcd12345*()', 'abcdef123456*()'))
        self.assertTrue(str_includes_only('abcd12345*()', 'abcd12345*()'))
        self.assertTrue(str_includes_only('', 'abcd'))
        self.assertTrue(str_includes_only('', ''))

    def test_prohibited_chars(self):
        # Verifies that `False` is returned when any "non-allowed" characters
        # are present
        self.assertFalse(str_includes_only('abcde', 'abcd'))
        self.assertFalse(str_includes_only('abcd1234', 'efg'))
        self.assertFalse(str_includes_only('abc', ''))
