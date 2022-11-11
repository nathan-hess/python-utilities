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

Basics
^^^^^^

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
...         unit_system=pyxx.units.UnitSystemSI(),
...         base_unit_exps=[1, 0, 0, 0, 0, 0, 0],
...         to_base_function=lambda x, exp: x,
...         from_base_function=lambda x, exp: x,
...         identifier='m', name='meter'
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


Unit Arithmetic
^^^^^^^^^^^^^^^

Once we have already defined several units, we may want to create new units
based on the units we have already defined.  For instance, we already created
a unit of meters, and suppose we also define a unit representing seconds:

>>> s = pyxx.units.UnitLinearSI(
...         base_unit_exps=[0, 1, 0, 0, 0, 0, 0],
...         scale=1, offset=0,
...         identifier='s', name='second'
... )
>>> print(s)
s - second - [0. 1. 0. 0. 0. 0. 0.] - scale: 1.0 - offset: 0.0

Now suppose we want to define a new unit: meters per second squared.  We
*could* create an entirely new unit, like this:

>>> print(pyxx.units.UnitLinearSI(
...          base_unit_exps=[1, -2, 0, 0, 0, 0, 0],
...          scale=1, offset=0,
...          identifier='m/s^2'
... ))
m/s^2 - [ 1. -2.  0.  0.  0.  0.  0.] - scale: 1.0 - offset: 0.0

However, there's a much simpler, less error-prone way.  We can use our existing
units ``m`` and ``s`` to create a new unit:

>>> m_s2 = m/s**2
>>> print(m_s2)
m/(s^2.0) - meter/(second^2.0) - [ 1. -2.  0.  0.  0.  0.  0.]

Supported operations include multiplication (``*``), division (``/``), and
exponents (``**``).

.. dropdown:: [Advanced] Unit Arithmetic with Constants
    :animate: fade-in

    By default, multiplying or dividing a |PackageNameStylized| unit by a
    constant will result in an error being thrown.  For instance, this code
    would result in an error:

    >>> 1000 * mm  # throws an error  # doctest: +SKIP

    However, there are cases in which this functionality could be useful.  For
    instance, if we have already defined a unit of millimeters, we may want to
    define another unit, such as centimeters, that is a known multiple of
    millimeters.  Fortunately, |PackageNameStylized| provides a means to do so.

    As explained in the :py:class:`pyxx.units.ConstantUnitMathConventions`
    documentation, the meaning of multiplying a unit by a constant is ambiguous.
    Thus, we must first enable this feature by selecting an appropriate math
    convention; for instance, by using:

    >>> from pyxx.units import Unit, ConstantUnitMathConventions
    >>> Unit.CONSTANT_MATH_CONVENTION = ConstantUnitMathConventions.UNIT_BASED

    Then, we can perform operations multiplying or dividing units by a constant:

    >>> cm = 10 * mm
    >>> print( cm.to_base(100) )
    1.0

    However, this is an advanced feature, and it requires detailed
    understanding of the meaning of each of the options specified in
    :py:class:`pyxx.units.ConstantUnitMathConventions`.  In most cases,
    it is safer to leave this feature in its default setting (``DISABLE``):

    >>> Unit.CONSTANT_MATH_CONVENTION = ConstantUnitMathConventions.DISABLE


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

>>> print( mm.to_base(100) )
0.1

We can also perform conversions in cases where units are raised to an exponent.
For instance, this is one way to convert :math:`1\ m^2` to square millimeters:

>>> print( mm.from_base(1, exponent=2) )
1000000.0


Converting Between Units
^^^^^^^^^^^^^^^^^^^^^^^^

Perhaps a more interesting case, however, is to convert between units.  This
can be accomplished using the :py:meth:`pyxx.units.Unit.convert` method.

For instance, we previously defined units of :math:`m` and :math:`mm`, so to
convert :math:`2\ m` to :math:`mm`, we can use:

>>> print( m.convert(2, 'to', mm) )
2000.0

We can just as easily convert "the other direction," from :math:`mm` to
:math:`m`:

>>> print( m.convert(2, 'from', mm) )
0.002

It's also possible to convert multiple values at once by providing a list,
tuple, or NumPy array as an input:

>>> print( m.convert([1, 2, 3, 4], 'to', mm) )
[1000. 2000. 3000. 4000.]

More complex unit conversions can be performed using unit arithmetic:

>>> print( (m/s).convert([3.14, 6.28], 'to', mm/s) )
[3140. 6280.]
