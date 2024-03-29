# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import datetime
import pathlib
import shutil
import sys

sys.path.append(str(pathlib.Path(__file__).resolve().parents[2]))
import pyxx
from pyxx.arrays.functions.equality import Array_or_Number_or_String

sys.path.append(str(pathlib.Path(__file__).resolve().parent / '_scripts'))
import create_unit_table


# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'PyXX'
author = 'Nathan Hess'
copyright = f'{datetime.datetime.now().year}'
release = pyxx.__version__
url = 'https://github.com/nathan-hess/python-utilities'


# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

# Add any Sphinx extension module names here, as strings
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.doctest',
    'sphinx.ext.imgconverter',
    'sphinx.ext.inheritance_diagram',
    'sphinx.ext.napoleon',
    'sphinxcontrib.spelling',
    'sphinx_copybutton',
    'sphinx_design',
    'sphinx_remove_toctrees',
    'matplotlib.sphinxext.plot_directive',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# HTML theme
html_theme = 'furo'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Site logo and favicon
html_logo = '_static/logo_header.svg'
html_favicon = '_static/favicon.ico'

# General HTML options
html_title = f'{project} v{release}'
html_last_updated_fmt = '%b %d, %Y'
html_permalinks = True
html_show_sourcelink = False
html_show_sphinx = False

# Pages to exclude from table of contents and navigation bar
remove_from_toctrees = [
    'api_reference/concepts/*',
]

# Theme-specific HTML options
html_theme_options = {
    'source_repository': url,
    'source_branch': 'main',
    'source_directory': 'docs/source/',
}


# -- Other general Sphinx configuration options ------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# Show parentheses after function and method names
add_function_parentheses = True


# -- Spell-checking options --------------------------------------------------
# https://sphinxcontrib-spelling.readthedocs.io/en/latest/

# Spelling language
spelling_lang = 'en_US'
tokenizer_lang = 'en_US'

# Whitelisted words
spelling_word_list_filename = [
    'spelling_wordlist.txt',
]


# -- Sphinx `autodoc` extension options --------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html

# Clean up auto-generated API reference files before building documentation
shutil.rmtree(
    pathlib.Path(__file__).resolve().parent / 'api_reference' / 'api',
    ignore_errors=True)

# Default content when documenting classes
autoclass_content = 'class'

# Default `autodoc` options
autodoc_default_options = {
    'members': True,
    'undoc-members': True,
    'private-members': False,
    'special-members': '__init__',
    'inherited-members': True,
    'member-order': 'bysource',
    'show-inheritance': True,
}

# Type aliases
autodoc_type_aliases = {
    Array_or_Number_or_String: Array_or_Number_or_String,
}


# -- Sphinx `doctest` extension options --------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/doctest.html

# Test code in "standard" reStructuredText blocks (i.e., lines that are not
# inside a `.. doctest::` block but start with `>>>` are tested)
doctest_test_doctest_blocks = 'default'

# Code executed before running test code snippets for all documentation files
doctest_global_setup = 'import pyxx'


# -- Matplotlib plotting extension options -----------------------------------
# https://matplotlib.org/stable/api/sphinxext_plot_directive_api.html

# Source and download links to show with plots
plot_html_show_source_link = False
plot_html_show_formats = False


# -- Code snippet copy button settings ---------------------------------------
# https://sphinx-copybutton.readthedocs.io/en/latest/

# Prevent copying Python prompt (">>>") and continuation ("...") characters
copybutton_prompt_text = r'>>> |\.\.\. |\$ |In \[\d*\]: | {2,5}\.\.\.: | {5,8}: '
copybutton_prompt_is_regexp = True


# -- Custom scripts ----------------------------------------------------------
# Scripts that run pre-processing tasks before building documentation

# Generate table of units used by default in the unit converter CLI and
# `UnitConverterSI` instances
create_unit_table.main()
