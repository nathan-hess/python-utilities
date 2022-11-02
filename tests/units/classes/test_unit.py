import unittest

import numpy as np

from pyxx.units import (
    Unit,
    UnitSystem,
    UnitSystemSI,
)


class Test_Unit(unittest.TestCase):
    def setUp(self):
        self.unit01 = Unit(
            unit_system=UnitSystemSI(),
            base_unit_exps=[0, 0, 0, 0, 0, 0, 1],
            to_base_function=lambda x, exp: x,
            from_base_function=lambda x, exp: x,
            identifier='kg', name='kilogram')

        self.unit02 = Unit(
            unit_system=UnitSystem(5),
            base_unit_exps=[0, 1, 0, 0, 0],
            to_base_function=lambda x, exp: x / 1000.0,
            from_base_function=lambda x, exp: x * 1000.0,
            identifier='ms', name='millisecond')

        self.unit03 = Unit(
            unit_system=UnitSystemSI(),
            base_unit_exps=[0, 0, 0, 0, 0, 0, 1],
            to_base_function=lambda x, exp: x,
            from_base_function=lambda x, exp: x,
            identifier='kg')

        self.unit04 = Unit(
            unit_system=UnitSystemSI(),
            base_unit_exps=[0, 0, 0, 0, 0, 0, 1],
            to_base_function=lambda x, exp: x,
            from_base_function=lambda x, exp: x,
            name='kilogram')

        self.unit05_exponent = Unit(
            unit_system=UnitSystemSI(),
            base_unit_exps=[0, 4, 0, 0, 0, 0, 1],
            to_base_function=lambda x, exp: (x**exp - (x/2 * exp)),
            from_base_function=lambda x, exp: (x**(exp+1) + exp*x),
            identifier='mv', name='millivalue')

    def test_get_unit_system(self):
        # Verifies that unit system can be retrieved correctly
        self.assertIs(type(self.unit01.unit_system), UnitSystemSI)
        self.assertIs(type(self.unit02.unit_system), UnitSystem)

        self.assertIsNot(type(self.unit01.unit_system), UnitSystem)
        self.assertIsNot(type(self.unit02.unit_system), UnitSystemSI)

    def test_get_identifier(self):
        # Verifies that "identifier" attribute can be retrieved correctly
        self.assertEqual(self.unit01.identifier, 'kg')
        self.assertEqual(self.unit02.identifier, 'ms')

    def test_get_name(self):
        # Verifies that "name" attribute can be retrieved correctly
        self.assertEqual(self.unit01.name, 'kilogram')
        self.assertEqual(self.unit02.name, 'millisecond')

    def test_invalid_unit_system(self):
        # Verifies that an appropriate error is thrown if a valid system
        # of units is not provided
        with self.assertRaises(TypeError):
            Unit(
                unit_system='SI',
                base_unit_exps=[0, 0, 0, 0, 0, 0, 1],
                to_base_function=lambda x, exp: x,
                from_base_function=lambda x, exp: x,
                identifier='kg', name='kilogram')

    def test_invalid_identifier(self):
        # Verifies that an invalid "identifier" attribute
        # results in an error being thrown
        with self.assertRaises(TypeError):
            Unit(unit_system=UnitSystemSI(),
                 base_unit_exps=[0, 0, 0, 0, 0, 0, 1],
                 to_base_function=lambda x: x,
                 from_base_function=lambda x: x,
                 identifier=0, name='kilogram')

    def test_invalid_name(self):
        # Verifies that an invalid "name" attribute
        # results in an error being thrown
        with self.assertRaises(TypeError):
            Unit(
                unit_system=UnitSystemSI(),
                base_unit_exps=[0, 0, 0, 0, 0, 0, 1],
                to_base_function=lambda x: x,
                from_base_function=lambda x: x,
                identifier='kg', name=0)

    def test_get_base_unit_exps(self):
        # Verifies that derived exponents can be retrieved correctly
        self.assertTrue(np.array_equal(
            self.unit01.base_unit_exps,
            np.array([0, 0, 0, 0, 0, 0, 1])))

        self.assertTrue(np.array_equal(
            self.unit02.base_unit_exps,
            np.array([0, 1, 0, 0, 0])))

    def test_invalid_base_unit_exps(self):
        # Verifies that an error is thrown if attempting to create
        # a unit with the wrong number of derived exponent values
        with self.assertRaises(ValueError):
            Unit(
                unit_system=UnitSystemSI(),
                base_unit_exps=[0, 0, 0, 0, 0, 1],
                to_base_function=lambda x: x,
                from_base_function=lambda x: x)

        with self.assertRaises(ValueError):
            Unit(
                unit_system=UnitSystem(4),
                base_unit_exps=[0, 0, 0, 0, 0, 0, 1],
                to_base_function=lambda x: x,
                from_base_function=lambda x: x)

    def test_str(self):
        # Verifies that string representation of unit is formatted correctly
        self.assertEqual(str(self.unit01),
                         'kg - kilogram - [0. 0. 0. 0. 0. 0. 1.]')

        self.assertEqual(str(self.unit02),
                         'ms - millisecond - [0. 1. 0. 0. 0.]')

        self.assertEqual(str(self.unit03),
                         'kg - [0. 0. 0. 0. 0. 0. 1.]')

        self.assertEqual(str(self.unit04),
                         'kilogram - [0. 0. 0. 0. 0. 0. 1.]')

    def test_repr(self):
        # Verifies that representation of unit is formatted correctly
        self.assertEqual(str(self.unit01.__repr__()),
            "<class 'pyxx.units.classes.unit.Unit'> kg - kilogram - [0. 0. 0. 0. 0. 0. 1.]")

    def test_is_convert_valid(self):
        # Verifies that units that are compatible for conversion are
        # correctly identified
        self.assertTrue(self.unit01.is_convertible(self.unit03))

        unit02_convert = Unit(
            unit_system=UnitSystem(5),
            base_unit_exps=[0, 1, 0, 0, 0],
            to_base_function=lambda x: x / 1000.0,
            from_base_function=lambda x: x * 1000.0,
            identifier='s', name='second')
        self.assertTrue(self.unit02.is_convertible(unit02_convert))

    def test_is_convert_invalid_type(self):
        # Verifies that units with different types are identified as
        # incompatible for conversion
        unit01_different_type = Unit(
            unit_system=UnitSystem(7),
            base_unit_exps=[0, 0, 0, 0, 0, 0, 1],
            to_base_function=lambda x: x,
            from_base_function=lambda x: x,
            identifier='kg', name='kilogram')
        self.assertFalse(self.unit01.is_convertible(unit01_different_type))

    def test_is_convert_invalid_exps(self):
        # Verifies that units with different `base_unit_exps` attributes
        # are identified as incompatible for conversion
        with self.subTest(issue='different_exp_values'):
            unit01_different_exp = Unit(
                unit_system=UnitSystemSI(),
                base_unit_exps=[0, 1, 0, 0, 0, 0, 1],
                to_base_function=lambda x: x,
                from_base_function=lambda x: x,
                identifier='kg', name='kilogram')
            self.assertFalse(self.unit01.is_convertible(unit01_different_exp))

        with self.subTest(issue='different_class'):
            unit02_different_exp = Unit(
                unit_system=UnitSystem(6),
                base_unit_exps=[0, 1, 0, 0, 0, 1],
                to_base_function=lambda x: x / 1000.0,
                from_base_function=lambda x: x * 1000.0,
                identifier='ms', name='millisecond')
            self.assertFalse(self.unit02.is_convertible(unit02_different_exp))

    def test_to_base_int(self):
        # Verifies that conversion of an integer value from
        # given object's units to base units is performed correctly
        self.assertAlmostEqual(self.unit01.to_base(1000), 1000)
        self.assertAlmostEqual(self.unit02.to_base(1000), 1)

    def test_to_base_float(self):
        # Verifies that conversion of a floating-point value from
        # given object's units to base units is performed correctly
        self.assertAlmostEqual(self.unit01.to_base(3.23), 3.23)
        self.assertAlmostEqual(self.unit02.to_base(932.3), 0.9323)

    def test_to_base_array(self):
        # Verifies that conversion of an array of values from
        # given object's units to base units is performed correctly
        inputs = [3.23, 1000, 5095.3, 1900]

        outputs = np.array([3.23, 1000, 5095.3, 1900])
        self.assertTrue(np.array_equal(
            self.unit01.to_base(np.array(inputs)),
            outputs))
        self.assertTrue(np.array_equal(
            self.unit01.to_base(inputs),
            outputs))
        self.assertTrue(np.array_equal(
            self.unit01.to_base(tuple(inputs)),
            outputs))

        outputs = np.array([0.00323, 1, 5.0953, 1.9])
        self.assertTrue(np.array_equal(
            self.unit02.to_base(np.array(inputs)),
            outputs))
        self.assertTrue(np.array_equal(
            self.unit02.to_base(inputs),
            outputs))
        self.assertTrue(np.array_equal(
            self.unit02.to_base(tuple(inputs)),
            outputs))

    def test_from_base_int(self):
        # Verifies that conversion of an integer value from
        # base units to the given object's units is performed correctly
        self.assertAlmostEqual(self.unit01.from_base(1000), 1000)
        self.assertAlmostEqual(self.unit02.from_base(1000), 1e6)

    def test_from_base_float(self):
        # Verifies that conversion of a floating-point value from
        # base units to the given object's units is performed correctly
        self.assertAlmostEqual(self.unit01.from_base(3.23), 3.23)
        self.assertAlmostEqual(self.unit02.from_base(932.3), 9.323e5)

    def test_from_base_array(self):
        # Verifies that conversion of an array of values from
        # base units to the given object's units is performed correctly
        inputs = [3.23, 1000, 5095.3, 1900]

        outputs = np.array([3.23, 1000, 5095.3, 1900])
        self.assertTrue(np.array_equal(
            self.unit01.from_base(np.array(inputs)),
            outputs))
        self.assertTrue(np.array_equal(
            self.unit01.from_base(inputs),
            outputs))
        self.assertTrue(np.array_equal(
            self.unit01.from_base(tuple(inputs)),
            outputs))

        outputs = np.array([3230, 1e6, 5.0953e6, 1.9e6])
        self.assertTrue(np.array_equal(
            self.unit02.from_base(np.array(inputs)),
            outputs))
        self.assertTrue(np.array_equal(
            self.unit02.from_base(inputs),
            outputs))
        self.assertTrue(np.array_equal(
            self.unit02.from_base(tuple(inputs)),
            outputs))

    def test_to_base_exponent(self):
        # Verifies that conversion of an array of values from
        # base units to the given object's units is performed correctly
        self.assertAlmostEqual(self.unit05_exponent.to_base(7, 3), 332.5)
        self.assertAlmostEqual(self.unit05_exponent.to_base(7.4, 0.2), 0.7522663431747895)
        self.assertAlmostEqual(self.unit05_exponent.to_base(9, -0.5), 2.5833333333333335)
        self.assertTrue(np.array_equal(
            self.unit05_exponent.to_base((7, 7.4, 9), 0.2),
            np.array((0.7757731615945521, 0.7522663431747895, 0.6518455739153598))))
        self.assertTrue(np.array_equal(
            self.unit05_exponent.to_base(np.array((7, 7.4, 9)), 0.2),
            np.array((0.7757731615945521, 0.7522663431747895, 0.6518455739153598))))

    def test_from_base_exponent(self):
        # Verifies that conversion of an array of values from
        # base units to the given object's units is performed correctly
        self.assertAlmostEqual(self.unit05_exponent.from_base(7, 3), 2422)
        self.assertAlmostEqual(self.unit05_exponent.from_base(7.4, 0.2), 12.522770939493443)
        self.assertAlmostEqual(self.unit05_exponent.from_base(9, -0.5), -1.5)
        self.assertTrue(np.array_equal(
            self.unit05_exponent.from_base((7, 7.4, 9), 0.2),
            np.array((11.730412131161865, 12.522770939493443, 15.766610165238236))))
        self.assertTrue(np.array_equal(
            self.unit05_exponent.from_base(np.array((7, 7.4, 9)), 0.2),
            np.array((11.730412131161865, 12.522770939493443, 15.766610165238236))))
