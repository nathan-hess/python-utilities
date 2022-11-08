"""This module contains classes for representing units that are part of a
given system of units.
"""

import enum
import string
from typing import Any, Callable, List, Optional, Tuple, Union

import numpy as np

from pyxx.arrays.functions.equality import is_array_equal
from pyxx.strings.functions.content import str_includes_only
from pyxx.units.exceptions import InvalidUnitMathError
from .unitsystem import UnitSystem, UnitSystemSI


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


class ConstantUnitMathConventions(enum.Enum):
    """Options for defining what happens when a :py:class:`Unit` object is
    multiplied by a constant

    When defining units, there are often cases where one unit is simply a
    multiple of another; for instance, a meter is 100 times the size of a
    centimeter, and an inch is 2.54 times the size of a centimeter.  Rather
    than defining entirely new units, it would be helpful if there was a quick
    way to generate them from existing units.

    These options provide precisely this functionality.  However, there is a
    significant complication: what convention should we take?  Should
    multiplying a unit of *meters* by 1000 result in a unit 1000 times larger
    (a *kilometer*), or should it return a unit 1000 times smaller (a
    *millimeter*, since :math:`1\\ m * \\frac{1000\\ mm}{1\\ m} = 1000\\ mm`)?

    Due to this ambiguity, by default PyXX prohibits multiplication of
    :py:class:`Unit` objects and constants.  However, by setting the
    :py:attr:`Unit.CONSTANT_MATH_CONVENTION` attribute to one of the values
    described on this page,  it is possible to override this default and
    specify the desired math convention for multiplying :py:class:`Unit`
    objects by constants.

    Warnings
    --------
    This is an advanced option.  If you are uncertain about how it functions,
    leave it set to the default value (:py:attr:`DISABLE`) -- you won't lose
    any functionality of the PyXX package; you'll only lose a minor shortcut
    intended purely for convenience.

    Notes
    -----
    In general, it is best to set this option at the beginning of your code,
    as it can get confusing if you set it later in your code and as a result
    different parts of your code follow different conventions.

    To select a math convention for multiplying :py:class:`Unit` objects by
    constants, include code similar to:

    >>> from pyxx.units import Unit, ConstantUnitMathConventions
    >>> Unit.CONSTANT_MATH_CONVENTION = ConstantUnitMathConventions.DISABLE
    """
    #: Multiplying a unit by a constant is forbidden, and any attempt to do so
    #: results in an error being thrown.
    DISABLE = enum.auto()

    #: To create a new unit, multiply or divide by a constant as if you were
    #: directly manipulating the units themselves.
    #:
    #: For example, suppose that we have already defined a unit of
    #: milliseconds ``ms`` and we want to create a new unit seconds ``s``.
    #: Since one second is 1000 times larger than a millisecond, the unit of
    #: ``s`` could be created by:
    #:
    #: .. code-block:: python
    #:
    #:     s = 1000 * ms
    UNIT_BASED = enum.auto()

    #: To create a new unit, multiply or divide by a constant as you would do
    #: if converting quantities in the respective units.
    #:
    #: For example, suppose that we have already defined a unit of
    #: milliseconds ``ms`` and we want to create a new unit seconds ``s``.
    #: Since :math:`x` milliseconds is equal to :math:`0.001x` seconds, the
    #: unit of ``s`` could be created by:
    #:
    #: .. code-block:: python
    #:
    #:     s = 0.001 * ms
    QUANTITY_BASED = enum.auto()


