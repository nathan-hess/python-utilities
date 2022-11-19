.. include:: ../../constants.rst

.. spelling:word-list::

    candela


.. _section-units_concepts:

Unit Conversion Concepts
========================

This page explains some of the important concepts and definitions used by
the unit conversion tools in |PackageNameStylized|.


Systems of Units
----------------

On a high level, the key concept behind unit conversions is there are **systems
of units**, such as the `SI system <https://www.nist.gov/pml/owm/metric-si/si-units>`__.
Within such a system, there are a set of **base units**, defined such that every
other unit can be derived from these base units (as some combination of the base
units multiplied and/or divided by each other).

.. _si_base_units:

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


Units
-----

A **unit** is a measure of quantity that belongs to a system of units and can
be related to the base units in two ways: (1) the unit can be written as a
multiplicative combination of the base units, raised to given powers, and
(2) there must be a deterministic function relating a quantity in the given
unit to the equivalent quantity expressed in exclusively base units (and a
corresponding "inverse" function relating a quantity in exclusively base units
to the given unit).

This definition immediately follows from an understanding of a system of
units.  As explained previously, a system of units consists of a set of base
units and derived units, where all derived units can be written in terms of
the base units.  The definition of a unit in the previous paragraph is the
a general expression of this system: by expressing a unit as an arbitrary
multiplicative combination of base units and defining arbitrary, deterministic
functions to convert to and from the base units, this guarantees that every
unit in the system of units is either a base unit or is related to the base
units in a deterministic way, satisfying the requirements of a system of units.

For concrete examples of the syntax used to define units using the
|PackageNameStylized| package, refer to the :ref:`section-examples_units` page.


"Linear" Units
^^^^^^^^^^^^^^

Many of the units encountered in everyday life permit a significant simplification
to the previous definition of units.  These units, which are referred to as
**"linear" units** in the |PackageNameStylized| package code and documentation, are
units in which the functions relating quantities in the given unit to quantities
expressed exclusively in base units are linear functions.

To provide a few examples:

- Millimeters are related to the base unit (meters) by multiplying by a factor
  of :math:`\frac{1000\ mm}{1\ m}`.  This is a linear function.
- Temperature in degrees Fahrenheit (:math:`^\circ F`) is related to the
  temperature in degrees Celsius (:math:`^\circ C`) by the linear function
  :math:`^\circ F = \frac{9}{5} * ^\circ C + 32`.

Note that the definition of "linear" and "nonlinear" units in |PackageNameStylized|
differs slightly from other sources.  For instance, GNU refers to "linear" units
as units that are proportional to the base unit (`documentation <https://www.gnu.org/
software/units/manual/html_node/Defining-Nonlinear-Units.html>`__); that is, there
is no "offset" allowed.  However, many common units (such as :math:`^\circ F`, gauge
pressure, etc.) include an "offset," so the definition used in |PackageNameStylized|
was selected to be as general as possible and match these common use cases.


Relationship Between Units and Systems of Units
-----------------------------------------------

One implication of the aforementioned definition of a unit is that it is
possible to consider a unit a purely mathematical quantity, with no connection
to the physical meaning of the unit.

Since each system of units has a finite, defined number of base units, we can
relate any derived unit to the base units with a list of exponents; that is,
the exponents to which each base unit are raised to form the derived unit.  In
the |PackageNameStylized| code, these are are given by the
:py:attr:`pyxx.units.Unit.base_unit_exps` property.  Likewise, by imposing a
convention for what the base units are, we can define functions to convert any
derived unit to or from base the units (these functions are referred to in
the code using the :py:attr:`pyxx.units.Unit.to_base_function` and
:py:attr:`pyxx.units.Unit.from_base_function` properties, respectively).

For instance, consider the SI system of units, which has seven base units.  As
a few examples, using the order of base units :ref:`above <si_base_units>`, we
could define:

- Meters (:math:`m`):

  - ``base_unit_exps = [1, 0, 0, 0, 0, 0, 0]`` (since :math:`m = m^1 s^0 mol^0 A^0 K^0 cd^0 kg^0`)
  - ``to_base_function`` and ``from_base_function`` are identity functions (since
    meters are already a base unit)

