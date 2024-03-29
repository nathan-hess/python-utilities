.. spelling:word-list::

   args
   BinaryFile
   ConstantUnitMathConventions
   dev
   exps
   InterruptibleLoop
   ndarray
   np
   num
   TextFile
   TimeIt
   TypedList
   TypedListWithID
   UnitConverter
   UnitConverterEntry
   UnitConverterSI
   UnitLinear
   UnitLinearSI
   UnitSystem
   UnitSystemSI


{{ fullname | escape | underline}}

.. currentmodule:: {{ module }}

.. autoclass:: {{ objname }}

   {%- set attributes_non_inherited = [] %}
   {%- set attributes_inherited = [] %}

   {%- for item in attributes %}
      {%- if item not in inherited_members %}
         {{- attributes_non_inherited.append(item) or '' }}
      {%- else %}
         {{- attributes_inherited.append(item) or '' }}
      {%- endif %}
   {%- endfor %}


   {%- set methods_non_inherited = [] %}
   {%- set methods_inherited = [] %}

   {%- for item in methods %}
      {%- if item not in inherited_members %}
         {{- methods_non_inherited.append(item) or '' }}
      {%- else %}
         {{- methods_inherited.append(item) or '' }}
      {%- endif %}
   {%- endfor %}


   {% if attributes_non_inherited %}
   .. rubric:: {{ _('Attributes') }}

   .. autosummary::
   {% for item in attributes_non_inherited %}
      ~{{ name }}.{{ item }}
   {%- endfor %}
   {% endif %}


   {% if methods_non_inherited %}
   .. rubric:: {{ _('Methods') }}

   .. autosummary::
   {% for item in methods_non_inherited %}
      ~{{ name }}.{{ item }}
   {%- endfor %}
   {% endif %}


   {% if attributes_inherited %}
   .. rubric:: {{ _('Inherited Attributes') }}

   .. autosummary::
   {% for item in attributes_inherited %}
      ~{{ name }}.{{ item }}
   {%- endfor %}
   {% endif %}


   {% if methods_inherited %}
   .. rubric:: {{ _('Inherited Methods') }}

   .. autosummary::
   {% for item in methods_inherited %}
      ~{{ name }}.{{ item }}
   {%- endfor %}
   {% endif %}
