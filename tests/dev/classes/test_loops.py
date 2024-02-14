import signal
import unittest

from pyxx.dev import InterruptibleLoop


class Test_InterruptibleLoop(unittest.TestCase):
    def test_interrupted_attribute(self):
        # Verifies that the `InterruptibleLoop.interrupted` attribute
        # changes when Ctrl+c is pressed
        with InterruptibleLoop() as loop:
            self.assertFalse(loop.interrupted)

            signal.raise_signal(signal.SIGINT)
            self.assertTrue(loop.interrupted)

    def test_restore_handler(self):
        # Verifies that the `InterruptibleLoop` class restores the
        # original SIGINT handler when the context manager exits
        sigint_handler = signal.getsignal(signal.SIGINT)

        self.assertIs(signal.getsignal(signal.SIGINT), sigint_handler)

        with InterruptibleLoop():
            self.assertIsNot(signal.getsignal(signal.SIGINT), sigint_handler)

        self.assertIs(signal.getsignal(signal.SIGINT), sigint_handler)

    def test_throw_exception(self):
        # Verifies that an exception is thrown when pressing Ctrl+c
        # if the `throw_exception` option is set to `True`
        with InterruptibleLoop(throw_exception=True):
            with self.assertRaises(InterruptedError):
                signal.raise_signal(signal.SIGINT)
