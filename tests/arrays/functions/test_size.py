from typing import List
import unittest

from pyxx.arrays import (
    check_len_equal,
    is_len_equal,
    max_list_item_len,
)


class Test_CheckLenEqual(unittest.TestCase):
    def test_check_list_equal(self):
        # Verifies that lengths of lists are evaluated correctly
        with self.subTest(num_lists=2):
            self.assertTupleEqual(
                check_len_equal(['a', 'b', 'c'], [1, 2, 3]),
                (True, 3)
            )
            self.assertTupleEqual(check_len_equal(['a'], [1]), (True, 1))

        with self.subTest(num_lists=3):
            self.assertTupleEqual(
                check_len_equal(['a', 'b'], [1, 2], ['cd', 3]),
                (True, 2)
            )
            self.assertTupleEqual(check_len_equal(['a'], [1], ['c']), (True, 1))

        with self.subTest(num_lists=4):
            self.assertTupleEqual(
                check_len_equal(['a', 'b'], [1, 2], ['cd', 3], [None, None]),
                (True, 2)
            )
            self.assertTupleEqual(check_len_equal(['a'], [1], ['c'], [None]), (True, 1))

    def test_check_tuple_equal(self):
        # Verifies that lengths of tuples are evaluated correctly
        with self.subTest(num_tuples=2):
            self.assertTupleEqual(
                check_len_equal(('a', 'b', 'c'), (1, 2, 3)),
                (True, 3)
            )
            self.assertTupleEqual(check_len_equal(('a',), (1,)), (True, 1))

        with self.subTest(num_tuples=3):
            self.assertTupleEqual(
                check_len_equal(('a', 'b'), (1, 2), ('cd', 3)),
                (True, 2)
            )
            self.assertTupleEqual(check_len_equal(('a',), (1,), ('cd',)), (True, 1))

        with self.subTest(num_tuples=4):
            self.assertTupleEqual(
                check_len_equal(('a', 'b'), (1, 2), ('cd', 3), (None, None)),
                (True, 2)
            )
            self.assertTupleEqual(check_len_equal(('a',), (1,), ('cd',), (None,)), (True, 1))

    def test_check_str_equal(self):
        # Verifies that lengths of strings are evaluated correctly
        with self.subTest(num_strings=2):
            self.assertTupleEqual(
                check_len_equal('abc', '123'),
                (True, 3)
            )

        with self.subTest(num_strings=3):
            self.assertTupleEqual(
                check_len_equal('ab', '12', 'c3'),
                (True, 2)
            )

        with self.subTest(num_strings=4):
            self.assertTupleEqual(
                check_len_equal('ab', '12', 'c3', 'No'),
                (True, 2)
            )

    def test_check_mixed_type_equal(self):
        # Verifies that lengths of mixed list/tuple/string arguments
        # are evaluated correctly
        self.assertTupleEqual(
            check_len_equal(['a', 'b'], (1, 2), ('cd', 3), (None, None), 'ce'),
            (True, 2)
        )
        self.assertTupleEqual(check_len_equal(('a',), (1,), ('cd',), (None,), 'c'), (True, 1))

    def test_check_mixed_type_unequal(self):
        # Verifies that lengths of mixed list/tuple/string arguments with
        # different lengths are compared correctly
        with self.subTest(num_args=2):
            self.assertTupleEqual(
                check_len_equal((1, 2), 'abcdefjkl'),
                (False, [2, 9])
            )

        with self.subTest(num_args=3):
            self.assertTupleEqual(
                check_len_equal(('cd', 3), (None, None), 'abcdefjkl'),
                (False, [2, 2, 9])
            )

        with self.subTest(num_args=5):
            self.assertTupleEqual(
                check_len_equal(['a', 'b', 'c'], (1, 2), ('cd', 3), (None, None), 'abcdefjkl'),
                (False, [3, 2, 2, 2, 9])
            )


