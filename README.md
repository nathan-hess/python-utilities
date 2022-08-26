# PyXX: Python Utilities Package

## Overview

PyXX bundles a collection of Python utilities useful for a variety of projects.  It is intended to accelerate development of Python code by providing ready-to-use, tested objects and functions for tasks commonly encountered in code development projects, reducing the need to duplicate code between projects.


## Features

A number of different general-purpose tools are provided.  Some of the tools provided by PyXX include:
- **Unit Converter**: Components to support a fully customizable unit converter.  Users can define arbitrary units and systems of units.  Functions are available to parse and simplify complex units (such as `(kg*(m/s)^2)/(m^3)`).
- **String Parsers**: Can assist in a number of string-parsing tasks, particularly related to scientific applications.  For instance, functions are available to analyze a string such as `((x-2)/4)^(-1)` and determine which parentheses form matched pairs.
- **File Processors**: Objects are available to perform useful file I/O and processing operations, such as removing comments from files and computing file hashes.
- **Dictionaries**: A customized version of Python's built-in `dict` objects is available.  This class provides greater flexibility in managing and searching dictionary content, and subclasses provide functionality tailored to storing particular types of data, such as lists of files and information needed for unit conversions.


## Installation

The easiest way to install PyXX is through [pip](https://pypi.org/project/pyxx/):

```
pip install pyxx
```

For more information about configuring Python and using packages, refer to the official Python documentation on [setting up Python](https://docs.python.org/3/using/index.html) and [installing packages](https://packaging.python.org/en/latest/tutorials/installing-packages/).


## Documentation

Detailed documentation for the PyXX project can be found here: http://pyxx.readthedocs.io/.
