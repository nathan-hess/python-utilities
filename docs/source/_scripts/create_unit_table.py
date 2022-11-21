"""Adds a table to the documentation containing all the units defined by
default in the PyXX unit converter CLI and the :py:class:`UnitConverterSI`
class.  This table is constructed based on the PyXX source code, so it is
automatically updated if units are added or removed.
"""

import pathlib

from pyxx.arrays.functions.convert import convert_to_tuple
from pyxx.units.classes.constants import SAMPLE_SI_UNITS


DOCS_DIR = pathlib.Path(__file__).resolve().parents[2]

def main():
    print('Creating unit table...', end='')

    # Settings
    path_io = DOCS_DIR / 'source' / 'getting_started' / 'reference'
    input_file = path_io / 'unitconverter_units.rst.template'
    output_file = path_io / 'unitconverter_units.rst'

    # Read input (template) file
    with open(input_file, 'r', encoding='utf_8') as fileID:
        template_lines = fileID.readlines()

    # Copy file, replacing `[[INSERT_UNIT_TABLE]]` with the table of units
    with open(output_file, 'w', encoding='utf_8') as fileID:
        for line in template_lines:
            if line.strip() == '[[INSERT_UNIT_TABLE]]':
                for key, unit_data in SAMPLE_SI_UNITS.items():
                    fileID.write(f'    * - ``{key}``\n')

                    if 'name' in unit_data and (unit_data['name'] is not None):
                        fileID.write(f'      - {unit_data["name"]}\n')
                    else:
                        fileID.write('      -\n')

                    if 'description' in unit_data \
                            and (unit_data['description'] is not None):
                        fileID.write(f'      - {unit_data["description"]}\n')
                    else:
                        fileID.write('      -\n')

                    if 'tags' in unit_data and (unit_data['tags'] is not None):
                        unit_tags = convert_to_tuple(unit_data['tags'])

                        if len(unit_tags) > 0:
                            output_tags = ''
                            for i, tag in enumerate(unit_tags):
                                output_tags += f'{", " if i > 0 else ""}``{tag}``'
                            fileID.write(f'      - {output_tags}\n')
                        else:
                            fileID.write('      -\n')
                    else:
                        fileID.write('      -\n')

                    if 'aliases' in unit_data and (unit_data['aliases'] is not None):
                        unit_aliases = convert_to_tuple(unit_data['aliases'])

                        if len(unit_aliases) > 0:
                            output_aliases = ''
                            for i, alias in enumerate(unit_aliases):
                                output_aliases += f'{", " if i > 0 else ""}``{alias}``'
                            fileID.write(f'      - {output_aliases}\n')
                        else:
                            fileID.write('      -\n')
                    else:
                        fileID.write('      -\n')
            else:
                fileID.write(line)

    print('Done')
