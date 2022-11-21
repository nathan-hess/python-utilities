import unittest

from pyxx.units import UnitConverterSI


class Test_UnitConverterSI(unittest.TestCase):
    def test_unit_conversions(self):
        # Verifies that a variety of unit conversions are performed correctly
        test_cases = [
            {'quantity': 1,  'from': 'm',  'to': 'm',  'expected': 1},
        ]

        for case in test_cases:
            quantity = case['quantity']
            from_unit = case['from']
            to_unit = case['to']
            expected_value = case['expected']

            unit_conversion \
                = f'{quantity} {from_unit} --> {expected_value} {to_unit}'

            with self.subTest(case=unit_conversion):
                self.assertEqual(
                    UnitConverterSI().convert(quantity=quantity,
                        from_unit=from_unit, to_unit=to_unit),
                    expected_value
                )
