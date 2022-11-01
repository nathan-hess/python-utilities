import math
import unittest

from pyxx.numbers import is_float, is_integer


class Test_IsFloat(unittest.TestCase):
    def test_is_float_true(self):
        # Checks that the `is_float()` function correctly identifies
        # floating-point numbers
        test_cases = (165, 1.561, 1.513e-5, -16.5, math.pi, '165', '1.561',
                      '1.513e-5', '-16.5')

        for inputs in test_cases:
            with self.subTest(inputs=inputs):
                self.assertTrue(is_float(inputs))

    def test_is_float_false(self):
        # Checks that the `is_float()` function correctly identifies
        # values that are not floating-point numbers
        for inputs in ('string', float):
            with self.subTest(inputs=inputs):
                self.assertFalse(is_float(inputs))


class Test_IsInteger(unittest.TestCase):
    def test_is_integer_true(self):
        # Checks that the `is_integer()` function correctly identifies integers
        test_cases = (165, 0, -416, 3e6, '165', '0', '-416', '3e6')

        for inputs in test_cases:
            with self.subTest(inputs=inputs):
                self.assertTrue(is_integer(inputs))

    def test_is_integer_false(self):
        # Checks that the `is_integer()` function correctly identifies
        # values that are not integers
        for inputs in ('string', 0.2, int):
            with self.subTest(inputs=inputs):
                self.assertFalse(is_integer(inputs))
