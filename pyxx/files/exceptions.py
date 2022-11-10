"""Customized exceptions for the :py:mod:`pyxx.files` module
"""


class NoFileSpecifiedError(AttributeError):
    """Error thrown if attempting to perform an operation that requires
    the ``pyxx.files.File.file`` attribute, but this attribute is set
    to ``None``"""


class UntrackedFileError(Exception):
    """Error thrown if trying to determine whether a file has been modified,
    but without having previously computed hashes of the file"""
