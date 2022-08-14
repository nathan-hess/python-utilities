"""**Code for processing, parsing, and modifying strings**

The ``pyxx.strings`` module is intended to assist with processing data in the
form of Python strings.  Submodules provide functionality such as analyzing
strings with parentheses (e.g., determining which parentheses in a string are
"matched" with each other), assisting with string indexing and splitting, and
checking string content.
"""

from .content import str_excludes_chars
from .brackets import (
    contains_all_matched_brackets,
    find_matching_bracket,
    find_skip_brackets,
)
from .split import split_at_index
