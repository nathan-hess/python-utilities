"""**Code for reading, writing, and processing files**

The ``pyxx.files`` module is intended to assist with processing files.  It
contains a set of classes intended to represent generic file types (binary
files, text files, etc.), as well as functions to perform common file-
related operations (such as computing file hashes).
"""

from .classes import (
    BinaryFile,
    File,
    TextFile,
)
from .functions.hash import compute_file_hash
