"""Customized exceptions for the :py:mod:`pyxx.units` module
"""


class InvalidUnitError(ValueError):
    """Error thrown if a unit string is not formatted in a valid way"""


class InvalidExponentError(InvalidUnitError):
    """Error thrown if attempting to parse a unit string and a value is
    raised to a non-numeric exponent"""


class InvalidUnitMathError(TypeError):
    """Error thrown if attempting to perform invalid math operations with
    :py:class:`Unit` objects"""


class ParserMaxIterationError(InvalidUnitError):
    """Error thrown if unit parser reaches its iteration limit"""
