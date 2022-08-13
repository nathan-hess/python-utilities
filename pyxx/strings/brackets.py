"""
This module contains functions for processing and simplifying strings
containing brackets.  It provides functionality for identifying whether
brackets in a string form matched pairs (every opening bracket has
a corresponding closing bracket, in the correct order), among other
capabilities.
"""

from .exceptions import (
    NotABracketError,
)


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
        Character representing opening bracket (default is ``'('``)
    closing_bracket : str, optional
        Character representing closing bracket (default is ``')'``)

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


def find_matching_bracket(value: str, begin: int, opening_bracket: str = '(',
                          closing_bracket: str = ')'):
    """Finds the index of the bracket that forms a matched pair with another
    bracket at a given index

    Finds the "other bracket" that forms a closed pair of matched brackets in
    a string ``value``, beginning from the bracket at index ``begin``. Note
    that if the character at index ``begin`` is an opening bracket, then
    ``value`` is searched in the forward direction (left to right); while if
    it is a closing bracket, then the search direction is reversed (right to
    left).

    Parameters
    ----------
    value : str
        String to search for matching brackets
    begin : int
        Index in ``value`` where one of the brackets in the matched
        pair is found
    opening_bracket : str, optional
        Character representing opening bracket (default is ``'('``)
    closing_bracket : str, optional
        Character representing closing bracket (default is ``')'``)

    Returns
    -------
    int
        Returns the index of the matching bracket, or ``-1`` if the
        bracket at index ``begin`` in ``value`` does not have a
        matching bracket in ``value``

    Raises
    ------
    ValueError
        If the character at index ``begin`` in ``value`` is not one of:
        ``opening_bracket`` or ``closing_bracket``
    """
    # Adjust if user provides an index relative to the end of the string
    if begin < 0:
        begin += len(value)

    # Define search direction and ending index depending on whether the
    # `begin` index specifies and opening or closing parenthesis
    begin_char = value[begin]

    if begin_char == opening_bracket:
        k = 1
        end = len(value)
    elif begin_char == closing_bracket:
        k = -1
        end = -1
    else:
        raise NotABracketError(
            f'Character at index {begin} of "{value}" is "{begin_char}", '
            'which is not an opening or closing bracket')

    # Search string to find the matching bracket
    counter = 0
    for i in range(begin, end, k):
        if value[i] == opening_bracket:
            counter += 1
        elif value[i] == closing_bracket:
            counter -= 1

        # The first time `counter` returns to zero, the matching
        # bracket has been found
        if counter == 0:
            return i

    return -1
