"""
Customized exceptions for the ``pyxx.strings`` module
"""


class BracketErrors(Exception):
    """Errors for the ``pyxx.strings.brackets`` module"""


class NotABracketError(BracketErrors, ValueError):
    """Error thrown if encountering a non-bracket character when
    expecting to encounter a bracket character"""
