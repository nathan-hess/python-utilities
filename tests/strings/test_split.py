import unittest

from pyxx.strings import split_at_index


class Test_SplitAtIndex(unittest.TestCase):
    def test_split_no_return_index(self):
        # Checks that format of returned tuple is correct when not returning
        # the character at position "index"
        self.assertTupleEqual(split_at_index('abcd', 0), ('', 'bcd'))
        self.assertTupleEqual(split_at_index('abcd', 1), ('a', 'cd'))
        self.assertTupleEqual(split_at_index('abcd', 2), ('ab', 'd'))
        self.assertTupleEqual(split_at_index('abcd', 3), ('abc', ''))

        self.assertTupleEqual(split_at_index('abcd', -4), ('', 'bcd'))
        self.assertTupleEqual(split_at_index('abcd', -3), ('a', 'cd'))
        self.assertTupleEqual(split_at_index('abcd', -2), ('ab', 'd'))
        self.assertTupleEqual(split_at_index('abcd', -1), ('abc', ''))

    def test_split_return_index(self):
        # Checks that format of returned tuple is correct when returning
        # the character at position "index"
        self.assertTupleEqual(split_at_index('abcd', 0, True), ('', 'a', 'bcd'))
        self.assertTupleEqual(split_at_index('abcd', 1, True), ('a', 'b', 'cd'))
        self.assertTupleEqual(split_at_index('abcd', 2, True), ('ab', 'c', 'd'))
        self.assertTupleEqual(split_at_index('abcd', 3, True), ('abc', 'd', ''))

        self.assertTupleEqual(split_at_index('abcd', -4, True), ('', 'a', 'bcd'))
        self.assertTupleEqual(split_at_index('abcd', -3, True), ('a', 'b', 'cd'))
        self.assertTupleEqual(split_at_index('abcd', -2, True), ('ab', 'c', 'd'))
        self.assertTupleEqual(split_at_index('abcd', -1, True), ('abc', 'd', ''))
