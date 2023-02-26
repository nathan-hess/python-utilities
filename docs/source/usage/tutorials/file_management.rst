.. include:: ../../constants.rst

.. spelling:word-list::

    aren
    ini
    txt
    ve


.. _section-tutorials_files_basic:

Files 1: Basic File Management
==============================

This page will explain how to perform basic file tasks such as computing file
hashes and removing comments from text files.

.. note::

    Prior to reading this example, it is recommended that you review the
    :ref:`section-file_concepts` page.

In general, files can be divided into two main categories: binary files and text
files.  Some operations, such as computing file hashes, are valid for either type
of file, and the :ref:`first section <section-example_files_basic-arbitrary>` of
this page will focus on such examples.  There are also operations that are only
valid for text files, such as removing whitespace and comments.  These will be
discussed in the :ref:`second section <section-example_files_basic-text>` of
this page.

To follow along with these examples, begin by opening a Python terminal and
importing the |PackageNameStylized| package:

>>> import pyxx


.. _section-example_files_basic-arbitrary:

Arbitrary Files
---------------

The following actions are available to any type of file (binary or text).


Computing File Hashes
^^^^^^^^^^^^^^^^^^^^^

As described in the :ref:`Concepts <section-file_concepts>` section, |PackageNameStylized|
does not assume that the files it is processing are necessarily present on the disk.
However, *if* the file is indeed present on the disk, certain operations such as computing
file hashes are possible.

Let's see how to use |PackageNameStylized| to compute file hashes.  To begin, create a
file with the following content in your working directory:

.. code-block:: text
    :caption: example_hashes_file.txt
    :name: file-example_hashes_file

    abcdefghijklmnopqrstuvwxyz
    0123456789

Make sure that you use LF line endings and that your file has a trailing newline
(``\n`` should be the last character of the file).

.. testsetup::

    with open('example_hashes_file.txt', 'w', encoding='utf_8', newline='\n') as file:
        _ = file.write('abcdefghijklmnopqrstuvwxyz\n')
        _ = file.write('0123456789\n')

First, create a new :py:class:`pyxx.files.File` object and record the file's path:

>>> file01 = pyxx.files.File(path='example_hashes_file.txt')

The file hashes are stored in the :py:attr:`pyxx.files.File.hashes` attribute.  By
default, |PackageNameStylized| does not automatically compute these hashes (since
the file may or may not exist).  Thus, for our file, this attribute is currently
empty:

>>> print(file01.hashes)
{}

However, we can easily compute and store the file hashes, optionally specifying
which hash algorithms we want (in this case, MD5):

>>> file01.store_file_hashes('md5')
>>> print(file01.hashes)
{'md5': '1c4869372601e354523a6f0dbc4dde55'}

By default, MD5 and SHA256 hashes are computed:

>>> file01.store_file_hashes()
>>> print(file01.hashes.keys())
dict_keys(['md5', 'sha256'])

There can also be cases in which we may want to view the file's hashes but not
store them in :py:attr:`pyxx.files.File.hashes`.  This can be easily
accomplished using:

>>> print(file01.compute_file_hashes('sha224', store=False))
{'sha224': 'bdab73e6764007235911384ca047daf20e708478c367964f21e965af'}


Checking Whether Files are Identical
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

File hashes are often used to identify whether two files are identical.
|PackageNameStylized| provides convenient methods for performing such analysis.

To check whether two files are identical, simply compare the files'
:py:attr:`pyxx.files.File.hashes` attributes.  For instance, suppose that in
addition to our :ref:`previous file <file-example_hashes_file>`, we now
create a new file:

.. code-block:: text
    :caption: new_hashes_file.txt

    This file is not identical
    to the previously created file.

.. testsetup::

    with open('new_hashes_file.txt', 'w', encoding='utf_8', newline='\n') as file:
        _ = file.write('This file is not identical\n')
        _ = file.write('to the previously created file.\n')

Now, we can compare the files as illustrated below:

>>> # Create the `pyxx.files.File` objects
>>> file02a = pyxx.files.File(path='example_hashes_file.txt')
>>> file02b = pyxx.files.File(path='new_hashes_file.txt')
>>>
>>> # Compute hashes for both files
>>> file02a.store_file_hashes()
>>> file02b.store_file_hashes()
>>>
>>> # Show that each file is identical to itself
>>> print(file02a.hashes == file02a.hashes)
True
>>> print(file02b.hashes == file02b.hashes)
True
>>>
>>> # Show that files are NOT identical to each other
>>> print(file02a.hashes == file02b.hashes)
False


Testing for File Modifications
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

We may also want to check whether a given file has been modified since the
last time we used it.  This can be helpful, for instance, if parsing the file
is time-consuming -- checking whether it's been modified beforehand can save
unnecessary parsing steps.

Returning to our :ref:`previous file <file-example_hashes_file>`, first make
sure you've saved the file's hashes:

