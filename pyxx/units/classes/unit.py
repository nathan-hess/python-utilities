"""This module contains classes for representing units that are part of a
given system of units.
"""

from typing import Any, Callable, List, Optional, Tuple, Union

import numpy as np

from pyxx.arrays.functions.equality import is_array_equal
from .unitsystem import UnitSystem


# Disable Pylint's "unused argument" warnings.  In this case, we want to allow
# users to pass keyword arguments but ignore them -- this allows users to
# define different units using the same code.
#
# For instance, using the line below, if users set "myUnit" using one
# of the lines below:
#   myUnit = pyxx.units.Unit(...)
#   myUnit = pyxx.units.UnitLinearSI(...)
# However, each of these classes requires a different set of keyword
# arguments, which can cause issues if attempting to create a single line of
# code that can create an instance of either class.
#
# However, if we allow arbitrary keyword arguments (with **kwargs) in the
# `Unit` class constructors, then users can easily define different units
# using the same code:
#   unit = myUnit(unit_system=UnitSystem(1), ...)
#
# This becomes particularly useful when setting up unit converters, which need
# to be general enough to handle any type of `Unit` class.
#
# pylint: disable=unused-argument


class Unit:
    """Base class for representing a unit

    This class can be used to represent an arbitrary unit that is part
    of a given system of units.  The attributes of this class specify how
    the unit relates to the base units of the system of units.
    """

    def __init__(
            self,
            unit_system: UnitSystem,
            base_unit_exps: Union[List[float], Tuple[float, ...], np.ndarray],
            to_base_function: Callable[[np.ndarray, float], np.ndarray],
            from_base_function: Callable[[np.ndarray, float], np.ndarray],
            identifier: Optional[str] = None,
            name: Optional[str] = None,
            **kwargs: Any):
        """Creates an instance of the :py:class:`Unit` class

        Defines an object representing a base or derived unit that is part of
        a given system of units.

        Parameters
        ----------
        unit_system : pyxx.units.UnitSystem
            The system of units to which the unit belongs
        base_unit_exps : list or tuple or np.ndarray
            A 1D list of exponents relating the given object's unit to the
            base units of ``unit system``
        to_base_function : Callable
            A function that transforms a value in the given object's unit
            to the base units of ``unit_system``
        from_base_function : Callable
            A function that transforms a value in the base units of
            ``unit_system`` to the given object's unit
        identifier : str, optional
            A short identifier describing the unit (example: ``'kg'``)
            (default is ``None``)
        name : str, optional
            A name describing the unit (example: ``'kilogram'``) (default
            is ``None``)
        **kwargs : Any, optional
            Other keyword arguments (can be passed as inputs but are ignored)
        """
        # Store system of units
        if not isinstance(unit_system, UnitSystem):
            raise TypeError('Argument "unit_system" must be derived from '
                            '"pyxx.units.UnitSystem"')
        self._unit_system = unit_system

        # Store identifier and name
        if not (identifier is None or isinstance(identifier, str)):
            raise TypeError(
                'Argument "identifier" must be "None" or of type "str"')
        self._identifier = identifier

        if not (name is None or isinstance(name, str)):
            raise TypeError('Argument "name" must be "None" or of type "str"')
        self._name = name

        # Store exponents relating unit to base units
        self._base_unit_exps = np.array([float(i) for i in base_unit_exps])

        # Verify that number of base units matches that of unit system
        if len(self.base_unit_exps) != self.unit_system.num_base_units:
            raise ValueError(
                'Argument "base_unit_exps" implies '
                f'{len(self.base_unit_exps)} base units but unit '
                f'system "{self.unit_system}" has '
                f'{self.unit_system.num_base_units} base units')

        # Store functions to transform to or from base units
        self._to_base_function = to_base_function
        self._from_base_function = from_base_function

    def __repr__(self):
        return f'{self.__class__} {str(self)}'

    def __str__(self):
        representation = ''

        if self.identifier is not None:
            representation += f'{self.identifier} - '

        if self.name is not None:
            representation += f'{self.name} - '

        representation += f'{self.base_unit_exps}'

        return representation

    @property
    def base_unit_exps(self):
        """A list of exponents relating the given object's units to the
        base units of :py:attr:`unit_system`"""
        return self._base_unit_exps

    @property
    def identifier(self):
        """A user-defined string that represents the unit
        (examples: kg, m, rad)"""
        return self._identifier

    @property
    def from_base_function(self):
        """A function that transforms a value in the base units of the system
        of units :py:attr:`unit_system` to the given object's units"""
        return self._from_base_function

    @property
    def name(self):
        """A user-defined string that describes the unit
        (examples: kilogram, meter, radian)"""
        return self._name

    @property
    def to_base_function(self):
        """A function that transforms a value from the given object's units
        to the base units of :py:attr:`unit_system`"""
        return self._to_base_function

    @property
    def unit_system(self):
        """The system of units to which the unit belongs"""
        return self._unit_system

    def is_convertible(self, unit: 'Unit'):
        """Checks whether a unit can be converted to another unit

        Checks two units can be converted between each other (i.e., whether
        they belong to the same system of units and have the same
        :py:attr:`base_unit_exps` relating them to the base units).

        Parameters
        ----------
        unit : Unit
            Another :py:class:`Unit` instance

        Returns
        -------
        bool
            Returns ``True`` if this unit instance and ``unit`` belong to the
            same system of units and have the same :py:attr:`base_unit_exps`
            attribute, and ``False`` otherwise
        """
        if not (type(self.unit_system) is type(unit.unit_system)):  # noqa: E721
            return False

        return is_array_equal(self.base_unit_exps, unit.base_unit_exps)

    def from_base(self, value: Union[np.ndarray, list, tuple, float],
                  exponent: float = 1.0):
        """Converts a value or array from base units of the unit
        system to the given unit

        Parameters
        ----------
        value : np.ndarray or list or tuple or float
            Value(s) to convert to base units
        exponent : float, optional
            Exponent to which the unit is raised (default is 1.0)

        Returns
        -------
        np.ndarray
            NumPy array with the same shape as ``value`` containing the
            value(s) in ``value`` expressed in base units

        Notes
        -----
        Use the ``exponent`` argument to handle units which are raised to a
        power.  For instance, to convert square kilometers to base units
        (square meters), set ``exponent`` to 2.
        """
        inputs = np.array(value)

        return self.from_base_function(inputs, exponent)

    def to_base(self, value: Union[np.ndarray, list, tuple, float],
                exponent: float = 1.0):
        """Converts a value or array from the given unit to the base
        units of the unit system

        Parameters
        ----------
        value : np.ndarray or list or tuple or float
            Value(s) to convert from base units to the given unit
        exponent : float, optional
            Exponent to which the unit is raised (default is 1.0)

        Returns
        -------
        np.ndarray
            NumPy array with the same shape as ``value`` containing the
            value(s) in ``value`` converted from base units to the given
            unit

        Notes
        -----
        Use the ``exponent`` argument to handle units which are raised to a
        power.  For instance, to convert to cubic kilometers from cubic
        meters (the base unit), set ``exponent`` to 3.
        """
        inputs = np.array(value)

        return self.to_base_function(inputs, exponent)