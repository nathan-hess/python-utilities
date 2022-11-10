"""Functions for converting data to an array, or converting one type of
array to another
"""

from typing import Any


def convert_to_tuple(value: Any) -> tuple:
    """Convert an input to a tuple

    Convert any input to a one-element tuple, or directly return
    the input (if it is already a tuple).

    Parameters
    ----------
    value : Any
        Value to convert to a tuple

    Returns
    -------
    tuple
        Directly returns ``value`` if it is already a tuple; otherwise,
        a one-element tuple containing ``value`` is returned

    Notes
    -----
    This function is intended to address an issue in which a value
    such as ``('value')`` is not considered a tuple (in this case,
    it would be a string), which may be unintuitive to users since
    it is in parentheses.  This function addresses this issue by
    converting any input to a tuple
    """
    return value if isinstance(value, tuple) else (value,)
