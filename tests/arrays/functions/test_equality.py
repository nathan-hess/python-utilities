import unittest
import warnings

import numpy as np

from pyxx.arrays import is_array_equal


class Test_NumPyListEqual(unittest.TestCase):
    def setUp(self):
        self.array = np.array([[   3, 6,   -3.213,   0],
                               [3.23, 1, -1.42e-3, 4e6]])

        self.array_uneq_shape = np.array([[3,    6,   -3.213,   0],
                                          [3.23, 1, -1.42e-3, 4e6],
                                          [1,    2,        3,   4]])

        self.array_uneq_val = np.array([[   3, 6,   -3.213,   0],
                                        [3.23, 1, -1.41e-3, 4e6]])

    def test_equal(self):
        # Verifies that arrays of equal shape and values are evaluated as equal
        with self.subTest(args=2):
            self.assertTrue(is_array_equal(self.array, self.array))

        with self.subTest(args=3):
            self.assertTrue(is_array_equal(self.array, self.array, self.array))

        with self.subTest(args=4):
            self.assertTrue(is_array_equal(self.array, self.array, self.array, self.array))

    def test_unequal_shape(self):
        # Verifies that arrays of different shape are evaluated as not equal
        with self.subTest(args=2):
            self.assertFalse(is_array_equal(self.array, self.array_uneq_shape))

        with self.subTest(args=3):
            self.assertFalse(is_array_equal(
                self.array_uneq_shape, self.array, self.array))
            self.assertFalse(is_array_equal(
                self.array, self.array_uneq_shape, self.array))
            self.assertFalse(is_array_equal(
                self.array, self.array, self.array_uneq_shape))

        with self.subTest(args=4):
            self.assertFalse(is_array_equal(
                self.array_uneq_shape, self.array, self.array, self.array))
            self.assertFalse(is_array_equal(
                self.array, self.array_uneq_shape, self.array, self.array))
            self.assertFalse(is_array_equal(
                self.array, self.array, self.array_uneq_shape, self.array))
            self.assertFalse(is_array_equal(
                self.array, self.array, self.array, self.array_uneq_shape))

        with self.subTest(comment='number_and_list'):
            self.assertFalse(is_array_equal(
                [1, [2, 3, 4]], [[1], [2, 3, 4]]))
            self.assertFalse(is_array_equal(
                [[1], [2, 3, 4]], [1, [2, 3, 4]]))
            self.assertFalse(is_array_equal(
                [[1, 2, 3], [4, [5, 6, 7]]], [[1, 2, 3], [4, [5, 7]]]
            ))

        with self.subTest(comment='string_and_char_array'):
            self.assertFalse(is_array_equal(
                'myString', ['m', 'y', 'S', 't', 'r', 'i', 'n', 'g']))
            self.assertFalse(is_array_equal(
                ['m', 'y', 'S', 't', 'r', 'i', 'n', 'g'], 'myString'))

    def test_unequal_values(self):
        # Verifies that arrays with different values are evaluated as not equal
        with self.subTest(args=2):
            self.assertFalse(is_array_equal(self.array, self.array_uneq_val))

        with self.subTest(args=3):
            self.assertFalse(is_array_equal(
                self.array_uneq_val, self.array, self.array))
            self.assertFalse(is_array_equal(
                self.array, self.array_uneq_val, self.array))
            self.assertFalse(is_array_equal(
                self.array, self.array, self.array_uneq_val))

        with self.subTest(args=4):
            self.assertFalse(is_array_equal(
                self.array_uneq_val, self.array, self.array, self.array))
            self.assertFalse(is_array_equal(
                self.array, self.array_uneq_val, self.array, self.array))
            self.assertFalse(is_array_equal(
                self.array, self.array, self.array_uneq_val, self.array))
            self.assertFalse(is_array_equal(
                self.array, self.array, self.array, self.array_uneq_val))

    def test_tolerance(self):
        # Verifies that setting tolerance for equality functions as expected
        diff = np.abs(self.array_uneq_val - self.array)

        with self.subTest(error='positive'):
            self.assertTrue(
                is_array_equal(self.array, self.array + diff, tol=0.000011))

            self.assertFalse(
                is_array_equal(self.array, self.array + 2*diff, tol=0.000011))

        with self.subTest(error='negative'):
            self.assertTrue(
                is_array_equal(self.array, self.array - diff, tol=0.000011))

            self.assertFalse(
                is_array_equal(self.array, self.array - 2*diff, tol=0.000011))

    def test_list(self):
        # Verifies that equality can be checked for lists
        with self.subTest(result='equal'):
            self.assertTrue(is_array_equal(
                [0, 4.2, 9, -0.323, 1e5],
                [0, 4.2, 9, -0.323, 1e5],
                [0, 4.2, 9, -0.323, 1e5]
            ))

        with self.subTest(result='unequal_shape'):
            self.assertFalse(is_array_equal(
                [0, 4.2, 9, -0.323, 1e5],
                [0, 4.2, 9, -0.323],
                [0, 4.2, 9, -0.323, 1e5]
            ))

        with self.subTest(result='unequal_value'):
            self.assertFalse(is_array_equal(
                [0, 4.2, 9, -0.3233, 1e5],
                [0, 4.2, 9, -0.323, 1e5],
                [0, 4.2, 9, -0.323, 1e5]
            ))

    def test_tuple(self):
        # Verifies that equality can be checked for tuples
        with self.subTest(result='equal'):
            self.assertTrue(is_array_equal(
                (0, 4.2, 9, -0.323, 1e5),
                (0, 4.2, 9, -0.323, 1e5),
                (0, 4.2, 9, -0.323, 1e5)
            ))

        with self.subTest(result='unequal_shape'):
            self.assertFalse(is_array_equal(
                (0, 4.2, 9, -0.323, 1e5),
                (0, 4.2, 9, -0.323),
                (0, 4.2, 9, -0.323, 1e5)
            ))

        with self.subTest(result='unequal_value'):
            self.assertFalse(is_array_equal(
                (0, 4.2, 9, -0.3233, 1e5),
                (0, 4.2, 9, -0.323, 1e5),
                (0, 4.2, 9, -0.323, 1e5)
            ))

    def test_number(self):
        # Verifies that equality can be checked for numbers
        with self.subTest(result='equal'):
            self.assertTrue(is_array_equal(3.142, 3.142))
            self.assertTrue(is_array_equal(3.142, 3.141, tol=0.0011))
            self.assertTrue(is_array_equal(-5, -5))
            self.assertTrue(is_array_equal(-5.0, -5))

        with self.subTest(result='equal_numpy'):
            self.assertTrue(is_array_equal(-5.0, np.array(-5)))
            self.assertTrue(is_array_equal(-5.0, np.array(-5), np.int32(-5)))

        with self.subTest(result='unequal'):
            self.assertFalse(is_array_equal(3.142, 3.1))
            self.assertFalse(is_array_equal(-5, 5))

    def test_string(self):
        # Verifies that equality can be checked for strings
        with self.subTest(result='equal_str'):
            self.assertTrue(is_array_equal('myString', 'myString'))
            self.assertTrue(is_array_equal('ab', 'ab', 'ab'))
            self.assertTrue(is_array_equal('ab\n', 'ab\n', 'ab\n', 'ab\n'))

        with self.subTest(result='equal_str_array'):
            self.assertTrue(is_array_equal(
                ['myString', 'a', ['bc', 'd']], ['myString', 'a', ['bc', 'd']]))

        with self.subTest(result='unequal_str'):
            self.assertFalse(is_array_equal('myStrinG', 'myString'))
            self.assertFalse(is_array_equal('abc', 'ab', 'ab'))
            self.assertFalse(is_array_equal('ab', 'abc', 'ab'))
            self.assertFalse(is_array_equal('ab', 'ab', 'abc'))
            self.assertFalse(is_array_equal('ab\nc', 'ab\n', 'ab\n', 'ab\n'))
            self.assertFalse(is_array_equal('ab\n', 'ab\nc', 'ab\n', 'ab\n'))
            self.assertFalse(is_array_equal('ab\n', 'ab\n', 'ab\nc', 'ab\n'))
            self.assertFalse(is_array_equal('ab\n', 'ab\n', 'ab\n', 'ab\nc'))

        with self.subTest(result='unequal_str_array'):
            self.assertFalse(is_array_equal(
                ['myString', 'a', ['b', 'c', 'd']], ['myString', 'a', ['bc', 'd']]))

            self.assertFalse(is_array_equal(
                ['myString', 'a', ['bc', 'e']], ['myString', 'a', ['bc', 'd']]))

    def test_mixed_type_numeric(self):
        # Verifies that equality can be checked for mixed types of arrays

        # Disable display of NumPy warnings when creating "ragged" array
        warnings.filterwarnings('ignore', category=np.VisibleDeprecationWarning)

        with self.subTest(dim=1):
            self.assertTrue(is_array_equal(
                [3.14, 1/2, 0, 5, -6.28, 2e10, 1e-13],
                (3.14, 1/2, 0, 5, -6.28, 2e10, 1e-13),
                np.array([3.14, 1/2, 0, 5, -6.28, 2e10, 1e-13])
            ))

        with self.subTest(dim=2):
            self.assertTrue(is_array_equal(
                [[3.14, 1/2, 0, 5, -6.28, 2e10, 1e-13], [4, 3, 2, 1]],
                ((3.14, 1/2, 0, 5, -6.28, 2e10, 1e-13), [4, 3, 2, 1]),
                ((3.14, 1/2, 0, 5, -6.28, 2e10, 1e-13), (4, 3, 2, 1)),
                np.array([[3.14, 1/2, 0, 5, -6.28, 2e10, 1e-13], [4, 3, 2, 1]])
            ))

        with self.subTest(dim=3):
            self.assertTrue(is_array_equal(
                [[3.14, 1/2, 0, 5, -6.28, 2e10, 1e-13], [[3, 6], 9], [4, 3, 2, 1]],
                ((3.14, 1/2, 0, 5, -6.28, 2e10, 1e-13), [np.array([3, 6]), np.array(9)], [4, 3, 2, 1]),
                ((3.14, 1/2, 0, 5, -6.28, 2e10, 1e-13), ([3, 6], 9), (4, 3, 2, 1)),
                np.array([[3.14, 1/2, 0, 5, -6.28, 2e10, 1e-13], ((3, 6), 9), [4, 3, 2, 1]])
            ))

    def test_mixed_type_numeric_str(self):
        # Verifies that equality can be checked for mixed types of arrays
        # with both numbers and strings

        # Disable display of NumPy warnings when creating "ragged" array
        warnings.filterwarnings('ignore', category=np.VisibleDeprecationWarning)

        with self.subTest(comment='no_numpy_array'):
            self.assertTrue(is_array_equal(
                [[3.14, 1/2, 0, 5, 'myString', ['a,', 3], -6.28, 2e10, 1e-13], [4, 3, 2, 1]],
                ((3.14, 1/2, 0, 5, 'myString', ['a,', 3], -6.28, 2e10, 1e-13), [4, 3, 2, 1]),
                ((3.14, 1/2, 0, 5, 'myString', ['a,', 3], -6.28, 2e10, 1e-13), (4, 3, 2, 1))
            ))

        with self.subTest(comment='numpy_no_dtype_object'):
            self.assertFalse(is_array_equal(np.array([1, 'a']), [1, 'a']))

        with self.subTest(comment='numpy_dtype_object'):
            self.assertTrue(is_array_equal(np.array([1, 'a'], dtype=object), [1, 'a']))
            self.assertTrue(is_array_equal(
                [[3.14, 1/2, 0, 5, 'myString', ['a,', 3], -6.28, 2e10, 1e-13], [4, 3, 2, 1]],
                ((3.14, 1/2, 0, 5, 'myString', ['a,', 3], -6.28, 2e10, 1e-13), [4, 3, 2, 1]),
                ((3.14, 1/2, 0, 5, 'myString', ['a,', 3], -6.28, 2e10, 1e-13), (4, 3, 2, 1)),
                np.array([[3.14, 1/2, 0, 5, 'myString', ['a,', 3], -6.28, 2e10, 1e-13], [4, 3, 2, 1]],
                         dtype=object)
            ))

    def test_incompatible_type(self):
        # Verifies that arrays are assessed as not equal if they require
        # comparing types that are not exactly equal or cannot be subtracted
        with self.subTest(comment='int_str'):
            self.assertFalse(is_array_equal([1.0, (2, 3)], ('1', [2, 3])))

        with self.subTest(comment='number_type'):
            self.assertFalse(is_array_equal(int, 3, 0))
            self.assertFalse(is_array_equal([1, 2, 3], [1, 2, float]))

    def test_unspecified_type(self):
        # Verifies that objects that are evaluated as equal (even if not
        # numbers or strings) can be compared
        with self.subTest(comment='single_value'):
            self.assertTrue(is_array_equal(int, int))

        with self.subTest(comment='array'):
            self.assertTrue(is_array_equal([int, float], [int, float]))

    def test_empty(self):
        # Verifies that empty arrays are evaluated as equal
        self.assertTrue(is_array_equal([], []))
        self.assertTrue(is_array_equal((), ()))
        self.assertTrue(is_array_equal(np.array([]), np.array([])))
        self.assertTrue(is_array_equal(np.array([]), [], ()))
