import itertools
import unittest
from typing import List

from pyxx.strings import (
    contains_all_matched_brackets,
    find_matching_bracket,
    find_skip_brackets,
)
from pyxx.strings.brackets import _check_valid_brackets
from pyxx.strings.exceptions import (
    NotABracketError,
    UnmatchedBracketsError,
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
            opening_bracket = brackets[0]
            closing_bracket = brackets[1]

            with self.subTest(value=string, open=opening_bracket,
                              close=closing_bracket):
                # Replace brackets in input string
                test_string = string \
                    .replace('(', opening_bracket) \
                    .replace(')', closing_bracket)

                # Run check
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
            opening_bracket: str = brackets[0]
            closing_bracket: str = brackets[1]

            with self.subTest(value=case['value'], begin=case['begin'],
                              open=opening_bracket, close=closing_bracket):
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


class Test_FindSkipBrackets(unittest.TestCase):
    def setUp(self):
        self.test_brackets = [
            ('(', ')'),
            ('[', ']'),
            ('{', '}'),
        ]

    def __test_product(self, test_cases: List[dict]):
        # Runs and tests `find_skip_brackets()` for every possible
        # combination of `test_cases` and `self.test_brackets`
        for case, brackets in itertools.product(test_cases, self.test_brackets):
            with self.subTest(value=case['value'], target=case['target_chars'],
                    direction=case['direction'], begin=case['begin'],
                    open=brackets[0], close=brackets[1]):
                opening_bracket: str = brackets[0]
                closing_bracket: str = brackets[1]

                # Replace brackets in input string
                test_string = case['value'] \
                    .replace('(', opening_bracket) \
                    .replace(')', closing_bracket)

                # Run check
                self.assertEqual(
                    find_skip_brackets(test_string, case['target_chars'],
                        case['begin'], case['direction'],
                        opening_bracket, closing_bracket),
                    case['ground_truth'])

    def test_invalid_direction(self):
        # Verifies that an error is thrown if "direction" argument is not valid
        with self.assertRaises(ValueError):
            find_skip_brackets('abcd', 'd', 0, 'invalid_direction')

    def test_invalid_search_string(self):
        # Verifies that an error is thrown if "value" argument is not a string
        with self.assertRaises(TypeError):
            find_skip_brackets(100, 'd', 0, 'invalid_direction')

    def test_invalid_begin_index(self):
        # Verifies that an error is thrown if "begin" argument is not a valid
        # index within the length of the string
        with self.assertRaises(IndexError):
            find_skip_brackets('abcd', 'd', -5)

        with self.assertRaises(IndexError):
            find_skip_brackets('abcd', 'd', 4)

    def test_invalid_unmatched_brackets(self):
        # Verifies that an error is thrown if "value" argument has
        # unmatched brackets
        with self.assertRaises(UnmatchedBracketsError):
            find_skip_brackets('abc(d(ef)ghi', 'i', 2)

        with self.assertRaises(UnmatchedBracketsError):
            find_skip_brackets('abc(d(ef)ghi', 'i', 4)

    def test_no_brackets(self):
        # Verifies that correct index is found in strings with no brackets
        test_cases = [
            {'value': 'abcdef1a234a5',  'target_chars': 'a',         'begin': 0,  'direction': 'forward',  'ground_truth': 0},
            {'value': 'abcdef1a234a5',  'target_chars': 'a',         'begin': 1,  'direction': 'forward',  'ground_truth': 7},
            {'value': 'abcdef1a234a5',  'target_chars': 'acf',       'begin': 1,  'direction': 'forward',  'ground_truth': 2},
            {'value': 'abcdef1a234a5',  'target_chars': 'g',         'begin': 0,  'direction': 'forward',  'ground_truth': -1},
            {'value': 'abcdef1a234a5',  'target_chars': 'f',         'begin': 7,  'direction': 'forward',  'ground_truth': -1},
            {'value': 'abcdef1a234a5',  'target_chars': ('a',),      'begin': 0,  'direction': 'forward',  'ground_truth': 0},
            {'value': 'abcdef1a234a5',  'target_chars': ('a', 'c'),  'begin': 1,  'direction': 'forward',  'ground_truth': 2},
            {'value': 'abcdef1a234a5',  'target_chars': ('g', 'h'),  'begin': 1,  'direction': 'forward',  'ground_truth': -1},
                                                                                                                         
            {'value': 'abcdef1a234a5',  'target_chars': 'a',         'begin': 4,   'direction': 'reverse',  'ground_truth': 0},
            {'value': 'abcdef1a234a5',  'target_chars': 'a',         'begin': -2,  'direction': 'reverse',  'ground_truth': 11},
            {'value': 'abcdef1a234a5',  'target_chars': 'acf',       'begin': 6,   'direction': 'reverse',  'ground_truth': 5},
            {'value': 'abcdef1a234a5',  'target_chars': 'g',         'begin': -1,  'direction': 'reverse',  'ground_truth': -1},
            {'value': 'abcdef1a234a5',  'target_chars': 'f',         'begin': 4,   'direction': 'reverse',  'ground_truth': -1},
            {'value': 'abcdef1a234a5',  'target_chars': ('a',),      'begin': 4,   'direction': 'reverse',  'ground_truth': 0},
            {'value': 'abcdef1a234a5',  'target_chars': ('a', 'c'),  'begin': 5,   'direction': 'reverse',  'ground_truth': 2},
            {'value': 'abcdef1a234a5',  'target_chars': ('g', 'h'),  'begin': 5,   'direction': 'reverse',  'ground_truth': -1},
        ]

        self.__test_product(test_cases)

    def test_begin_outside_brackets(self):
        # Verifies that correct index is found in strings with brackets, beginning
        # the search outside the brackets
        test_cases = [
            {'value': 'abc (deabfef(e)f) 1a2a5',  'target_chars': 'a',         'begin': 0,   'direction': 'forward',  'ground_truth': 0},
            {'value': 'abc (deabfef(e)f) 1a2a5',  'target_chars': 'a',         'begin': 1,   'direction': 'forward',  'ground_truth': 19},
            {'value': 'abc (deabfef(e)f) 1a2a5',  'target_chars': 'a1',        'begin': 1,   'direction': 'forward',  'ground_truth': 18},
            {'value': 'abc (deabfef(e)f) 1a2a5',  'target_chars': 'c',         'begin': 16,  'direction': 'forward',  'ground_truth': -1},
            {'value': 'abc (deabfef(e)f) 1a2a5',  'target_chars': 'a5',        'begin': -3,  'direction': 'forward',  'ground_truth': 21},
            {'value': 'abc (deabfef(e)f) 1a2a5',  'target_chars': ('a',),      'begin': 1,   'direction': 'forward',  'ground_truth': 19},
            {'value': 'abc (deabfef(e)f) 1a2a5',  'target_chars': ('a', '1'),  'begin': 1,   'direction': 'forward',  'ground_truth': 18},
            {'value': 'abc (deabfef(e)f) 1a2a5',  'target_chars': ('c',),      'begin': 16,  'direction': 'forward',  'ground_truth': -1},

            {'value': 'abc (deabfef(e)f) 1a2a5',  'target_chars': 'b',         'begin': 1,   'direction': 'reverse',  'ground_truth': 1},
            {'value': 'abc (deabfef(e)f) 1a2a5',  'target_chars': 'b',         'begin': 19,  'direction': 'reverse',  'ground_truth': 1},
            {'value': 'abc (deabfef(e)f) 1a2a5',  'target_chars': 'bc',        'begin': 19,  'direction': 'reverse',  'ground_truth': 2},
            {'value': 'abc (deabfef(e)f) 1a2a5',  'target_chars': '5',         'begin': 19,  'direction': 'reverse',  'ground_truth': -1},
            {'value': 'abc (deabfef(e)f) 1a2a5',  'target_chars': ('b',),      'begin': 19,  'direction': 'reverse',  'ground_truth': 1},
            {'value': 'abc (deabfef(e)f) 1a2a5',  'target_chars': ('b', 'c'),  'begin': 19,  'direction': 'reverse',  'ground_truth': 2},
            {'value': 'abc (deabfef(e)f) 1a2a5',  'target_chars': ('5',),      'begin': 19,  'direction': 'reverse',  'ground_truth': -1},
        ]

        self.__test_product(test_cases)

    def test_begin_inside_brackets(self):
        # Verifies that correct index is found in strings with brackets, beginning
        # the search inside the brackets
        test_cases = [
            {'value': 'abc (deabfef(eq)fbe) 1a2a5',  'target_chars': 'a',         'begin': 5,    'direction': 'forward',  'ground_truth': 7},
            {'value': 'abc (deabfef(eq)fbe) 1a2a5',  'target_chars': 'b',         'begin': 9,    'direction': 'forward',  'ground_truth': 17},
            {'value': 'abc (deabfef(eq)fbe) 1a2a5',  'target_chars': 'e',         'begin': 11,   'direction': 'forward',  'ground_truth': 18},
            {'value': 'abc (deabfef(eq)fbe) 1a2a5',  'target_chars': 'be',        'begin': 11,   'direction': 'forward',  'ground_truth': 17},
            {'value': 'abc (deabfef(eq)fbe) 1a2a5',  'target_chars': 'q',         'begin': 6,    'direction': 'forward',  'ground_truth': -1},
            {'value': 'abc (deabfef(eq)fbe) 1a2a5',  'target_chars': 'qv',        'begin': 12,   'direction': 'forward',  'ground_truth': -1},
            {'value': 'abc (deabfef(eq)fbe) 1a2a5',  'target_chars': 'qv',        'begin': 13,   'direction': 'forward',  'ground_truth': 14},
            {'value': 'abc (deabfef(eq)fbe) 1a2a5',  'target_chars': 'bqv',       'begin': -16,  'direction': 'forward',  'ground_truth': 17},
            {'value': 'abc (deabfef(eq)fbe) 1a2a5',  'target_chars': ('e',),      'begin': 11,   'direction': 'forward',  'ground_truth': 18},
            {'value': 'abc (deabfef(eq)fbe) 1a2a5',  'target_chars': ('b', 'e'),  'begin': 11,   'direction': 'forward',  'ground_truth': 17},
            {'value': 'abc (deabfef(eq)fbe) 1a2a5',  'target_chars': ('q',),      'begin': 6,    'direction': 'forward',  'ground_truth': -1},
        
            {'value': 'abc (deabfef(eq)fbe) 1a2a5',  'target_chars': 'b',         'begin': 18,  'direction': 'reverse',  'ground_truth': 17},
            {'value': 'abc (deabfef(eq)fbe) 1a2a5',  'target_chars': 'b',         'begin': 16,  'direction': 'reverse',  'ground_truth': 8},
            {'value': 'abc (deabfef(eq)fbe) 1a2a5',  'target_chars': 'e',         'begin': 17,  'direction': 'reverse',  'ground_truth': 10},
            {'value': 'abc (deabfef(eq)fbe) 1a2a5',  'target_chars': 'cd',        'begin': 17,  'direction': 'reverse',  'ground_truth': 5},
            {'value': 'abc (deabfef(eq)fbe) 1a2a5',  'target_chars': 'q',         'begin': 17,  'direction': 'reverse',  'ground_truth': -1},
            {'value': 'abc (deabfef(eq)fbe) 1a2a5',  'target_chars': 'qv',        'begin': 17,  'direction': 'reverse',  'ground_truth': -1},
            {'value': 'abc (deabfef(eq)fbe) 1a2a5',  'target_chars': 'ev',        'begin': 14,  'direction': 'reverse',  'ground_truth': 13},
            {'value': 'abc (deabfef(eq)fbe) 1a2a5',  'target_chars': 'ade',       'begin': -9,  'direction': 'reverse',  'ground_truth': 10},
            {'value': 'abc (deabfef(eq)fbe) 1a2a5',  'target_chars': ('e',),      'begin': 17,  'direction': 'reverse',  'ground_truth': 10},
            {'value': 'abc (deabfef(eq)fbe) 1a2a5',  'target_chars': ('c', 'd'),  'begin': 17,  'direction': 'reverse',  'ground_truth': 5},
            {'value': 'abc (deabfef(eq)fbe) 1a2a5',  'target_chars': ('q',),      'begin': 17,  'direction': 'reverse',  'ground_truth': -1},
        ]

        self.__test_product(test_cases)
