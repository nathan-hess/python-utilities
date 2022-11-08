.. include:: ../../constants.rst


.. _section-examples_units:

Unit Examples
=============

Overview
--------

This section explains how to use the :py:mod:`pyxx.units` module to define
units, and perform unit conversions and related operations.

To follow along with these examples, begin by opening a Python terminal and
importing the |PackageNameStylized| package:

>>> import pyxx


Creating Units
--------------

As discussed in the :ref:`section-units_concepts` section, to define a unit,
we need to specify several pieces of information: (1) the system of units to
which the unit belongs, (2) the powers to which the base units are raised to
relate the unit to the base units, (3) a function to convert quantities from
the given unit to base units, and (4) an inverse function to convert quantities
from the base units to the given unit.

There are several ways to define units that meet such requirements.  One
approach is to create :py:class:`pyxx.units.Unit` objects.  For instance, let's
define a unit of *meters*.  Since meters are one of the base units in the SI
system of units, this is fairly straightforward:

>>> m = pyxx.units.Unit(
...          unit_system=pyxx.units.UnitSystemSI(),
...          base_unit_exps=[1, 0, 0, 0, 0, 0, 0],
...          to_base_function=lambda x, exp: x,
...          from_base_function=lambda x, exp: x,
...          identifier='m', name='meter'
... )
>>> print(m)
m - meter - [1. 0. 0. 0. 0. 0. 0.]

However, there's an arguably easier shortcut.  Suppose we want to define another
unit in the SI system of units: the *millimeter*.  Since this unit has a linear
relationship to the base units (meters), we can define it using a
:py:class:`pyxx.units.UnitLinearSI`.  In this case, the object definition is
easier, since we don't need to worry about the ``to_base_function`` and
``from_base_function`` arguments -- these are automatically generated for us.
Since a millimeter is :math:`1/1000` of a meter, the unit can be defined as:

>>> mm = pyxx.units.UnitLinearSI(
...          base_unit_exps=[1, 0, 0, 0, 0, 0, 0],
...          scale=0.001, offset=0,
...          identifier='mm', name='millimeter'
... )
>>> print(mm)
mm - millimeter - [1. 0. 0. 0. 0. 0. 0.] - scale: 0.001 - offset: 0.0


Unit Conversions
----------------

Checking for Ability to Convert Units
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Prior to performing a unit conversion, it can be useful to know whether two
units are "compatible" and quantities can be converted between the units.
The :py:meth:`pyxx.units.Unit.is_convertible` method provides this
functionality.

Since the ``m`` and ``mm`` units we defined previously both belong to the same
system of units (SI) and have the same ``base_unit_exps`` property, it should
be possible to convert between these units, which we can verify using:

>>> mm.is_convertible(m)
True
>>> m.is_convertible(mm)
True

Converting To/From Base Units
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The first, and relatively simple, unit conversion we may want to perform is to
convert a given quantity from a given unit to the base units, or vice versa.

For instance, to convert a value from millimeters to the base units (meters),
we could run:

>>> mm.to_base(100)
0.1

We can also perform conversions in cases where units are raised to an exponent.
For instance, this is one way to convert :math:`1\ m^2` to square millimeters:

>>> mm.from_base(1, exponent=2)
1000000.0
