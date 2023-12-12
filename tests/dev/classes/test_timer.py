import time
import unittest

from pyxx.dev import TimeIt
from tests import CapturePrint


class Test_TimeIt(unittest.TestCase):
    def test_duration(self):
        # Verifies that duration is measured within a reasonable range
        timer = TimeIt(print_duration=False)
        with timer:
            time.sleep(1.5)

        self.assertAlmostEqual(timer.duration(), 1.5, delta=0.1)

    def test_default_message(self):
        # Verifies that correct default message is printed after code completes
        with CapturePrint() as terminal_output:
            timer = TimeIt()
            with timer:
                time.sleep(0.1)

            self.assertEqual(
                terminal_output.getvalue(),
                f'Code duration: {timer.duration()} s\n',
            )

    def test_custom_message(self):
        # Verifies that correct custom message is printed after code completes
        with CapturePrint() as terminal_output:
            timer = TimeIt(message='Execution time: {time} {units}', units='ms')
            with timer:
                time.sleep(0.1)

            self.assertEqual(
                terminal_output.getvalue(),
                f'Execution time: {timer.duration() * 1000} ms\n',
            )

    def test_convert_duration(self):
        # Verifies that unit conversion of returned duration is performed correctly
        timer = TimeIt(print_duration=False)
        with timer:
            time.sleep(0.5)

        self.assertAlmostEqual(
            timer.duration(units='s') * 1000,
            timer.duration(units='ms'),
        )

    def test_invalid_units(self):
        # Verify that an error is raised when invalid units are specified
        with self.assertRaises(ValueError):
            with TimeIt(units='invalid'):
                pass
