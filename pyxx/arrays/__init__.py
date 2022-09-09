"""**Code for processing lists, tuples, or other array-formatted data**

The :py:mod:`pyxx.arrays` module is intended to assist with processing data
stored in lists, tuples, NumPy arrays, or other matrix or tensor formats.
"""

from .functions.convert import convert_to_tuple
from .functions.equality import np_array_equal
from .functions.size import check_len_equal, max_list_item_len
