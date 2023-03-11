"""This module contains a set of commonly-used units.  All units are defined
in terms of the SI system (https://www.nist.gov/pml/owm/metric-si/si-units),
with the following sequence of seven base units:

1. Length: meter [:math:`m`]
2. Time: second [:math:`s`]
3. Amount of substance: mole [:math:`mol`]
4. Electric current: ampere [:math:`A`]
5. Temperature: Kelvin [:math:`K`]
6. Luminous intensity: candela [:math:`cd`]
7. Mass: kilogram [:math:`kg`]
"""

import math
from typing import Any, Dict

from .unit import UnitLinearSI


## PHYSICAL CONSTANTS --------------------------------------------------------
# Assumed physical constants used in performing unit conversions

# Atmospheric pressure
ATMOSPHERIC_PRESSURE_PA = 101325    # Pa (absolute pressure)

# Standard acceleration due to gravity
# https://physics.nist.gov/cgi-bin/cuu/Value?gn
STANDARD_GRAVITY = 9.80665  # m/s^2


## CONVERSION FACTORS --------------------------------------------------------
# Conversion factors used internally by the unit converter

# Inches to meters
_IN_TO_M_SCALE = 0.0254  # m/in

# Pound-mass to kilograms
_LBM_TO_KG_SCALE = 0.45359237  # kg/lbm

# Pound-force to Newtons
_LBF_TO_N_SCALE = 4.4482216152605  # N/lbf
# _LBF_TO_N_SCALE = _LBM_TO_KG_SCALE * STANDARD_GRAVITY

# Pounds per square inch (psi) to pascals (Pa)
_PSI_TO_PA_SCALE = 4.4482216152605 / 0.00064516  # Pa/psi
#                = _LBF_TO_N_SCALE / (_IN_TO_M_SCALE**2)

# Degrees Celsius to Kelvin
_DEG_C_TO_K_OFFSET = 273.15

# Degrees Fahrenheit to Kelvin
_DEG_F_TO_K_SCALE = 5/9
_DEG_F_TO_K_OFFSET = -160/9 + 273.15
#                  = -32 * _DEG_F_TO_K_SCALE + _DEG_C_TO_K_OFFSET

# Gallons to cubic meters
_GAL_TO_M3_SCALE = 0.003785411784  # gal/m^3


## UNIT CONVERTER DEFAULT UNITS ----------------------------------------------

