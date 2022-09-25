import unittest

from pyxx.units import (
    UnitSystem,
)


class Test_UnitSystem(unittest.TestCase):
    def test_set_num_base_units(self):
        # Verifies that number of base units are set correctly
        self.assertEqual(UnitSystem(7)._num_base_units, 7)
        self.assertEqual(UnitSystem(3)._num_base_units, 3)

    def test_invalid_num_base_units(self):
        # Verifies that an error is thrown if the number of base
        # units provided is invalid
        with self.subTest(issue='float'):
            with self.assertRaises(TypeError):
                UnitSystem(7.3)

        with self.subTest(issue='str'):
            with self.assertRaises(TypeError):
                UnitSystem('9')

        with self.subTest(issue='zero'):
            with self.assertRaises(ValueError):
                UnitSystem(0)

        with self.subTest(issue='negative'):
            with self.assertRaises(ValueError):
                UnitSystem(-4)

    def test_set_name(self):
        # Verifies that name is set correctly
        with self.subTest(comment='name_provided'):
            self.assertEqual(UnitSystem(7, name='System')._name, 'System')

        with self.subTest(comment='no_name_provided'):
            self.assertIsNone(UnitSystem(7)._name)

    def test_invalid_name(self):
        # Verifies that an error is thrown if the name provided is invalid
        with self.assertRaises(TypeError):
            UnitSystem(7, name=100)

    def test_set_description(self):
        # Verifies that description is set correctly
        self.assertEqual(UnitSystem(7, description='UnitSys').description, 'UnitSys')
        self.assertIsNone(UnitSystem(7).description)

    def test_invalid_description(self):
        # Verifies that an error is thrown if the description
        # provided is invalid
        with self.assertRaises(TypeError):
            UnitSystem(7, description=100)

    def test_str(self):
        # Verifies that unit system string representation is correct
        self.assertEqual(
            str(UnitSystem(7)),
            "<class 'pyxx.units.classes.unitsystem.UnitSystem'>")

        self.assertEqual(
            str(UnitSystem(7, name='TestName')),
            "<class 'pyxx.units.classes.unitsystem.UnitSystem'> - TestName")

        self.assertEqual(
            str(UnitSystem(7, description='TestDescription')),
            "<class 'pyxx.units.classes.unitsystem.UnitSystem'> - TestDescription")

        self.assertEqual(
            str(UnitSystem(7, name='TestName', description='TestDescription')),
            "<class 'pyxx.units.classes.unitsystem.UnitSystem'> - TestName - TestDescription")

    def test_repr(self):
        # Verifies that unit system object representation is correct
        unit_system = UnitSystem(7, name='TestName', description='TestDescription')
        self.assertEqual(
            unit_system.__repr__(),
            "<class 'pyxx.units.classes.unitsystem.UnitSystem'> - TestName - TestDescription")

    def test_name_getter(self):
        # Verifies that "name" attribute is retrieved correctly
        system = UnitSystem(7)
        system._name = 'myUnitSystemName'

        self.assertEqual(system.name, 'myUnitSystemName')

    def test_name_setter(self):
        # Verifies that "name" attribute is set correctly
        with self.subTest(step='set_name'):
            system = UnitSystem(7)
            system.name = 'mySystem'
            self.assertEqual(system._name, 'mySystem')

        with self.subTest(step='delete_name'):
            system.name = None
            self.assertIsNone(system._name)

    def test_description_getter(self):
        # Verifies that "description" attribute is retrieved correctly
        system = UnitSystem(7)
        system._description = 'myUnitSystemDescription'

        self.assertEqual(system.description, 'myUnitSystemDescription')

    def test_description_setter(self):
        # Verifies that "description" attribute is set correctly
        with self.subTest(step='set_description'):
            system = UnitSystem(7)
            system.description = 'Description of the system'
            self.assertEqual(system._description, 'Description of the system')

        with self.subTest(step='delete_description'):
            system.description = None
            self.assertIsNone(system._description)

    def test_num_base_units_getter(self):
        # Verifies that "num_base_units" attribute is retrieved correctly
        system = UnitSystem(7)
        system._num_base_units = 30302

        self.assertEqual(system.num_base_units, 30302)

    def test_num_base_units_setter(self):
        # Verifies that an error is thrown if attempting to modify the
        # "num_base_units" attribute
        system = UnitSystem(7)
        with self.assertRaises(AttributeError):
            system.num_base_units = 10
