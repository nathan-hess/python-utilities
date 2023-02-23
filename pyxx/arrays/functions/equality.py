"""Functions for evaluating equality of array-like objects
"""

from __future__ import annotations
from numbers import Number
from typing import List, Tuple, Union

import numpy as np

from .size import is_len_equal


# Type alias: type for each `item` argument in `is_array_equal()`
__element_types = Union[Number, np.ndarray, str]
Array_or_Number_or_String = Union[List[__element_types],
                                  Tuple[__element_types],
                                  __element_types]


def is_array_equal(item1: Array_or_Number_or_String,
                   item2: Array_or_Number_or_String,
                   *args: Array_or_Number_or_String,
                   tol: float = 1e-16) -> bool:
    """Checks that arrays are equal in shape and content

    Returns ``True`` if all arrays passed as arguments are of the same shape
    and all elements are equal within a given tolerance ``tol`` (for numeric
    elements) or exactly equal (for string elements), and returns ``False``
    otherwise.  Inputs can be lists, tuples, NumPy arrays, numbers, strings,
    or nested arrays composed of any of these types.

    Parameters
    ----------
    item1 : list or tuple or np.ndarray or Number or str
        First array to evaluate
    item2 : list or tuple or np.ndarray or Number or str
        Second item to evaluate
    *args : list or tuple or np.ndarray or Number or str, optional
        Any other arrays to be evaluated
    tol : float, optional
        Maximum difference between numeric values to consider equivalent
        (default is ``1e-16``)

    Returns
    -------
    bool
        Whether ``item1``, ``item2``, ``*args`` have the same shape, and
        all elements are equal within tolerance ``tol`` (for numeric elements)
        and exactly equal (for string elements)

    Warnings
    --------
    - The shape of the input arrays must be identical for the arrays to be
      considered equal.  The shape of numbers is considered different from the
      shape of lists, so observe that ``0`` and ``[0]`` are **not** considered
      equal in shape.

    - By default, NumPy arrays are of homogeneous type.  This means that, for
      instance, ``pyxx.arrays.is_array_equal(np.array([1, 'a']), [1, 'a'])``
      evaluates to ``False`` (because the NumPy array is converted to all
      strings).  To avoid this issue, it is possible to create NumPy arrays
      with the ``dtype=object`` argument and allow mixed types.  For example,
      ``pyxx.arrays.is_array_equal(np.array([1, 'a'], dtype=object), [1, 'a'])``
      evaluates to ``True``.

    Notes
    -----
    **Recursion Limit**

    Internally, :py:func:`is_array_equal` is a recursive function.  It is
    possible that for extremely large nested arrays, Python's recursion limit
    may be reached.  If this occurs and it is necessary to compare such a
    large array, consider increasing the recursion limit using
    the `sys.setrecursionlimit() <https://docs.python.org/3/library/sys.html
    #sys.setrecursionlimit>`__ function.

    **Purpose**

    One question that may arise is, *why is this function necessary?*  NumPy
    already offers functions like `numpy.array_equal() <https://numpy.org/doc
    /stable/reference/generated/numpy.array_equal.html>`__, `numpy.isclose()
    <https://numpy.org/doc/stable/reference/generated/numpy.isclose.html>`__,
    and `numpy.allclose() <https://numpy.org/doc/stable/reference/generated
    /numpy.allclose.html>`__.

    There are several main advantages of :py:func:`is_array_equal`:

    - NumPy requires that arrays are numeric and are not "ragged" (sub-lists
      must all have the same length, recursively. For example, the array
      ``x = [[1,2,3], [1,2]]`` is "ragged" since ``len(x[0]) != len(x[1])``).
      In contrast, :py:func:`is_array_equal` can compare arrays with a mix of
      strings, numbers, lists, and tuples, as well as "ragged" arrays.

    - The NumPy functions mentioned will typically throw an exception if the
      array sizes being compared differ, but :py:func:`is_array_equal` simply
      returns ``False`` in this case.  This can eliminate the need to catch
      exceptions for certain applications.
    """
    # Create list of array(s) to compare with `item1`
    items = [item2] + list(args)

    # Check whether each of the input arguments is an array-like object
    is_array = [isinstance(x, (list, tuple, np.ndarray))
                for x in [item1, *items]]

    # If inputs are numbers, directly compare them (requiring difference
    # between numbers to be less than or equal to `tol` to consider the
    # inputs equal)
    if isinstance(item1, Number) \
            or (isinstance(item1, np.ndarray) and item1.ndim == 0):
        for x in items:
            # Check whether `item2` or any of `args` are an array.  If so,
            # this indicates that the array shapes are not equal
            if isinstance(x, (list, tuple)) \
                    or (isinstance(x, np.ndarray) and x.ndim > 0):
                return False

            # Argument `item1` is known to be a number, so attempt to see
            # whether each corresponding element in the other input arrays
            # is within tolerance `tol`
            try:
                # Disable Mypy warnings on the following line, since errors
                # will be handled with the try statement
                if abs(x - item1) > tol:  # type: ignore
                    return False

            except TypeError:
                return False

        return True

    # If inputs are array-like objects, compare their contents
    if any(is_array):
        # Verify that inputs are array-like objects
        if not all(is_array):
            return False

        # Verify that all inputs have equal length
        if not is_len_equal(item1, *items):
            return False

        # Check whether each sub-array's elements are equal (recursively)
        for i, x in enumerate(item1):

            # Disable Mypy warnings on the following line, since we've
            # already checked that the lengths of `x` and all elements
            # in `items` are equal
            if not is_array_equal(x, *[item[i] for item in items],  # type: ignore
                                  tol=tol):
                return False

        return True

    # Inputs are not numbers or array-like objects, so try to directly
    # compare them.  This allows strings, user-defined classes/types,
    # or other objects to be compared
    for x in items:
        if item1 != x:
            return False
    return True
