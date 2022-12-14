"""This module provides a command-line interface (CLI) that can be used to
interact with the :py:class:`UnitConverterSI` class.
"""

import argparse
import difflib
import sys
from typing import List, Optional

# Importing the package version is a cylic import, but because the
# `__version__` variable is defined at the beginning of `pyxx/__init__.py`,
# the variable is cached and cyclic import does not cause problems
from pyxx import __version__ as PYXX_VERSION    # pylint: disable=R0401
from pyxx.units.classes.unitconverter import UnitConverterSI
from pyxx.units.exceptions import InvalidSearchFieldError


def execute_from_command_line(argv: Optional[List[str]] = None) -> None:
    """Calls the PyXX unit converter CLI

    Runs the PyXX unit converter CLI, allowing users to perform actions such
    as converting quantities from one unit to another or viewing information
    about units.

    Parameters
    ----------
    argv : list, optional
        List of arguments to pass to the PyXX unit converter CLI.  If not
        provided or ``None``, arguments are obtained from ``sys.argv``
        (default is ``None``)
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

        Notes
        -----
        The first item in :py:attr:`sys.argv` is the script name, but this
        item should be omitted when calling :py:meth:`execute`.  In other
        words, :py:meth:`execute` should be passed an input argument ``argv``
        similar to ``sys.argv[1:]``.
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

        if command in ('info', 'i'):
            return self._info(argv)

        if command in ('search', 's'):
            return self._search(argv)

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
            ),
            add_help=False
        )

        required_args = parser.add_argument_group('Required arguments')
        optional_args = parser.add_argument_group('Optional arguments')

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

        optional_args.add_argument(
            '-h', '--help',
            action='help',
            help='Show this help message and exit'
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
            quantity = [float(x.strip()) for x in str(args.quantity).split(',')]
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

        if not (0 < exit_code <= 255):
            raise ValueError('Exit code must be in the range (0, 255]')

        if print_help:
            self.help()
            print(f'{"-" * self._LINE_LENGTH}\n')

        print(f'{self.PROGRAM_NAME}: error: {message}')

        return exit_code

    def _info(self, argv: List[str]) -> int:
        # Process command-line arguments
        parser = argparse.ArgumentParser(
            prog=f'{self.PROGRAM_NAME} info',
            description=(
                'Display detailed information about a unit in the unit '
                'converter. Refer to the PyXX documentation '
                '(https://pyxx.readthedocs.io) or use the "search" command '
                'to view a list of available units.'
            ),
            add_help=False
        )

        required_args = parser.add_argument_group('Required arguments')
        optional_args = parser.add_argument_group('Optional arguments')

        required_args.add_argument(
            'unit',
            action='store',
            type=str,
            help='The unit about which to display detailed information'
        )

        optional_args.add_argument(
            '-h', '--help',
            action='help',
            help='Show this help message and exit'
        )

        args = parser.parse_args(argv)

        # Validate inputs
        unit = str(args.unit)

        if not UnitConverterSI().is_simplified_unit(unit):
            return self._exit_with_error(
                f'Unit "{unit}" is a compound unit. Detailed information can '
                'only be shown for simple units'
            )

        if not UnitConverterSI().is_defined_unit(unit):
            close_matches = difflib.get_close_matches(
                word=unit, possibilities=list(UnitConverterSI().keys()),
                n=5, cutoff=0.6)

            return self._exit_with_error(
                f'Unit "{unit}" has not been defined in the unit converter. '
                f'The most similar available units are: {close_matches}')

        # Display unit details
        unit_entry = UnitConverterSI()[unit]

        print(f'Unit ID:          {unit}')
        print(f'Name:             {unit_entry.name}')
        print(f'Description:      {unit_entry.description}')
        print(f'Tags:             {unit_entry.tags}')
        print(f'Aliases:          {UnitConverterSI().get_aliases(unit)}')
        print(f'Unit definition:  {unit_entry.unit}')

        return 0

    def _search(self, argv: List[str]) -> int:
        # Process command-line arguments
        parser = argparse.ArgumentParser(
            prog=f'{self.PROGRAM_NAME} search',
            description=(
                'Search the list of units and associated metadata for units '
                'defined in the unit converter. Refer to the PyXX '
                'documentation (https://pyxx.readthedocs.io) to view a list '
                'of available units.'
            ),
            add_help=False
        )

        required_args = parser.add_argument_group('Required arguments')
        optional_args = parser.add_argument_group('Optional arguments')

        required_args.add_argument(
            'search_term',
            action='store',
            type=str,
            help=('Search term. Use a wildcard (\'*\' or \'**\') to match '
                  'any string')
        )

        optional_args.add_argument(
            '-h', '--help',
            action='help',
            help='Show this help message and exit'
        )
        optional_args.add_argument(
            '--search-fields',
            action='store',
            type=str,
            default='key,name,tags,description',
            help=(
                'If provided, only the specified fields in the unit converter '
                'will be searched. Available search fields are: (\'key\', '
                '\'name\', \'tags\', \'description\'). Multiple fields can be '
                'provided as a comma-separated list. The default behavior is '
                'to search all available fields'
            )
        )
        optional_args.add_argument(
            '--filter-by-tags',
            action='store',
            type=str,
            default=None,
            help=(
                'If provided, only search results with the given tag(s) will '
                'be displayed. Use a comma-separated list to filter by '
                'multiple tags'
            )
        )
        optional_args.add_argument(
            '--hide-aliases',
            action='store_true',
            help=(
                'If this flag is provided, units with multiple aliases will '
                'be shown only once in the search results (only the first '
                'alias defined will be shown)'
            )
        )

        args = parser.parse_args(argv)

        if args.filter_by_tags is None:
            filter_by_tags = None
        else:
            filter_by_tags \
                = [x.strip() for x in str(args.filter_by_tags).split(',')]

        hide_aliases = bool(args.hide_aliases)
        search_fields = [x.strip() for x in str(args.search_fields).split(',')]
        search_term = str(args.search_term)

        # Display search results
        try:
            UnitConverterSI().search(
                search_term    = search_term,
                search_fields  = search_fields,
                filter_by_tags = filter_by_tags,
                hide_aliases   = hide_aliases,
                print_results  = True,
                return_results = False
            )
        except InvalidSearchFieldError as exception:
            return self._exit_with_error(str(exception))

        return 0
