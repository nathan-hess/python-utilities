import unittest

import numpy as np

from pyxx.arrays import TypedList
from pyxx.units import (
    Unit,
    UnitConverter,
    UnitConverterEntry,
    UnitLinearSI,
    UnitSystem,
    UnitSystemSI,
)
from pyxx.units.exceptions import (
    IncompatibleUnitsError,
    UnitAlreadyDefinedError,
    UnitNotFoundError,
)
from tests import CapturePrint


class Test_UnitConverterEntry(unittest.TestCase):
    def setUp(self):
        self.entry_all_args = UnitConverterEntry(
            unit=UnitLinearSI([0, -1, 0, 0, 0, 0, 1],
                              1, 0, 'kg/s'),
            tags=['flow_rate', 'Metric'],
            name='kilogram/sec',
            description='kilograms per second'
        )

        self.entry_required_args = UnitConverterEntry(
            UnitLinearSI([1, 0, 0, 0, 0, 0, 0],
                         1, 0, 'm')
        )

        self.sample_unit = UnitLinearSI([0, -1, 0, 0, 0, 0, 1], 1, 0, 'kg/s')

    def test_repr(self):
        # Verifies that printable string representation of objects are
        # created as expected
        with self.subTest(unit_converter_entry='all_args'):
            self.assertEqual(
                self.entry_all_args.__repr__(),
                ("<class 'pyxx.units.classes.unitconverter.UnitConverterEntry'>\n"
                 "-- Name: kilogram/sec\n"
                 "-- Description: kilograms per second\n"
                 "-- Tags: ['flow_rate', 'Metric']\n"
                 "-- Unit: kg/s - [ 0. -1.  0.  0.  0.  0.  1.] - scale: 1.0 - offset: 0.0"
                )
            )

        with self.subTest(unit_converter_entry='minimal_args'):
            self.assertEqual(
                self.entry_required_args.__repr__(),
                ("<class 'pyxx.units.classes.unitconverter.UnitConverterEntry'>\n"
                 "-- Unit: m - [1. 0. 0. 0. 0. 0. 0.] - scale: 1.0 - offset: 0.0"
                )
            )

    def test_str(self):
        # Verifies that string representation of objects are created as expected
        with self.subTest(unit_converter_entry='all_args'):
            self.assertEqual(
                str(self.entry_all_args),
                ("<class 'pyxx.units.classes.unitconverter.UnitConverterEntry'>\n"
                 "-- Name: kilogram/sec\n"
                 "-- Description: kilograms per second\n"
                 "-- Tags: ['flow_rate', 'Metric']\n"
                 "-- Unit: kg/s - [ 0. -1.  0.  0.  0.  0.  1.] - scale: 1.0 - offset: 0.0"
                )
            )

        with self.subTest(unit_converter_entry='minimal_args'):
            self.assertEqual(
                str(self.entry_required_args),
                ("<class 'pyxx.units.classes.unitconverter.UnitConverterEntry'>\n"
                 "-- Unit: m - [1. 0. 0. 0. 0. 0. 0.] - scale: 1.0 - offset: 0.0"
                )
            )

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

    def test_set_name(self):
        # Verifies that "name" attribute is set correctly
        with self.subTest(method='constructor'):
            self.assertEqual(self.entry_all_args._name, 'kilogram/sec')

        with self.subTest(method='attribute'):
            self.assertIsNone(self.entry_required_args._name)

            self.entry_required_args.name = 'kg / sec'
            self.assertEqual(self.entry_required_args._name, 'kg / sec')

            self.entry_required_args.name = 12345
            self.assertEqual(self.entry_required_args._name, '12345')

            self.entry_required_args.name = None
            self.assertIsNone(self.entry_required_args._name)

    def test_get_name(self):
        # Verifies that "name" attribute is retrieved correctly
        self.entry_required_args._name = 'myUnitName'
        self.assertEqual(self.entry_required_args.name, 'myUnitName')

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


