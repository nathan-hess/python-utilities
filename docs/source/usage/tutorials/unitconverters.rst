.. include:: ../../constants.rst

.. spelling:word-list::

    UnitConverter


.. _section-tutorials_unitconverters:

Units 2: Unit Converters
========================

Overview
--------

This page explains how to perform unit conversions with the |PackageNameStylized|
unit converters.

.. note::

    Prior to using the unit converters, it is recommended that you review the
    :ref:`section-tutorials_units` page.

There are two primary ways to use the unit converters: with the terminal-based
command-line interface (CLI), or by directly accessing the
:py:class:`pyxx.units.UnitConverter` class, or with command-line interface (CLI).
Throughout this page, use the "CLI" and "UnitConverter Class" tabs, respectively,
to view instructions for each method.


Setup
-----

.. tab-set::

    .. tab-item:: CLI
        :sync: unitconverter_example_cli

        To follow along with these examples, first install the |PackageNameStylized|
        package through pip with the instructions on the :ref:`section-installation`
        page.

        .. code-block:: shell

            pip install pyxx

        For general information and CLI options, run:

        .. code-block:: text

            $ unit-converter --help

    .. tab-item:: UnitConverter Class
        :sync: unitconverter_example_class

        To follow along with these examples, begin by opening a Python terminal
        and importing the |PackageNameStylized| package:

        >>> import pyxx

        Then, create an instance of the :py:class:`pyxx.units.UnitConverter`
        class or a subclass.  For this example, we'll use the
        :py:class:`pyxx.units.UnitConverterSI` class, as it contains a set of
        pre-defined units which will make it easier to demonstrate the
        functionality of the class:

        >>> unit_converter = pyxx.units.UnitConverterSI()


Performing Unit Conversions
---------------------------

.. tab-set::

    .. tab-item:: CLI
        :sync: unitconverter_example_cli

        The unit converter CLI ships with a pre-defined set of common units, listed
        on the :ref:`section-unitconverter_units` page.  Unit conversions can be
        performed between any such units.

        To perform unit conversions, use the ``unit-converter convert`` command.
        The units from and to which to perform the conversion should be specified
        using the ``-f``/``--from`` and ``-t``/``--to`` flags, respectively, and the
        quantity to be converted should be provided as a positional argument.

        For instance, to convert :math:`60\ mi/hr` to :math:`ft/s`, run:

        .. code-block:: text

            $ unit-converter convert --from mi/hr --to ft/s 60
            88.0

        It's also possible to use shortened versions of the command to reduce the
        amount of text that users must enter.  For example, the previous unit
        conversion can be equivalently performed using:

        .. code-block:: text

            $ unit-converter c -f mi/hr -t ft/s 60
            88.0

        To convert multiple quantities at once, provide a comma-separated list of
        values to convert.  For example, to convert :math:`1,\ 2,\ 5` inches to
        centimeters, run:

        .. code-block:: text

            $ unit-converter convert -f in -t cm "1,2,5"
            2.54,5.08,12.7

        For more information and options for unit conversions using the CLI, run:

        .. code-block:: text

            $ unit-converter convert --help

    .. tab-item:: UnitConverter Class
        :sync: unitconverter_example_class

        The :py:class:`pyxx.units.UnitConverterSI` class contains a pre-defined
        set of common units, listed on the :ref:`section-unitconverter_units`
        page.  Unit conversions can be performed between any such units.

        To perform unit conversions, use the :py:meth:`pyxx.units.UnitConverterSI.convert`
        method.  The units from and to which to perform the conversion should be specified
        as strings.

        For instance, to convert :math:`60\ mi/hr` to :math:`ft/s`, run:

        >>> print( unit_converter.convert(60, from_unit='mi/hr', to_unit='ft/s') )
        88.0

        To convert multiple quantities at once, provide a the values as a list,
        tuple, or NumPy array.  For example, to convert :math:`1,\ 2,\ 5` inches
        to centimeters, run:

        >>> print( unit_converter.convert([1, 2, 5], from_unit='in', to_unit='cm') )
        [ 2.54  5.08 12.7 ]


Searching for Units
-------------------

There can potentially be a large number of units defined in a unit converter,
and when performing a unit conversion, it may be useful to search the defined
units to see whether the unit(s) you need are available.

