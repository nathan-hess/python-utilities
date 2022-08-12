import itertools
import unittest
from typing import List

from pyxx.strings import (
    contains_all_matched_brackets,
)


class Test_CheckContainsMatchedBrackets(unittest.TestCase):
    def setUp(self):
        self.test_brackets = [
            ('(', ')'),
            ('[', ']'),
            ('{', '}'),
        ]

    def __test_product(self, assert_func,
                       test_strings: List[str], test_brackets: List[str]):
        # Runs and tests `contains_all_matched_brackets()` for every possible
        # combination of `test_strings` and `test_brackets`
        for string, brackets in itertools.product(test_strings, test_brackets):
            with self.subTest(value=string, open=brackets[0], close=brackets[1]):
                opening_bracket=brackets[0]
                closing_bracket=brackets[1]

                test_string = string \
                    .replace('(', opening_bracket) \
                    .replace(')', closing_bracket)

                assert_func(contains_all_matched_brackets(
                    test_string, opening_bracket, closing_bracket))

    def test_matched(self):
        # Verifies that strings with matching brackets are correctly identified
        test_strings = [
            '(())() variables ((())())',
            '',
            '()',
            '(      )',
        ]

        self.__test_product(self.assertTrue, test_strings, self.test_brackets)

    def test_unmatched_count(self):
        # Verifies that strings with differing numbers of opening and closing
        # brackets are identified as not having matching brackets
        test_strings = [
            '((  )()',
            '((  (()',
        ]

        self.__test_product(self.assertFalse, test_strings, self.test_brackets)

    def test_unmatched_order(self):
        # Verifies that strings with equal numbers of opening and closing
        # brackets but in which each opening bracket does not correspond
        # to a closing bracket *later in the string* are identified as
        # not having matching brackets
        test_strings = [
            '()(()))(()',
            ')(()',
            ')(',
        ]

        self.__test_product(self.assertFalse, test_strings, self.test_brackets)

    def test_inputs_not_string(self):
        # Verifies that an error is thrown if attempting to call
        # the `contains_all_matched_brackets()` function with inputs
        # that are not strings
        with self.assertRaises(TypeError):
            contains_all_matched_brackets(32.2)

        with self.assertRaises(TypeError):
            contains_all_matched_brackets('value()', 3, ')')

        with self.assertRaises(TypeError):
            contains_all_matched_brackets('value()', '(', 5)

    def test_multi_char_brackets(self):
        # Verifies that an error is thrown if attempting to call
        # the `contains_all_matched_brackets()` function opening or closing
        # brackets that are not a single character
        with self.assertRaises(ValueError):
            contains_all_matched_brackets('value()', '((', ')')

        with self.assertRaises(ValueError):
            contains_all_matched_brackets('value()', '(', '))')

    def test_identical_brackets(self):
        # Verifies that an error is thrown if attempting to call
        # the `contains_all_matched_brackets()` function with the same
        # opening and closing bracket character
        with self.assertRaises(ValueError):
            contains_all_matched_brackets('value()', '#', '#')
