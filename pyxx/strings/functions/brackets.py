"""
This module contains functions for processing and simplifying strings
containing brackets.  It provides functionality for identifying whether
brackets in a string form matched pairs (every opening bracket has
a corresponding closing bracket, in the correct order), among other
capabilities.
"""

from typing import Union

from pyxx.strings.exceptions import (
    NotABracketError,
    UnmatchedBracketsError,
)


def _check_valid_brackets(opening_bracket: str, closing_bracket: str,
                          opening_bracket_name: str = 'opening_bracket',
                          closing_bracket_name: str = 'closing_bracket'):
    """Checks that a given set of opening and closing brackets form a
    valid pair

    Verifies that a given pair of opening and closing brackets are a
    valid choice for the PyXX bracket-matching algorithm.  To meet this
    criterion, brackets must be strings of a single character in length,
    and the opening and closing bracket must be different.

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
    # `begin` index specifies an opening or closing bracket
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


def find_skip_brackets(value: str, target_chars: Union[str, tuple],
                       begin: int, direction: str = 'forward',
                       opening_bracket: str = '(', closing_bracket: str = ')'):
    """Finds the index of a target character, skipping over matched brackets

    This function is useful for finding the index of a particular character
    in a string, ignoring content inside of matched brackets.  It begins
    at a given index in a string and searches until any of a given set of
    target character(s) are found.  If an opening or closing bracket is
    reached, the function skips to the corresponding matched bracket before
    resuming the search (i.e., content inside of matched brackets is not
    searched).

    Parameters
    ----------
    value : str
        String to search
    target_chars : str or tuple
        A string or tuple with one or more characters to search for
    begin : int
        Index in ``value`` at which to begin searching
    direction : str, optional
        Whether to search ``value`` in order of increasing or decreasing
        index.  Can be either ``'forward'`` or ``'reverse'`` (default
        is ``'forward'``)
    opening_bracket : str, optional
        Character representing opening bracket (default is ``'('``)
    closing_bracket : str, optional
        Character representing closing bracket (default is ``')'``)

    Returns
    -------
    int
        The index of the first occurrence of any characters in ``target_chars``
        found in ``value``, beginning the search at index ``begin`` and
        searching in the direction specified by ``direction`` and ignoring
        content inside of matched brackets.  If none of ``target_chars``
        are found, ``-1`` is returned

    Notes
    -----
    When searching, the function will not "enter" matched brackets; however,
    if the index specified by ``begin`` is inside a set of brackets, the
    function will search inside of these brackets and can "leave" these
    brackets and search in parts of the string outside these brackets
    """
    # Verify that "value" argument is a string
    if not isinstance(value, str):
        raise TypeError('Argument "value" must be of type "str"')

    # Verify that "begin" is a valid index for the given string
    if not (-len(value) <= begin <= len(value) - 1):
        raise IndexError(
            f'Index {begin} at which to begin search is not valid for '
            f'string "{value}" (length {len(value)})')

    # Adjust if user provides an index relative to the end of the string
    i = begin + len(value) if begin < 0 else begin

    # Set increment by which to advance to next character when
    # searching string
    if direction not in ('forward', 'reverse'):
        raise ValueError('Argument "direction" must be one of: '
                         '"forward" or "reverse"')

    k = 1 if direction == 'forward' else -1

    # Verify that "value" argument doesn't have unmatched brackets
    if not contains_all_matched_brackets(value, opening_bracket,
                                         closing_bracket):
        raise UnmatchedBracketsError(
            'Argument "value" contains unmatched brackets')

    while 0 <= i < len(value):
        # Check whether target character has been found
        if value[i] in target_chars:
            return i

        # Check whether an opening or closing bracket has been
        # found; if so, move to the end of the matched pair
        if any(((direction == 'forward' and value[i] == opening_bracket),
                (direction == 'reverse' and value[i] == closing_bracket))):

            if (i := find_matching_bracket(
                    value, i, opening_bracket, closing_bracket)) == -1:

                # This error should never be thrown since the string was
                # previously check for matching brackets; however, it's
                # included as an added precaution
                raise UnmatchedBracketsError(
                    f'Unmatched brackets found in string "{value}"')

        # Advance to next character in string
        i += k

    return -1


def strip_matched_brackets(value: str, max_pairs: int = -1, strip: bool = True,
                           return_num_pairs_removed: bool = False,
                           opening_bracket: str = '(', closing_bracket: str = ')'):
    """Remove matched leading/trailing brackets from strings

    Removes matched brackets from a string (i.e., if a string begins with
    ``opening_bracket`` and the corresponding closing bracket
    ``closing_bracket`` is the last character in the string, the brackets
    are removed), as well as (optionally) any leading and/or trailing
    whitespace.

    Parameters
    ----------
    value : str
        String from which to remove matched brackets and leading/trailing
        whitespace (if ``strip`` is ``True``)
    max_pairs : int, optional
        Maximum pairs of matched brackets to remove.  Set to ``-1`` to
        remove an unlimited number of matched brackets (default is ``-1``)
    strip : bool, optional
        Whether to remove leading and/or trailing whitespace when processing
        ``value`` (default is ``True``)
    return_num_pairs_removed : bool, optional
        Whether to return the number of pairs of brackets that were removed
        (default is ``False``)

    Returns
    -------
    str
        Input string ``value`` with matched brackets removed
    int
        The number of pairs of matched brackets that were removed (returned
        if and only if ``return_num_pairs_removed`` is ``True``)

    Notes
    -----
    If ``strip`` is set to ``False``, then matched brackets are removed if and
    only if the first character in ``value`` is ``opening_bracket`` and the
    last character is ``closing_bracket`` and they form a matching pair
    """
    value = value.strip() if strip else value

    num_removed = 0
    while (value.startswith(opening_bracket) and value.endswith(closing_bracket)):
        # If the maximum number of pairs of brackets have been
        # removed, exit the loop
        if num_removed >= max_pairs >= 0:
            break

        # Only remove leading and trailing brackets if they form
        # a matching pair
        if find_matching_bracket(value, -1,
                                 opening_bracket=opening_bracket,
                                 closing_bracket=closing_bracket) == 0:
            value = value[1:-1].strip() if strip else value[1:-1]
            num_removed += 1
        else:
            break

    # Output results
    if not return_num_pairs_removed:
        return value

    return value, num_removed
