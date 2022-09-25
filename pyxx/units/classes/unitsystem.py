"""This module contains classes intended to represent a system of
units (that is, a system with a set of base units from which all
other relevant units can be derived).
"""

from typing import Optional


class UnitSystem:
    """Base class representing a system of units

    This class can be used to represent a system of units with an arbitrary
    number of base units.  For more information about systems of units and
    unit conversions, refer to the :ref:`section-units_concepts` section
    of the documentation.
    """

    def __init__(self, num_base_units: int, name: Optional[str] = None,
                 description: Optional[str] = None):
        """Creates an instance of the :py:class:`UnitSystem` class

        Creates a system of units, assigning the number of base units
        (which cannot be changed later) and optionally an identifying name
        and description.

        Parameters
        ----------
        num_base_units : int
            The number of base units in the system of units
        name : str, optional
            A short, descriptive name of the system of units (default is
            ``None``)
        description : str, optional
            A description of the system of units (default is ``None``)
        """
        # Store number of base units
        if not isinstance(num_base_units, int):
            raise TypeError(
                'Argument "num_base_units" must be of type "int"')
        if num_base_units <= 0:
            raise ValueError(
                'Argument "num_base_units" must be positive')
        self._num_base_units = num_base_units

        # Store name and description
        self.name = name
        self.description = description

    def __repr__(self):
        return str(self)

    def __str__(self):
        representation = str(self.__class__)

        if self.name is not None:
            representation += f' - {self.name}'

        if self.description is not None:
            representation += f' - {self.description}'

        return representation

    @property
    def description(self):
        """A brief description of the system of units, such as a list of the
        base units or details on other relevant specifications"""
        return self._description

    @description.setter
    def description(self, description: Optional[str]):
        if not (isinstance(description, str) or description is None):
            raise TypeError('Argument "description" must be of type "str"')

        self._description = description

    @property
    def name(self):
        """A short, descriptive name identifying the system of units"""
        return self._name

    @name.setter
    def name(self, name: Optional[str]):
        if not (isinstance(name, str) or name is None):
            raise TypeError('Argument "name" must be of type "str"')

        self._name = name

    @property
    def num_base_units(self):
        """The number of base units in the system of units"""
        return self._num_base_units


class UnitSystemSI(UnitSystem):
    """Class representing the SI system of units

    Class that can be used to represent the International System of
    Units (SI).  This system of units has 7 base units, which are
    described in the "Notes" section.

    Notes
    -----
    The base units in the SI system are:

    1. Length: meter [:math:`m`]
    2. Time: second [:math:`s`]
    3. Amount of substance: mole [:math:`mol`]
    4. Electric current: ampere [:math:`A`]
    5. Temperature: Kelvin [:math:`K`]
    6. Luminous intensity: candela [:math:`cd`]
    7. Mass: kilogram [:math:`kg`]

    References
    ----------
    https://www.nist.gov/pml/weights-and-measures/metric-si/si-units
    """

    def __init__(self, name: Optional[str] = 'SI',
                 description: Optional[str] = 'International System of Units'):
        """Creates an instance of the :py:class:`UnitSystemSI` class

        Creates a system of units corresponding to the International System of
        Units (SI).  This system of units has 7 base units.

        Parameters
        ----------
        name : str, optional
            A short, descriptive name of the system of units (default is
            ``'SI'``)
        description : str, optional
            A description of the system of units (default is ``'International
            System of Units'``)
        """
        # Configure the appropriate number of base units (7) for SI
        num_base_units = 7

        # Initialize the object
        super().__init__(
            num_base_units=num_base_units,
            name=name,
            description=description
        )
