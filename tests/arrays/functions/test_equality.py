import unittest

import numpy as np

from pyxx.arrays import np_array_equal


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
            self.assertTrue(np_array_equal(self.array, self.array))

        with self.subTest(args=3):
            self.assertTrue(np_array_equal(self.array, self.array, self.array))

        with self.subTest(args=4):
            self.assertTrue(np_array_equal(self.array, self.array, self.array, self.array))

    def test_unequal_shape(self):
        # Verifies that arrays of different shape are evaluated as not equal
        with self.subTest(args=2):
            self.assertFalse(np_array_equal(self.array, self.array_uneq_shape))

        with self.subTest(args=3):
            self.assertFalse(np_array_equal(
                self.array_uneq_shape, self.array, self.array))
            self.assertFalse(np_array_equal(
                self.array, self.array_uneq_shape, self.array))
            self.assertFalse(np_array_equal(
                self.array, self.array, self.array_uneq_shape))

        with self.subTest(args=4):
            self.assertFalse(np_array_equal(
                self.array_uneq_shape, self.array, self.array, self.array))
            self.assertFalse(np_array_equal(
                self.array, self.array_uneq_shape, self.array, self.array))
            self.assertFalse(np_array_equal(
                self.array, self.array, self.array_uneq_shape, self.array))
            self.assertFalse(np_array_equal(
                self.array, self.array, self.array, self.array_uneq_shape))

    def test_unequal_values(self):
        # Verifies that arrays with different values are evaluated as not equal
        with self.subTest(args=2):
            self.assertFalse(np_array_equal(self.array, self.array_uneq_val))

        with self.subTest(args=3):
            self.assertFalse(np_array_equal(
                self.array_uneq_val, self.array, self.array))
            self.assertFalse(np_array_equal(
                self.array, self.array_uneq_val, self.array))
            self.assertFalse(np_array_equal(
                self.array, self.array, self.array_uneq_val))

        with self.subTest(args=4):
            self.assertFalse(np_array_equal(
                self.array_uneq_val, self.array, self.array, self.array))
            self.assertFalse(np_array_equal(
                self.array, self.array_uneq_val, self.array, self.array))
            self.assertFalse(np_array_equal(
                self.array, self.array, self.array_uneq_val, self.array))
            self.assertFalse(np_array_equal(
                self.array, self.array, self.array, self.array_uneq_val))

    def test_tolerance(self):
        # Verifies that setting tolerance for equality functions as expected
        self.assertTrue(
            np_array_equal(self.array, self.array_uneq_val, tol=0.000011))
