"""**Code for reading, writing, and processing files**

The :py:mod:`pyxx.files` module is intended to assist with processing
files.  It contains a set of classes intended to represent generic file
types (binary files and text files), as well as functions to perform
common file-related operations (such as computing file hashes).

An important concept about the classes in :py:mod:`pyxx.files` is that
files are considered *a data structure for storing information as a sequence
of characters*.  Files are not necessarily linked to a location on the disk
(although they can be).  Therefore, classes in :py:mod:`pyxx.files` can, but
do not necessarily, have an assigned path.

The intention of this module is that by subclassing the included classes,
the basic structure should be provided to manage file content, and a few very
general functions are provided.  Developers can add custom methods to
subclasses *specific to their file format*.  For instance, if creating a
``ShellScript`` subclass to parse shell scripts, a ``ShellScript.read()``
method might be added that parses the file, extracting the shebang line and
storing the interpreter in an attribute ``ShellScript.interpreter``.

Thus, the focus of the :py:mod:`pyxx.files` classes and subclasses should,
in most cases, be on processing context-specific file content, and less
focused on specific files on the disk (Python's built-in ``pathlib``,
``shutil``, and ``os`` modules are already well-suited to these purposes).
"""

from .classes import (
    BinaryFile,
    File,
    TextFile,
)
from .functions.hash import compute_file_hash
