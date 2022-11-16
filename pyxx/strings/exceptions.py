"""Customized exceptions for the :py:mod:`pyxx.strings` module
"""


class BracketErrors(Exception):
    """Errors for the ``pyxx.strings.brackets`` module"""

class NotABracketError(BracketErrors, ValueError):
    """Error thrown if encountering a non-bracket character when
    expecting to encounter a bracket character"""

class UnmatchedBracketsError(BracketErrors, ValueError):
    """Error thrown if unmatched brackets are found in an
    unexpected context"""
