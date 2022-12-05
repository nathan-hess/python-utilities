import sys
import unittest
from unittest.mock import Mock

import pyxx
from pyxx.units.classes.cli import UnitConverterCLI
from tests import CapturePrint


class Test_ExecuteFromCommandLine(unittest.TestCase):
    def setUp(self) -> None:
        self._execute = UnitConverterCLI.execute
        self._exit = sys.exit

    def tearDown(self) -> None:
        sys.exit = self._exit
        UnitConverterCLI.execute = self._execute

    def test_argv(self):
        # Verifies that if a list of command-line arguments is passed as
        # input, the unit converter CLI is run with these arguments
        UnitConverterCLI.execute = Mock(return_value=159)
        sys.exit = Mock()

        argv = ['arg1', '--flag1', 'val2']
        pyxx.units.execute_from_command_line(argv)

        with self.subTest(comment='arguments'):
            UnitConverterCLI.execute.assert_called_once_with(['arg1', '--flag1', 'val2'])

        with self.subTest(comment='exit_code'):
            sys.exit.assert_called_once_with(159)

    def test_sys_argv(self):
        # Verifies that if no command-line arguments are passed as input, the
        # unit converter CLI is run with `sys.argv[1:]`
        UnitConverterCLI.execute = Mock(return_value=159)
        sys.exit = Mock()

        pyxx.units.execute_from_command_line()
        UnitConverterCLI.execute.assert_called_once_with(sys.argv[1:])


