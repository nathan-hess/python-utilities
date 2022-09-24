.. include:: ../constants.rst


.. _section-installation:

Installation
============

pip
---

|PackageNameStylized| has been packaged through PyPI, so the easiest way to
install the package is through pip:

.. code-block:: shell

    pip install pyxx


Source Code
-----------

Alternatively, if you prefer to download the source code directly, you can do
so using Git.  First, clone the source repository to a location of your choice:

.. code-block:: shell

    git clone https://github.com/nathan-hess/python-utilities.git

Then, add the root directory of the repository to your ``PYTHONPATH`` environment
variable:

.. tab-set::

    .. tab-item:: Linux / MacOS

        .. code-block:: shell

            export PYTHONPATH="$PYTHONPATH:$(pwd)/python-utilities"

    .. tab-item:: Windows

        .. code-block:: powershell

            set PYTHONPATH=%PYTHONPATH%;%CD%\python-utilities

Finally, make sure to install required dependencies through pip:

.. code-block:: shell

    pip install -r python-utilities/requirements.txt
