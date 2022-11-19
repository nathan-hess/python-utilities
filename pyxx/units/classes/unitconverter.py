"""This module provides a data structure in which a collection of units
belonging to a common system of units can be stored, each with a unique
identifier.  This structure also allows metadata, such as tags and a
description, to be stored.
"""

from typing import Dict, List, Optional, Tuple, Union

import numpy as np

from pyxx.arrays.classes.typedlist import TypedList
from pyxx.arrays.functions.convert import convert_to_tuple
from pyxx.units.exceptions import (
    IncompatibleUnitsError,
    UnitAlreadyDefinedError,
    UnitNotFoundError,
)
from pyxx.units.functions.parser import parse_unit
from .unit import Unit
from .unitsystem import UnitSystem


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
                 name: Optional[str] = None,
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
        name : str, optional
            A name for the unit (default is ``None``)
        description : str, optional
            A written description of the unit (default is ``None``)
        """
        self.description = description
        self.name = name
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
    def name(self) -> Union[str, None]:
        """A name by which to reference the unit"""
        return self._name

    @name.setter
    def name(self, name: Optional[str]) -> None:
        if name is None:
            self._name = None
        else:
            self._name = str(name)

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
                self._tags = TypedList(*tags, list_type=str)
            except (TypeError, ValueError) as exception:
                raise TypeError('Unable to set unit tags.  All tags must be of '
                                'type "str"') from exception

        else:
            raise TypeError('Argument "tags" is not a valid type')

        self._tags.print_multiline = False

    @property
    def unit(self) -> Unit:
        """A :py:class:`Unit` object representing the unit"""
        return self._unit

    @unit.setter
    def unit(self, unit: Unit) -> None:
        if not isinstance(unit, Unit):
            raise TypeError(f'Argument "unit" must be of type {Unit}')

        self._unit = unit


class UnitConverter(Dict[str, UnitConverterEntry]):
    """Data structure for storing units and performing unit conversions

    This class is intended to store a collection of units, and provide methods
    to convert quantities between the stored units or any valid arithmetic
    combination of stored units.  There are no limit on the number or types of
    units that can be stored; however, all units must belong to the same
    system of units.

    The :py:class:`UnitConverter` class inherits from Python's built-in
    :py:class:`dict` object, so any of the methods that are defined for a
    :py:class:`dict` should also work for :py:class:`UnitConverter` objects.

    Examples
    --------
    For examples, refer to the :ref:`section-examples_units` page.
    """

    def __init__(self, unit_system: UnitSystem):
        """Creates a new unit converter

        Creates an new :py:class:`UnitConverter` class with no units defined.

        Parameters
        ----------
        unit_system : UnitSystem
            The system of units to which all units in the unit converter must
            belong
        """
        # Validate and store inputs
        if not isinstance(unit_system, UnitSystem):
            raise TypeError('Argument "unit_system" must be an instance or '
                            f'subclass of {UnitSystem}')
        self._unit_system = unit_system

    def __getitem__(self, key: str) -> UnitConverterEntry:
        if not isinstance(key, str):
            raise TypeError('Argument "key" must be of type "str"')

        if key not in self:
            raise UnitNotFoundError(
                f'Unit "{key}" was not found in unit dictionary')

        return super().__getitem__(key)

    def __setitem__(self, key: str, value: UnitConverterEntry):
        if not isinstance(value, UnitConverterEntry):
            raise TypeError(
                f'Unit converter units must be of type {UnitConverterEntry}. '
                'Consider using the `.add_unit()` method to add units')

        # Validate `key`
        if not isinstance(key, str):
            raise TypeError(
                'Unit converter unit identifier keys must be of type "str"')

        if not self.is_simplified_unit(key):
            raise ValueError(
                f'Unit identifier key "{key}" is not a fully-simplified unit')

        # Verify that system of units of `value` matches unit dictionary
        #   This does not use `isinstance()` or else units with system of units
        #   `UnitSystem` could be converted to any other system of units
        if type(value.unit.unit_system) is not type(self.unit_system):  # noqa: E721
            raise TypeError(
                'System of units used by unit converter and new unit '
                f'differ: unit converter uses {type(self.unit_system)} '
                f'while new unit uses {type(value.unit.unit_system)}')

        super().__setitem__(key, value)

    @property
    def unit_system(self) -> UnitSystem:
        """The system of units used by all units in the unit converter"""
        return self._unit_system

    def add_unit(self, key: str, unit: Unit,
                 tags: Optional[
                     Union[TypedList[str], List[str], Tuple[str, ...], str]
                 ] = None,
                 description: Optional[str] = None,
                 overwrite: bool = False) -> None:
        """Adds a unit to the unit converter

        Adds a unit and possibly unit metadata (tags, description) to the unit
        converter, so that the unit can be used to perform later unit
        conversions.

        Parameters
        ----------
        key : str
            A short string, such as ``'kg'``, uniquely identifying the unit
        unit : Unit
            A :py:class:`Unit` object (or subclass) specifying the unit
        tags : TypedList or list or tuple or str, optional
            One or more strings containing brief, one-word descriptors to use
            to group similar units, such as "length" or "speed" (default is
            ``None``, meaning that no tags are associated with the unit)
        description : str, optional
            A written description of the unit (default is ``None``)
        overwrite : bool, optional
            Whether to overwrite units if they already exist in the unit
            dictionary (default is ``False``)
        """
        if key in self.keys() and not overwrite:
            raise UnitAlreadyDefinedError(
                f'Key "{key}" already exists. To automatically overwrite, '
                'call `.add_unit()` with `overwrite=True`')

        self[key] = UnitConverterEntry(unit=unit, tags=tags,
                                       description=description)

    def add_alias(self, key: str,
                  aliases: Union[str, List[str], Tuple[str, ...]]) -> None:
        """Add one or more aliases for a unit

        Adds alternate identifiers (keys) that may be used to identify a unit in
        simple or compound unit strings.  This method is useful for adding
        units which have multiple equivalent representations, such as "micron"
        and ":spelling:word:`μm`," to the unit converter efficiently.

        Parameters
        ----------
        key : str
            The unit identifier of a unit already in the unit converter for
            which to add an alias
        aliases : str or list or tuple
            Alternate identifiers to add to unit converter

        Warnings
        --------
        Aliased units are added to the :py:class:`UnitConverter` **by
        reference**.  Thus, if one of the aliased units is modified, all the
        other aliased units will also be updated.
        """
        for alias in convert_to_tuple(aliases):
            self[alias] = self[key]

    def convert(self, quantity: Union[np.ndarray, list, tuple, float],
                from_unit: str, to_unit: str) -> np.ndarray:
        """Converts a quantity from one unit in the :py:class:`UnitConverter`
        to another

        Converts a value or array from one unit to another, where the units
        can be either units in the unit converter, or compound units composed
        of units in the unit converter.

        Parameters
        ----------
        quantity : np.ndarray or list or tuple or float
            Value(s) to convert from ``from_unit`` to ``to_unit``
        from_unit : str
            String specifying the simple or compound unit of ``quantity``
        to_unit : str
            String specifying the simple or compound unit to which
            ``quantity`` is to be converted

        Returns
        -------
        np.ndarray
            NumPy array with the same shape as ``quantity`` containing the
            value(s) in ``quantity`` converted from ``from_unit`` to
            ``to_unit``
        """
        if not (isinstance(from_unit, str) and isinstance(to_unit, str)):
            raise TypeError(
                'Arguments "from_unit" and "to_unit" must be strings '
                'corresponding to units defined in the unit converter')

        if not self.is_convertible(from_unit, to_unit):
            raise IncompatibleUnitsError(
                f'Unable to convert quantity: units "{from_unit}" and '
                f'"{to_unit}" are not compatible')

        # Convert to `Unit` objects
        from_unit_obj = self.str_to_unit(from_unit)
        to_unit_obj = self.str_to_unit(to_unit)

        return from_unit_obj.convert(quantity, 'to', to_unit_obj)

    def is_convertible(self, unit1: str, unit2: str, *args: str):
        """Checks whether units can be converted between each other

        Checks whether two or more units are compatible and can be directly
        converted between each other.  Inputs can be strings of simple or
        compound units.  The corresponding units (or component units of
        compound units) must exist in the :py:class:`UnitConverter` before
        calling this method.

        Parameters
        ----------
        unit1 : str
            Key/identifier of the first unit to check
        unit2 : str
            Key/identifier of the second unit to check
        *args : str, optional
            Keys/identifiers of any other units to check

        Returns
        -------
        bool
            Whether all units can be converted directly between each other
        """
        unit1_unit = self.str_to_unit(unit1)
        units_to_check = [self.str_to_unit(i) for i in ([unit2] + list(args))]

        for unit in units_to_check:
            if not unit1_unit.is_convertible(unit):
                return False

        return True

    def is_simplified_unit(self, unit: str) -> bool:
        """Evaluates whether a unit is a fully-simplified unit

        Returns whether a unit is NOT a complex unit.  Fully-simplified units
        can be added to the :py:class:`UnitConverter`, but compound units
        cannot.  Note that units that are not of type :py:class:`str` or which
        are enclosed in brackets (such as ``'(m)'``) are not considered
        fully-simplified.

        Parameters
        ----------
        unit : str
            The unit to check

        Returns
        -------
        bool
            Whether ``unit`` is fully-simplified and can be added to the
            :py:class:`UnitConverter`
        """
        if not isinstance(unit, str):
            return False

        return parse_unit(unit) == {unit: 1.0}

    def str_to_unit(self, unit: str) -> Unit:
        """Converts a string to a :py:class:`Unit` object using units
        defined in the :py:class:`UnitConverter`

        Parses a string containing a simple or compound unit, converting it
        to a :py:class:`Unit` object.  All simple units and all component
        units in compound units must be defined in the unit converter prior
        to calling this method.

        Parameters
        ----------
        unit : str
            String containing the simple or compound unit to parse

        Returns
        -------
        Unit
            A :py:class:`Unit` object representation of the unit specified
            by ``unit``
        """
        parsed_unit = parse_unit(unit)

        # For special case of dimensionless units, output a constant unit
        if len(parsed_unit) == 0:
            return Unit(
                unit_system        = self.unit_system,
                base_unit_exps     = [0] * self.unit_system.num_base_units,
                to_base_function   = lambda x, exp: x,
                from_base_function = lambda x, exp: x
            )

        # Initialize output unit using one of the units in `parsed_unit`
        unit_str0, exp0 = parsed_unit.popitem()
        output_unit = (self[unit_str0].unit)**exp0

        # Add all remaining units in `parsed_unit`
        for unit_str, exp in parsed_unit.items():
            output_unit *= (self[unit_str].unit)**exp

        return output_unit