class Unit:
    """Base class for representing a unit

    This class can be used to represent an arbitrary unit that is part
    of a given system of units.  The attributes of this class specify how
    the unit relates to the base units of the system of units.
    """

    # Characters expected in unit names
    __unit_chars = string.ascii_letters + '_'

    #: Defines the mathematical conventions for multiplying or dividing a
    #: :py:class:`Unit` object by a constant
    #:
    #: Configures whether :py:class:`Unit` objects can be generated by
    #: multiplying or dividing another :py:class:`Unit` object by a constant,
    #: and if so what mathematical conventions are adopted.  For more detail,
    #: refer to the :py:class:`ConstantUnitMathConventions` documentation.
    #:
    #: The default is :py:attr:`ConstantUnitMathConventions.DISABLE`, which
    #: prohibits multiplying or dividing :py:class:`Unit` objects by constants.
    #:
    #: Warnings
    #: --------
    #: This is a class attribute, so changing its value for one class (such as
    #: :py:class:`UnitLinear`) will change it for ALL classes that are an
    #: instance of or inherit from :py:class:`Unit`.
    #:
    #: Notes
    #: -----
    #: To select a math convention for multiplying :py:class:`Unit` objects by
    #: constants, include code similar to:
    #:
    #: >>> from pyxx.units import Unit, ConstantUnitMathConventions
    #: >>> Unit.CONSTANT_MATH_CONVENTION = ConstantUnitMathConventions.DISABLE
    #:
    #: In general, it is best to set this option at the beginning of your code,
    #: as it can get confusing if you set it later in your code and as a result
    #: different parts of your code follow different conventions.
    CONSTANT_MATH_CONVENTION = ConstantUnitMathConventions.DISABLE

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
        unit_system : UnitSystem
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

    def __mul__(self, value: Union['Unit', float]) -> 'Unit':
        # Verify that "value" is a valid unit or can be converted to
        # a constant unit
        if isinstance(value, Unit):
            unit = value
        elif self.CONSTANT_MATH_CONVENTION == ConstantUnitMathConventions.DISABLE:
            raise InvalidUnitMathError(
                'Unable to multiply units.  Constants can only be used as an '
                'operated if "CONSTANT_MATH_CONVENTION" attribute is NOT set '
                'to "DISABLE"')
        else:
            try:
                unit = self.__create_const_unit(value)
            except (TypeError, ValueError) as exception:
                raise InvalidUnitMathError(
                    f'Unable to multiply units.  Operand {value} is not of '
                    'type "Unit" or a constant') from exception

        # Set name and identifier of output unit
        if self.identifier is None or unit.identifier is None:
            identifier = None
        else:
            identifier = f'{self.identifier}*{unit.identifier}'

        if self.name is None or unit.name is None:
            name = None
        else:
            name = f'{self.name}*{unit.name}'

        # Output units after multiplication
        return Unit(
            unit_system        = self.unit_system,
            base_unit_exps     = self.base_unit_exps + unit.base_unit_exps,
            to_base_function   = lambda x, exp:
                self.to_base_function(unit.to_base_function(x, exp), exp),
            from_base_function = lambda x, exp:
                self.from_base_function(unit.from_base_function(x, exp), exp),
            identifier         = identifier,
            name               = name
        )

    def __pow__(self, exponent: float):
        # Ensure that exponent is a number
        exponent = float(exponent)
        exponent_str = f'{exponent}' if exponent >= 0 else f'({exponent})'

        # Set name and identifier of output unit
        if self.identifier is None:
            identifier = None
        elif str_includes_only(self.identifier, self.__unit_chars):
            identifier = f'{self.identifier}^{exponent_str}'
        else:
            identifier = f'({self.identifier})^{exponent_str}'

        if self.name is None:
            name = None
        elif str_includes_only(self.name, self.__unit_chars):
            name = f'{self.name}^{exponent_str}'
        else:
            name = f'({self.name})^{exponent_str}'

        return Unit(
            unit_system        = self.unit_system,
            base_unit_exps     = exponent * self.base_unit_exps,
            to_base_function   = lambda x, exp:
                self.to_base_function(x, exp*exponent),
            from_base_function = lambda x, exp:
                self.from_base_function(x, exp*exponent),
            identifier         = identifier,
            name               = name
        )

    def __truediv__(self, value: Union['Unit', float]) -> 'Unit':
        # Verify that "value" is a valid unit or can be converted to
        # a constant unit
        if isinstance(value, Unit):
            divisor = value
        elif self.CONSTANT_MATH_CONVENTION == ConstantUnitMathConventions.DISABLE:
            raise InvalidUnitMathError(
                'Unable to multiply units.  Constants can only be used as an '
                'operated if "CONSTANT_MATH_CONVENTION" attribute is NOT set '
                'to "DISABLE"')
        else:
            try:
                divisor = self.__create_const_unit(value)
            except (TypeError, ValueError) as exception:
                raise InvalidUnitMathError(
                    f'Unable to divide units.  Operand {value} is not of '
                    'type "Unit" or a constant') from exception

        # Set name and identifier of output unit
        if self.identifier is None or divisor.identifier is None:
            identifier = None
        elif str_includes_only(divisor.identifier, self.__unit_chars):
            identifier = f'{self.identifier}/{divisor.identifier}'
        else:
            identifier = f'{self.identifier}/({divisor.identifier})'

        if self.name is None or divisor.name is None:
            name = None
        elif str_includes_only(divisor.name, self.__unit_chars):
            name = f'{self.name}/{divisor.name}'
        else:
            name = f'{self.name}/({divisor.name})'

        # Output units after division
        return Unit(
            unit_system        = self.unit_system,
            base_unit_exps     = self.base_unit_exps - divisor.base_unit_exps,
            to_base_function   = lambda x, exp:
                self.to_base_function(divisor.to_base_function(x, -exp), exp),
            from_base_function = lambda x, exp:
                self.from_base_function(divisor.from_base_function(x, -exp), exp),
            identifier         = identifier,
            name               = name
        )

    def __repr__(self):
        return f'{self.__class__} {str(self)}'

    def __rmul__(self, value: Union['Unit', float]) -> 'Unit':
        return self.__mul__(value)

    def __rtruediv__(self, value: Union['Unit', float]) -> 'Unit':
        return (self.__truediv__(value))**(-1)

    def __str__(self):
        representation = ''

        if self.identifier is not None:
            representation += f'{self.identifier} - '

        if self.name is not None:
            representation += f'{self.name} - '

        representation += f'{self.base_unit_exps}'

        return representation

    def __create_const_unit(self, value: float):
        try:
            if self.CONSTANT_MATH_CONVENTION \
                    == ConstantUnitMathConventions.UNIT_BASED:
                return Unit(
                    unit_system        = self.unit_system,
                    base_unit_exps     = [0] * self.unit_system.num_base_units,
                    to_base_function   = lambda x, exp: (float(value))**exp * x,
                    from_base_function = lambda x, exp: x / (float(value))**exp,
                    identifier         = f'{float(value)}'
                )

            if self.CONSTANT_MATH_CONVENTION \
                    == ConstantUnitMathConventions.QUANTITY_BASED:
                return Unit(
                    unit_system        = self.unit_system,
                    base_unit_exps     = [0] * self.unit_system.num_base_units,
                    to_base_function   = lambda x, exp: x / (float(value))**exp,
                    from_base_function = lambda x, exp: (float(value))**exp * x,
                    identifier         = f'{float(value)}'
                )

        except (TypeError, ValueError) as exception:
            raise TypeError(
                f'Unable to create constant unit.  Constant {value} '
                'cannot be converted to type "float"') from exception

        # Ideally, this exception should never be thrown since caller
        # functions should check that "CONSTANT_MATH_CONVENTION" before
        # trying to create a constant unit.  However, it is still included
        # here as a backup
        raise InvalidUnitMathError(  # pragma: no cover
            'Unable to create constant unit.  Attribute '
            '"CONSTANT_MATH_CONVENTION" is not set to a recognized value')

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


