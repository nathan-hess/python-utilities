"""This module provides a command-line interface (CLI) that can be used to
interact with the :py:class:`UnitConverterSI` class.
"""

import argparse
import sys
from typing import List, Optional

from pyxx import __version__ as PYXX_VERSION
from pyxx.units.classes.unitconverter import UnitConverterSI


def execute_from_command_line(argv: Optional[List[str]] = None) -> None:
    """Calls the ScaleUtil CLI

    Runs the ScaleUtil CLI, allowing users to perform actions such as running
    a scaling analysis or post-processing results.

    Parameters
    ----------
    argv : list, optional
        List of arguments to pass to the ScaleUtil CLI.  If not provided or
        ``None``, arguments are obtained from ``sys.argv`` (default is
        ``None``)
    """
    if argv is None:
        argv = sys.argv[1:]

    sys.exit(UnitConverterCLI().execute(argv))


class UnitConverterCLI:
    """A command-line tool to interact with the PyXX unit conversion utilities

    This class is a wrapper around the :py:class:`UnitConverterSI` class,
    allowing users to access pre-defined units and perform basic searches and
    unit conversions from the terminal.  In most cases, to use this class,
    the :py:meth:`execute` method should be called with the desired arguments
    and flags in a :py:attr:`sys.argv`-style list.
    """

    def __init__(self) -> None:
        # Program metadata
        self.PROGRAM_NAME: str = 'unit-converter'

        self.PROGRAM_DESCRIPTION: str = '\n'.join([
            'PyXX unit converter command-line interface (CLI). This '
            'interface provides a\nsimple, terminal-based method to search '
            'and perform unit conversions with the\nPyXX package, without '
            'the need to set up scripts or launch a Python interpreter.\n'
            'For more information about unit conversions and available units,'
            'refer to the\nPyXX documentation (https://pyxx.readthedocs.io).',
            '',
            'Options:',
            '  -h, --help       Display this help message and exit',
            '      --version    Display PyXX unit converter version and exit',
            '',
            'Commands:',
            '  c, convert    Perform a unit conversion*',
            '  h, help       Display this help message and exit',
            '  i, info       Display information about a unit*',
            '  s, search     Search the units available in the unit converter*',
            '  v, version    Display PyXX unit converter version and exit',
            '',
            f'*Run \'{self.PROGRAM_NAME} COMMAND --help\' for more information '
            'about these commands',
        ]) + '\n'

        self.VERSION: str = PYXX_VERSION

        # Settings
        self._LINE_LENGTH: int = 80

    def help(self) -> int:
        """Prints the general help documentation for the CLI

        Outputs the general CLI usage information and command descriptions to
        the terminal.  More specific help (for each command) can be viewed by
        specifying the command with the "--help" flag.

        Returns
        -------
        int
            Exit code (0)
        """
        print(f'Usage:  {self.PROGRAM_NAME} [OPTIONS] COMMAND [COMMAND_OPTIONS]')
        print(f'\n{self.PROGRAM_DESCRIPTION}')

        return 0

    def execute(self, argv: List[str]) -> int:
        """Runs the PyXX unit converter CLI

        Parses a given set of :py:attr:`sys.argv`-style command-line arguments
        and displays to the terminal the results of the user-specified CLI
        actions.

        Parameters
        ----------
        argv : list
            A list of strings specifying the command-line arguments passed to
            the CLI.  Must be formatted in the same way as :py:attr:`sys.argv`

        Returns
        -------
        int
            Exit code
        """
        try:
            command = argv[0]
            argv = argv[1:]
        except IndexError:
            return self._exit_with_error(message='No command provided',
                                         print_help=True)

        if command in ('convert', 'c'):
            return self._convert(argv)

        if command in ('help', 'h', '--help', '-h'):
            return self.help()

        if command in ('version', 'v', '--version'):
            return self.version()

        return self._exit_with_error(message=f'Invalid command "{command}"',
                                     print_help=True)

    def version(self) -> int:
        """Displays the PyXX program version

        Returns
        -------
        int
            Exit code (0)
        """
        print(self.VERSION)

        return 0

    def _convert(self, argv: List[str]) -> int:
        # Process command-line arguments
        parser = argparse.ArgumentParser(
            prog=f'{self.PROGRAM_NAME} convert',
            description=(
                'Convert a quantity (either a single number or a comma-'
                'separated list of numbers) from one unit to another. Refer '
                'to the PyXX documentation (https://pyxx.readthedocs.io) or '
                'use the "search" command to view a list of available units.'
            )
        )

        required_args = parser.add_argument_group('required arguments')

        required_args.add_argument(
            'quantity',
            action='store',
            type=str,
            help=('The quantity to be converted from one unit to another. '
                  'Either formatted as a number or a comma-separated list '
                  'of numbers')
        )

        required_args.add_argument(
            '-f', '--from',
            action='store',
            type=str,
            dest='from_unit',
            help='The original unit in which the quantity was expressed',
            required=True
        )
        required_args.add_argument(
            '-t', '--to',
            action='store',
            type=str,
            dest='to_unit',
            help='The unit to which the quantity is to be converted',
            required=True
        )

        args = parser.parse_args(argv)

        # Validate inputs
        from_unit = str(args.from_unit)
        to_unit = str(args.to_unit)

        for unit in (from_unit, to_unit):
            if not UnitConverterSI().is_defined_unit(unit):
                return self._exit_with_error(
                    f'Cannot perform unit conversion. Unit "{unit}" has not '
                    'been defined in the unit converter')

        if not UnitConverterSI().is_convertible(from_unit, to_unit):
            return self._exit_with_error(
                f'Cannot perform unit conversion. Units "{from_unit}" '
                f'and {to_unit} are not compatible')

        try:
            quantity = [float(x) for x in str(args.quantity).split(',')]
        except (TypeError, ValueError):
            return self._exit_with_error(
                f'Invalid format "{args.quantity}" of quantity to convert. '
                'Quantity must either be a number or a comma-separated list '
                'of numbers')

        # Perform unit conversion
        converted_quantity: List[float] = list(UnitConverterSI().convert(
            quantity  = quantity,
            from_unit = from_unit,
            to_unit   = to_unit
        ))

        print(','.join([str(x) for x in converted_quantity]))
        return 0

    def _exit_with_error(self, message: str, exit_code: int = 1,
                         print_help: bool = False) -> int:
        """Displays a CLI error message and returns a specified, nonzero
        exit code

        Parameters
        ----------
        message : str
            Error message to display
        exit_code : int, optional
            The exit code to return.  Must be a nonzero integer (default
            is ``1``)
        print_help : bool, optional
            Whether to print the CLI help (i.e., whether to call
            :py:meth:`help`) before displaying error message (default
            is ``False``)

        Returns
        -------
        int
            Exit code specified by ``exit_code``
        """
        if not isinstance(exit_code, int):
            raise TypeError('Exit code must be an integer')

        if exit_code == 0:
            raise ValueError('Exit code should be nonzero')

        if print_help:
            self.help()
            print(f'{"-" * self._LINE_LENGTH}\n')

        print(f'{self.PROGRAM_NAME}: error: {message}')

        return exit_code
