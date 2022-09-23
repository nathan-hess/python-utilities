"""Functions for evaluating or comparing sizes of array-like objects
"""

from typing import Any, Union


def check_len_equal(item1: Any, item2: Any, *args: Any):
    """Checks whether the lengths of a set of sequence-type objects
    are equal

    Evaluates the lengths of a set of items (such as lists, tuples, or
    strings), returning whether all items have the same length as well as
    either the length of all items (if all lengths are equal) or a list
    containing the lengths of each item (if they are not equal).

    Parameters
    ----------
    item1 : Any
        First item whose length to evaluate
    item2 : Any
        Second item whose length to evaluate
    *args : Any, optional
        Any other items whose lengths are to be evaluated

    Returns
    -------
    bool
        Whether all items have the same length
    int or list
        Returns an integer containing the length of all items (if all
        lengths are equal), or a list containing the lengths of each
        item (if lengths differ)

    See Also
    --------
    is_len_equal :
        Identical functionality, but returns only the ``bool`` output and
        may theoretically run slightly faster in cases where the length(s)
        of the inputs does not need to be returned
    """
    lengths = [len(item1)] + [len(item2)] + [len(i) for i in args]

    if len(set(lengths)) == 1:
        return True, lengths[0]
    else:
        return False, lengths


def is_len_equal(item1: Any, item2: Any, *args: Any):
    """Checks whether the lengths of a set of sequence-type objects
    are equal

    Evaluates the lengths of a set of items (such as lists, tuples, or
    strings), returning whether all items have the same length.  This
    function should be slightly faster than :py:func:`check_len_equal`
    for applications where the lengths of the input arguments do not
    need to be returned.

    Parameters
    ----------
    item1 : Any
        First item whose length to evaluate
    item2 : Any
        Second item whose length to evaluate
    *args : Any, optional
        Any other items whose lengths are to be evaluated

    Returns
    -------
    bool
        Whether all items have the same length

    See Also
    --------
    check_len_equal :
        Identical functionality, but additionally returns the length of the
        input arguments
    """
    length1 = len(item1)

    for item in [item2] + list(args):
        if not len(item) == length1:
            return False

    return True


def max_list_item_len(input_list: Union[list, tuple]):
    """Finds the maximum length of any item in a list or tuple

    Parameters
    ----------
    input_list : list or tuple
        Array of items to process

    Returns
    -------
    int
        Length of item in list with maximum length
    """
    return max(list(map(len, input_list)))