>>> file01.store_file_hashes()

The :py:meth:`pyxx.files.File.has_changed` method determines whether a file
has changed since the last time its hashes were stored.  Since we haven't
altered the file, we can see that calling this method shows no changes:

>>> print(file01.has_changed())
False

However, suppose that we edit the file:

>>> with open('example_hashes_file.txt', 'a') as file:
...     _ = file.write('new file content\n')

Now, we can identify that the file has changed with:

>>> print(file01.has_changed())
True


.. _section-example_files_basic-text:

Text Files
----------

For text files, |PackageNameStylized| provides additional functions that can
be used to parse and modify file contents.


Reading File Contents
^^^^^^^^^^^^^^^^^^^^^

To begin, create a sample `INI file <https://en.wikipedia.org/wiki/INI_file>`__
as shown below:

.. code-block:: ini
    :caption: sample_ini_file.ini

    # Sample INI file

    [section1]
    variable1 = 10  ; comment1
    variable2 = 20  # comment 2
    [section2]
    variable3 = Sphinx

.. testsetup::

    with open('sample_ini_file.ini', 'w', encoding='utf_8', newline='\n') as file:
        _ = file.write('\n'.join([
            '# Sample INI file',
            '',
            '[section1]',
            'variable1 = 10  ; comment1',
            'variable2 = 20  # comment 2',
            '[section2]',
            'variable3 = Sphinx\n',
        ]))

First, we need to create a new :py:class:`pyxx.files.TextFile` instance and
read in the file as follows:

>>> text_file = pyxx.files.TextFile(comment_chars = ('#', ';'))
>>> text_file.read('sample_ini_file.ini')

Notice that ``#`` and ``;`` indicate comments in INI files, so we specified
this property in the constructor with the ``comment_chars`` argument.


Text File ``contents`` Attribute
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The :py:attr:`pyxx.files.TextFile.contents` attribute is a list that stores
each line of the text file.  It is considered to reflect the "current" state
of the data in the file.

When calling :py:meth:`pyxx.files.TextFile.read` as done above, this attribute
is automatically populated with the contents of the text file.  We can see
this using:

>>> print(*text_file.contents, sep='\n')
# Sample INI file
<BLANKLINE>
[section1]
variable1 = 10  ; comment1
variable2 = 20  # comment 2
[section2]
variable3 = Sphinx

.. note::
    For more information about the philosophy behind how data are stored and
    exchanged between attributes of :py:class:`pyxx.files.TextFile` objects
    and the reasoning behind this structure, refer to the
    :ref:`section-file_concepts` section.


In-Place File Editing
^^^^^^^^^^^^^^^^^^^^^

Since the :py:attr:`pyxx.files.TextFile.contents` attribute contains the
"current" file contents and because this property is returned *by reference*,
by simply editing this attribute we can modify the file.

For instance, we could remove the last line with:

>>> last_line = text_file.contents.pop()
>>> print(*text_file.contents, sep='\n')
# Sample INI file
<BLANKLINE>
[section1]
variable1 = 10  ; comment1
variable2 = 20  # comment 2
[section2]

|PackageNameStylized| also provides methods for common text file content
manipulation.  For instance, text files often contain comments, blank lines,
and trailing whitespace that aren't necessary when parsing file data.  We can
easily remove these items from the file by:

>>> text_file.clean_contents(
...     remove_comments=True,
...     remove_blank_lines=True,
...     strip=True
... )
>>> print(*text_file.contents, sep='\n')
[section1]
variable1 = 10
variable2 = 20
[section2]

Notice that both full-line comments and comments on a line containing data
were removed.

Additional file-cleaning options are available, such as concatenating lines
when a line continuation character (``\``) was used to split a long line.
For more information, refer to the :py:meth:`pyxx.files.TextFile.clean_contents`
reference.


Writing Text Files
^^^^^^^^^^^^^^^^^^

After modifying a text file, it's may be necessary to write the modified version
to the disk.

The data in the :py:attr:`pyxx.files.TextFile.contents` attribute can be dumped
to any valid location on the disk using:

>>> text_file.write(output_file='modified_ini_file.ini')

After running this command, you should see a new file with the following contents:

.. code-block:: ini
    :caption: modified_ini_file.ini

    [section1]
    variable1 = 10
    variable2 = 20
    [section2]

There may also be cases in which we want to directly overwrite the original file
with the modified contents.  This can be accomplished by:

>>> text_file.overwrite()

After running this command, your original ``sample_ini_file.ini`` should now have
the following contents:

.. code-block:: ini
    :caption: sample_ini_file.ini

    [section1]
    variable1 = 10
    variable2 = 20
    [section2]


.. testcleanup::

    import os
    os.remove('example_hashes_file.txt')
    os.remove('new_hashes_file.txt')
    os.remove('sample_ini_file.ini')
    os.remove('modified_ini_file.ini')
