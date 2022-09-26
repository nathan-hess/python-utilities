"""Code to assist in analyzing string content
"""


def str_excludes_chars(value: str, prohibited_chars: str):
    """Checks that a string does not contain any of a specified list of
    prohibited characters

    Parameters
    ----------
    value : str
        String whose contents are to be analyzed
    prohibited_chars : str
        Characters which, if found in ``value``, should result in
        the function returning ``False``

    Returns
    -------
    bool
        Returns ``True`` if none of the characters in ``prohibited_chars`` are
        found in ``value``, and ``False`` otherwise

    Examples
    --------
    >>> pyxx.strings.str_excludes_chars('abcdefg', 'xyz')
    True

    >>> pyxx.strings.str_excludes_chars('abcdefg', 'a')
    False
    """
    if not (isinstance(value, str) and isinstance(prohibited_chars, str)):
        raise TypeError('Arguments must be of type "str"')

    return len(set(value).intersection(set(prohibited_chars))) <= 0


def str_includes_only(value: str, allowed_chars: str):
    """Checks that a string contains only characters present in a specified
    set of characters

    Parameters
    ----------
    value : str
        String whose contents are to be analyzed
    allowed_chars : str
        If ``value`` contains characters that are not in ``allowed_chars``,
        the function should return ``False``

    Returns
    -------
    bool
        Returns ``True`` if ``value`` is composed of only characters found
        in ``allowed_chars``, and ``False`` otherwise
    """
    if not (isinstance(value, str) and isinstance(allowed_chars, str)):
        raise TypeError('Arguments must be of type "str"')

    return set(value).issubset(set(allowed_chars))
