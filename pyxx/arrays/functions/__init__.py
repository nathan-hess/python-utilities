"""This module contains functions for parsing lists, tuples, and other
array-like data storage objects
"""

from .convert import convert_to_tuple
from .equality import is_array_equal
from .size import (
    check_len_equal,
    is_len_equal,
    max_list_item_len,
)
