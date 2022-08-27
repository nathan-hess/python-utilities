"""
This module contains functions for splitting strings.
"""


def split_at_index(value: str, index: int, return_index: bool = False):
    """Splits a string at a given index

    This function can be used to split a string at a given position,
    returning the parts of the string before and after the given index, and
    optionally returning the character located at the index at which the
    string was split.

    Parameters
    ----------
    value : str
        String to split
    index : int
        Index specifying position at which to split ``value``
    return_index : bool, optional
        Whether to include the character located at ``index`` in the tuple of
        strings returned by the function (default is ``False``)

    Returns
    -------
    tuple
        A tuple containing the portions of ``value`` before and after
        the position specified by ``index``, and possibly the value
        ``value[index]`` (see Notes section for format details)

    Notes
    -----
    Suppose that ``begin``, ``delimiter``, and ``end`` are strings, and
    that ``value = f'{begin}{delimiter}{end}'``, where ``index = len(begin)``.

    - If ``return_index = False``, the following tuple is returned:
      ``(begin, end)``
    - If If ``return_index = True``, the following tuple is returned:
      ``(begin, delimiter, end)``
    """
    # Adjust if user provides an index relative to the end of the string
    if index < 0:
        index += len(value)

    if not return_index:
        return value[:index], value[index+1:]

    return value[:index], value[index], value[index+1:]
