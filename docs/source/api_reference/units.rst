.. spelling:word-list::

    exps
    num


pyxx.units
==========

.. automodule:: pyxx.units

.. currentmodule:: pyxx.units

.. note::

    For more information on terminology definitions and a conceptual overview
    of units and systems of units, refer to the :ref:`section-units_concepts`
    page.


Unit Converters
---------------

These classes handle unit conversions at the "highest" level, providing a
simple-to-use interface to convert units, specified as strings.  Most of the
lower-level details of parsing units and performing unit conversions are
abstracted away from the user for simplicity.

.. inheritance-diagram:: UnitConverterEntry
    :parts: 1

|

.. autosummary::
    :toctree: ./api
    :template: ../_templates/api_reference_class_template.rst

    UnitConverterEntry


Systems of Units
----------------

The classes in this section are intended to represent a system of units, which
must be defined prior to setting up custom units or performing unit
conversions.

.. inheritance-diagram:: UnitSystem UnitSystemSI
    :parts: 1

|

.. autosummary::
    :toctree: ./api
    :template: ../_templates/api_reference_class_template.rst

    UnitSystem
    UnitSystemSI


Units
-----

The classes in this section can be used to define custom units associated with
a given system of units.

.. inheritance-diagram:: Unit UnitLinear UnitLinearSI
    :parts: 1

|

.. autosummary::
    :toctree: ./api
    :template: ../_templates/api_reference_class_template.rst

    Unit
    UnitLinear
    UnitLinearSI
    ConstantUnitMathConventions


Unit-Parsing
------------

The objects in this section can be used to parse strings containing units (such
as ``'kg/m/(s*m^2)'``), separating the component units in the string.  This is
an essential precursor to performing unit conversions with complex units.

.. autosummary::
    :toctree: ./api

    parse_unit
