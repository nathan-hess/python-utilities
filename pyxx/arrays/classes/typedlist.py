"""The :py:class:`TypedList` class and inherited classes are intended to
provide nearly the same functionality of a Python :py:class:`list`, with the
added requirement that all items in the list are of a specific, user-specified
type.
"""

import collections.abc
import itertools
from typing import Any

from pyxx.arrays.functions.size import max_list_item_len


class TypedList(collections.abc.MutableSequence):
    """A list whose elements must be of a specific type

    This class defines a custom version of Python's :py:class:`list` object.
    When defining the :py:class:`TypedList` instance, users are required to
    specify a type, and all items added to the list must be of this type.
    Most of the attributes and methods of the built-in :py:class:`list` object
    can be used to manage data in a :py:class:`TypedList` instance.
    """

    def __init__(self, *values: Any, list_type: type,
                 print_multiline: bool = True, multiline_padding: int = 1):
        """Creates a :py:class:`TypedList` list instance

        Creates an instance of the :py:class:`TypedList` object.  This list
        functions nearly identically to Python's built-in :py:class:`list`, but
        it requires that all items in the list be of a user-specified type.

        Parameters
        ----------
        *values : Any
            Items to add to the list when initializing the list
        list_type : type
            The required type of all items in the list
        print_multiline : bool, optional
            Whether to return a printable string representation of the list in
            multiline format (default is ``True``).  Multiline format places
            each item in the list on its own line
        multiline_padding : int, optional
            The amount of horizontal padding to place between brackets and
            list items when creating a printable string representation in
            multiline format (default is ``1``).  Only applicable if
            ``print_multiline`` is ``True``
        """
        super().__init__()

        # Define internal list to store elements
        self._data: list = []

        # Store required type of all list elements
        self._list_type = list_type

        # Set default options when displaying object representation
        self._print_multiline = print_multiline
        self._multiline_padding = multiline_padding

        # Add any provided items to the list
        for item in values:
            self.append(item)

    def __check_item_type(self, value: Any) -> None:
        """Checks whether an item is of the type required for all items
        in the list, throwing an error if it is not"""
        if not isinstance(value, self.list_type):
            raise TypeError(f'Item {value} is not of type {self.list_type}')

    def __delitem__(self, index) -> None:
        """Deletes an item at a specified index from the list"""
        del self._data[index]

    def __eq__(self, value: object) -> bool:
        """Checks whether two :py:class:`TypedList` objects are equal (same
        list item type, same length, and all elements are equal)"""
        if not isinstance(value, TypedList):
            return False

        if self.list_type is not value.list_type:
            return False

        if not len(self) == len(value):
            return False

        for i, item in enumerate(self):
            if not item == value[i]:
                return False

        return True

    def __getitem__(self, index):
        """Retrieves an item at a specified index from the list"""
        return self._data[index]

    def __len__(self):
        """Returns the number of items in the list"""
        return len(self._data)

    def __repr__(self):
        """Create a string representation illustrating the list and its
        contents"""
        if self.print_multiline:
            padding = ' ' * self.multiline_padding

            output = '['
            for i, item in enumerate(self._data):
                # If string representation of `item` has multiple lines,
                # add padding to each line
                item_formatted = str(item).replace('\n', '\n ' + padding)

                # Append each item in the list to the output string
                output += ((('\n ' if i > 0 else '')
                            + f'{padding}{str(item_formatted)},'))

            end_padding = max_list_item_len(output.split('\n')) \
                - len(output.split('\n')[-1]) + self.multiline_padding

            return output + f'{" " * end_padding}]'

        return str(self._data)

    def __setitem__(self, index, value) -> None:
        """Sets the value of items at one or more indices in the list

        Like the built-in :py:class:`list` object, this method can either set
        a single item at a single specified index, or replace a slice given by
        ``index`` with the items in an iterable specified by ``value``.
        """
        # Check input types
        if isinstance(index, int):
            self.__check_item_type(value)
        elif isinstance(index, slice) \
                and isinstance(value, collections.abc.Iterable):
            for val in value:
                self.__check_item_type(val)
        else:
            raise TypeError(
                'Incompatible index-value type combination. Either provide a '
                'single index and a single value, or a slice of indices '
                'and a corresponding iterable of values')

        # Store items in list
        self._data[index] = value

    def __str__(self):
        """Returns a string representation of the list"""
        return self.__repr__()

    def insert(self, index: int, value: Any):
        """Inserts a value at a given index in the list"""
        self.__check_item_type(value)
        self._data.insert(index, value)

    @property
    def list_type(self):
        """The required type of all items in the list"""
        return self._list_type

    @property
    def print_multiline(self):
        """Whether to display the object's string representation in
        multiline format"""
        return self._print_multiline

    @print_multiline.setter
    def print_multiline(self, print_multiline: bool):
        if not isinstance(print_multiline, bool):
            raise TypeError(
                'Argument "print_multiline" must be of type "bool"')

        self._print_multiline = print_multiline

    @property
    def multiline_padding(self):
        """The number of spaces on either side of the list of items in
        the list when displaying the list's string representation in
        multiline format"""
        return self._multiline_padding

    @multiline_padding.setter
    def multiline_padding(self, multiline_padding: int):
        if type(multiline_padding) is not int:  # pylint: disable=C0123
            raise TypeError(
                'Argument "multiline_padding" must be of type "int"')
        self._multiline_padding = multiline_padding


class TypedListWithID(TypedList):
    """A list whose elements must be of a specific type, where each class
    instance is given a unique identifier

    This class modifies the :py:class:`TypedList` class, assigning a unique
    identification number to each class instance.  This can be useful in
    tasks such as creating unique class instance names.

    Notes
    -----
    The identification number is shared by all instances of the
    :py:class:`TypedListWithID` class *and inherited classes*.  To reset
    the identifier for an inherited class, simply override the ``_id``
    iterator by defining ``_id = itertools.count(0)`` as a class variable
    for the subclass.
    """

    # Iterator that assigns a unique identification number to each
    # class instance
    _id = itertools.count(0)

    def __init__(self, *values, list_type: type,
                 print_multiline: bool = True, multiline_padding: int = 1):
        super().__init__(
            *values,
            list_type=list_type,
            print_multiline=print_multiline,
            multiline_padding=multiline_padding
        )

        # Set class instance identifier
        self.__id = next(self._id)

    @property
    def id(self):
        """A unique class instance identification number"""
        return self.__id