.. include:: ../constants.rst

.. spelling:word-list::

    candela


.. _section-units_concepts:

Unit Conversion Concepts
========================

This page explains some of the important concepts and definitions used by
the unit conversion tools in |PackageNameStylized|.


Systems of Units
^^^^^^^^^^^^^^^^

On a high level, the key concept behind unit conversions is there are **systems
of units**, such as the `SI system <https://www.nist.gov/pml/owm/metric-si/si-units>`__.
Within such a system, there are a set of **base units**, defined such that every
other unit can be derived from these base units (as some combination of the base
units multiplied and/or divided by each other).

*Example:* In the `SI system <https://www.nist.gov/pml/owm/metric-si/si-units>`__,
there are seven base units:

1. Length: meter [:math:`m`]
2. Time: second [:math:`s`]
3. Amount of substance: mole [:math:`mol`]
4. Electric current: ampere [:math:`A`]
5. Temperature: Kelvin [:math:`K`]
6. Luminous intensity: candela [:math:`cd`]
7. Mass: kilogram [:math:`kg`]

These base units can be combined to obtain derived units such
as Newtons (:math:`kg*m/s^2`).

Systems of units provide a convenient means of performing **unit conversions**.
Because all units in the system are derived from the base units, it is
immediately evident whether a conversion from one unit to another is
permissible: for a unit conversion to be valid, the beginning and ending
units must both have the same combination of base units (that is, they must
both be multiplicative combinations of base units raised to the same powers).
Furthermore, since any derived unit can be related to the base units, to
convert from one unit to another, all we must do is convert the quantity to
the base units, and from there we can convert to any other unit as desired.
