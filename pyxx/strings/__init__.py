"""Code for processing, parsing, and modifying strings

The ``pyxx.strings`` module is intended to assist with processing data in the
form of Python strings.  Submodules provide functionality such as analyzing
strings with parentheses (e.g., determining which parentheses in a string are
"matched" with each other), assisting with string indexing and splitting, and
checking string content
"""

from .split import split_at_index
