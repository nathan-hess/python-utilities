"""Functions for identifying the type of numerical data

The functions in this module can assist in identifying what type of data
is represented by a numerical type.
"""

from typing import Any


def is_float(value: Any):
    """Checks whether a value is a floating-point number

    Determines whether a value can be converted to a real number and
    expressed as a Python :py:class:`float`.

    Parameters
    ----------
    value : Any
        The value to be analyzed

    Returns
    -------
    bool
        Whether ``value`` represents a floating-point number

    Examples
    --------
    Decimal numbers and integers are identified as floating-point numbers:

    >>> pyxx.numbers.is_float(3.14)
    True
    >>> pyxx.numbers.is_float(3)
    True
    >>> pyxx.numbers.is_float(2/3)
    True

    This function checks if values *can be converted to* floating-point
    numbers, so string inputs may also be classified as valid floating-point
    numbers:

    >>> pyxx.numbers.is_float('-6.28')
    True

    """
    try:
        float(value)
    except (TypeError, ValueError):
        return False

    return True


def is_integer(value: Any):
    """Checks whether a value is an integer

    Parameters
    ----------
    value : Any
        The value to be analyzed

    Returns
    -------
    bool
        Whether ``value`` represents an integer

    Examples
    --------
    Integers (of type :py:class:`int` or :py:class:`float`) are identified
    as integers:

    >>> pyxx.numbers.is_integer(3)
    True
    >>> pyxx.numbers.is_integer(3.0)
    True
    >>> pyxx.numbers.is_integer(6/3.0)
    True

    This function checks if values *can be converted to* integers, so string
    inputs may also be classified as valid integers:

    >>> pyxx.numbers.is_float('6.0')
    True

    However, floating-point numbers with a nonzero fractional part are not
    classified as valid integers:

    >>> pyxx.numbers.is_integer(0.5)
    False

    """
    return is_float(value) and float(value).is_integer()
