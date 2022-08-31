from typing import List
import unittest

from pyxx.arrays import max_list_item_len


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
