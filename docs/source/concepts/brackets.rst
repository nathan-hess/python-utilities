.. include:: ../constants.rst


.. _section-bracket_concepts:

Bracket Concepts
================

This section describes some of the basic concepts and terminology used in the
documentation and source code of the bracket-related functions in the
:py:mod:`pyxx.strings` module.


Definitions
-----------

Bracket
^^^^^^^

The term "bracket" refers to any of following sets of characters that are used
to enclose quantities of interest: parentheses ``()``, square brackets ``[]``,
and braces ``{}``.

Note that the term "bracket" is used loosely here.  Technically, the term "bracket"
refers specifically to ``[]`` characters.  However, in software projects such as
`Visual Studio Code <https://code.visualstudio.com/blogs/2021/09/29/bracket-pair-colorization>`__,
the term "bracket" is used to refer to any of parentheses, square brackets,
and braces.

Rather than using a complex and potentially confusing term such as "enclosing
characters" to refer to parentheses, square brackets, and braces, in
|PackageNameStylized| all of these characters are collectively referred to as
"brackets," and the ``[]`` are specifically referred to as "square brackets."
This approach aims to strike a balance between precise lexical terminology
and intelligibility for end users.


Opening/Closing Brackets
^^^^^^^^^^^^^^^^^^^^^^^^

Brackets consist of *pairs* of characters (``()``, ``[]``, or ``{}``), and
are generally used to enclose a quantity of interest.  Using the typical
English convention of reading left-to-right, the character that denotes the
left side of each pair is termed the "opening" bracket, and the character
on the right side of each pair is termed the "closing" character.

For example, in the case of parentheses, an "opening parenthesis" is defined
as ``(``, and a "closing parenthesis" is defined as ``)``.


Matched Brackets
^^^^^^^^^^^^^^^^

When enclosing a quantity of interest, brackets must occur in a matched pair
containing the opening bracket and its *corresponding* closing bracket.  That
is, a matched bracket pair consists of an opening bracket and the first
closing bracket encountered proceeding rightward in the string, skipping over
any nested, matched bracket pairs along the way.

For instance, consider the example below.  In this example, the parentheses at
indices 0 and 9 form a matched pair, as do the parentheses at indices 3 and 4,
and at indices 5 and 7.

.. code-block:: python

    String:    '( * * ( ) ( * ) * )'
    Indices:    0 1 2 3 4 5 6 7 8 9

In contrast, if we modify a few of the parentheses as is done in the example
below, the matched pairs are now at indices 0 and 3, indices 4 and 9, and
indices 5 and 7.

.. code-block:: python

    String:    '( * * ) ( ( * ) * )'
    Indices:    0 1 2 3 4 5 6 7 8 9

There are a few other important rules to be aware of.  First, different
"types" of characters (parentheses, square brackets, or braces) are considered
*independently*, and a matched bracket pair *must* consist of the same type
of character.  For example, the parenthesis at index 0 and square bracket
at index 2 below do **not** form a matched pair, but the parentheses at
indices 0 and 2 and indices 4 and 7, and the braces at indices 5 and 8, could
be considered to form matched pairs.

.. code-block:: python

    String:    '( * ] ) ( { * ) } *'
    Indices:    0 1 2 3 4 5 6 7 8 9

Additionally, there may be cases in which the structure of the string is
invalid and matched pairs are not defined.  For instance, in the example
below, the closing parenthesis at index 2 occurs *before* its corresponding
opening parenthesis, so matched bracket pairs cannot be defined.

.. code-block:: python

    String:    '( ) ) ( )'
    Indices:    0 1 2 3 4


Bracket-Matching Algorithm
--------------------------

The algorithm used by |PackageNameStylized| to identify pairs of matched
brackets is conceptually relatively simple.  Suppose that we have a string
as given below and we are interested in finding the matching parenthesis for
the opening parenthesis at index 1.

.. code-block:: python

    String:    '( ( [ * ( ] * ) ) )'
    Indices:    0 1 2 3 4 5 6 7 8 9

By inspection, we can see that the matched closing parenthesis occurs at
index 8.

The algorithm used by |PackageNameStylized| uses a single forward pass through
the string to determine this result.  We begin at index 1, the location of the
bracket whose matching bracket we seek to find.

The key idea upon which the bracket-matching algorithm used in
|PackageNameStylized| is based is that as we move through the string, we will
keep a "counter" that tracks the number of nested bracket pairs we have
entered.  The value of this counter will tell us a number of important pieces
of information, such as when we have reached the matching bracket (or if there
is no matching bracket).

We initialize the counter at zero at index 1.  Then, we move through the
string, one character at a time.  Each time we encounter an *opening bracket*,
we increase the counter by one, and each time we encounter a *closing
bracket*, we decrease the counter by one.

Thus, for the given example, beginning at index 1, we increase the counter by
one (since this is an opening bracket).  Then we move from left to right
through the string, one character at a time.  When we get to index 4, the
counter increases from one to two since an index 4 is an opening bracket.  In
contrast, when we get to indices 7 and 8, the counter drops to one and then
zero, respectively.  The plot below illustrates the value of the counter as
we move through the string.

.. plot::

    x = [1, 1, 2, 3, 4, 4, 5, 6, 7, 7, 8, 8]
    y = [0, 1, 1, 1, 1, 2, 2, 2, 2, 1, 1, 0]
    plt.figure(figsize=(8,4))
    plt.plot(x, y, linewidth=3)
    plt.xlabel('Index', fontsize=12)
    plt.ylabel('Counter', fontsize=12)
    plt.yticks([0, 1, 2])
    plt.grid()
    plt.show()

At this point, consider what the counter represents: in essence, it simply
tracks the number of "levels deep" we are inside nested brackets.  Thus,
when the counter returns to zero at index 8 in the example above, this means
that we are no longer inside of any nested brackets -- in other words, we
have found the matching bracket.

This is precisely the strategy employed by |PackageNameStylized|: for a given
bracket (call it "Bracket A"), to find the matching bracket, we simply begin
at the index of Bracket A and proceed one character at a time through the
string, tracking the number of "levels deep" inside nested brackets with a
counter as described previously.  As soon as the counter reaches zero for the
first time, we have found the matching bracket.


Extensions
^^^^^^^^^^

The bracket-matching algorithm described above can be extended in a number
of ways, several of which are provided by |PackageNameStylized|.

**Determining Whether All Brackets Come in Matched Pairs**
Suppose we want to determine whether all brackets in a string come in matched
pairs (e.g., we want to determine that a string like ``'(1) 2 ) 3 (4 (5)'``
does not contain all matched pairs because the parenthesis between ``2`` and
``3`` does not have a matching parenthesis).  In this case, all we need to do
is start at the beginning of the string and increment/decrement the counter
in the same manner as described above.  *If the counter ever becomes negative,
then all brackets in the string are not matched pairs*.

**Applying the Algorithm to Different Types of Brackets**
The bracket-matching algorithm is *applicable to any types of brackets, including
parentheses, square brackets, braces, or any arbitrary choice of opening and
closing character as long as the opening and closing characters are different*.
Additionally, we *can apply the same algorithm to a given string repeatedly*.
This allows us, for instance, to verify that all parentheses, square brackets,
and braces occur exclusively in matched pairs.

**Finding the Matching Bracket, Searching Backward**
The bracket-matching algorithm described above can be used in almost identical
form to search a string for a matching bracket from right to left.  The only
change that must be made is to *increase the counter by one when we encounter
a closing bracket and decrease the counter by one when we encounter an
opening bracket*.
