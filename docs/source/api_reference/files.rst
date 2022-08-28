pyxx.files
==========

.. automodule:: pyxx.files

.. currentmodule:: pyxx.files


File Objects
------------

The classes below are intended to represent files (existing on the file system
or not).  Once a class instance is created, various read/write and content
processing methods are available to perform common file-related tasks.

.. autosummary::
    :toctree: ./api
    :template: ../_templates/api_reference_files_classes.rst

    BinaryFile
    File
    TextFile

.. inheritance-diagram:: File BinaryFile TextFile
    :parts: 1


File Hashes
-----------

The functions in this section can be used to compute and analyze file hashes.

.. autosummary::
    :toctree: ./api

    compute_file_hash