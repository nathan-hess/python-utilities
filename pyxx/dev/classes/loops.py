"""Classes for controlling loop execution.
"""

import signal


class InterruptibleLoop:
    """Context manager to create an interruptible loop

    This context manager allows users to interrupt and terminate a loop early
    by pressing ``Ctrl+c``.  This can be useful to stop a long process early
    while monitoring results (such as stopping training of a machine learning
    model).  When interrupted, the context manager will change its
    :py:attr:`interrupted` attribute to ``True``.  Additionally, if the
    ``throw_exception`` option is enabled, an ``InterruptedError`` will be
    raised (which can be caught and handled as desired).

    Examples
    --------
    Basic usage:

    >>> with pyxx.dev.InterruptibleLoop() as loop:
    ...     for i in range(1000):
    ...         # Do something
    ...
    ...         if loop.interrupted:
    ...             print('Loop was interrupted')
    ...             break

    Example of using the ``throw_exception`` option:

    >>> try:
    ...     with pyxx.dev.InterruptibleLoop(throw_exception=True) as loop:
    ...         for i in range(1000):
    ...             pass  # Do something
    ...
    ... except InterruptedError:
    ...     print('Loop was interrupted')
    ...
    ... else:
    ...     print('Loop was NOT interrupted')
    Loop was NOT interrupted
    """

    def __init__(self, throw_exception: bool = False) -> None:
        # Store user inputs
        self.__throw_exception = throw_exception

        # Initialize context manager internal state
        self.__interrupted = False
        self.__original_sigint_handler = signal.getsignal(signal.SIGINT)

    @property
    def interrupted(self) -> bool:
        """Whether the loop has been interrupted"""
        return self.__interrupted

    def _interrupt_handler(self, *args, **kwargs) -> None:  # pylint: disable=W0613
        self.__interrupted = True

        if self.__throw_exception:
            raise InterruptedError

    def __enter__(self) -> 'InterruptibleLoop':
        signal.signal(signal.SIGINT, self._interrupt_handler)
        self.__interrupted = False

        return self

    def __exit__(self, *args, **kwargs) -> None:
        signal.signal(signal.SIGINT, self.__original_sigint_handler)
