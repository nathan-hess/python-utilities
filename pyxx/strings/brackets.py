"""
This module contains functions for processing and simplifying strings
containing brackets.  It provides functionality for identifying whether
brackets in a string form matched pairs (every opening bracket has
a corresponding closing bracket, in the correct order), among other
capabilities.
"""


def contains_all_matched_brackets(value: str, opening_bracket: str = '(',
                                  closing_bracket: str = ')'):
    """Checks whether all opening brackets in a string have a
    corresponding closing bracket

    Parameters
    ----------
    value : str
        String to process
    opening_bracket : str, optional
        Character representing opening bracket (default is ``(``)
    closing_bracket : str, optional
        Character representing closing bracket (default is ``)``)

    Returns
    -------
    bool
        Returns ``True`` if for every opening bracket there is a
        single corresponding closing bracket that occurs later in
        the string, and ``False`` otherwise
    """
    # Validate inputs
    if not (isinstance(value, str)
            and isinstance(opening_bracket, str)
            and isinstance(closing_bracket, str)):
        raise TypeError(
            'Arguments "opening" and "closing" must be of type "str"')

    if (len(opening_bracket) != 1) or (len(closing_bracket) != 1):
        raise ValueError(
            'Arguments "opening" and "closing" must have length 1')

    if opening_bracket == closing_bracket:
        raise ValueError(
            'Arguments "opening" and "closing" must be different characters')

    # Parse string, checking for matched brackets
    counter = 0
    for char in value:
        if char == opening_bracket:
            counter += 1
        elif char == closing_bracket:
            counter -= 1

        # If counter is negative, this indicates that closing bracket
        # occurred before the corresponding opening bracket
        if counter < 0:
            return False

    return counter == 0
