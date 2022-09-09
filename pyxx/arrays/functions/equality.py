"""Functions for evaluating equality of array-like objects
"""

import numpy as np


def np_array_equal(array1: np.ndarray, array2: np.ndarray, *args: np.ndarray,
                   tol: float = 1e-16):
    """Checks that NumPy arrays are equal within a given tolerance

    Returns ``True`` if the NumPy arrays passed as arguments are of the same
    shape and the maximum difference between their elements is less than or
    equal to ``tol``, and returns ``False`` otherwise.

    Parameters
    ----------
    array1 : np.ndarray
        First array to evaluate
    array2 : np.ndarray
        Second item to evaluate
    *args : np.ndarray, optional
        Any other arrays to be evaluated
    tol : float, optional
        Maximum difference between arrays to consider equivalent (default
        is ``1e-16``)

    Returns
    -------
    bool
        Whether ``array1``, ``array2``, ``*args`` have the same shape and
        are equal within tolerance ``tol``

    Notes
    -----
    One question that may arise is, *why is this function necessary?*  NumPy
    already offers functions like `numpy.array_equal() <https://numpy.org/doc
    /stable/reference/generated/numpy.array_equal.html>`__, `numpy.isclose()
    <https://numpy.org/doc/stable/reference/generated/numpy.isclose.html>`__,
    and `numpy.allclose() <https://numpy.org/doc/stable/reference/generated
    /numpy.allclose.html>`__.

    The main difference between these functions and :py:func:`np_array_equal`
    is that the NumPy functions mentioned will typically throw an exception
    if the array sizes being compared differ, while :py:func:`np_array_equal`
    simply returns ``False``.  Thus, this function eliminates the need to
    catch exceptions -- it simply returns ``True`` or ``False`` directly.  In
    certain cases, this can simplify code.
    """
    # Convert all inputs to Numpy arrays and create a list of all arrays
    # to be compared with `array1`
    array1 = np.array(array1)
    arrays = [np.array(array2)] + [np.array(i) for i in args]

    # Check that arrays have equal shape and are equal within tolerance `tol`
    for array in arrays:
        if not ((array1.shape == array.shape)
                and (np.max(np.abs(array - array1)) <= tol)):
            return False

    return True
