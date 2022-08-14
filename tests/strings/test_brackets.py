import itertools
import unittest
from typing import List

from pyxx.strings import (
    contains_all_matched_brackets,
    find_matching_bracket,
)
from pyxx.strings.brackets import _check_valid_brackets
from pyxx.strings.exceptions import (
    NotABracketError,
)


class Test_ValidateBrackets(unittest.TestCase):
    def test_valid_brackets(self):
        # Verifies that the `_check_valid_brackets()` function correctly
        # identifies valid brackets
        test_brackets = [
            ('(', ')'),
            ('[', ']'),
            ('{', '}'),
            ('a', 'b'),
        ]

        for brackets in test_brackets:
            with self.subTest(brackets=brackets):
                self.assertTrue(_check_valid_brackets(*brackets))

    def test_brackets_not_str(self):
        # Verifies that an error is thrown if attempting to call
        # the `_check_valid_brackets()` function with inputs
        # that are not strings
        with self.assertRaises(TypeError):
            _check_valid_brackets(3, ')')

        with self.assertRaises(TypeError):
            _check_valid_brackets('(', 5)

    def test_multi_char_brackets(self):
        # Verifies that an error is thrown if attempting to call
        # the `_check_valid_brackets()` function opening or closing
        # brackets that are not a single character
        with self.assertRaises(ValueError):
            _check_valid_brackets('((', ')')

        with self.assertRaises(ValueError):
            _check_valid_brackets('(', '))')

    def test_identical_brackets(self):
        # Verifies that an error is thrown if attempting to call
        # the `_check_valid_brackets()` function with the same
        # opening and closing bracket character
        with self.assertRaises(ValueError):
            _check_valid_brackets('#', '#')


class Test_CheckContainsMatchedBrackets(unittest.TestCase):
    def setUp(self):
        self.test_brackets = [
            ('(', ')'),
            ('[', ']'),
            ('{', '}'),
        ]

    def __test_product(self, assert_func, test_strings: List[str]):
        # Runs and tests `contains_all_matched_brackets()` for every possible
        # combination of `test_strings` and `self.test_brackets`
        for string, brackets in itertools.product(test_strings, self.test_brackets):
            with self.subTest(value=string, open=brackets[0], close=brackets[1]):
                opening_bracket = brackets[0]
                closing_bracket = brackets[1]

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

        self.__test_product(self.assertTrue, test_strings)

    def test_unmatched_count(self):
        # Verifies that strings with differing numbers of opening and closing
        # brackets are identified as not having matching brackets
        test_strings = [
            '((  )()',
            '((  (()',
        ]

        self.__test_product(self.assertFalse, test_strings)

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

        self.__test_product(self.assertFalse, test_strings)

    def test_inputs_not_string(self):
        # Verifies that an error is thrown if attempting to call
        # the `contains_all_matched_brackets()` function with inputs
        # that are not strings
        with self.assertRaises(TypeError):
            contains_all_matched_brackets(32.2)


class Test_FindMatchingBracket(unittest.TestCase):
    def setUp(self):
        self.test_brackets = [
            ('(', ')'),
            ('[', ']'),
            ('{', '}'),
        ]

    def __test_product(self, test_cases: List[dict]):
        # Runs and tests `find_matching_bracket()` for every possible
        # combination of `test_cases` and `self.test_brackets`
        for case, brackets in itertools.product(test_cases, self.test_brackets):
            with self.subTest(value=case['value'], begin=case['begin'],
                              open=brackets[0], close=brackets[1]):
                opening_bracket: str = brackets[0]
                closing_bracket: str = brackets[1]

                # Replace brackets in input string
                test_string = case['value'] \
                    .replace('(', opening_bracket) \
                    .replace(')', closing_bracket)

                # Run check
                self.assertEqual(
                    find_matching_bracket(test_string, case['begin'],
                                          opening_bracket, closing_bracket),
                    case['ground_truth'])

    def test_find_index_forward(self):
        # Verify that matching bracket index is identified correctly
        # when searching in the forward direction
        test_cases = [
            {'value': '(  )',        'begin': 0, 'ground_truth': 3},
            {'value': ' ()',         'begin': 1, 'ground_truth': 2},
            {'value': '(()(()))  )', 'begin': 0, 'ground_truth': 7},
            {'value': '(()(()))  )', 'begin': 1, 'ground_truth': 2},
        ]

        self.__test_product(test_cases)

    def test_find_index_reverse(self):
        # Verify that matching bracket index is identified correctly
        # when searching in the reverse direction
        test_cases = [
            {'value': '(  )',        'begin': 3, 'ground_truth': 0},
            {'value': ' ()',         'begin': 2, 'ground_truth': 1},
            {'value': '(()(()))  )', 'begin': 7, 'ground_truth': 0},
            {'value': '(()(()))  )', 'begin': 2, 'ground_truth': 1},
        ]

        self.__test_product(test_cases)

    def test_find_negative_index(self):
        # Verify that matching bracket index is identified correctly
        # when providing a negative `begin` index
        test_cases = [
            {'value': '(  )',        'begin': -1, 'ground_truth': 0},
            {'value': ' ()',         'begin': -2, 'ground_truth': 2},
            {'value': '(()(()))  )', 'begin': -5, 'ground_truth': 3},
        ]

        self.__test_product(test_cases)

    def test_find_no_match(self):
        # Verify that -1 is returned if there is no matching bracket
        test_cases = [
            {'value': '( ( ) ', 'begin': 0,  'ground_truth': -1},
            {'value': '( ( ) ', 'begin': -6, 'ground_truth': -1},
            {'value': '( ) ) ', 'begin': 4,  'ground_truth': -1},
            {'value': '( ) ) ', 'begin': -2, 'ground_truth': -1},
        ]

        self.__test_product(test_cases)

    def test_no_begin_bracket(self):
        # Verify that an error is thrown if the character at index
        # `begin` is not a bracket
        with self.assertRaises(NotABracketError):
            find_matching_bracket('( ( ) ', 1)

        with self.assertRaises(NotABracketError):
            find_matching_bracket('( ( ) ', -1)
