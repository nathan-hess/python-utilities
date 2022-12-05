"""**Objects for performing unit conversions**

The :py:mod:`pyxx.units` module provides unit conversion capabilities.  It
allows users to define customized systems of units and add associated,
arbitrary units and convert quantities between such units.
"""

from .classes import (
    ConstantUnitMathConventions,
    Unit,
    UnitConverter,
    UnitConverterEntry,
    UnitConverterSI,
    UnitLinear,
    UnitLinearSI,
    UnitSystem,
    UnitSystemSI,
)
from .classes.cli import execute_from_command_line
from .functions import parse_unit
