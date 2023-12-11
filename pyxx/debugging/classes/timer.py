"""Classes for timing code execution.
"""

import time

from pyxx.units.classes.unitconverter import UnitConverterSI


class TimeIt:
    """A context manager for measuring the duration of a code block.

    This context manager can be used in a "with" statement to measure the
    duration of code within the statement.  The resulting duration will be
    printed to the console when the "with" statement completes.

    Warnings
    --------
    Using this timer will add some overhead to the code block being measured.
    The measured duration outputted to the terminal will be slightly larger
    than the actual execution time of the code block.

    Examples
    --------

    .. code-block:: python

        >>> from pyxx.debugging import TimeIt
        >>> import time
        >>> with TimeIt(units='ms', message='Execution time: {time} {units}'):
        ...     # Code block of which to measure the duration
        ...     time.sleep(1)
        Execution time: 1000.1010101010101 ms
    """

    def __init__(self, units: str = 's',
                 message: str = 'Command duration: {time} {units}') -> None:
        """Creates a new context manager for measuring the duration of a code block

        Parameters
        ----------
        units : str, optional
            The units in which the duration will be displayed (default is ``'s'``)
        message : str, optional
            The message template to display the duration (default is
            ``'Command duration: {time} {units}'``).  The ``{time}`` and
            ``{units}`` placeholders will be replaced by the duration and
            units, respectively

        Raises
        ------
        ValueError
            If the specified units are invalid and cannot be converted from
            seconds
        """
        self.__unit_converter = UnitConverterSI()

        if (not (self.__unit_converter.is_defined_unit(units)
                 and self.__unit_converter.is_convertible('s', units))):
            raise ValueError(
                f'Invalid units: cannot convert from seconds to "{units}"')

        self.__units = units
        self.__message = message

        self.__t0 = 0.0

    def __enter__(self) -> None:
        self.__t0 = time.time()

    def __exit__(self, *args, **kwargs) -> None:
        t1 = time.time()
        duration = self.__unit_converter.convert(quantity=t1 - self.__t0,
                                                 from_unit='s',
                                                 to_unit=self.__units)

        print(self.__message.format(time=duration, units=self.__units))
