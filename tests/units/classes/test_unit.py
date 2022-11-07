import unittest

import numpy as np

from pyxx.units import (
    Unit,
    UnitLinear,
    UnitLinearSI,
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

        self.unit06_no_id_name = Unit(
            unit_system=UnitSystemSI(),
            base_unit_exps=[0, 0, 0, 0, 0, 0, 1],
            to_base_function=lambda x, exp: x,
            from_base_function=lambda x, exp: x)

        self.unit07_complex_id_name = Unit(
            unit_system=UnitSystemSI(),
            base_unit_exps=[0, 6, 0, 9, 0, 0, 1],
            to_base_function=lambda x, exp: x,
            from_base_function=lambda x, exp: x,
            identifier='(kg/s)*m', name='(kilogram/second)*meter')

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

    def test_multiply_single_unit(self):
        # Verifies that cases of multiplying units are performed correctly
        m = Unit(
            unit_system=UnitSystem(3),
            base_unit_exps=[1, 0, 0],
            to_base_function=lambda x, exp: x,
            from_base_function=lambda x, exp: x
        )

        mm = Unit(
            unit_system=UnitSystem(3),
            base_unit_exps=[1, 0, 0],
            to_base_function=lambda x, exp: (0.001**exp)*x,
            from_base_function=lambda x, exp: (1000**exp)*x
        )

        with self.subTest(unit='m'):
            with self.subTest(exponent=2):
                with self.subTest(check='base_unit_exps'):
                    self.assertTrue(np.allclose((m*m).base_unit_exps, np.array([2, 0, 0])))

                with self.subTest(check='to_base'):
                    inputs = 100*np.random.randn(100)
                    outputs = inputs
                    self.assertTrue(np.allclose((m*m).to_base(inputs), outputs))

                with self.subTest(check='from_base'):
                    inputs = 100*np.random.randn(100)
                    outputs = inputs
                    self.assertTrue(np.allclose((m*m).from_base(inputs), outputs))

            with self.subTest(exponent=4):
                with self.subTest(check='base_unit_exps'):
                    self.assertTrue(np.allclose((m*m*m*m).base_unit_exps, np.array([4, 0, 0])))

                with self.subTest(check='to_base'):
                    inputs = 100*np.random.randn(100)
                    outputs = inputs
                    self.assertTrue(np.allclose((m*m*m*m).to_base(inputs), outputs))

                with self.subTest(check='from_base'):
                    inputs = 100*np.random.randn(100)
                    outputs = inputs
                    self.assertTrue(np.allclose((m*m*m*m).from_base(inputs), outputs))

        with self.subTest(unit='mm'):
            with self.subTest(exponent=2):
                with self.subTest(check='base_unit_exps'):
                    self.assertTrue(np.allclose((mm*mm).base_unit_exps, np.array([2, 0, 0])))

                with self.subTest(check='to_base'):
                    inputs = 100*np.random.randn(100)
                    outputs = inputs / 1e6
                    self.assertTrue(np.allclose((mm*mm).to_base(inputs), outputs))

                with self.subTest(check='from_base'):
                    inputs = 100*np.random.randn(100)
                    outputs = inputs * 1e6
                    self.assertTrue(np.allclose((mm*mm).from_base(inputs), outputs))

            with self.subTest(exponent=4):
                with self.subTest(check='base_unit_exps'):
                    self.assertTrue(np.allclose((mm*mm*mm*mm).base_unit_exps, np.array([4, 0, 0])))

                with self.subTest(check='to_base'):
                    inputs = 100*np.random.randn(100)
                    outputs = inputs / 1e12
                    self.assertTrue(np.allclose((mm*mm*mm*mm).to_base(inputs), outputs))

                with self.subTest(check='from_base'):
                    inputs = 100*np.random.randn(100)
                    outputs = inputs * 1e12
                    self.assertTrue(np.allclose((mm*mm*mm*mm).from_base(inputs), outputs))

        with self.subTest(check='nested_exponent'):
            with self.subTest(check='to_base'):
                inputs = 1e6*np.random.randn(100)
                outputs = 1e-12*inputs
                self.assertTrue(np.allclose((mm*mm).to_base(inputs, 2), outputs))

            with self.subTest(check='from_base'):
                inputs = 1e-6*np.random.randn(100)
                outputs = 1e12*inputs
                self.assertTrue(np.allclose((mm*mm).from_base(inputs, 2), outputs))

    def test_multiply_multiple_units(self):
        # Verifies that cases of multiplying units are performed correctly
        m = Unit(
            unit_system=UnitSystem(3),
            base_unit_exps=[0, 1, 0],
            to_base_function=lambda x, exp: x,
            from_base_function=lambda x, exp: x
        )

        kN = Unit(
            unit_system=UnitSystem(3),
            base_unit_exps=[1, 1, -2],
            to_base_function=lambda x, exp: (1000**exp)*x,
            from_base_function=lambda x, exp: (0.001**exp)*x
        )

        torque = kN*m

        with self.subTest(check='base_unit_exps'):
            self.assertTrue(np.allclose(torque.base_unit_exps, np.array([1, 2, -2])))

        with self.subTest(check='to_base'):
            inputs = 100*np.random.randn(100)
            outputs = 1000 * inputs
            self.assertTrue(np.allclose(torque.to_base(inputs), outputs))

        with self.subTest(check='from_base'):
            inputs = 100*np.random.randn(100)
            outputs = inputs / 1000
            self.assertTrue(np.allclose(torque.from_base(inputs), outputs))

    def test_multiply_constant(self):
        # Verifies that cases of multiplying units are performed correctly
        N = Unit(
            unit_system=UnitSystem(3),
            base_unit_exps=[1, 1, -2],
            to_base_function=lambda x, exp: x,
            from_base_function=lambda x, exp: x
        )

        for i, kN in enumerate((N*1000, 1000*N)):
            with self.subTest(order=('left' if i == 0 else 'right')):
                with self.subTest(check='base_unit_exps'):
                    self.assertTrue(np.allclose(kN.base_unit_exps, np.array([1, 1, -2])))

                for exponent in [1, 2, 3, 4, -1, -3]:
                    with self.subTest(exponent=exponent):
                        with self.subTest(check='to_base'):
                            inputs = 100*np.random.randn(100)
                            outputs = (1000**exponent)*inputs
                            self.assertTrue(np.allclose(kN.to_base(inputs, exponent), outputs))

                        with self.subTest(check='from_base'):
                            inputs = 100*np.random.randn(100)
                            outputs = inputs/(1000**exponent)
                            self.assertTrue(np.allclose(kN.from_base(inputs, exponent), outputs))

    def test_multiply_invalid(self):
        # Verifies that an error is thrown if attempting to multiply a unit
        # by an invalid value
        test_cases = [
            'mm',
            float,
        ]

        m = Unit(
            unit_system=UnitSystem(3),
            base_unit_exps=[0, 1, 0],
            to_base_function=lambda x, exp: x,
            from_base_function=lambda x, exp: x
        )

        for value in test_cases:
            with self.subTest(value=value):
                with self.subTest(order='left'):
                    with self.assertRaises(TypeError):
                        value * m
                with self.subTest(order='right'):
                    with self.assertRaises(TypeError):
                        m * value

    def test_multiply_id(self):
        # Verifies that the "identifier" attribute of units is
        # correct after multiplication
        with self.subTest(case='none'):
            self.assertEqual((self.unit06_no_id_name * self.unit06_no_id_name).identifier, None)
            self.assertEqual((self.unit01 * self.unit06_no_id_name).identifier, None)
            self.assertEqual((self.unit06_no_id_name * self.unit01).identifier, None)

        with self.subTest(case='simple'):
            self.assertEqual((self.unit01 * self.unit01).identifier, 'kg*kg')

        with self.subTest(case='complex'):
            self.assertEqual(
                (self.unit07_complex_id_name * self.unit07_complex_id_name).identifier,
                '(kg/s)*m*(kg/s)*m'
            )

    def test_multiply_name(self):
        # Verifies that the "name" attribute of units is
        # correct after multiplication
        with self.subTest(case='none'):
            self.assertEqual((self.unit06_no_id_name * self.unit06_no_id_name).name, None)
            self.assertEqual((self.unit01 * self.unit06_no_id_name).name, None)
            self.assertEqual((self.unit06_no_id_name * self.unit01).name, None)

        with self.subTest(case='simple'):
            self.assertEqual((self.unit01 * self.unit01).name, 'kilogram*kilogram')

        with self.subTest(case='complex'):
            self.assertEqual(
                (self.unit07_complex_id_name * self.unit07_complex_id_name).name,
                '(kilogram/second)*meter*(kilogram/second)*meter'
            )


class Test_LinearUnit(unittest.TestCase):
    def setUp(self):
        self.unit01 = UnitLinear(
            unit_system=UnitSystemSI(),
            base_unit_exps=[0, 0, 0, 0, 0, 0, 1],
            scale=0.001, offset=0,
            identifier='g', name='gram')

        self.unit02 = UnitLinear(
            unit_system=UnitSystem(5),
            base_unit_exps=[0, 1, 0, 0, 0],
            scale=5/9, offset=273.15-32*5/9,
            identifier='°F', name='degrees Fahrenheit')

    def test_set_scale(self):
        # Verifies that "scale" attribute is set correctly
        self.assertAlmostEqual(self.unit01.scale, 0.001)
        self.assertAlmostEqual(self.unit02.scale, 5/9)

    def test_set_scale_invalid(self):
        # Verifies that an error is thrown if attempting to set the "scale"
        # attribute to an invalid value
        with self.assertRaises(TypeError):
            UnitLinear(
                unit_system=UnitSystemSI(),
                base_unit_exps=[0, 0, 0, 0, 0, 0, 1],
                scale='1.5', offset=0,
                identifier='g', name='gram'
            )

    def test_set_offset(self):
        # Verifies that "offset" attribute is set correctly
        self.assertAlmostEqual(self.unit01.offset, 0)
        self.assertAlmostEqual(self.unit02.offset, 273.15-32*5/9)

    def test_set_offset_invalid(self):
        # Verifies that an error is thrown if attempting to set the "offset"
        # attribute to an invalid value
        with self.assertRaises(TypeError):
            UnitLinear(
                unit_system=UnitSystemSI(),
                base_unit_exps=[0, 0, 0, 0, 0, 0, 1],
                scale=0.001, offset='0',
                identifier='g', name='gram'
            )

    def test_str(self):
        # Verifies that string representation of object is formatted correctly
        self.assertEqual(
            str(self.unit01),
            'g - gram - [0. 0. 0. 0. 0. 0. 1.] - scale: 0.001 - offset: 0.0')

        self.assertEqual(
            str(self.unit02),
            ('°F - degrees Fahrenheit - [0. 1. 0. 0. 0.] '
             '- scale: 0.5555555555555556 - offset: 255.3722222222222'))

    def test_to_base(self):
        # Verifies that conversion of from base units to the given object's
        # units is performed correctly
        self.assertTrue(np.array_equal(
            self.unit01.to_base([2, 4.3, 930]),
            np.array([0.002, 0.0043, 0.93])))

        diff = self.unit02.to_base([32, 9.332, 14, -40]) \
            - np.array([273.15, 273.15+(9.332-32)*(5/9), 263.15, 233.15])
        self.assertLessEqual(np.max(np.abs(diff)), 1e-12)

    def test_from_base(self):
        # Verifies that conversion of from the given object's
        # units to the base units is performed correctly
        self.assertTrue(np.array_equal(
            self.unit01.from_base([0.002, 0.0043, 0.93]),
            np.array([2, 4.3, 930])))

        diff = self.unit02.from_base([273.15, 273.15+(9.332-32)*(5/9), 263.15, 233.15]) \
            - np.array([32, 9.332, 14, -40])
        self.assertLessEqual(np.max(np.abs(diff)), 1e-12)

    def test_to_base_exponent(self):
        # Checks conversion of value to base units with user-specified exponent
        self.assertTrue(np.array_equal(
            self.unit01.to_base((40, -5), 1),
            np.array((0.04, -0.005))))

        self.assertTrue(all(np.isclose(
            self.unit01.to_base((40, -5), 2),
            np.array((40e-6, -5e-6)))))

        self.assertTrue(np.array_equal(
            self.unit01.to_base((40, -5), 3),
            np.array((40e-9, -5e-9))))

    def test_from_base_exponent(self):
        # Checks conversion of value from base units with user-specified exponent
        self.assertTrue(np.array_equal(
            self.unit01.from_base((40, -5), 1),
            np.array((40000, -5000))))

        self.assertTrue(np.array_equal(
            self.unit01.from_base((40, -5), 2),
            np.array((40e6, -5e6))))

        self.assertTrue(np.array_equal(
            self.unit01.from_base((40, -5), 3),
            np.array((40e9, -5e9))))


class Test_LinearUnitSI(unittest.TestCase):
    def test_unit_system(self):
        # Verifies that the unit system is set to "SI"
        unit = UnitLinearSI(
            base_unit_exps=[0, 0, 0, 0, 0, 0, 1],
            scale=0.001, offset=0)

        self.assertIs(type(unit.unit_system), UnitSystemSI)
