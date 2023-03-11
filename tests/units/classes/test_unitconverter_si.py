import math
import unittest

from pyxx.units import UnitConverterSI
from tests import TEST_FLOAT_TOLERANCE_DECIMAL_PLACES


class Test_UnitConverterSI(unittest.TestCase):
    def test_unit_conversions(self):
        # Verifies that a variety of unit conversions are performed correctly
        test_cases = [
            {'quantity': 1,          'from': 'm',           'to': 'm',       'expected': 1},
            {'quantity': 1,          'from': 'mm',          'to': 'm',       'expected': 0.001},
            {'quantity': 1,          'from': 'm',           'to': 'cm',      'expected': 100},
            {'quantity': 1,          'from': 'm',           'to': 'km',      'expected': 0.001},
            {'quantity': 1,          'from': 'in',          'to': 'cm',      'expected': 2.54},
            {'quantity': 1,          'from': 'ft',          'to': 'in',      'expected': 12},
            {'quantity': 1,          'from': 'mi',          'to': 'ft',      'expected': 5280},
            {'quantity': 1,          'from': 'yd',          'to': 'ft',      'expected': 3},
            {'quantity': 20000,      'from': 'league',      'to': 'm',       'expected': 96560640},
            {'quantity': 1,          'from': 'm',           'to': 'micron',  'expected': 1e6},
            {'quantity': 4.5,        'from': 'cm',          'to': 'μm',      'expected': 4.5e4},
            {'quantity': 1,          'from': 'acre',        'to': 'ft^2',    'expected': 43560},
            {'quantity': 10,         'from': 'L',           'to': 'm^3',     'expected': 0.01},
            {'quantity': 1000,       'from': 'mL',          'to': 'L',       'expected': 1},
            {'quantity': 1,          'from': 'gal',         'to': 'L',       'expected': 3.785411784},
            {'quantity': 1,          'from': 'gal',         'to': 'qt',      'expected': 4},
            {'quantity': 1,          'from': 'gal',         'to': 'pt',      'expected': 8},
            {'quantity': 1,          'from': 'gal',         'to': 'cup',     'expected': 16},
            {'quantity': 1,          'from': 'gal',         'to': 'fl_oz',   'expected': 128},
            {'quantity': 1,          'from': 'cup',         'to': 'tbsp',    'expected': 16},
            {'quantity': 1,          'from': 'tbsp',        'to': 'tsp',     'expected': 3},
            {'quantity': 1,          'from': 's',           'to': 'ms',      'expected': 1000},
            {'quantity': 1,          'from': 's',           'to': 'μs',      'expected': 1e6},
            {'quantity': 7e9,        'from': 'ns',          'to': 's',       'expected': 7},
            {'quantity': 1,          'from': 'min',         'to': 's',       'expected': 60},
            {'quantity': 1,          'from': 'hr',          'to': 'min',     'expected': 60},
            {'quantity': 1,          'from': 'week',        'to': 'day',     'expected': 7},
            {'quantity': 7,          'from': 'Hz',          'to': 's^-1',    'expected': 7},
            {'quantity': 7,          'from': 'kHz',         'to': 'Hz',      'expected': 7000},
            {'quantity': 7,          'from': 'MHz',         'to': 'Hz',      'expected': 7e6},
            {'quantity': 7,          'from': 'GHz',         'to': 'Hz',      'expected': 7e9},
            {'quantity': 1,          'from': 'mi/hr',       'to': 'mph',     'expected': 1},
            {'quantity': 24,         'from': 'hr',          'to': 'day',     'expected': 1},
            {'quantity': 60,         'from': 'mi/hr',       'to': 'ft/s',    'expected': 88},
            {'quantity': 20,         'from': 'kg*m/s^2',    'to': 'N',       'expected': 20},
            {'quantity': 1,          'from': 'kN',          'to': 'N',       'expected': 1000},
            {'quantity': 1e3,        'from': 'g',           'to': 'kg',      'expected': 1},
            {'quantity': 1e6,        'from': 'mg',          'to': 'kg',      'expected': 1},
            {'quantity': 1e9,        'from': 'μg',          'to': 'kg',      'expected': 1},
            {'quantity': 1,          'from': 'lbm',         'to': 'g',       'expected': 453.59237},
            {'quantity': 1,          'from': 't',           'to': 'kg',      'expected': 1000},
            {'quantity': 1,          'from': 'ton',         'to': 'lbm',     'expected': 2000},
            {'quantity': 1,          'from': 'long_ton',    'to': 'lbm',     'expected': 2240},
            {'quantity': 200,        'from': 'mg',          'to': 'carat',   'expected': 1},
            {'quantity': math.pi/6,  'from': 'rad',         'to': 'deg',     'expected': 30},
            {'quantity': 1080,       'from': 'deg',         'to': 'rev',     'expected': 3},
            {'quantity': 1,          'from': 'lbf',         'to': 'N',       'expected': 4.4482216152605},
            {'quantity': 1,          'from': 'Pa',          'to': 'N/m^2',   'expected': 1},
            {'quantity': 1,          'from': 'kPa',         'to': 'Pa',      'expected': 1000},
            {'quantity': 1,          'from': 'MPa',         'to': 'Pa',      'expected': 1e6},
            {'quantity': 1,          'from': 'GPa',         'to': 'Pa',      'expected': 1e9},
            {'quantity': 1,          'from': 'bar',         'to': 'Pa',      'expected': 100000},
            {'quantity': 1,          'from': 'psi',         'to': 'Pa',      'expected': 6894.757293168361},
            {'quantity': 273.15,     'from': 'K',           'to': 'degC',    'expected': 0},
            {'quantity': 303.15,     'from': 'K',           'to': 'degC',    'expected': 30},
            {'quantity': 32,         'from': 'degF',        'to': 'degC',    'expected': 0},
            {'quantity': -40,        'from': 'degF',        'to': 'degC',    'expected': -40},
            {'quantity': 212,        'from': 'degF',        'to': 'degC',    'expected': 100},
            {'quantity': 0,          'from': 'degR',        'to': 'K',       'expected': 0},
            {'quantity': 25,         'from': 'degF',        'to': 'degR',    'expected': 484.67},
            {'quantity': 25,         'from': 'degC_diff',   'to': 'K',       'expected': 25},
            {'quantity': 25,         'from': 'degF_diff',   'to': 'degR',    'expected': 25},
            {'quantity': 7,          'from': 'kg*m^2/s^2',  'to': 'J',       'expected': 7},
            {'quantity': 7,          'from': 'mJ',          'to': 'J',       'expected': 0.007},
            {'quantity': 7,          'from': 'kJ',          'to': 'J',       'expected': 7000},
            {'quantity': 7,          'from': 'MJ',          'to': 'J',       'expected': 7e6},
            {'quantity': 7,          'from': 'GJ',          'to': 'J',       'expected': 7e9},
            {'quantity': 7,          'from': 'kg*m^2/s^3',  'to': 'W',       'expected': 7},
            {'quantity': 7,          'from': 'J/s',         'to': 'W',       'expected': 7},
            {'quantity': 7,          'from': 'mW',          'to': 'W',       'expected': 0.007},
            {'quantity': 7,          'from': 'kW',          'to': 'W',       'expected': 7000},
            {'quantity': 7,          'from': 'MW',          'to': 'W',       'expected': 7e6},
            {'quantity': 7,          'from': 'GW',          'to': 'W',       'expected': 7e9},
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
