import unittest

from pyxx.strings import str_excludes_chars


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
