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
    """
    return len(set(value).intersection(set(prohibited_chars))) <= 0
