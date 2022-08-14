pyxx.strings
============

.. automodule:: pyxx.strings

.. currentmodule:: pyxx.strings


Analyzing String Content
------------------------

The functions in this section can be used to analyze string content, checking
whether certain characters or patterns are present or whether the string
content has a particular structure.

.. autosummary::
    :toctree: ./api
    :template: ../_templates/api_reference_strings_content.rst

    str_excludes_chars


Bracket Parsing
---------------

The objects in this section are intended to assist in processing strings with
brackets, loosely defined as pairs of characters that enclose quantities of
interest (``()``, ``[]``, ``{}``, etc.).  Particularly in scientific contexts,
it can be useful to parse strings containing brackets and identify pairs of
*matched* brackets.

.. note::

    For more information on terminology definitions and how the functions in
    this section operate on a conceptual level, refer to the
    :ref:`section-bracket_concepts` page.

.. toctree::
    :hidden:

    concepts/brackets

.. autosummary::
    :toctree: ./api

    contains_all_matched_brackets
    find_matching_bracket
    find_skip_brackets
    strip_matched_brackets


Splitting Strings
-----------------

The functions in this section can be used to analyze strings and split them
into sub-strings or lists of strings.

.. autosummary::
    :toctree: ./api

    split_at_index
