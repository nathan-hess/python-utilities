"""This module can be used to process text files
"""

import copy
import pathlib
from typing import List, Optional, Union

from pyxx.arrays.functions.convert import convert_to_tuple
from .file import File


class TextFile(File):
    """Base class for processing text files

    This class can be used to represent text files (that is, files with
    a series of ASCII-based characters as content, that can be open and
    read with an editor such as Notepad).  It provides the capability to
    read/write text files and perform processing operations such as
    removing commented lines.
    """

    def __init__(self, file: Union[str, pathlib.Path],
                 comment_chars: Optional[Union[tuple, str]] = None):
        """Define a text file

        Creates an object that represents and can be used to process
        a text file.

        Parameters
        ----------
        file : str or pathlib.Path
            Path and filename of the text file
        comment_chars : tuple or str, optional
            Character(s) considered to represent comments in the text file
            (default is ``None``, which considers no characters to denote
            comments in the file)
        """
        super().__init__(file)

        self._contents: List[str] = []
        self._raw_contents: List[str] = []
        self._comment_chars = convert_to_tuple(comment_chars)

    @property
    def comment_chars(self):
        """A tuple of all characters considered to denote comments"""
        return self._comment_chars

    @property
    def contents(self):
        """A copy of the file content

        Returns a list containing the text on each line of the file.  Note
        that this list may have been modified when cleaning the file contents.
        """
        return copy.deepcopy(self._contents)

    @property
    def raw_contents(self):
        """A copy of the raw file content

        Returns a list containing the original text on each line of the file.
        """
        return copy.deepcopy(self._raw_contents)

    @property
    def trailing_newline(self):
        """Whether the original file had a newline at the end
        of the file"""
        return self._raw_contents[-1].endswith('\n')

    def clean_contents(self,
            remove_comments: bool = True,           # noqa : E128
            skip_full_line_comments: bool = False,  # noqa : E128
            strip: bool = True,                     # noqa : E128
            concat_lines: bool = True,              # noqa : E128
            remove_blank_lines: bool = True):       # noqa : E128
        """Clean :py:attr:`contents` in-place

        Cleans :py:attr:`contents` (removing comments, blank lines, etc.)
        based on user-defined rules.  Modifications are made in-place
        (i.e., the resulting content is stored in :py:attr:`contents`).

        Parameters
        ----------
        remove_comments : bool, optional
            Whether to remove comments from file (default is ``True``)
        skip_full_line_comments : bool, optional
            Whether to skip removing comments where the comment is the only
            text on a line.  Only applies if ``remove_comments`` is ``True``
            (default is ``False``)
        strip : bool, optional
            Whether to strip leading and trailing whitespace from each
            line (default is ``True``)
        concat_lines : bool, optional
            Whether to concatenate lines ending with a backslash with the
            following line (default is ``True``)
        remove_blank_lines : bool, optional
            Whether to remove lines that contain no content after other
            cleaning operations have completed (default is ``True``)
        """
        # Store original file contents
        orig_contents = self.contents

        # Clean file line-by-line
        self._contents = []
        i = 0
        while (i < len(orig_contents)):
            line = orig_contents[i]

            # If line ends with "\", concatenate with next line
            if concat_lines:
                while (line.strip().endswith('\\') and (i < len(orig_contents))):
                    line = line.rsplit('\\', maxsplit=1)[0] + orig_contents[i+1]
                    i += 1

            # Remove comments
            if remove_comments:
                if not (skip_full_line_comments
                        and line.strip().startswith(self.comment_chars)):
                    for comment_char in self.comment_chars:
                        line = line.split(comment_char, maxsplit=1)[0]

            # Strip whitespace from beginning and end of line
            if strip:
                line = line.strip()

            # Remove blank lines
            if not (remove_blank_lines and len(line.strip()) == 0):
                self._contents.append(line)

            i += 1

    def read(self):
        """Read file from disk

        Calling this method reads the file specified by the :py:attr:`file`
        attribute from the disk, populating :py:attr:`contents` and
        :py:attr:`raw_contents`.  Additionally, the file hashes stored in
        the :py:attr:`hashes` attribute are updated (to make it easier to
        check if the file has been modified later).
        """
        # Compute and store file hashes
        super().store_file_hashes()

        # Read file
        with open(self.file, 'r', encoding='utf_8') as fileID:
            self._raw_contents = fileID.readlines()

        # Remove trailing newlines.  This is beneficial because if the
        # file is later cleaned and, for example, comments are removed,
        # this can result in an unpredictable mix of lines with trailing
        # newlines and lines without, so it's simpler to remove them all
        # at the beginning and add them when writing the file
        self._contents = [line[:-1] if line.endswith('\n') else line
                          for line in self._raw_contents]

    def write(self, output_file: Union[str, pathlib.Path],
              write_mode: str = 'w', write_raw: bool = False,
              prologue: str = '', epilogue: Optional[str] = None,
              separator: str = '\n', warn_before_overwrite: bool = True):
        """Write file to disk

        Calling this method writes the file contents stored in either
        :py:attr:`contents` or :py:attr:`raw_contents` to the disk.

        Parameters
        ----------
        output_file : str or pathlib.Path
            Output file to which to write content
        write_mode : str, optional
            Any mode (such as ``'w'`` or ``'a'``) for the built-in
            ``open()`` function for writing files (default is ``'w'``)
        write_raw : bool, optional
            Whether to write contents of :py:attr:`raw_contents`.  If set
            to ``False``, the contents of :py:attr:`contents` are written
            (default is ``False``)
        prologue : str, optional
            Content written at beginning of file (default is ``''``)
        epilogue : str, optional
            Content written at end of file (default is ``'\\n'`` if
            :py:attr:`trailing_newline` is ``True`` and ``''`` otherwise)
        separator : str, optional
            String written between each line when writing file content
            (default is ``'\\n'``)
        warn_before_overwrite : bool, optional
            Whether to throw an error if ``output_file`` already exists
            (default is ``True``)
        """
        # Convert output file to `pathlib.Path`
        output_file = pathlib.Path(output_file).expanduser().resolve()

        # Check before overwriting file
        if warn_before_overwrite and output_file.is_file():
            raise FileExistsError(
                f'Output file "{output_file}" already exists')

        # Set epilogue
        if epilogue is None:
            epilogue = '\n' if self.trailing_newline else ''

        # Write output file
        output_content = self.raw_contents if write_raw else self.contents
        with open(output_file, write_mode, encoding='utf_8') as fileID:
            fileID.write(prologue + separator.join(output_content) + epilogue)
