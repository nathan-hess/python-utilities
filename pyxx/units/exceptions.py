"""Customized exceptions for the :py:mod:`pyxx.units` module
"""

## UNIT-PARSING ERRORS -------------------------------------------------------
# Errors thrown when issues are encountered when parsing strings
# containing units


class InvalidUnitError(ValueError):
    """Error thrown if a unit string is not formatted in a valid way"""


class InvalidUnitMathError(TypeError):
    """Error thrown if attempting to perform invalid math operations with
    :py:class:`Unit` objects"""


class ParserMaxIterationError(InvalidUnitError):
    """Error thrown if unit parser reaches its iteration limit"""


## UNIT ARITHMETIC ERRORS ----------------------------------------------------
# Errors thrown when attempting to perform invalid unit arithmetic operations


class InvalidExponentError(InvalidUnitError):
    """Error thrown if attempting to parse a unit string and a value is
    raised to a non-numeric exponent"""


## UNIT CONVERSION ERRORS ----------------------------------------------------
# Errors thrown when issues are encountered when attempting to perform
# unit conversions


class UnitConversionError(Exception):
    """General error for issues when performing unit conversions"""


class IncompatibleUnitsError(UnitConversionError):
    """Error thrown when attempting to convert a quantity between units, but
    the units are not compatible"""