- Kilonewtons (:math:`kN`, where :math:`1\ kN = 1000\ N`):

  - ``base_unit_exps = [1, -2, 0, 0, 0, 0, 1]`` (since :math:`N = kg*m/s^2 = m^1 s^{-2} mol^0 A^0 K^0 cd^0 kg^1`)
  - ``to_base_function`` and ``from_base_function`` are defined such that any
    value in :math:`kN` is 1000 times smaller than the value in base units

Importantly, *notice that this definition of units assigns no physical meaning
to a unit itself*.  A meter is simply identified by ``[1, 0, 0, 0, 0, 0, 0]``,
but we have no concept of what it means (is it a length, measure of time,
etc.?).  Likewise, we may not know what a kilonewton means physically, but
from a mathematical perspective, we know that it is derived from a combination
of meters, seconds, and kilograms, each raised to particular exponents, and we
know that :math:`1\ kN` is 1000 times larger than a quantity expressed in all
base units (:math:`1\ N`).

In fact, this definition affords a significant degree of flexibility to users.
For instance, the order of units in ``base_unit_exps`` can be easily switched;
if we wanted define a system of units similar to SI but with :math:`s` and
:math:`kg` swapped relative to the example :ref:`above <si_base_units>`, we could
do so, and the only change we'd need to make is to define units such as
:math:`kN` using ``base_unit_exps = [1, 1, 0, 0, 0, 0, -2]``.  Likewise, if
we wanted consider :math:`mm` a base unit instead of :math:`m`, we would simply
need to change the definitions of ``to_base_function`` and ``from_base_function``,
but otherwise all unit-related math operations would remain the same.

Mathematically, the advantage of such a generic definition is that once the
``base_unit_exps``, ``to_base_function``, and ``from_base_function`` properties
are defined, all unit operations, such as unit conversions and `dimensional analysis
<https://en.wikipedia.org/wiki/Dimensional_analysis>`__, can be performed using
the same algorithms.  Thus, users have the flexibility to define arbitrary units
in any system of units they wish, and as long as they manage the conventions
correctly, |PackageNameStylized| will be able to handle (behind-the-scenes) the
complications of unit arithmetic, dimensional analysis, and unit conversions.
This provides a high degree of flexibility and ability for end users to
customize the system to their needs.


Unit Conversions
----------------

Based on the framework we have defined, unit conversions are relatively
straightforward.

To perform a unit conversion, we must first make sure that the units we are
converting to and from are **"compatible"**.  Units must satisfy two criteria
to be considered "compatible."  First, *the units must belong to the same
system of units*.  This requirement implies that the units share the same
base units, and the order of the base units in ``base_unit_exps`` is identical.
Second, *the units must have the same* ``base_unit_exps``.  Based on the
previously-discussed definition of units, two units with the same
``base_unit_exps`` describe the same physical measure, so it should be possible
to convert quantities between them.

Note that there are some important physical exceptions to these rules; in
particular, cases when the same units are used to describe two quantities which
are different physically in some *conceptual* way.  For example, both energy
and torque have the same ``base_unit_exps`` (since both can be described in
units of :math:`N*m`), but it is not necessarily valid to convert quantities
between energy and torque.  However, these are *conceptual* differences, so it
is the responsibility of the user to understand such unit *interpretations* when
using units.

Regardless, after confirming that two units are compatible and a unit
conversion can be performed between them, it is relatively easy to **perform
the unit conversion**.  Suppose that we want to convert a quantity ``quantity``
from a unit ``unitA`` to another unit ``unitB``.  Based on the framework
defined, since any unit can be related to/from the base units in terms of
deterministic functions, we simply need to follow these steps:

1. First, convert ``quantity`` to be exclusively in terms of base units by
   calling the ``to_base_function`` of ``unitA``.
2. Next, convert the output from Step 1 to units of ``unitB`` by calling
   the ``from_base_function`` of ``unitB``. 
