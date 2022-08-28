"""
Customized exceptions for the ``pyxx.files`` module
"""


class UntrackedFileError(Exception):
    """Error thrown if trying to determine whether a file has been modified,
    but without having previously computed hashes of the file"""
