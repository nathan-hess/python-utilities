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

    Time a code block and print the duration to the terminal:

    .. code-block:: python

        >>> from pyxx.dev import TimeIt
        >>> import time
        >>> with TimeIt(units='ms', message='Execution time: {time:.2f} {units}'):
        ...     # Code block of which to measure the duration
        ...     time.sleep(1)
        Execution time: 1000.10 ms

    Time a code block and store the duration in a variable:

    .. code-block:: python

        >>> from pyxx.dev import TimeIt
        >>> import time
        >>> timer = TimeIt(print_duration=False)
        >>> with timer:
        ...     # Code block of which to measure the duration
        ...     time.sleep(1)
        >>> print(timer.duration('ms'))
        1000.1010101010101
    """

    def __init__(self, print_duration: bool = True, units: str = 's',
                 message: str = 'Command duration: {time} {units}') -> None:
        """Creates a new context manager for measuring the duration of a code block

        Parameters
        ----------
        print_duration : bool, optional
            Whether to print to the terminal the duration of the code block
        units : str, optional
            Only applicable if ``print_duration`` is ``True``.  Specifies the
            units in which the duration will be displayed to the terminal
            (default is ``'s'``)
        message : str, optional
            Only applicable if ``print_duration`` is ``True``.  The message
            template to display the duration (default is
            ``'Command duration: {time} {units}'``).  The ``{time}`` and
            ``{units}`` placeholders will be replaced by the duration and
            units, respectively
        """
        self.__unit_converter = UnitConverterSI()

        if (not (self.__unit_converter.is_defined_unit(units)
                 and self.__unit_converter.is_convertible('s', units))):
            raise ValueError(
                f'Invalid units: cannot convert from seconds to "{units}"')

        self.__print = bool(print_duration)
        self.__units = units
        self.__message = message

        self.__t0_s = 0.0
        self.__dt_s = 0.0

    def __enter__(self) -> None:
        self.__t0_s = time.time()

    def __exit__(self, *args, **kwargs) -> None:
        t1_s = time.time()

        # Calculate duration in seconds
        self.__dt_s = t1_s - self.__t0_s

        if self.__print:
            duration = self.__unit_converter.convert(
                quantity=self.__dt_s, from_unit='s', to_unit=self.__units)

            print(self.__message.format(time=duration, units=self.__units))

    def duration(self, units: str = 's') -> float:
        """Returns the last measured duration from the context manager

        Parameters
        ----------
        units : str
            The units in which to return the duration (default is ``'s'``)
        """
        return self.__unit_converter.convert(
            quantity=self.__dt_s, from_unit='s', to_unit=units
        )
