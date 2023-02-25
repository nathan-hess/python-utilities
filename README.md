# PyXX: Python Utilities Package

[![CI/CD](https://github.com/nathan-hess/python-utilities/actions/workflows/cicd.yml/badge.svg)](https://github.com/nathan-hess/python-utilities/actions/workflows/cicd.yml)
[![Documentation Status](https://readthedocs.org/projects/pyxx/badge/?version=latest)](https://pyxx.readthedocs.io)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/pyxx?label=PyPI%20downloads&logo=python&logoColor=yellow)](https://pypi.org/project/pyxx)


## Overview

PyXX bundles a collection of Python utilities useful for a variety of projects.  It is intended to accelerate development of Python code by providing ready-to-use, tested objects and functions for tasks commonly encountered in code development projects, reducing the need to duplicate code between projects.


## Features

A number of different general-purpose tools are provided.  Some of the tools provided by PyXX include:
- **Unit Converter**: Components to support a fully customizable unit converter (including a command-line interface).  Users can define arbitrary units and systems of units.  Functions are available to parse and simplify complex units (such as `(kg*(m/s)^2)/(m^3)`).
- **Array Tools**: A variety of functions are available for common tasks involving lists, tuples, NumPy arrays, and other array-like objects, intended to reduce the need to include duplicate code across projects.  For instance, a Python implementation of lists that enforce homogeneous type (similar to a C++ `std::vector`) is available.
- **File Processors**: A set of Python classes are included, capable of performing file I/O and file processing operations such as removing comments and computing file hashes.  These are intended to serve as a basis for other customized, user-specific applications.
- **String Parsers**: Can assist in a number of string-parsing tasks, particularly related to scientific applications.  For instance, functions are available to analyze a string such as `((x-2)/4)^(-1)` and determine which parentheses form matched pairs.


## Installation

The recommended way to install PyXX is through [pip](https://pypi.org/project/pyxx):

```
pip install pyxx
```

For more information about configuring Python and using packages, refer to the official Python documentation on [setting up Python](https://docs.python.org/3/using/index.html) and [installing packages](https://packaging.python.org/en/latest/tutorials/installing-packages).


## Usage and Documentation

Detailed documentation for the PyXX project can be found here: https://pyxx.readthedocs.io.

The project documentation contains example code, explanation of the concepts behind the package architecture, and detailed API reference.  If you're still not certain how to do something after reading it, feel free to [create a discussion post](https://github.com/nathan-hess/python-utilities/discussions/categories/q-a)!


## Acknowledgments

Project source code is hosted on [GitHub](https://github.com/nathan-hess/python-utilities), releases are distributed through [PyPI](https://pypi.org/project/pyxx), and documentation is hosted through [Read the Docs](https://docs.readthedocs.io/en/stable/index.html).  Some README badges were generated using [Shields.io](https://shields.io).
