.. include:: ../../constants.rst

.. spelling:word-list::

    txt


.. _section-examples_files_custom_class:

Files 2: Creating Custom File Classes
=====================================

This example will illustrate how to create a custom derived class from
:py:class:`pyxx.files.File` that can read, write, and parse files of a
user-defined format.

.. important::

    Prior to reading this example, it is recommended that you review the
    :ref:`section-file_concepts` page.  This provides important context on
    the philosophy and data structure of :py:class:`pyxx.files.TextFile`
    that will be extended in this example.

To follow along with these examples, begin by opening a Python terminal and
importing the |PackageNameStylized| package:

>>> import pyxx


Sample Problem
--------------

For this tutorial, suppose that we want to parse a file that contains a list of
constants with units, removing any comments from the file and storing the values
and units in a :py:class:`dict`.

A sample of such a file is shown below.  To begin, copy this content into a
file in your working directory.

.. code-block:: ini
    :name: sample_custom_parser_file
    :caption: my_custom_file.txt

    # Estimated value of pi
    PI = 3.14159

    # Estimated value of Euler's number
    e = 2.71828

    # Speed of light in a vacuum
    C = 3e8 m/s

.. testsetup::

    with open('my_custom_file.txt', 'w', encoding='utf_8') as file:
        _ = file.write('\n'.join([
            '# Estimated value of pi',
            'PI = 3.14159',
            '',
            '# Estimated value of Euler\'s number',
            'e = 2.71828',
            '',
            '# Speed of light in a vacuum',
            'C = 3e8 m/s',
        ]) + '\n')


Defining the Custom Class
-------------------------

To process this file, create a class similar to below.

.. code-block:: python
    :linenos:

    class ConstantVariablesFile(pyxx.files.TextFile):
        def __init__(self, path = None):
            super().__init__(path = None, comment_chars='#')

            # Initialize a dictionary to store the constants defined in the file
            self.variables = {}

            # If the user provided a file path, read and parse the file
            if path is not None:
                self.read(path, parse=True)

        def parse(self):
            """This method needs to translate content from "self.contents"
            to other class attributes (e.g., the "variables" dictionary)"""

            # First, remove comments and unnecessary whitespace from the file
            self.clean_contents(remove_comments=True, remove_blank_lines=True,
                                concat_lines=True, strip=True)

            # Next, read the remaining lines of the file
            for line in self.contents:
                key, value_with_unit = line.split('=', maxsplit=1)
                value_with_unit = value_with_unit.strip().split(maxsplit=1) + [None]

                key = key.strip()
                value = value_with_unit[0]
                units = value_with_unit[1]

                self.variables[key] = (value, units)

        def update_contents(self):
            """This method needs to translate content from custom attributes (e.g.,
            the "variables" dictionary) to the "self.contents" attribute"""

            # Remove any existing content in "self.contents"
            self.contents.clear()

            # Populate "self.contents" with all recorded constants
            for key, (value, units) in self.variables.items():
                line = f'{key} = {value}'

                if units is not None:
                    line += f' {units}'

                self.contents.append(line)

.. testsetup::

    class ConstantVariablesFile(pyxx.files.TextFile):
        def __init__(self, path = None):
            super().__init__(path = None, comment_chars='#')

            # Initialize a dictionary to store the constants defined in the file
            self.variables = {}

            # If the user provided a file path, read and parse the file
            if path is not None:
                self.read(path, parse=True)

        def parse(self):
            """This method needs to translate content from "self.contents"
            to other class attributes (e.g., the "variables" dictionary)"""

            # First, remove comments and unnecessary whitespace from the file
            self.clean_contents(remove_comments=True, remove_blank_lines=True,
                                concat_lines=True, strip=True)

            # Next, read the remaining lines of the file
            for line in self.contents:
                key, value_with_unit = line.split('=', maxsplit=1)
                value_with_unit = value_with_unit.strip().split(maxsplit=1) + [None]

                key = key.strip()
                value = value_with_unit[0]
                units = value_with_unit[1]

                self.variables[key] = (value, units)

        def update_contents(self):
            """This method needs to translate content from custom attributes (e.g.,
            the "variables" dictionary) to the "self.contents" attribute"""

            # Remove any existing content in "self.contents"
            self.contents.clear()

            # Populate "self.contents" with all recorded constants
            for key, (value, units) in self.variables.items():
                line = f'{key} = {value}'

                if units is not None:
                    line += f' {units}'

                self.contents.append(line)

