import unittest

from pyxx.arrays import TypedList
from pyxx.units import (
    UnitConverterEntry,
    UnitLinearSI,
)


class Test_UnitConverterEntry(unittest.TestCase):
    def setUp(self):
        self.entry_all_args = UnitConverterEntry(
            UnitLinearSI([0, -1, 0, 0, 0, 0, 1],
                         1, 0, 'kg/s'),
            ['flow_rate', 'Metric'],
            'kilograms per second'
        )

        self.entry_required_args = UnitConverterEntry(
            UnitLinearSI([1, 0, 0, 0, 0, 0, 0],
                         1, 0, 'm')
        )

        self.sample_unit = UnitLinearSI([0, -1, 0, 0, 0, 0, 1], 1, 0, 'kg/s')

    def test_set_description(self):
        # Verifies that "description" attribute is set correctly
        with self.subTest(method='constructor'):
            self.assertEqual(self.entry_all_args._description, 'kilograms per second')

        with self.subTest(method='attribute'):
            self.assertIsNone(self.entry_required_args._description)

            self.entry_required_args.description = 'mass flow rate, kg/s'
            self.assertEqual(self.entry_required_args._description, 'mass flow rate, kg/s')

            self.entry_required_args.description = 12345
            self.assertEqual(self.entry_required_args._description, '12345')

            self.entry_required_args.description = None
            self.assertIsNone(self.entry_required_args._description)

    def test_get_description(self):
        # Verifies that "description" attribute is retrieved correctly
        self.entry_required_args._description = 'myUnitDescription'
        self.assertEqual(self.entry_required_args.description, 'myUnitDescription')

    def test_set_tags(self):
        # Verifies that "tags" attribute is set correctly
        test_cases = (
            (TypedList('flow_rate', 'Metric', list_type=str),  TypedList('flow_rate', 'Metric', list_type=str)),
            (['flow_rate', 'Metric'],                          TypedList('flow_rate', 'Metric', list_type=str)),
            (('flow_rate', 'Metric'),                          TypedList('flow_rate', 'Metric', list_type=str)),
            (['flow_rate'],                                    TypedList('flow_rate', list_type=str)),
            ('mass_flow',                                      TypedList('mass_flow', list_type=str)),
            (None,                                             TypedList(list_type=str)),
        )

        for inputs, outputs in test_cases:
            with self.subTest(inputs=inputs, input_type=type(inputs)):
                with self.subTest(method='constructor'):
                    self.assertEqual(
                        UnitConverterEntry(unit=self.sample_unit, tags=inputs)._tags, outputs)

                with self.subTest(method='attribute'):
                    self.entry_required_args.tags = inputs

                    self.assertEqual(self.entry_required_args._tags, outputs)

        with self.subTest(method='constructor', comment='initialized_none'):
            self.assertEqual(UnitConverterEntry(self.sample_unit)._tags, TypedList(list_type=str))

        with self.subTest(comment='invalid_inputs'):
            with self.assertRaises(TypeError):
                self.entry_required_args.tags = [0, 1, 2]

            with self.assertRaises(TypeError):
                self.entry_required_args.tags = 0

    def test_get_tags(self):
        # Verifies that "tags" attribute is retrieved correctly
        self.entry_required_args._tags = 'myUnitTags'
        self.assertEqual(self.entry_required_args.tags, 'myUnitTags')

    def test_tag_methods(self):
        # Verifies that `TypedList` methods can be used to modify tags
        self.assertEqual(self.entry_required_args.tags, TypedList(list_type=str))

        self.entry_required_args.tags.append('tag1')
        self.assertEqual(self.entry_required_args.tags, TypedList('tag1', list_type=str))

        self.entry_required_args.tags.insert(0, 'tag0')
        self.assertEqual(self.entry_required_args.tags, TypedList('tag0', 'tag1', list_type=str))

    def test_set_unit(self):
        # Verifies that "unit" attribute is set correctly
        with self.subTest(method='constructor'):
            self.assertListEqual(
                list(self.entry_all_args._unit.base_unit_exps),
                [0, -1, 0, 0, 0, 0, 1])
            self.assertEqual(self.entry_all_args._unit.scale, 1)
            self.assertEqual(self.entry_all_args._unit.offset, 0)
            self.assertEqual(self.entry_all_args._unit.identifier, 'kg/s')

        with self.subTest(method='attribute'):
            self.entry_required_args.unit = UnitLinearSI([0, 1, 0, 0, 0, 0, 0],
                                                     1000, 0, 'ks')

            self.assertListEqual(
                list(self.entry_required_args._unit.base_unit_exps),
                [0, 1, 0, 0, 0, 0, 0])
            self.assertEqual(self.entry_required_args._unit.scale, 1000)
            self.assertEqual(self.entry_required_args._unit.offset, 0)
            self.assertEqual(self.entry_required_args._unit.identifier, 'ks')

        with self.subTest(method='invalid'):
            with self.assertRaises(TypeError):
                self.entry_required_args.unit = None

            with self.assertRaises(TypeError):
                self.entry_required_args.unit = 'degrees'

    def test_get_unit(self):
        # Verifies that "unit" attribute is retrieved correctly
        self.entry_required_args._unit = 'myUnit'
        self.assertEqual(self.entry_required_args.unit, 'myUnit')