.. tab-set::

    .. tab-item:: CLI
        :sync: unitconverter_example_cli

        The ``unit-converter search`` command (or ``unit-converter s`` for
        short) allows users to search the unit converter.  For instance,
        suppose we want to search for "millimeter."  The most basic search
        would be to run:

        .. code-block:: text

            $ unit-converter search millimeter
            Key            Name          Tags          base_unit_exps            Description
            --------------------------------------------------------------------------------
            mm             millimeter    ['length']    [1. 0. 0. 0. 0. 0. 0.]    None
            millimeter     millimeter    ['length']    [1. 0. 0. 0. 0. 0. 0.]    None
            millimeters    millimeter    ['length']    [1. 0. 0. 0. 0. 0. 0.]    None

        We may want greater control over search results.  For instance, considering
        the above output, notice that several units representing millimeters are
        displayed.  These are all aliases of the same unit, so in order to avoid
        showing duplicates, we can use the ``--hide-aliases`` flag:

        .. code-block:: text

            $ unit-converter search --hide-aliases millimeter
            Key    Name          Tags          base_unit_exps            Description
            ------------------------------------------------------------------------
            mm     millimeter    ['length']    [1. 0. 0. 0. 0. 0. 0.]    None

        We might also want to search only certain fields, which can be done using the
        ``--search-fields`` flag, providing either a single field or a comma-separated
        list of fields to include in the search results.  For example, to search only
        the "key" field, run:

        .. code-block:: text

            $ unit-converter search --search-fields=key millimeter
            Key            Name          Tags          base_unit_exps            Description
            --------------------------------------------------------------------------------
            millimeter     millimeter    ['length']    [1. 0. 0. 0. 0. 0. 0.]    None
            millimeters    millimeter    ['length']    [1. 0. 0. 0. 0. 0. 0.]    None

        Notice that now, only entries with the phrase "millimeter" in the "key" field
        are displayed.

        Another useful option is to restrict search results to only a specific tag.
        This can be accomplished using the ``--filter-by-tags`` flag and providing either
        a single tag or a comma-separated list of tags.

        Additionally, to match all units, a wildcard can be specified as ``*`` or ``**``.
        Note that a wildcard should not be specified as part of a string; for instance,
        searching for ``milli**`` is not valid.

        As an example, combining a wildcard with filtering by tags, if we wanted to view
        all units with the "length" and "time" tags, we could run:

        .. code-block:: text

            $ unit-converter search --filter-by-tags=length,time '*'
            Key            Name          Tags          base_unit_exps            Description
            --------------------------------------------------------------------------------
            m              meter         ['length']    [1. 0. 0. 0. 0. 0. 0.]    None
            meter          meter         ['length']    [1. 0. 0. 0. 0. 0. 0.]    None
            ...

        For more information and options for searching units with the CLI, run:

        .. code-block:: text

            $ unit-converter search --help

    .. tab-item:: UnitConverter Class
        :sync: unitconverter_example_class

        The :py:meth:`pyxx.units.UnitConverterSI.search` method allows users to
        search a unit converter's defined units.  By default, results are printed
        to the terminal, although it is possible (using the ``return_results``
        argument) to return a list of search results for use in scripts.

        Suppose we want to search for "millimeter."  The most basic search would
        be to run:

        >>> unit_converter.search('millimeter')
        Key            Name          Tags          base_unit_exps            Description
        --------------------------------------------------------------------------------
        mm             millimeter    ['length']    [1. 0. 0. 0. 0. 0. 0.]    None
        millimeter     millimeter    ['length']    [1. 0. 0. 0. 0. 0. 0.]    None
        millimeters    millimeter    ['length']    [1. 0. 0. 0. 0. 0. 0.]    None

        We may want greater control over search results.  For instance, considering
        the above output, notice that several units representing millimeters are
        displayed.  These are all aliases of the same unit, so in order to avoid
        showing duplicates, we can use the ``hide_aliases`` argument:

        >>> unit_converter.search('millimeter', hide_aliases=True)
        Key    Name          Tags          base_unit_exps            Description
        ------------------------------------------------------------------------
        mm     millimeter    ['length']    [1. 0. 0. 0. 0. 0. 0.]    None

        We might also want to search only certain fields, which can be done using the
        ``search_fields`` argument, providing either a single field or a list of fields to
        include in the search results.  For example, to search only the "key" field, run:

        >>> unit_converter.search('millimeter', search_fields='key')
        Key            Name          Tags          base_unit_exps            Description
        --------------------------------------------------------------------------------
        millimeter     millimeter    ['length']    [1. 0. 0. 0. 0. 0. 0.]    None
        millimeters    millimeter    ['length']    [1. 0. 0. 0. 0. 0. 0.]    None

        Notice that now, only entries with the phrase "millimeter" in the "key" field
        are displayed.

        Another useful option is to restrict search results to only a specific tag.
        This can be accomplished using the ``filter_by_tags`` argument and providing either
        a single tag or a list of tags.

        Additionally, to match all units, a wildcard can be specified as ``*`` or ``**``.
        Note that a wildcard should not be specified as part of a string; for instance,
        searching for ``milli**`` is not valid.

        As an example, combining a wildcard with filtering by tags, if we wanted to view
        all units with the "length" and "time" tags, we could run:

        >>> unit_converter.search('*', filter_by_tags=['length', 'time'])  # doctest: +SKIP
        Key            Name          Tags          base_unit_exps            Description
        --------------------------------------------------------------------------------
        m              meter         ['length']    [1. 0. 0. 0. 0. 0. 0.]    None       
        meter          meter         ['length']    [1. 0. 0. 0. 0. 0. 0.]    None
        ...