Let's take a look at how this class is set up and what each method is doing.

``__init__()``
^^^^^^^^^^^^^^

This is constructor, called when the object is created.

The first action performed is to call the parent class constructor, which stores
the ``path`` argument and comment characters.  Notice that in this case, we assume
that for our custom file, comments always use ``#`` characters, so this is
hard-coded in Line 3 and will be adopted for all ``ConstantVariablesFile`` objects.

The second action in Line 6 is to create a public attribute ``variables`` and initialize
it to an empty dictionary.  This will be the data structure in which the physical
constants read from files like the :ref:`previous example <sample_custom_parser_file>`
will be stored.

The third action performed in Lines 9-10 is to read and parse the file, if the
user provided the file's path.  Including this allows users to either create an
an "empty" file by calling:

>>> my_file = ConstantVariablesFile()

Or, the file can be parsed and the ``variables`` dictionary populated when
initializing the object by calling the constructor and supplying the ``path``
argument:

>>> my_file = ConstantVariablesFile('my_custom_file.txt')


``parse()``
^^^^^^^^^^^

This method is fairly straightforward -- as discussed on the
:ref:`section-file_concepts` page, we simply need to override the parent
class's ``parse()`` method and implement custom code to extract relevant data
from the :py:attr:`pyxx.files.TextFile.contents` list and save it as object
attributes (in this case, save it into our ``variables`` dictionary).

For this example, we first remove comments and unnecessary whitespace by
calling the parent class's :py:meth:`pyxx.files.TextFile.clean_contents` in
Lines 17-18.  Note that this is one of the key benefits and the main motivation
behind the :py:mod:`pyxx.files` module -- rather than having to write custom
code for every file to perform tasks like removing comments, we can simply
reuse the parent class's code.

Once the comments and unnecessary whitespace have been removed, only the list
of constants, values, and units remain in the file.  Lines 21-29 parse these
data and store each variable into the ``variables`` dictionary (assigning
``None`` to variables with no units provided).


``update_contents()``
^^^^^^^^^^^^^^^^^^^^^

This method is also fairly straightforward -- as discussed on the
:ref:`section-file_concepts` page, it essentially performs the reverse of
:py:meth:`pyxx.files.TextFile.parse`: it uses data in object attributes
(such as the ``variables`` dictionary) to populate the
:py:attr:`pyxx.files.TextFile.contents` list with the "current" content
of the file.

In terms of implementation, Line 36 first removes all existing content
from :py:attr:`pyxx.files.TextFile.contents`.  Then, in Lines 39-45, we
iterate through each entry in the ``variables`` dictionary, saving it to
the file contents in the format ``VARIABLE = VALUE [UNITS]``.


Using the Custom Class
----------------------

First, let's create a new ``ConstantVariablesFile`` object and read the data
from the :ref:`example file <sample_custom_parser_file>` created previously:

>>> my_file = ConstantVariablesFile('my_custom_file.txt')
>>> print(my_file.variables)
{'PI': ('3.14159', None), 'e': ('2.71828', None), 'C': ('3e8', 'm/s')}

The key advantage of using a :py:class:`pyxx.files.File` object is that now
that we've parsed the file content, we can interact with the file through
high-level Python attributes, rather than directly parsing and editing the
text of the file.  For instance, suppose we wanted to remove ``e`` from the
file.  We could do this by simply editing the ``variables`` dictionary:

>>> del my_file.variables['e']
>>> my_file.update_contents()
>>> print(my_file.contents)
['PI = 3.14159', 'C = 3e8 m/s']

Similarly, if we wanted to increase the precision of the definition of
pi, we could simply perform:

>>> my_file.variables['PI'] = (3.141592653589793, None)
>>> my_file.update_contents()
>>> print(my_file.contents)
['PI = 3.141592653589793', 'C = 3e8 m/s']

Now that we've made some modifications, we might want to save the modified file.
The following command will write our modified file to ``my_new_file.txt``:

>>> my_file.write('my_new_file.txt')

Alternatively, we might want to overwrite the original file with our changes.
This can be accomplished by:

>>> my_file.overwrite()

If you open ``my_custom_file.txt``, you should now notice that the content has
changed and reflects the modifications we made to the file content.


.. testcleanup::

    import os
    os.remove('my_custom_file.txt')
    os.remove('my_new_file.txt')
