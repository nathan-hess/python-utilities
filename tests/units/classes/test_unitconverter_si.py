import math
import unittest

from pyxx.units import UnitConverterSI
from tests import TEST_FLOAT_TOLERANCE_DECIMAL_PLACES


class Test_UnitConverterSI(unittest.TestCase):
    def test_unit_conversions(self):
        # Verifies that a variety of unit conversions are performed correctly
        test_cases = [
            {'quantity': 1,          'from': 'm',         'to': 'm',       'expected': 1},
            {'quantity': 1,          'from': 'mm',        'to': 'm',       'expected': 0.001},
            {'quantity': 1,          'from': 'm',         'to': 'cm',      'expected': 100},
            {'quantity': 1,          'from': 'm',         'to': 'km',      'expected': 0.001},
            {'quantity': 1,          'from': 'in',        'to': 'cm',      'expected': 2.54},
            {'quantity': 1,          'from': 'ft',        'to': 'in',      'expected': 12},
            {'quantity': 1,          'from': 'mi',        'to': 'ft',      'expected': 5280},
            {'quantity': 1,          'from': 'yd',        'to': 'ft',      'expected': 3},
            {'quantity': 1,          'from': 'min',       'to': 's',       'expected': 60},
            {'quantity': 1,          'from': 'hr',        'to': 'min',     'expected': 60},
            {'quantity': 1,          'from': 'mi/hr',     'to': 'mph',     'expected': 1},
            {'quantity': 24,         'from': 'hr',        'to': 'day',     'expected': 1},
            {'quantity': 60,         'from': 'mi/hr',     'to': 'ft/s',    'expected': 88},
            {'quantity': 20,         'from': 'kg*m/s^2',  'to': 'N',       'expected': 20},
            {'quantity': 1,          'from': 'kN',        'to': 'N',       'expected': 1000},
            {'quantity': 1,          'from': 'kg',        'to': 'g',       'expected': 1000},
            {'quantity': 1,          'from': 'lbm',       'to': 'g',       'expected': 453.59237},
            {'quantity': math.pi/6,  'from': 'rad',       'to': 'deg',     'expected': 30},
            {'quantity': 1080,       'from': 'deg',       'to': 'rev',     'expected': 3},
            {'quantity': 1,          'from': 'm',         'to': 'micron',  'expected': 1e6},
            {'quantity': 4.5,        'from': 'cm',        'to': 'μm',      'expected': 4.5e4},
            {'quantity': 10,         'from': 'L',         'to': 'm^3',     'expected': 0.01},
            {'quantity': 1000,       'from': 'mL',        'to': 'L',       'expected': 1},
            {'quantity': 1,          'from': 'lbf',       'to': 'N',       'expected': 4.4482216152605},
        ]

        for case in test_cases:
            quantity       = case['quantity']
            from_unit      = case['from']
            to_unit        = case['to']
            expected_value = case['expected']

            unit_conversion \
                = f'{quantity} {from_unit} --> {expected_value} {to_unit}'

            with self.subTest(case=unit_conversion):
                self.assertAlmostEqual(
                    UnitConverterSI().convert(quantity=quantity,
                        from_unit=from_unit, to_unit=to_unit),
                    expected_value,
                    places=TEST_FLOAT_TOLERANCE_DECIMAL_PLACES
                )
