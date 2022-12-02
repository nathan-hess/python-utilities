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

from typing import Any, Dict

from .unit import UnitLinearSI


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
    'km': {
        'unit': UnitLinearSI((1, 0, 0, 0, 0, 0, 0), scale=1000, offset=0),
        'tags': ('length',),
        'name': 'kilometer',
        'aliases': ('kilometer', 'kilometers'),
    },
    'in': {
        'unit': UnitLinearSI((1, 0, 0, 0, 0, 0, 0), scale=0.0254, offset=0),
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

    ## TIME ------------------------------------------------------------------
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

    ## SPEED -----------------------------------------------------------------
    'mph': {
        'unit': UnitLinearSI((1, -1, 0, 0, 0, 0, 0), scale=1609.344/3600, offset=0),
        'tags': ('speed',),
        'name': 'miles per hour',
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
}
