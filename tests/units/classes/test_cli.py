import importlib
import unittest

import pyxx
from pyxx.units.classes.cli import UnitConverterCLI
from tests import CapturePrint


class Test_UnitConverterCLI(unittest.TestCase):
    def setUp(self) -> None:
        self.cli = UnitConverterCLI()

    def tearDown(self) -> None:
        importlib.reload(pyxx)

    def test_help(self):
        # Verifies that content is printed when showing the main CLI help
        with CapturePrint() as terminal_stdout:
            # Verify correct exit code
            self.assertEqual(self.cli.help(), 0)

            # Verify some help text is printed
            self.assertGreater(len(terminal_stdout.getvalue().strip()), 0)

    def test_version(self):
        # Verifies that PyXX version is displayed correctly
        with CapturePrint() as terminal_stdout:
            # Verify correct exit code
            self.assertEqual(self.cli.version(), 0)

            # Verify correct version is printed
            self.assertEqual(terminal_stdout.getvalue().strip(),
                             pyxx.__version__)