class Test_IsLenEqual(unittest.TestCase):
    def test_is_list_equal(self):
        # Verifies that equality of lengths of lists is evaluated correctly
        with self.subTest(num_lists=2):
            self.assertTrue(is_len_equal(['a', 'b', 'c'], [1, 2, 3]))
            self.assertTrue(is_len_equal(['a'], [1]))

        with self.subTest(num_lists=3):
            self.assertTrue(is_len_equal(['a', 'b'], [1, 2], ['cd', 3]))
            self.assertTrue(is_len_equal(['a'], [1], ['c']))

        with self.subTest(num_lists=4):
            self.assertTrue(is_len_equal(['a', 'b'], [1, 2], ['cd', 3], [None, None]))
            self.assertTrue(is_len_equal(['a'], [1], ['c'], [None]))

    def test_is_tuple_equal(self):
        # Verifies that equality of lengths of tuples is evaluated correctly
        with self.subTest(num_tuples=2):
            self.assertTrue(is_len_equal(('a', 'b', 'c'), (1, 2, 3)))
            self.assertTrue(is_len_equal(('a',), (1,)))

        with self.subTest(num_tuples=3):
            self.assertTrue(is_len_equal(('a', 'b'), (1, 2), ('cd', 3)))
            self.assertTrue(is_len_equal(('a',), (1,), ('cd',)))

        with self.subTest(num_tuples=4):
            self.assertTrue(is_len_equal(('a', 'b'), (1, 2), ('cd', 3), (None, None)))
            self.assertTrue(is_len_equal(('a',), (1,), ('cd',), (None,)))

    def test_is_str_equal(self):
        # Verifies that equality of lengths of strings is evaluated correctly
        with self.subTest(num_strings=2):
            self.assertTrue(is_len_equal('abc', '123'))

        with self.subTest(num_strings=3):
            self.assertTrue(is_len_equal('ab', '12', 'c3'))

        with self.subTest(num_strings=4):
            self.assertTrue(is_len_equal('ab', '12', 'c3', 'No'))

    def test_is_mixed_type_equal(self):
        # Verifies that equality of lengths of mixed list/tuple/string arguments
        # is evaluated correctly
        self.assertTrue(is_len_equal(['a', 'b'], (1, 2), ('cd', 3), (None, None), 'ce'))
        self.assertTrue(is_len_equal(('a',), (1,), ('cd',), (None,), 'c'))

    def test_is_mixed_type_unequal(self):
        # Verifies that equality of lengths of mixed list/tuple/string arguments with
        # different lengths is evaluated correctly
        with self.subTest(num_args=2):
            self.assertFalse(is_len_equal((1, 2), 'abcdefjkl'))

        with self.subTest(num_args=3):
            self.assertFalse(is_len_equal(('cd', 3), (None, None), 'abcdefjkl'))

        with self.subTest(num_args=5):
            self.assertFalse(is_len_equal(['a', 'b', 'c'], (1, 2), ('cd', 3),
                                          (None, None), 'abcdefjkl'))


class Test_MaxListLength(unittest.TestCase):
    def __test_batch(self, test_cases: List[dict]):
        for sample in test_cases:
            with self.subTest(inputs=sample['inputs'], outputs=sample['outputs']):
                self.assertEqual(
                    max_list_item_len(sample['inputs']),
                    sample['outputs']
                )

    def test_string_list(self):
        # Verifies that the maximum length of a list of strings
        # is correctly identified
        test_cases = [
            {'inputs': ['item1', 'phrase with spaces', 'newline\n', ''],  'outputs': 18},
            {'inputs': ['', '', '', '', ''],                              'outputs': 0},
        ]

        self.__test_batch(test_cases)

    def test_mixed_list(self):
        # Verifies that the maximum length of a list of mixed types
        # is correctly identified
        test_cases = [
            {'inputs': ['item1', [1, 2, 0], (int, dict), ''],  'outputs': 5},
            {'inputs': ['m1', [1, 2, 0], (int, dict), ''],     'outputs': 3},
        ]

        self.__test_batch(test_cases)

    def test_max_length_tuple(self):
        # Verifies that the maximum length of items in a tuple is
        # correctly identified
        test_cases = [
            {'inputs': ('item1', 'phrase with spaces', 'newline\n', ''),  'outputs': 18},
            {'inputs': ('m1', [1, 2, 0], (int, dict), ''),                'outputs': 3},
        ]

        self.__test_batch(test_cases)

    def test_invalid_object_list(self):
        # Verifies that an error is thrown if attempting to determine the
        # maximum length of a list with types whose lengths are not defined
        with self.assertRaises(TypeError):
            max_list_item_len([2, 'string'])
