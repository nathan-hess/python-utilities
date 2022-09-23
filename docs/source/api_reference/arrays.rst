.. spelling:word-list::

    args
    np
    tol


pyxx.arrays
===========

.. automodule:: pyxx.arrays

.. currentmodule:: pyxx.arrays


Array Conversion
----------------

The functions in this section can be used to convert values to an array, or to
convert one or more arrays of one type to a different type.

.. autosummary::
    :toctree: ./api

    convert_to_tuple


Array Equality
--------------

The functions in this section are intended to check whether arrays have equal
size and/or content.

.. autosummary::
    :toctree: ./api
    :template: ../_templates/api_reference_arrays_equality.rst

    np_array_equal


Array Size
----------

These functions can be useful when determining or comparing the sizes of
array-like objects.

.. autosummary::
    :toctree: ./api
    :template: ../_templates/api_reference_arrays_size.rst

    check_len_equal
    is_len_equal
    max_list_item_len
