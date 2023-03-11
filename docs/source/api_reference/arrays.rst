.. spelling:word-list::

    args
    np
    tol


pyxx.arrays
===========

.. automodule:: pyxx.arrays

.. currentmodule:: pyxx.arrays


Type-Specific Lists
-------------------

These classes provide nearly identical functionality as a Python :py:class:`list`
but, similar to C++ ``std::vector`` objects, they additionally enforce the
requirement (albeit not as strictly as C++) that all items in the list be of
a specific type.

.. inheritance-diagram:: TypedList TypedListWithID
    :top-classes: pyxx.arrays.classes.typedlist.TypedList
    :parts: 1

|

.. autosummary::
    :toctree: ./api
    :template: ../_templates/api_reference_class_template.rst

    TypedList
    TypedListWithID


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
    :template: ../_templates/api_reference_function_template.rst

    is_array_equal


Array Size
----------

These functions can be useful when determining or comparing the sizes of
array-like objects.

.. autosummary::
    :toctree: ./api
    :template: ../_templates/api_reference_function_template.rst

    check_len_equal
    is_len_equal
    max_list_item_len