class UnitLinear(Unit):
    """Class for representing units with linear transformations to/from
    the base units

    Defines a unit in which the transformations to/from the base units
    of the system of units (that is, the functions given by
    :py:attr:`from_base_function` and :py:attr:`to_base_function`) are linear.
    A large portion of the units encountered in everyday use can be considered
    linear units, so this class was created to simplify defining such units.

    Notes
    -----
    To convert an array of arbitrary dimensions ``inputs`` from the given
    object's unit to the base units, the following equation is applied:

    .. code-block:: python

        outputs = (scale * inputs) + offset

    Examples
    --------
    First, create two units, one that represents *millimeters* and another
    that represents *meters*:

    >>> mm = pyxx.units.UnitLinear(
    ...          unit_system=pyxx.units.UnitSystemSI(),
    ...          base_unit_exps=[1, 0, 0, 0, 0, 0, 0],
    ...          scale=0.001, offset=0,
    ...          identifier='mm', name='millimeter'
    ... )
    >>> m = pyxx.units.UnitLinear(
    ...          unit_system=pyxx.units.UnitSystemSI(),
    ...          base_unit_exps=[1, 0, 0, 0, 0, 0, 0],
    ...          scale=1, offset=0,
    ...          identifier='m', name='meter'
    ... )

    Display the units' properties:

    >>> print(mm)
    mm - millimeter - [1. 0. 0. 0. 0. 0. 0.] - scale: 0.001 - offset: 0.0
    >>> print(m)
    m - meter - [1. 0. 0. 0. 0. 0. 0.] - scale: 1.0 - offset: 0.0

    Verify that it's possible to convert values from millimeters to meters
    and vice versa:

    >>> mm.is_convertible(m)
    True
    >>> m.is_convertible(mm)
    True

    With these units defined, we can now convert a value from millimeters
    to the base units (meters):

    >>> mm.to_base(100)
    0.1

    We can also perform conversions in cases where units are raised to an
    exponent.  For instance, this is one way to convert :math:`1\ m^2` to
    square millimeters:

    >>> mm.from_base(1, exponent=2)
    1000000.0
    """

    def __init__(
            self, unit_system: UnitSystem,
            base_unit_exps: Union[List[float], Tuple[float, ...], np.ndarray],
            scale: float,
            offset: float,
            identifier: Optional[str] = None,
            name: Optional[str] = None,
            **kwargs):
        """Creates an instance of the :py:class:`UnitLinear` class

        Defines an object representing a base or derived unit in which the
        functions converting a value to/from the base units of the system
        of units :py:attr:`unit_system` are linear functions.

        Parameters
        ----------
        unit_system : UnitSystem
            The system of units to which the unit belongs
        base_unit_exps : list or tuple or np.ndarray
            A 1D list of exponents relating the given object's unit to the
            base units of ``unit system``
        scale : float
            The multiplicative factor applied when converting from
            the given object's unit to the base units
        offset : float
            The constant value added when converting from the given
            object's unit to the base units
        identifier : str, optional
            A short identifier describing the unit (example: ``'kg'``)
            (default is ``None``)
        name : str, optional
            A name describing the unit (example: ``'kilogram'``) (default
            is ``None``)
        **kwargs : Any, optional
            Other keyword arguments (can be passed as inputs but are ignored)
        """
        # Store inputs
        if not isinstance(scale, (float, int, np.number)):
            raise TypeError('Argument "scale" must be of type "float"')
        self._scale = float(scale)

        if not isinstance(offset, (float, int, np.number)):
            raise TypeError('Argument "offset" must be of type "float"')
        self._offset = float(offset)

        # Initialize object
        super().__init__(
            unit_system        = unit_system,
            base_unit_exps     = base_unit_exps,
            to_base_function   = lambda x, exp: (scale**exp) * x + offset,
            from_base_function = lambda x, exp: (x - offset) / (scale**exp),
            identifier         = identifier,
            name               = name
        )

    def __str__(self):
        return f'{super().__str__()} - scale: {self.scale} - offset: {self.offset}'

    @property
    def offset(self):
        """The constant value added when converting from the given
        object's unit to the base units"""
        return self._offset

    @property
    def scale(self):
        """The multiplicative factor applied when converting from
        the given object's unit to the base units"""
        return self._scale