class Test_UnitConverter(unittest.TestCase):
    def setUp(self) -> None:
        # Sample units
        self.m  = UnitLinearSI([1,0,0,0,0,0,0], scale=1, offset=0)
        self.mm  = UnitLinearSI([1,0,0,0,0,0,0], scale=0.001, offset=0)
        self.s  = UnitLinearSI([0,1,0,0,0,0,0], scale=1, offset=0)
        self.ms = UnitLinearSI([0,1,0,0,0,0,0], scale=0.001, offset=0)
        self.kg = UnitLinearSI([0,0,0,0,0,0,1], scale=1, offset=0)
        self.N = UnitLinearSI([1,-2,0,0,0,0,1], scale=1, offset=0)
        self.kN = UnitLinearSI([1,-2,0,0,0,0,1], scale=1000, offset=0)

        # Sample unit converter entries
        self.entry_m = UnitConverterEntry(
            unit        = UnitLinearSI([1,0,0,0,0,0,0], scale=1, offset=0),
            tags        = ['length'],
            name        = 'meter',
            description = 'meters')
        self.entry_mm = UnitConverterEntry(
            unit        = UnitLinearSI([1,0,0,0,0,0,0], scale=0.001, offset=0),
            tags        = ['length'],
            description = 'millimeters')
        self.entry_s = UnitConverterEntry(
            unit        = UnitLinearSI([0,1,0,0,0,0,0], scale=1, offset=0),
            tags        = ['time'],
            description = 'seconds')
        self.entry_ms = UnitConverterEntry(
            unit        = UnitLinearSI([0,1,0,0,0,0,0], scale=0.001, offset=0),
            tags        = ['time'],
            description = 'milliseconds')
        self.entry_kg = UnitConverterEntry(
            unit        = UnitLinearSI([0,0,0,0,0,0,1], scale=1, offset=0),
            tags        = ['mass'],
            name        = 'kilograms',
            description = 'SI unit of mass')
        self.entry_N = UnitConverterEntry(
            unit        = UnitLinearSI([1,-2,0,0,0,0,1], scale=1, offset=0),
            tags        = ['force'],
            description = 'Newtons')
        self.entry_kN = UnitConverterEntry(
            unit        = UnitLinearSI([1,-2,0,0,0,0,1], scale=1000, offset=0),
            tags        = ['force'],
            description = 'kilonewtons')

        # Sample unit converters
        self.unit_converter = UnitConverter(unit_system=UnitSystemSI())
        self.unit_converter['m'] = self.entry_m
        self.unit_converter['mm'] = self.entry_mm
        self.unit_converter['s'] = self.entry_s
        self.unit_converter['kg'] = self.entry_kg
        self.unit_converter['N'] = self.entry_N
        self.unit_converter['kN'] = self.entry_kN

        self.unit_converter_empty = UnitConverter(unit_system=UnitSystemSI())

    def test_repr(self):
        # Verifies that the printable string representation of a `UnitConverter`
        # object is constructed correctly
        self.assertEqual(
            self.unit_converter.__repr__(),
            ("<class 'pyxx.units.classes.unitconverter.UnitConverter'>\n"
             "-- System of units: <class 'pyxx.units.classes.unitsystem.UnitSystemSI'> - SI - International System of Units\n"
             "Key    Name         Tags          base_unit_exps                   Description    \n"
             "----------------------------------------------------------------------------------\n"
             "m      meter        ['length']    [1. 0. 0. 0. 0. 0. 0.]           meters         \n"
             "mm     None         ['length']    [1. 0. 0. 0. 0. 0. 0.]           millimeters    \n"
             "s      None         ['time']      [0. 1. 0. 0. 0. 0. 0.]           seconds        \n"
             "kg     kilograms    ['mass']      [0. 0. 0. 0. 0. 0. 1.]           SI unit of mass\n"
             "N      None         ['force']     [ 1. -2.  0.  0.  0.  0.  1.]    Newtons        \n"
             "kN     None         ['force']     [ 1. -2.  0.  0.  0.  0.  1.]    kilonewtons    ")
        )

    def test_str(self):
        # Verifies that the string representation of a `UnitConverter` object
        # is constructed correctly
        self.assertEqual(
            str(self.unit_converter),
            ("Key    Name         Tags          base_unit_exps                   Description    \n"
             "----------------------------------------------------------------------------------\n"
             "m      meter        ['length']    [1. 0. 0. 0. 0. 0. 0.]           meters         \n"
             "mm     None         ['length']    [1. 0. 0. 0. 0. 0. 0.]           millimeters    \n"
             "s      None         ['time']      [0. 1. 0. 0. 0. 0. 0.]           seconds        \n"
             "kg     kilograms    ['mass']      [0. 0. 0. 0. 0. 0. 1.]           SI unit of mass\n"
             "N      None         ['force']     [ 1. -2.  0.  0.  0.  0.  1.]    Newtons        \n"
             "kN     None         ['force']     [ 1. -2.  0.  0.  0.  0.  1.]    kilonewtons    ")
        )

    def test_generate_table(self):
        # Verifies that printable table of units is generated correctly
        with self.subTest(unit_converter='filled'):
            self.assertListEqual(
                self.unit_converter._generate_unit_table(list(self.unit_converter.keys())),
                ["Key    Name         Tags          base_unit_exps                   Description    ",
                 "----------------------------------------------------------------------------------",
                 "m      meter        ['length']    [1. 0. 0. 0. 0. 0. 0.]           meters         ",
                 "mm     None         ['length']    [1. 0. 0. 0. 0. 0. 0.]           millimeters    ",
                 "s      None         ['time']      [0. 1. 0. 0. 0. 0. 0.]           seconds        ",
                 "kg     kilograms    ['mass']      [0. 0. 0. 0. 0. 0. 1.]           SI unit of mass",
                 "N      None         ['force']     [ 1. -2.  0.  0.  0.  0.  1.]    Newtons        ",
                 "kN     None         ['force']     [ 1. -2.  0.  0.  0.  0.  1.]    kilonewtons    "]
            )

        with self.subTest(unit_converter='empty'):
            self.assertListEqual(
                self.unit_converter_empty._generate_unit_table(list(self.unit_converter_empty.keys())),
                ["Key    Name    Tags    base_unit_exps    Description",
                 "----------------------------------------------------"]
            )

    def test_generate_table_col_spacing(self):
        # Verifies that printable table of units is generated correctly with
        # non-default column spacing
        with self.subTest(unit_converter='filled'):
            self.assertListEqual(
                self.unit_converter._generate_unit_table(
                    list(self.unit_converter.keys()),
                    col_spacing=1
                ),
                ["Key Name      Tags       base_unit_exps                Description    ",
                 "----------------------------------------------------------------------",
                 "m   meter     ['length'] [1. 0. 0. 0. 0. 0. 0.]        meters         ",
                 "mm  None      ['length'] [1. 0. 0. 0. 0. 0. 0.]        millimeters    ",
                 "s   None      ['time']   [0. 1. 0. 0. 0. 0. 0.]        seconds        ",
                 "kg  kilograms ['mass']   [0. 0. 0. 0. 0. 0. 1.]        SI unit of mass",
                 "N   None      ['force']  [ 1. -2.  0.  0.  0.  0.  1.] Newtons        ",
                 "kN  None      ['force']  [ 1. -2.  0.  0.  0.  0.  1.] kilonewtons    "]
            )

        with self.subTest(unit_converter='empty'):
            self.assertListEqual(
                self.unit_converter_empty._generate_unit_table(
                    list(self.unit_converter_empty.keys()),
                    col_spacing=1
                ),
                ["Key Name Tags base_unit_exps Description",
                 "----------------------------------------"]
            )

    def test_generate_table_no_header(self):
        # Verifies that printable table of units is generated correctly with no header
        with self.subTest(unit_converter='filled'):
            self.assertListEqual(
                self.unit_converter._generate_unit_table(
                    list(self.unit_converter.keys()),
                    generate_header=False
                ),
                ["m      meter        ['length']    [1. 0. 0. 0. 0. 0. 0.]           meters         ",
                 "mm     None         ['length']    [1. 0. 0. 0. 0. 0. 0.]           millimeters    ",
                 "s      None         ['time']      [0. 1. 0. 0. 0. 0. 0.]           seconds        ",
                 "kg     kilograms    ['mass']      [0. 0. 0. 0. 0. 0. 1.]           SI unit of mass",
                 "N      None         ['force']     [ 1. -2.  0.  0.  0.  0.  1.]    Newtons        ",
                 "kN     None         ['force']     [ 1. -2.  0.  0.  0.  0.  1.]    kilonewtons    "]
            )

        with self.subTest(unit_converter='empty'):
            self.assertListEqual(
                self.unit_converter_empty._generate_unit_table(
                    list(self.unit_converter_empty.keys()),
                    generate_header=False
                ),
                []
            )

    def test_unit_system(self):
        # Verifies that "unit_system" attribute is stored correctly
        with self.subTest(comment='constructor'):
            self.assertIs(type(self.unit_converter.unit_system), UnitSystemSI)

        with self.subTest(comment='read_only'):
            with self.assertRaises(AttributeError):
                self.unit_converter.unit_system = UnitSystemSI(name='new_SI')

        with self.subTest(comment='invalid_type'):
            with self.assertRaises(TypeError):
                UnitConverter(unit_system=UnitSystemSI)

    def test_get_unit(self):
        # Verifies that units can be correctly retrieved from a unit converter
        self.assertIs(self.unit_converter['m'], self.entry_m)
        self.assertIs(self.unit_converter['mm'], self.entry_mm)
        self.assertIs(self.unit_converter['s'], self.entry_s)
        self.assertIs(self.unit_converter['kg'], self.entry_kg)
        self.assertIs(self.unit_converter['N'], self.entry_N)
        self.assertIs(self.unit_converter['kN'], self.entry_kN)

    def test_get_unit_invalid(self):
        # Verifies that an appropriate error is thrown if providing invalid
        # inputs when attempting to retrieve a unit
        with self.subTest(issue='invalid_key_type'):
            with self.assertRaises(TypeError):
                self.unit_converter[0]

            with self.assertRaises(TypeError):
                self.unit_converter[self.m]

        with self.subTest(issue='unit_not_found'):
            with self.assertRaises(UnitNotFoundError):
                self.unit_converter['ms']

    def test_set_unit(self):
        # Verifies that new units can be added to the unit converter as expected
        with self.subTest(operation='add_unit'):
            self.assertEqual(len(self.unit_converter), 6)
            self.assertListEqual(
                list(self.unit_converter.keys()),
                ['m', 'mm', 's', 'kg', 'N', 'kN']
            )

            self.unit_converter['ms'] = self.entry_ms
            self.assertEqual(len(self.unit_converter), 7)
            self.assertListEqual(
                list(self.unit_converter.keys()),
                ['m', 'mm', 's', 'kg', 'N', 'kN', 'ms']
            )

        with self.subTest(operation='modify'):
            self.unit_converter['m'] = self.entry_kN
            self.assertIs(self.unit_converter['m'], self.entry_kN)
            self.assertListEqual(
                list(self.unit_converter.keys()),
                ['m', 'mm', 's', 'kg', 'N', 'kN', 'ms']
            )

    def test_set_unit_invalid(self):
        # Verifies that an appropriate error is thrown if attempting to add a
        # unit to the unit converter and providing invalid inputs
        with self.subTest(issue='invalid_value_type'):
            with self.assertRaises(TypeError):
                self.unit_converter['ms'] = self.ms

        with self.subTest(issue='key_not_str'):
            with self.assertRaises(TypeError):
                self.unit_converter[self.ms] = self.entry_ms

            with self.assertRaises(TypeError):
                self.unit_converter[100] = self.entry_ms

        with self.subTest(issue='compound_unit_key'):
            with self.assertRaises(ValueError):
                self.unit_converter['m/s'] = self.entry_ms

        with self.subTest(issue='incorrect_unit_system'):
            with self.assertRaises(TypeError):
                self.unit_converter['ms'] = UnitConverterEntry(
                    Unit(UnitSystem(7), [1, 0, 0, 0, 0, 0, 0],
                    to_base_function=lambda x, exp: x,
                    from_base_function=lambda x, exp: x)
                )

    def test_add_unit(self):
        # Verifies that a new unit can be added to the unit converter
        with self.subTest(step='add_unit'):
            self.assertEqual(len(self.unit_converter), 6)
            self.assertListEqual(
                list(self.unit_converter.keys()),
                ['m', 'mm', 's', 'kg', 'N', 'kN']
            )

            self.unit_converter.add_unit(
                key='ms', unit=self.ms, tags=['time', 'milliseconds'],
                name='Milliseconds', description='units of milliseconds',
                overwrite=False)

            self.assertEqual(len(self.unit_converter), 7)
            self.assertListEqual(
                list(self.unit_converter.keys()),
                ['m', 'mm', 's', 'kg', 'N', 'kN', 'ms'])
            self.assertListEqual(
                list(self.unit_converter['ms'].tags), ['time', 'milliseconds'])
            self.assertEqual(
                self.unit_converter['ms'].name, 'Milliseconds')
            self.assertEqual(
                self.unit_converter['ms'].description, 'units of milliseconds')

        with self.subTest(step='no_overwrite'):
            with self.assertRaises(UnitAlreadyDefinedError):
                self.unit_converter.add_unit(
                    key='ms', unit=self.ms, tags=['time', 'milliseconds'],
                    description='units of milliseconds', overwrite=False)

        with self.subTest(step='overwrite'):
            self.unit_converter.add_unit(
                key='ms', unit=self.ms, tags=['duration'],
                description='units of ms', overwrite=True)

            self.assertEqual(len(self.unit_converter), 7)
            self.assertListEqual(
                list(self.unit_converter.keys()),
                ['m', 'mm', 's', 'kg', 'N', 'kN', 'ms'])
            self.assertListEqual(
                list(self.unit_converter['ms'].tags), ['duration'])
            self.assertEqual(
                self.unit_converter['ms'].description, 'units of ms')

    def test_add_alias(self):
        # Verifies that a single unit alias can be added as expected
        with self.subTest(step='add_alias'):
            self.assertEqual(len(self.unit_converter), 6)
            self.assertListEqual(
                list(self.unit_converter.keys()),
                ['m', 'mm', 's', 'kg', 'N', 'kN']
            )

            self.unit_converter.add_alias(key='s', aliases='second')

            self.assertEqual(len(self.unit_converter), 7)
            self.assertListEqual(
                list(self.unit_converter.keys()),
                ['m', 'mm', 's', 'kg', 'N', 'kN', 'second']
            )
            self.assertIs(self.unit_converter['second'], self.unit_converter['s'])

        with self.subTest(step='check_ref'):
            self.unit_converter['second'].description = 'seconds unit'
            self.assertEqual(self.unit_converter['s'].description, 'seconds unit')

    def test_add_aliases(self):
        # Verifies that multiple unit aliases can be added as expected
        self.assertEqual(len(self.unit_converter), 6)
        self.assertListEqual(
            list(self.unit_converter.keys()),
            ['m', 'mm', 's', 'kg', 'N', 'kN']
        )

        self.unit_converter.add_alias(key='s', aliases=('sec', 'second'))

        self.assertEqual(len(self.unit_converter), 8)
        self.assertListEqual(
            list(self.unit_converter.keys()),
            ['m', 'mm', 's', 'kg', 'N', 'kN', 'sec', 'second']
        )
        self.assertIs(self.unit_converter['sec'], self.unit_converter['s'])
        self.assertIs(self.unit_converter['second'], self.unit_converter['s'])

    def test_add_unit_alias(self):
        # Verifies that unit aliases can be added at the same time as adding
        # a unit to the unit converter
        self.assertEqual(len(self.unit_converter), 6)
        self.assertListEqual(
            list(self.unit_converter.keys()),
            ['m', 'mm', 's', 'kg', 'N', 'kN']
        )

        self.unit_converter.add_unit(
            key='ms', unit=self.ms, tags=['time', 'milliseconds'],
            name='Milliseconds', description='units of milliseconds',
            aliases=('myUnit', 'millisec'),
            overwrite=False)

        self.assertEqual(len(self.unit_converter), 9)
        self.assertListEqual(
            list(self.unit_converter.keys()),
            ['m', 'mm', 's', 'kg', 'N', 'kN', 'ms', 'myUnit', 'millisec'])

        self.assertIs(self.unit_converter['ms'], self.unit_converter['myUnit'])
        self.assertIs(self.unit_converter['ms'], self.unit_converter['millisec'])

    def test_convert_simple(self):
        # Verifies that unit converter performs unit conversions correctly
        # for simple units
        inputs = 1000 * np.random.randn(100)

        with self.subTest(unit_conversion='m -> m'):
            self.assertTrue(np.allclose(
                self.unit_converter.convert(quantity=inputs, from_unit='m', to_unit='m'),
                inputs
            ))

        with self.subTest(unit_conversion='mm -> m'):
            self.assertTrue(np.allclose(
                self.unit_converter.convert(quantity=inputs, from_unit='mm', to_unit='m'),
                inputs / 1000
            ))

        with self.subTest(unit_conversion='kN -> N'):
            self.assertTrue(np.allclose(
                self.unit_converter.convert(quantity=inputs, from_unit='kN', to_unit='N'),
                inputs * 1000
            ))

    def test_convert_compound(self):
        # Verifies that unit converter performs unit conversions correctly
        # for compound units
        inputs = 1000 * np.random.randn(100)

        with self.subTest(unit_conversion='m/s -> m/s'):
            self.assertTrue(np.allclose(
                self.unit_converter.convert(quantity=inputs, from_unit='m/s', to_unit='m/s'),
                inputs
            ))

        with self.subTest(unit_conversion='m^2/s -> mm^2/s'):
            self.assertTrue(np.allclose(
                self.unit_converter.convert(quantity=inputs, from_unit='m^2/s', to_unit='mm^2/s'),
                inputs * 1e6
            ))

        with self.subTest(unit_conversion='kg*m/s^2 -> N'):
            self.assertTrue(np.allclose(
                self.unit_converter.convert(quantity=inputs, from_unit='kg*m/s^2', to_unit='N'),
                inputs
            ))

        with self.subTest(unit_conversion='kg*m/s^2 -> kN'):
            self.assertTrue(np.allclose(
                self.unit_converter.convert(quantity=inputs, from_unit='kg*m/s^2', to_unit='kN'),
                inputs / 1000
            ))

        with self.subTest(unit_conversion='kN -> kg*mm/s^2'):
            self.assertTrue(np.allclose(
                self.unit_converter.convert(quantity=inputs, from_unit='kN', to_unit='kg*mm/s^2'),
                inputs * 1e6
            ))

    def test_convert_invalid(self):
        # Verifies that an appropriate error is thrown if attempting to
        # perform an invalid unit conversion
        with self.subTest(issue='not_str'):
            with self.assertRaises(TypeError):
                self.unit_converter.convert(quantity=100, from_unit=self.m, to_unit='mm')

            with self.assertRaises(TypeError):
                self.unit_converter.convert(quantity=100, from_unit='m', to_unit=self.mm)

            with self.assertRaises(TypeError):
                self.unit_converter.convert(quantity=100, from_unit=self.m, to_unit=self.mm)

        with self.subTest(issue='incompatible_units'):
            with self.assertRaises(IncompatibleUnitsError):
                self.unit_converter.convert(quantity=100, from_unit='kg', to_unit='mm')

    def test_is_convertible(self):
        # Verifies that incompatible units are recognized
        test_cases = (
            (('m', 'mm'),                       True),
            (('m', 'mm', 'm'),                  True),
            (('m', 'mm', 'mm', 'm'),            True),

            (('N*m', 'N*mm'),                   True),
            (('kN*m', 'N*mm', 'N*m'),           True),
            (('N*m', 'N*mm', 'kN*mm', 'kN*m'),  True),

            (('m', 's'),                        False),
            (('s', 'm'),                        False),
            (('s', 'm', 'm'),                   False),
            (('m', 's', 'm'),                   False),
            (('m', 'm', 's'),                   False),
            (('s', 'mm', 'mm', 'm'),            False),
            (('m', 's', 'mm', 'm'),             False),
            (('m', 'mm', 's', 'm'),             False),
            (('m', 'mm', 'mm', 's'),            False),
        )

        for inputs, outputs in test_cases:
            with self.subTest(inputs=inputs, outputs=outputs):
                self.assertIs(self.unit_converter.is_convertible(*inputs), outputs)

    def test_is_defined_unit(self):
        # Verifies that it is possible to check whether a simple or compound
        # unit contains exclusively component units defined in the unit converter
        with self.subTest(unit_type='simple', defined=True):
            for unit in ('kg', 'm', 'N'):
                self.assertTrue(self.unit_converter.is_defined_unit(unit))

        with self.subTest(unit_type='simple', defined=False):
            for unit in ('miles', 'yd'):
                self.assertFalse(self.unit_converter.is_defined_unit(unit))

        with self.subTest(unit_type='compound', defined=True):
            for unit in ('kg*m/s^2', 'mm/s', 'N*mm'):
                self.assertTrue(self.unit_converter.is_defined_unit(unit))

        with self.subTest(unit_type='compound', defined=False):
            for unit in ('kg*in/s^2', 'in/s', 'in/hr'):
                self.assertFalse(self.unit_converter.is_defined_unit(unit))

    def test_is_simplified(self):
        # Verifies that simple vs. compound units are distinguished correctly
        test_cases = (
            ('mm',        True),
            ('s',         True),
            ('kilogram',  True),
            ('(kg)',      False),
            ('m/s',       False),
            (self.m,      False),
        )

        for inputs, outputs in test_cases:
            with self.subTest(inputs=inputs, outputs=outputs):
                self.assertIs(self.unit_converter.is_simplified_unit(inputs), outputs)

    def test_get_aliases(self):
        # Verifies that aliases can be retrieved correctly
        self.assertListEqual(self.unit_converter.get_aliases('s'), [])

        self.unit_converter.add_alias(key='s', aliases=['sec', 'mySeconds'])
        self.assertListEqual(self.unit_converter.get_aliases('s'), ['sec', 'mySeconds'])
        self.assertListEqual(self.unit_converter.get_aliases('sec'), ['s', 'mySeconds'])
        self.assertListEqual(self.unit_converter.get_aliases('mySeconds'), ['s', 'sec'])

    def test_get_aliases_invalid(self):
        # Verifies that an appropriate error is thrown if attemtping to retrieve
        # aliases for a unit that has not been defined
        with self.subTest(comment='invalid_unit'):
            with self.assertRaises(UnitNotFoundError):
                self.unit_converter.get_aliases('invalid_unit')

        with self.subTest(comment='compound_unit'):
            with self.assertRaises(UnitNotFoundError):
                self.unit_converter.get_aliases('m/s')

    def test_list_tags(self):
        # Verifies that tags are extracted correctly
        with self.subTest(unit_converter='filled'):
            self.assertListEqual(self.unit_converter.list_tags(),
                                 ['force', 'length', 'mass', 'time'])

        with self.subTest(unit_converter='empty'):
            self.assertListEqual(self.unit_converter_empty.list_tags(), [])

    def test_search_fields(self):
        # Verifies that searching a `UnitConverter` returns the expected
        # results
        with self.subTest(search_term='*', search_fields=('key', 'name', 'tags', 'description')):
            self.assertListEqual(
                self.unit_converter.search(
                    search_term='*',
                    search_fields=('key', 'name', 'tags', 'description'),
                    filter_by_tags=None,
                    print_results=False, return_results=True),
                ['m', 'mm', 's', 'kg', 'N', 'kN']
            )

            self.assertListEqual(
                self.unit_converter.search(
                    search_term='**',
                    search_fields=('key', 'name', 'tags', 'description'),
                    filter_by_tags=None,
                    print_results=False, return_results=True),
                ['m', 'mm', 's', 'kg', 'N', 'kN']
            )

        with self.subTest(search_term='meter', search_fields=('key', 'name', 'tags', 'description')):
            self.assertListEqual(
                self.unit_converter.search(
                    search_term='meter',
                    search_fields=('key', 'name', 'tags', 'description'),
                    filter_by_tags=None,
                    print_results=False, return_results=True),
                ['m', 'mm']
            )

        with self.subTest(search_term='kilo', search_fields=('key', 'name', 'tags', 'description')):
            self.assertListEqual(
                self.unit_converter.search(
                    search_term='kilo',
                    search_fields=('key', 'name', 'tags', 'description'),
                    filter_by_tags=None,
                    print_results=False, return_results=True),
                ['kg', 'kN']
            )

        with self.subTest(search_term='kilo', search_fields=('description',)):
            self.assertListEqual(
                self.unit_converter.search(
                    search_term='kilo',
                    search_fields=('description',),
                    filter_by_tags=None,
                    print_results=False, return_results=True),
                ['kN']
            )

        with self.subTest(search_term='kilo', search_fields='description'):
            self.assertListEqual(
                self.unit_converter.search(
                    search_term='kilo',
                    search_fields='description',
                    filter_by_tags=None,
                    print_results=False, return_results=True),
                ['kN']
            )

        with self.subTest(search_term='len', search_fields=('key', 'name', 'tags', 'description')):
            self.assertListEqual(
                self.unit_converter.search(
                    search_term='len',
                    search_fields=('key', 'name', 'tags', 'description'),
                    filter_by_tags=None,
                    print_results=False, return_results=True),
                ['m', 'mm']
            )

        with self.subTest(search_term='kN', search_fields=('key', 'name', 'tags', 'description')):
            self.assertListEqual(
                self.unit_converter.search(
                    search_term='kN',
                    search_fields=('key', 'name', 'tags', 'description'),
                    filter_by_tags=None,
                    print_results=False, return_results=True),
                ['kN']
            )

    def test_search_filter_by_tags(self):
        # Verifies that searching a `UnitConverter` returns the expected
        # results
        with self.subTest(search_term='*', filter_by_tags=('length', 'mass')):
            self.assertListEqual(
                self.unit_converter.search(
                    search_term='*',
                    filter_by_tags=('length', 'mass'),
                    print_results=False, return_results=True),
                ['m', 'mm', 'kg']
            )

        with self.subTest(search_term='kilo', filter_by_tags=('mass', 'time')):
            self.assertListEqual(
                self.unit_converter.search(
                    search_term='kilo',
                    filter_by_tags=('mass', 'time'),
                    print_results=False, return_results=True),
                ['kg']
            )

        with self.subTest(search_term='kilo', search_fields=('time',)):
            self.assertListEqual(
                self.unit_converter.search(
                    search_term='kilo',
                    filter_by_tags=('time',),
                    print_results=False, return_results=True),
                []
            )

        with self.subTest(search_term='kilo', filter_by_tags='nonexistent'):
            self.assertListEqual(
                self.unit_converter.search(
                    search_term='kilo',
                    filter_by_tags='nonexistent',
                    print_results=False, return_results=True),
                []
            )

    def test_search_invalid(self):
        # Verifies that attempting to perform a search of a `UnitConverter`
        # with invalid inputs results in an appropriate error
        with self.subTest(issue='search_term_not_str'):
            with self.assertRaises(TypeError):
                self.unit_converter.search(
                    search_term=123,
                    print_results=False, return_results=True)

        with self.subTest(issue='invalid_search_fields'):
            with self.assertRaises(ValueError):
                self.unit_converter.search(
                    search_term='*',
                    search_fields=['key', 'nonexistent_field'],
                    print_results=False, return_results=True)

    def test_search_print(self):
        # Verifies that output displayed to the terminal by searching a
        # `UnitConverter` matches expectations
        with CapturePrint() as terminal_stdout:
            outputs = self.unit_converter.search(
                search_term='m',
                print_results=True, return_results=False)
            text = terminal_stdout.getvalue()

        self.assertIsNone(outputs)
        self.assertEqual(
            text,
            ("Key    Name         Tags          base_unit_exps            Description    \n"
             "---------------------------------------------------------------------------\n"
             "m      meter        ['length']    [1. 0. 0. 0. 0. 0. 0.]    meters         \n"
             "mm     None         ['length']    [1. 0. 0. 0. 0. 0. 0.]    millimeters    \n"
             "s      None         ['time']      [0. 1. 0. 0. 0. 0. 0.]    seconds        \n"
             "kg     kilograms    ['mass']      [0. 0. 0. 0. 0. 0. 1.]    SI unit of mass\n")
        )

    def test_search_hide_aliases(self):
        # Verifies that "search()" method options to show/hide aliases
        # function as expected
        self.unit_converter_empty['m'] = self.entry_m
        self.unit_converter_empty.add_alias('m', 'meter')

        with self.subTest(hide_aliases=False):
            self.assertListEqual(
                self.unit_converter_empty.search('*', hide_aliases=False,
                                                 print_results=False, return_results=True),
                ['m', 'meter'])

        with self.subTest(hide_aliases=True):
            self.assertListEqual(
                self.unit_converter_empty.search('*', hide_aliases=True,
                                                 print_results=False, return_results=True),
                ['m'])

    def test_str_to_unit(self):
        # Verifies that strings are converted to units correctly
        with self.subTest(unit='mm'):
            unit = self.unit_converter.str_to_unit('mm')

            self.assertListEqual(list(unit.base_unit_exps), [1, 0, 0, 0, 0, 0, 0])

            inputs = 100 * np.random.randn(100)
            self.assertTrue(np.allclose(unit.to_base(inputs), inputs / 1000))
            self.assertTrue(np.allclose(unit.from_base(inputs), inputs * 1000))

        with self.subTest(unit='kg*(mm/s)'):
            unit = self.unit_converter.str_to_unit('kg*(mm/s)')

            self.assertListEqual(list(unit.base_unit_exps), [1, -1, 0, 0, 0, 0, 1])

            inputs = 100 * np.random.randn(100)
            self.assertTrue(np.allclose(unit.to_base(inputs), inputs / 1000))
            self.assertTrue(np.allclose(unit.from_base(inputs), inputs * 1000))

        with self.subTest(unit='[empty]'):
            unit = self.unit_converter.str_to_unit('')

            self.assertListEqual(list(unit.base_unit_exps), [0, 0, 0, 0, 0, 0, 0])

            inputs = 100 * np.random.randn(100)
            self.assertTrue(np.allclose(unit.to_base(inputs), inputs))
            self.assertTrue(np.allclose(unit.from_base(inputs), inputs))
