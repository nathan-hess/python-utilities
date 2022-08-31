"""Functions for evaluating or comparing sizes of array-like objects"""

from typing import Union


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