SAMPLE_SI_UNITS: Dict[str, Dict[str, Any]] = {
    ## BASE UNITS ------------------------------------------------------------
    'm': {
        'unit': UnitLinearSI((1, 0, 0, 0, 0, 0, 0), scale=1, offset=0),
        'tags': ('length',),
        'name': 'meter',
        'aliases': ('meter', 'meters'),
    },
    's': {
        'unit': UnitLinearSI((0, 1, 0, 0, 0, 0, 0), scale=1, offset=0),
        'tags': ('time',),
        'name': 'second',
        'aliases': ('sec', 'second', 'seconds'),
    },
    'mol': {
        'unit': UnitLinearSI((0, 0, 1, 0, 0, 0, 0), scale=1, offset=0),
        'name': 'mole',
        'aliases': ('moles', 'mole'),
    },
    'A': {
        'unit': UnitLinearSI((0, 0, 0, 1, 0, 0, 0), scale=1, offset=0),
        'name': 'ampere',
        'description': 'Unit of measure of electric current',
        'aliases': ('amp', 'amps'),
    },
    'K': {
        'unit': UnitLinearSI((0, 0, 0, 0, 1, 0, 0), scale=1, offset=0),
        'tags': ('temperature',),
        'name': 'Kelvin',
        'description': 'Absolute temperature or temperature increment in Kelvin',
    },
    'cd': {
        'unit': UnitLinearSI((0, 0, 0, 0, 0, 1, 0), scale=1, offset=0),
        'tags': ('luminance',),
        'name': 'candela',
    },
    'kg': {
        'unit': UnitLinearSI((0, 0, 0, 0, 0, 0, 1), scale=1, offset=0),
        'tags': ('mass',),
        'name': 'kilogram',
        'description': 'Unit of measure of mass',
        'aliases': ('kilogram', 'kilograms'),
    },

    ## DIMENSIONLESS QUANTITIES ----------------------------------------------
    '-': {
        'unit': UnitLinearSI((0, 0, 0, 0, 0, 0, 0), scale=1, offset=0),
        'tags': ('dimensionless',),
        'name': 'dimensionless',
        'description': 'Unit assigned to dimensionless numbers',
        'aliases': ('dimensionless', 'unitless'),
    },

    ## LENGTH ----------------------------------------------------------------
    'mm': {
        'unit': UnitLinearSI((1, 0, 0, 0, 0, 0, 0), scale=0.001, offset=0),
        'tags': ('length',),
        'name': 'millimeter',
        'aliases': ('millimeter', 'millimeters'),
    },
    'cm': {
        'unit': UnitLinearSI((1, 0, 0, 0, 0, 0, 0), scale=0.01, offset=0),
        'tags': ('length',),
        'name': 'centimeter',
        'aliases': ('centimeter', 'centimeters'),
    },
    'micron': {
        'unit': UnitLinearSI((1, 0, 0, 0, 0, 0, 0), scale=1e-6, offset=0),
        'tags': ('length',),
        'name': 'micron',
        'aliases': ('microns', 'μm'),
    },
    'km': {
        'unit': UnitLinearSI((1, 0, 0, 0, 0, 0, 0), scale=1000, offset=0),
        'tags': ('length',),
        'name': 'kilometer',
        'aliases': ('kilometer', 'kilometers'),
    },
    'in': {
        'unit': UnitLinearSI((1, 0, 0, 0, 0, 0, 0), scale=_IN_TO_M_SCALE,
                             offset=0),
        'tags': ('length',),
        'name': 'inch',
        'aliases': ('inch', 'inches'),
    },
    'ft': {
        'unit': UnitLinearSI((1, 0, 0, 0, 0, 0, 0), scale=0.3048, offset=0),
        'tags': ('length',),
        'name': 'foot',
        'aliases': ('foot', 'feet'),
    },
    'mi': {
        'unit': UnitLinearSI((1, 0, 0, 0, 0, 0, 0), scale=1609.344, offset=0),
        'tags': ('length',),
        'name': 'mile',
        'aliases': ('mile', 'miles'),
    },
    'yd': {
        'unit': UnitLinearSI((1, 0, 0, 0, 0, 0, 0), scale=0.9144, offset=0),
        'tags': ('length',),
        'name': 'yard',
        'aliases': ('yard', 'yards'),
    },
    'league': {
        'unit': UnitLinearSI((1, 0, 0, 0, 0, 0, 0), scale=4828.032, offset=0),
        'tags': ('length',),
        'name': 'league',
        'aliases': ('leagues',),
    },

    ## AREA ------------------------------------------------------------------
    'ac': {
        'unit': UnitLinearSI((2, 0, 0, 0, 0, 0, 0), scale=4046.8564224, offset=0),
        'tags': ('area',),
        'name': 'acre',
        'aliases': ('acre', 'acres'),
    },

    ## VOLUME ----------------------------------------------------------------
    'L': {
        'unit': UnitLinearSI((3, 0, 0, 0, 0, 0, 0), scale=0.001, offset=0),
        'tags': ('volume',),
        'name': 'liter',
        'aliases': ('liter', 'liters'),
    },
    'mL': {
        'unit': UnitLinearSI((3, 0, 0, 0, 0, 0, 0), scale=1e-6, offset=0),
        'tags': ('volume',),
        'name': 'milliliter',
        'aliases': ('milliliter', 'milliliters'),
    },
    'gal': {
        'unit': UnitLinearSI((3, 0, 0, 0, 0, 0, 0), scale=_GAL_TO_M3_SCALE,
                             offset=0),
        'tags': ('volume',),
        'name': 'liquid gallon',
        'aliases': ('gallon', 'gallons'),
    },
    'qt': {
        'unit': UnitLinearSI((3, 0, 0, 0, 0, 0, 0), scale=_GAL_TO_M3_SCALE/4,
                             offset=0),
        'tags': ('volume',),
        'name': 'liquid quart',
        'aliases': ('quart', 'quarts'),
    },
    'pt': {
        'unit': UnitLinearSI((3, 0, 0, 0, 0, 0, 0), scale=_GAL_TO_M3_SCALE/8,
                             offset=0),
        'tags': ('volume',),
        'name': 'liquid pint',
        'aliases': ('pint', 'pints'),
    },
    'cup': {
        'unit': UnitLinearSI((3, 0, 0, 0, 0, 0, 0), scale=_GAL_TO_M3_SCALE/16,
                             offset=0),
        'tags': ('volume',),
        'name': 'liquid cup',
        'aliases': ('cups',),
    },
    'fl_oz': {
        'unit': UnitLinearSI((3, 0, 0, 0, 0, 0, 0), scale=_GAL_TO_M3_SCALE/128,
                             offset=0),
        'tags': ('volume',),
        'name': 'fluid ounce',
        'aliases': ('fluid_ounce',),
    },
    'tbsp': {
        'unit': UnitLinearSI((3, 0, 0, 0, 0, 0, 0), scale=_GAL_TO_M3_SCALE/256,
                             offset=0),
        'tags': ('volume',),
        'name': 'tablespoon',
        'aliases': ('tablespoon', 'tablespoons'),
    },
    'tsp': {
        'unit': UnitLinearSI((3, 0, 0, 0, 0, 0, 0), scale=_GAL_TO_M3_SCALE/768,
                             offset=0),
        'tags': ('volume',),
        'name': 'teaspoon',
        'aliases': ('teaspoon', 'teaspoons'),
    },

    ## TIME ------------------------------------------------------------------
    'ns': {
        'unit': UnitLinearSI((0, 1, 0, 0, 0, 0, 0), scale=1e-9, offset=0),
        'tags': ('time',),
        'name': 'nanosecond',
        'aliases': ('nanosecond', 'nanoseconds'),
    },
    'microsec': {
        'unit': UnitLinearSI((0, 1, 0, 0, 0, 0, 0), scale=1e-6, offset=0),
        'tags': ('time',),
        'name': 'microsecond',
        'aliases': ('microsecond', 'microseconds', 'μs'),
    },
    'ms': {
        'unit': UnitLinearSI((0, 1, 0, 0, 0, 0, 0), scale=0.001, offset=0),
        'tags': ('time',),
        'name': 'millisecond',
        'aliases': ('millisecond', 'milliseconds'),
    },
    'min': {
        'unit': UnitLinearSI((0, 1, 0, 0, 0, 0, 0), scale=60, offset=0),
        'tags': ('time',),
        'name': 'minute',
        'aliases': ('minute', 'minutes'),
    },
    'hr': {
        'unit': UnitLinearSI((0, 1, 0, 0, 0, 0, 0), scale=3600, offset=0),
        'tags': ('time',),
        'name': 'hour',
        'aliases': ('hour', 'hours'),
    },
    'day': {
        'unit': UnitLinearSI((0, 1, 0, 0, 0, 0, 0), scale=86400, offset=0),
        'tags': ('time',),
        'name': 'day',
        'aliases': ('days',),
    },
    'week': {
        'unit': UnitLinearSI((0, 1, 0, 0, 0, 0, 0), scale=604800, offset=0),
        'tags': ('time',),
        'name': 'week',
        'aliases': ('weeks',),
    },

    ## FREQUENCY -------------------------------------------------------------
    'Hz': {
        'unit': UnitLinearSI((0, -1, 0, 0, 0, 0, 0), scale=1, offset=0),
        'tags': ('frequency',),
        'name': 'hertz',
        'aliases': ('hertz',),
    },
    'kHz': {
        'unit': UnitLinearSI((0, -1, 0, 0, 0, 0, 0), scale=1000, offset=0),
        'tags': ('frequency',),
        'name': 'kilohertz',
        'aliases': ('kilohertz',),
    },
    'MHz': {
        'unit': UnitLinearSI((0, -1, 0, 0, 0, 0, 0), scale=1e6, offset=0),
        'tags': ('frequency',),
        'name': 'megahertz',
        'aliases': ('megahertz',),
    },
    'GHz': {
        'unit': UnitLinearSI((0, -1, 0, 0, 0, 0, 0), scale=1e9, offset=0),
        'tags': ('frequency',),
        'name': 'gigahertz',
        'aliases': ('gigahertz',),
    },

    ## SPEED -----------------------------------------------------------------
    'mph': {
        'unit': UnitLinearSI((1, -1, 0, 0, 0, 0, 0), scale=1609.344/3600, offset=0),
        'tags': ('speed',),
        'name': 'miles per hour',
    },

    ## MASS ------------------------------------------------------------------
    'g': {
        'unit': UnitLinearSI((0, 0, 0, 0, 0, 0, 1), scale=0.001, offset=0),
        'tags': ('mass',),
        'name': 'gram',
        'aliases': ('gram', 'grams'),
    },
    'mg': {
        'unit': UnitLinearSI((0, 0, 0, 0, 0, 0, 1), scale=1e-6, offset=0),
        'tags': ('mass',),
        'name': 'milligram',
        'aliases': ('milligram', 'milligrams'),
    },
    'microgram': {
        'unit': UnitLinearSI((0, 0, 0, 0, 0, 0, 1), scale=1e-9, offset=0),
        'tags': ('mass',),
        'name': 'microgram',
        'aliases': ('micrograms', 'μg'),
    },
    'lbm': {
        'unit': UnitLinearSI((0, 0, 0, 0, 0, 0, 1), scale=_LBM_TO_KG_SCALE,
                             offset=0),
        'tags': ('mass',),
        'name': 'pound-mass',
        'description': ('Avoirdupois pound, as defined by NIST Handbook 44'),
        'aliases': ('pound-mass',),
    },
    't': {
        'unit': UnitLinearSI((0, 0, 0, 0, 0, 0, 1), scale=1000, offset=0),
        'tags': ('mass',),
        'name': 'metric ton',
        'aliases': ('metric_ton',),
    },
    'tn': {
        'unit': UnitLinearSI((0, 0, 0, 0, 0, 0, 1), scale=907.18474, offset=0),
        'tags': ('mass',),
        'name': 'short ton',
        'aliases': ('ton', 'tons', 'short_ton', 'short_tons'),
    },
    'long_ton': {
        'unit': UnitLinearSI((0, 0, 0, 0, 0, 0, 1), scale=1016.0469088, offset=0),
        'tags': ('mass',),
        'name': 'long ton',
        'aliases': ('long_tons',),
    },
    'carat': {
        'unit': UnitLinearSI((0, 0, 0, 0, 0, 0, 1), scale=0.0002, offset=0),
        'tags': ('mass',),
        'name': 'carat',
        'aliases': ('carats',),
    },

    ## FORCE -----------------------------------------------------------------
    'N': {
        'unit': UnitLinearSI((1, -2, 0, 0, 0, 0, 1), scale=1, offset=0),
        'tags': ('force',),
        'name': 'Newtons',
        'aliases': ('Newton', 'Newtons'),
    },
    'kN': {
        'unit': UnitLinearSI((1, -2, 0, 0, 0, 0, 1), scale=1000, offset=0),
        'tags': ('force',),
        'name': 'kilonewtons',
        'aliases': ('kilonewton', 'kilonewtons'),
    },
    'lbf': {
        'unit': UnitLinearSI((1, -2, 0, 0, 0, 0, 1), scale=_LBF_TO_N_SCALE,
                             offset=0),
        'tags': ('force',),
        'name': 'pound-force',
        'description': ('Avoirdupois pound-force, as defined by NIST Handbook 44 '
                        'and using NIST\'s definition of standard acceleration '
                        f'due to gravity of {STANDARD_GRAVITY} m/s^2'),
        'aliases': ('pound-force',),
    },

    ## ANGLES ----------------------------------------------------------------
    'rad': {
        'unit': UnitLinearSI((0, 0, 0, 0, 0, 0, 0), scale=1, offset=0),
        'tags': ('angle',),
        'name': 'radian',
        'aliases': ('radian', 'radians'),
    },
    'deg': {
        'unit': UnitLinearSI((0, 0, 0, 0, 0, 0, 0), scale=math.pi/180, offset=0),
        'tags': ('angle',),
        'name': 'degrees',
        'aliases': ('degree', 'degrees'),
    },
    'rev': {
        'unit': UnitLinearSI((0, 0, 0, 0, 0, 0, 0), scale=2*math.pi, offset=0),
        'tags': ('angle',),
        'name': 'revolutions',
        'aliases': ('revolutions', 'rotations'),
    },

    ## PRESSURE --------------------------------------------------------------
    'Pa': {
        'unit': UnitLinearSI((-1, -2, 0, 0, 0, 0, 1), scale=1, offset=0),
        'tags': ('pressure',),
        'name': 'pascal',
        'description': 'Absolute pressure in units of pascals',
        'aliases': ('pascal', 'pascals'),
    },
    'kPa': {
        'unit': UnitLinearSI((-1, -2, 0, 0, 0, 0, 1), scale=1000, offset=0),
        'tags': ('pressure',),
        'name': 'kilopascal',
        'description': 'Absolute pressure in units of kilopascals',
        'aliases': ('kilopascal', 'kilopascals'),
    },
    'MPa': {
        'unit': UnitLinearSI((-1, -2, 0, 0, 0, 0, 1), scale=1e6, offset=0),
        'tags': ('pressure',),
        'name': 'megapascal',
        'description': 'Absolute pressure in units of megapascals',
        'aliases': ('megapascal', 'megapascals'),
    },
    'GPa': {
        'unit': UnitLinearSI((-1, -2, 0, 0, 0, 0, 1), scale=1e9, offset=0),
        'tags': ('pressure',),
        'name': 'gigapascal',
        'description': 'Absolute pressure in units of gigapascals',
        'aliases': ('gigapascal', 'gigapascals'),
    },
    'bar': {
        'unit': UnitLinearSI((-1, -2, 0, 0, 0, 0, 1), scale=1e5, offset=0),
        'tags': ('pressure',),
        'name': 'bar',
        'description': 'Absolute pressure in units of bar',
    },
    'psi': {
        'unit': UnitLinearSI((-1, -2, 0, 0, 0, 0, 1), scale=_PSI_TO_PA_SCALE,
                             offset=0),
        'tags': ('pressure',),
        'name': 'psi',
        'description': 'Absolute pressure in units of pounds per square inch',
    },

    ## TEMPERATURE -----------------------------------------------------------
    'degC': {
        'unit': UnitLinearSI((0, 0, 0, 0, 1, 0, 0), scale=1,
                             offset=_DEG_C_TO_K_OFFSET),
        'tags': ('temperature',),
        'name': 'Degrees Celsius',
        'description': 'Absolute temperature in degrees Celsius',
        'aliases': ('celsius', 'Celsius'),
    },
    'degF': {
        'unit': UnitLinearSI((0, 0, 0, 0, 1, 0, 0), scale=_DEG_F_TO_K_SCALE,
                             offset=_DEG_F_TO_K_OFFSET),
        'tags': ('temperature',),
        'name': 'Degrees Fahrenheit',
        'description': 'Absolute temperature in degrees Fahrenheit',
        'aliases': ('fahrenheit', 'Fahrenheit'),
    },
    'degR': {
        'unit': UnitLinearSI((0, 0, 0, 0, 1, 0, 0), scale=_DEG_F_TO_K_SCALE,
                             offset=0),
        'tags': ('temperature',),
        'name': 'Degrees Rankine',
        'description': ('Absolute temperature or temperature increment in '
                        'degrees Rankine'),
        'aliases': ('rankine', 'Rankine'),
    },
    'degC_diff': {
        'unit': UnitLinearSI((0, 0, 0, 0, 1, 0, 0), scale=1, offset=0),
        'tags': ('temperature',),
        'name': 'Degrees Celsius increment',
        'description': 'Temperature increment in degrees Celsius',
    },
    'degF_diff': {
        'unit': UnitLinearSI((0, 0, 0, 0, 1, 0, 0), scale=_DEG_F_TO_K_SCALE,
                             offset=0),
        'tags': ('temperature',),
        'name': 'Degrees Fahrenheit increment',
        'description': 'Temperature increment in degrees Fahrenheit',
    },

    # WORK/ENERGY ------------------------------------------------------------
    'J': {
        'unit': UnitLinearSI((2, -2, 0, 0, 0, 0, 1), scale=1, offset=0),
        'tags': ('work', 'energy',),
        'name': 'joule',
        'aliases': ('joule', 'joules'),
    },
    'mJ': {
        'unit': UnitLinearSI((2, -2, 0, 0, 0, 0, 1), scale=0.001, offset=0),
        'tags': ('work', 'energy',),
        'name': 'millijoule',
        'aliases': ('millijoule', 'millijoules'),
    },
    'kJ': {
        'unit': UnitLinearSI((2, -2, 0, 0, 0, 0, 1), scale=1000, offset=0),
        'tags': ('work', 'energy',),
        'name': 'kilojoule',
        'aliases': ('kilojoule', 'kilojoules'),
    },
    'MJ': {
        'unit': UnitLinearSI((2, -2, 0, 0, 0, 0, 1), scale=1e6, offset=0),
        'tags': ('work', 'energy',),
        'name': 'megajoule',
        'aliases': ('megajoule', 'megajoules'),
    },
    'GJ': {
        'unit': UnitLinearSI((2, -2, 0, 0, 0, 0, 1), scale=1e9, offset=0),
        'tags': ('work', 'energy',),
        'name': 'gigajoule',
        'aliases': ('gigajoule', 'gigajoules'),
    },

    # POWER ------------------------------------------------------------------
    'W': {
        'unit': UnitLinearSI((2, -3, 0, 0, 0, 0, 1), scale=1, offset=0),
        'tags': ('power',),
        'name': 'watt',
        'aliases': ('watt', 'watts'),
    },
    'mW': {
        'unit': UnitLinearSI((2, -3, 0, 0, 0, 0, 1), scale=0.001, offset=0),
        'tags': ('power',),
        'name': 'milliwatt',
        'aliases': ('milliwatt', 'milliwatts'),
    },
    'kW': {
        'unit': UnitLinearSI((2, -3, 0, 0, 0, 0, 1), scale=1000, offset=0),
        'tags': ('power',),
        'name': 'kilowatt',
        'aliases': ('kilowatt', 'kilowatts'),
    },
    'MW': {
        'unit': UnitLinearSI((2, -3, 0, 0, 0, 0, 1), scale=1e6, offset=0),
        'tags': ('power',),
        'name': 'megawatt',
        'aliases': ('megawatt', 'megawatts'),
    },
    'GW': {
        'unit': UnitLinearSI((2, -3, 0, 0, 0, 0, 1), scale=1e9, offset=0),
        'tags': ('power',),
        'name': 'gigawatt',
        'aliases': ('gigawatt', 'gigawatts'),
    },
}
