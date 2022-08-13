"""
This module contains functions for processing and simplifying strings
containing brackets.  It provides functionality for identifying whether
brackets in a string form matched pairs (every opening bracket has
a corresponding closing bracket, in the correct order), among other
capabilities.
"""


def _check_valid_brackets(opening_bracket: str, closing_bracket: str,
                          opening_bracket_name: str = 'opening_bracket',
                          closing_bracket_name: str = 'closing_bracket'):
    """Checks that a given set of opening and closing brackets form a
    valid pair

    Verifies that a given pair of opening and closing brackets are a
    valid choice for the PyXX bracket-matching algorithm.  To meet this
    criterion, brackets must be strings of a single character in length,
    and the opening and closing bracket must be different

    Parameters
    ----------
    opening_bracket : str
        Character representing opening bracket
    closing_bracket : str
        Character representing closing bracket
    opening_bracket_name : str, optional
        Name that should be used to refer to the ``opening_bracket`` argument
        in error messages (default is ``'opening_bracket'``)
    closing_bracket_name : str, optional
        Name that should be used to refer to the ``closing_bracket`` argument
        in error messages (default is ``'closing_bracket'``)

    Returns
    -------
    bool
        Whether ``opening_bracket`` and ``closing_bracket`` form a valid pair
        of brackets

    Raises
    ------
    TypeError
        If either ``opening_bracket`` or ``closing_bracket`` are not of
        type "str"
    ValueError
        If either ``opening_bracket`` or ``closing_bracket`` don't have length
        1, or if ``opening_bracket`` and ``closing_bracket`` are identical
    """
    if not (isinstance(opening_bracket, str)
            and isinstance(closing_bracket, str)):
        raise TypeError(f'Arguments "{opening_bracket_name}" and '
                        f'"{closing_bracket_name}" must be of type "str"')

    if (len(opening_bracket) != 1) or (len(closing_bracket) != 1):
        raise ValueError(f'Arguments "{opening_bracket_name}" and '
                         f'"{closing_bracket_name}" must have length 1')

    if opening_bracket == closing_bracket:
        raise ValueError(f'Arguments "{opening_bracket_name}" and '
                         f'"{closing_bracket_name}" must be different '
                         'characters')

    return True


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
    if not (isinstance(value, str)):
        raise TypeError('Argument "value" must be of type "str"')

    _check_valid_brackets(opening_bracket, closing_bracket)

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