class UnitLinearSI(UnitLinear):
    """Class for representing units with linear transformations to/from
    the base units and using the International System of Units (SI)

    This class is very similar to :py:class:`UnitLinear`, with the
    addition that the system of units is automatically set to SI.

    See Also
    --------
    UnitLinear :
        Nearly identical class, but additionally allows users to specify
        an arbitrary system of units
    """

    def __init__(
            self,
            base_unit_exps: Union[List[float], Tuple[float, ...], np.ndarray],
            scale: float,
            offset: float,
            identifier: Optional[str] = None,
            name: Optional[str] = None,
            **kwargs):
        """Creates an instance of the :py:class:`UnitLinearSI` class

        Defines an object representing a base or derived unit in which the
        functions converting a value to/from the base units of the system
        of units :py:attr:`unit_system` are linear functions, and the unit
        belongs to the SI system of units.

        Parameters
        ----------
        base_unit_exps : list or tuple or np.ndarray
            A 1D list of exponents relating the given object's unit to the
            base units of ``unit system``
        scale : float
            The multiplicative factor applied when converting from
            the given object's unit to the base units
        offset : float
            The constant value added when converting from the given
            object's unit to the base units
        identifier : str, optional
            A short identifier describing the unit (example: ``'kg'``)
            (default is ``None``)
        name : str, optional
            A name describing the unit (example: ``'kilogram'``) (default
            is ``None``)
        **kwargs : Any, optional
            Other keyword arguments (can be passed as inputs but are ignored)
        """
        super().__init__(
            unit_system    = UnitSystemSI(),
            base_unit_exps = base_unit_exps,
            scale          = scale,
            offset         = offset,
            identifier     = identifier,
            name           = name
        )
