"""This module provides a data structure in which a collection of units
belonging to a common system of units can be stored, each with a unique
identifier.  This structure also allows metadata, such as tags and a
description, to be stored.
"""

from typing import List, Optional, Tuple, Union

from pyxx.arrays.classes.typedlist import TypedList
from .unit import Unit


class UnitConverterEntry:
    """Data structure for storing information about a unit in a unit
    converter

    The :py:class:`UnitConverterEntry` is designed to be used in combination
    with a :py:class:`UnitConverter` object.  A :py:class:`UnitConverterEntry`
    object stores data about a particular unit, allowing such information to
    be grouped and changes to the data validated.  Many such objects are
    stored in in a :py:class:`UnitConverter`, allowing it to relate and perform
    conversions between different units, while the "lower-level" details of
    managing unit data are handled by :py:class:`UnitConverterEntry`.
    """

    def __init__(self, unit: Unit,
                 tags: Optional[
                     Union[TypedList[str], List[str], Tuple[str, ...], str]
                 ] = None,
                 description: Optional[str] = None) -> None:
        """Creates a :py:class:`UnitConverterEntry` to store data about a
        particular unit

        Parameters
        ----------
        unit : Unit
            A :py:class:`Unit` object describing the unit
        tags : TypedList or list or tuple or str, optional
            One or more strings containing brief, one-word descriptors to use
            to group similar units, such as "length" or "speed" (default is
            ``None``, meaning that no tags are associated with the unit)
        description : str, optional
            A written description of the unit (default is ``None``)
        """
        self.description = description
        self.tags = tags  # type: ignore
                          # (workaround for python/mypy#3004)  # noqa: E114, E116
        self.unit = unit

    @property
    def description(self) -> Union[str, None]:
        """A description of the unit"""
        return self._description

    @description.setter
    def description(self, description: Optional[str]) -> None:
        if description is None:
            self._description = None
        else:
            self._description = str(description)

    @property
    def tags(self) -> TypedList[str]:
        """Tags that associate the unit with various categories or groups"""
        return self._tags

    @tags.setter
    def tags(self,
             tags: Optional[
                 Union[TypedList[str], List[str], Tuple[str, ...], str]
             ]) -> None:

        if isinstance(tags, TypedList) and (tags.list_type is str):
            self._tags = tags

        elif tags is None:
            self._tags = TypedList(list_type=str)

        elif isinstance(tags, str):
            self._tags = TypedList(tags, list_type=str)

        elif isinstance(tags, (list, tuple)):
            try:
                self._tags = TypedList(*tags, list_type=str, print_multiline=False)
            except (TypeError, ValueError) as exception:
                raise TypeError('Unable to set unit tags.  All tags must be of '
                                'type "str"') from exception

        else:
            raise TypeError('Argument "tags" is not a valid type')

    @property
    def unit(self) -> Unit:
        """A :py:class:`Unit` object representing the unit"""
        return self._unit

    @unit.setter
    def unit(self, unit: Unit) -> None:
        if not isinstance(unit, Unit):
            raise TypeError(f'Argument "unit" must be of type {Unit}')

        self._unit = unit