class Test_UnitConverterCLI(unittest.TestCase):
    def setUp(self) -> None:
        self.cli = UnitConverterCLI()

    def test_execute_dispatch(self):
        # Verifies that sub-commands are executed correctly
        self.cli._convert = Mock()
        self.cli.help = Mock()
        self.cli._info = Mock()
        self.cli._search = Mock()
        self.cli.version = Mock()

        with self.subTest(command='convert'):
            for arg in ('convert', 'c'):
                with self.subTest(arg=arg):
                    self.cli._convert.reset_mock()
                    self.cli.execute([arg])
                    self.cli._convert.assert_called_once()

                    self.cli._convert.reset_mock()
                    self.cli.execute([arg, '-h', '--version'])
                    self.cli._convert.assert_called_once()

        with self.subTest(command='help'):
            for arg in ('help', 'h', '-h', '--help'):
                with self.subTest(arg=arg):
                    self.cli.help.reset_mock()
                    self.cli.execute([arg])
                    self.cli.help.assert_called_once()

                    self.cli.help.reset_mock()
                    self.cli.execute([arg, '-h', '--version'])
                    self.cli.help.assert_called_once()

        with self.subTest(command='info'):
            for arg in ('info', 'i'):
                with self.subTest(arg=arg):
                    self.cli._info.reset_mock()
                    self.cli.execute([arg])
                    self.cli._info.assert_called_once()

                    self.cli._info.reset_mock()
                    self.cli.execute([arg, '-h', '--version'])
                    self.cli._info.assert_called_once()

        with self.subTest(command='search'):
            for arg in ('search', 's'):
                with self.subTest(arg=arg):
                    self.cli._search.reset_mock()
                    self.cli.execute([arg])
                    self.cli._search.assert_called_once()

                    self.cli._search.reset_mock()
                    self.cli.execute([arg, '-h', '--version'])
                    self.cli._search.assert_called_once()

        with self.subTest(command='version'):
            for arg in ('version', 'v', '--version'):
                with self.subTest(arg=arg):
                    self.cli.version.reset_mock()
                    self.cli.execute([arg])
                    self.cli.version.assert_called_once()

                    self.cli.version.reset_mock()
                    self.cli.execute([arg, '-h', '--version'])
                    self.cli.version.assert_called_once()

    def test_execute_invalid(self):
        # Verifies that an appropriate error is generated if attempting
        # to run CLI with invalid inputs
        self.cli._exit_with_error = Mock()

        with self.subTest(issue='no_command'):
            self.cli._exit_with_error.reset_mock()
            self.cli.execute([])
            self.cli._exit_with_error.assert_called_once()

        with self.subTest(issue='invalid_command'):
            self.cli._exit_with_error.reset_mock()
            self.cli.execute(['invalid_command'])
            self.cli._exit_with_error.assert_called_once()

            self.cli._exit_with_error.reset_mock()
            self.cli.execute(['invalid_command', '--help'])
            self.cli._exit_with_error.assert_called_once()

    def test_convert_single(self):
        # Verifies that the unit converter CLI performs a unit conversion for
        # a single value correctly
        for from_flag in ('-f', '--from'):
            for to_flag in ('-t', '--to'):
                with CapturePrint() as terminal_output:
                    args = [from_flag, 'mi/hr', to_flag, 'm/s', '720.9185837']

                    with self.subTest(args=args):
                        # Check exit code
                        self.assertEqual(self.cli._convert(args), 0)

                        # Check printed text
                        converted_quantity = pyxx.units.UnitConverterSI().convert(
                            quantity=720.9185837,
                            from_unit='mi/hr', to_unit='m/s')

                        self.assertEqual(terminal_output.getvalue(), str(converted_quantity) + '\n')

    def test_convert_multiple(self):
        # Verifies that the unit converter CLI performs a unit conversion for
        # a multiple values correctly
        for from_flag in ('-f', '--from'):
            for to_flag in ('-t', '--to'):
                with CapturePrint() as terminal_output:
                    args = [from_flag, 'mi/hr', to_flag, 'm/s', '720.9185837,10, 0, -10']

                    with self.subTest(args=args):
                        # Check exit code
                        self.assertEqual(self.cli._convert(args), 0)

                        # Check printed text
                        converted_quantities = list(pyxx.units.UnitConverterSI().convert(
                            quantity=[720.9185837, 10, 0, -10],
                            from_unit='mi/hr', to_unit='m/s'))

                        self.assertEqual(
                            terminal_output.getvalue(),
                            ','.join([str(x) for x in converted_quantities]) + '\n'
                        )

    def test_convert_invalid(self):
        # Verifies that an appropriate error message is thrown if attempting
        # to perform a unit conversion with invalid inputs
        self.cli._exit_with_error = Mock()

        with self.subTest(issue='undefined_unit'):
            self.cli._exit_with_error.reset_mock()
            self.cli._convert(['-f', 'invalid_unit', '-t', 'm/s', '10'])
            self.cli._exit_with_error.assert_called_once()

            self.cli._exit_with_error.reset_mock()
            self.cli._convert(['-f', 'm/s', '-t', 'invalid_unit', '10'])
            self.cli._exit_with_error.assert_called_once()

        with self.subTest(issue='incompatible_units'):
            self.cli._exit_with_error.reset_mock()
            self.cli._convert(['-f', 'm', '-t', 'm/s', '10'])
            self.cli._exit_with_error.assert_called_once()

        with self.subTest(issue='invalid_quantity_format'):
            self.cli._exit_with_error.reset_mock()
            self.cli._convert(['-f', 'm', '-t', 'm', 'ten'])
            self.cli._exit_with_error.assert_called_once()

            self.cli._exit_with_error.reset_mock()
            self.cli._convert(['-f', 'm', '-t', 'm', '0,1,2,3:4'])
            self.cli._exit_with_error.assert_called_once()

            self.cli._exit_with_error.reset_mock()
            self.cli._convert(['-f', 'm', '-t', 'm', '0,1,2,3+4'])
            self.cli._exit_with_error.assert_called_once()

    def test_exit_with_error_message(self):
        # Verifies that correct message is displayed when exiting with error
        with CapturePrint() as terminal_stdout:
            self.cli._exit_with_error(message='My error message')

            self.assertEqual(
                terminal_stdout.getvalue(),
                f'{self.cli.PROGRAM_NAME}: error: My error message\n'
            )

    def test_exit_with_error_exit_code(self):
        # Verifies that correct exit code is returned when exiting with error
        with CapturePrint():
            for exit_code in range(1, 256):
                with self.subTest(exit_code=exit_code):
                    self.assertEqual(
                        self.cli._exit_with_error(
                            message='message',
                            exit_code=exit_code),
                        exit_code
                    )

    def test_exit_with_error_help(self):
        # Verifies that CLI help message printing can be enabled/disabled
        # when exiting with error
        self.cli.help = Mock()

        with CapturePrint():
            for print_help in (True, False):
                with self.subTest(print_help=print_help):
                    self.cli.help.reset_mock()
                    self.cli._exit_with_error(message='', print_help=print_help)
                    self.assertIs(self.cli.help.called, print_help)

    def test_exit_with_error_invalid(self):
        # Verifies that an appropriate error is thrown if attemtping to exit
        # with error and providing invalid arguments
        with CapturePrint():
            with self.subTest(issue='invalid_exit_code'):
                # Negative exit codes
                for exit_code in range(-1000, 1):
                    with self.subTest(exit_code=exit_code):
                        with self.assertRaises(ValueError):
                            self.cli._exit_with_error(message='', exit_code=exit_code)

                # Exit codes greater than 255
                for exit_code in range(256, 1000):
                    with self.subTest(exit_code=exit_code):
                        with self.assertRaises(ValueError):
                            self.cli._exit_with_error(message='', exit_code=exit_code)

            with self.subTest(issue='exit_code_not_integer'):
                with self.subTest(type=float):
                    with self.assertRaises(TypeError):
                        self.cli._exit_with_error(message='', exit_code=1.5)

                    with self.assertRaises(TypeError):
                        self.cli._exit_with_error(message='', exit_code=1.0)

                with self.subTest(type=str):
                    with self.assertRaises(TypeError):
                        self.cli._exit_with_error(message='', exit_code='1')

    def test_help(self):
        # Verifies that content is printed when showing the main CLI help
        with CapturePrint() as terminal_stdout:
            # Verify correct exit code
            self.assertEqual(self.cli.help(), 0)

            # Verify some help text is printed
            self.assertGreater(len(terminal_stdout.getvalue().strip()), 0)

    def test_info(self):
        # Verifies that expected output is printed when looking up information
        # on a unit
        with CapturePrint() as terminal_output:
            # Check exit code
            self.assertEqual(self.cli._info(['kg']), 0)

            # Check printed text
            key = 'kg'
            unit_entry = pyxx.units.UnitConverterSI()[key]
            aliases = pyxx.units.UnitConverterSI().get_aliases(key)

            self.assertEqual(
                terminal_output.getvalue(),
                (f'Unit ID:          {key}\n'
                 f'Name:             {unit_entry.name}\n'
                 f'Description:      {unit_entry.description}\n'
                 f'Tags:             {unit_entry.tags}\n'
                 f'Aliases:          {aliases}\n'
                 f'Unit definition:  {str(unit_entry.unit)}\n')
            )

    def test_info_invalid(self):
        # Verifies that an error is generated if attempting to look up
        # information on a unit but providing invalid arguments
        self.cli._exit_with_error = Mock()

        with self.subTest(issue='compound_unit'):
            self.cli._exit_with_error.reset_mock()
            self.cli._info(['m/s'])
            self.cli._exit_with_error.assert_called_once()

        with self.subTest(issue='undefined_unit'):
            self.cli._exit_with_error.reset_mock()
            self.cli._info(['invalid_unit'])
            self.cli._exit_with_error.assert_called_once()

    def test_search(self):
        # Verifies that a basic search produces expected results
        with CapturePrint() as terminal_output:
            pyxx.units.UnitConverterSI().search(
                'mi', print_results=True, return_results=False)

            expected_text = terminal_output.getvalue()

        with CapturePrint() as terminal_output:
            self.assertEqual(self.cli._search(['mi']), 0)
            self.assertEqual(terminal_output.getvalue(), expected_text)

    def test_search_search_fields(self):
        # Verifies that a search that limits search fields produces
        # expected results
        with self.subTest(num_search_fields=1):
            with CapturePrint() as terminal_output:
                pyxx.units.UnitConverterSI().search(
                    'mi', search_fields='name',
                    print_results=True, return_results=False)

                expected_text = terminal_output.getvalue()

            with CapturePrint() as terminal_output:
                self.assertEqual(self.cli._search(['--search-fields', 'name', 'mi']), 0)
                self.assertEqual(terminal_output.getvalue(), expected_text)

        with self.subTest(num_search_fields=3):
            with CapturePrint() as terminal_output:
                pyxx.units.UnitConverterSI().search(
                    'mi', search_fields=['name', 'key', 'description'],
                    print_results=True, return_results=False)

                expected_text = terminal_output.getvalue()

            with CapturePrint() as terminal_output:
                self.assertEqual(self.cli._search(['--search-fields', 'name, key,description', 'mi']), 0)
                self.assertEqual(terminal_output.getvalue(), expected_text)

    def test_search_filter_by_tags(self):
        # Verifies that a search that limits search fields produces
        # expected results
        with self.subTest(num_search_fields=1):
            with CapturePrint() as terminal_output:
                pyxx.units.UnitConverterSI().search(
                    'mi', filter_by_tags='length',
                    print_results=True, return_results=False)

                expected_text = terminal_output.getvalue()

            with CapturePrint() as terminal_output:
                self.assertEqual(self.cli._search(['--filter-by-tags', 'length', 'mi']), 0)
                self.assertEqual(terminal_output.getvalue(), expected_text)

        with self.subTest(num_search_fields=3):
            with CapturePrint() as terminal_output:
                pyxx.units.UnitConverterSI().search(
                    'mi', filter_by_tags=['length', 'time', 'pressure'],
                    print_results=True, return_results=False)

                expected_text = terminal_output.getvalue()

            with CapturePrint() as terminal_output:
                self.assertEqual(self.cli._search(['--filter-by-tags', 'length, time,pressure', 'mi']), 0)
                self.assertEqual(terminal_output.getvalue(), expected_text)

    def test_search_hide_aliases(self):
        # Verifies that a search that hides aliases produces expected results
        with CapturePrint() as terminal_output:
            pyxx.units.UnitConverterSI().search(
                'mi', hide_aliases=True,
                print_results=True, return_results=False)

            expected_text = terminal_output.getvalue()

        with CapturePrint() as terminal_output:
            self.assertEqual(self.cli._search(['mi', '--hide-aliases']), 0)
            self.assertEqual(terminal_output.getvalue(), expected_text)

    def test_search_invalid_fields(self):
        # Verifies that an error is generated if attempting to perform a
        # search with invalid search field arguments
        self.cli._exit_with_error = Mock()

        self.cli._exit_with_error.reset_mock()
        self.cli._search(['--search-fields', 'key,invalid_field', 's'])
        self.cli._exit_with_error.assert_called_once()

    def test_version(self):
        # Verifies that PyXX version is displayed correctly
        with CapturePrint() as terminal_stdout:
            # Verify correct exit code
            self.assertEqual(self.cli.version(), 0)

            # Verify correct version is printed
            self.assertEqual(terminal_stdout.getvalue().strip(),
                             pyxx.__version__)