Viewing Detailed Information about a Unit
-----------------------------------------

.. tab-set::

    .. tab-item:: CLI
        :sync: unitconverter_example_cli

        The ``unit-converter info`` command (or ``unit-converter i`` for
        short) displays detailed information about a unit in the unit converter.
        Units should be referenced by their "key", the unique identifier for
        the unit.
        
        For example, to view detailed information about the unit of seconds (key
        "s"), run:

        .. code-block:: text

            $ unit-converter info s
            Unit ID:          s
            Name:             second
            Description:      None
            Tags:             ['time']
            Aliases:          ['sec', 'second', 'seconds']
            Unit definition:  [0. 1. 0. 0. 0. 0. 0.] - scale: 1.0 - offset: 0.0

        For more information and options for searching units with the CLI, run:

        .. code-block:: text

            $ unit-converter info --help

    .. tab-item:: UnitConverter Class
        :sync: unitconverter_example_class

        The simplest way to view information about a unit is to simply print that
        unit's entry in the :py:class:`pyxx.units.UnitConverter` instance.  For
        example, to view information about units of seconds, run:

        >>> print( unit_converter['s'] )
        <class 'pyxx.units.classes.unitconverter.UnitConverterEntry'>
        -- Name: second
        -- Tags: ['time']
        -- Unit: [0. 1. 0. 0. 0. 0. 0.] - scale: 1.0 - offset: 0.0

        Additionally, the list of aliases for a unit can be obtained using the
        :py:meth:`pyxx.units.UnitConverter.get_aliases` method:

        >>> print( unit_converter.get_aliases('s') )
        ['sec', 'second', 'seconds']


Adding and Removing Units
-------------------------

.. tab-set::

    .. tab-item:: CLI
        :sync: unitconverter_example_cli

        Adding and removing units is not supported for the unit converter CLI.
        If custom units need to be defined in the unit converter, use the
        :py:class:`pyxx.units.UnitConverter` class.

    .. tab-item:: UnitConverter Class
        :sync: unitconverter_example_class

        Suppose that we want to add a new unit to the unit converter:

        >>> newUnit = pyxx.units.UnitLinearSI(
        ...     base_unit_exps=[1, 0, 1, 0, 1, 0, 1],
        ...     scale=1000, offset=0
        ... )

        For questions about how to define units, refer to the
        :ref:`section-tutorials_units` page.

        Every item in a :py:class:`pyxx.units.UnitConverter` must be an instance
        of :py:class:`pyxx.units.UnitConverterEntry`.  We can create such an
        object using:

        >>> newUnit_entry = pyxx.units.UnitConverterEntry(
        ...    unit=newUnit, name='newUnit', description='A demo unit')

        The :py:class:`pyxx.units.UnitConverter` class inherits from Python's
        built-in :py:class:`dict` class, so any of the methods that for
        managing items in a Python dictionary can be used for the
        |PackageNameStylized| unit converters.
        
        First, verify that our new unit is not already in the unit converter:

        >>> print( 'newUnit' in unit_converter )
        False

        Next, add the new unit to the unit converter:

        >>> unit_converter['newUnit'] = newUnit_entry

        Again, verify that the unit has been added:

        >>> print( 'newUnit' in unit_converter )
        True

        The unit can be removed from the unit converter using:

        >>> del unit_converter['newUnit']

        Finally, verify that the unit has been removed successfully:

        >>> print( 'newUnit' in unit_converter )
        False
