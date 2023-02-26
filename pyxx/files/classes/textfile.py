"""This module is used to process text files
"""

import copy
import pathlib
from typing import List, Optional, Tuple, Union

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

    def __init__(self, path: Optional[Union[str, pathlib.Path]] = None,
                 comment_chars: Optional[Union[Tuple[str, ...], str]] = None
                 ) -> None:
        """Define a text file

        Creates an object that represents and can be used to process
        a text file.

        Parameters
        ----------
        path : str or pathlib.Path, optional
            Location of the text file in the file system  (default is ``None``)
        comment_chars : tuple or str, optional
            Character(s) considered to represent comments in the text file
            (default is ``None``, which considers no characters to denote
            comments in the file)

        Notes
        -----
        Passing an empty string (``''``) or empty tuple (``()``) as the
        ``comment_chars`` argument is equivalent to passing ``None`` (or
        not providing this argument) -- in all these cases, the file will
        be considered to have no characters denoting comments.
        """
        super().__init__(path=path)

        # Mypy exclusions in constructor were added as workarounds
        # for python/mypy#3004

        # Initialize lists to store file content
        self._contents: List[str] = []
        self._raw_contents: Union[List[str], None] = None

        # Initialize file properties
        self._line_ending: Union[str, Tuple[str, ...], None] = None
        self.trailing_newline = None  # type: ignore

        # Store comment character
        self.comment_chars = comment_chars  # type: ignore

    def _check_contents(self, contents: List[str]) -> None:
        # Verify that input is a list
        if not isinstance(contents, list):
            raise TypeError('Argument "contents" must be of type "list"')

        # Verify that all elements of the input are strings
        for line in contents:
            if not isinstance(line, str):
                raise TypeError(
                    'All elements of "contents" must be of type "str"')

    @property
    def comment_chars(self) -> Union[Tuple[str, ...], None]:
        """A tuple of all characters considered to denote comments"""
        return self._comment_chars

    @comment_chars.setter
    def comment_chars(self, comment_chars: Union[Tuple[str, ...], str, None]
                      ) -> None:
        if comment_chars is None:
            self._comment_chars = None
        else:
            if isinstance(comment_chars, (str, tuple)):
                if len(comment_chars) == 0:
                    self._comment_chars = None
                else:
                    comment_chars_list = convert_to_tuple(comment_chars)

                    # Make sure every character of comment characters tuple is
                    # a string
                    for item in comment_chars_list:
                        if not isinstance(item, str):
                            raise TypeError(
                                'All comment characters must be of type "str"')

                    self._comment_chars = comment_chars_list
            else:
                raise TypeError(
                    'Argument "comment_chars" must be either `None` or of '
                    'type "str" or "tuple"')

    @property
    def contents(self) -> List[str]:
        """A reference to a list containing the (potentially modified) file
        content of each line of the file

        Warnings
        --------
        This attribute returns the list **by reference**.  This means that
        if you set a variable equal to this reference, then editing this
        variable will edit the :py:attr:`contents` attribute (e.g., if you
        set ``my_content = MyTextFile.contents``, then editing ``my_content``
        will change the content stored in ``MyTextFile``).

        Notes
        -----
        If trying to set the :py:attr:`contents` attribute, do not try to set
        this attribute directly (i.e., don't use code similar to
        ``MyTextFile.contents = ['line1', 'line2', 'line3']``).  Instead, use
        the :py:meth:`set_contents` method, as it offers greater control
        over whether the contents are passed by reference or value.
        """
        return self._contents

    @property
    def line_ending(self) -> Union[str, Tuple[str, ...]]:
        """The character(s) used to denote the end of lines in the text file

        This property only applies to files that were read using the
        :py:meth:`read` method.  After reading a file, this property stores
        the line ending(s) used in the file.  Lines in text files can be
        terminated with ``'\\n'`` (LF), ``'\\r\\n'`` (CRLF), ``'\\r'``, or a
        combination of these characters (potentially with different line
        endings on different lines).

        After reading a file, this property stores either a string containing
        the line endings on every line of the file, or a tuple containing all
        line endings encountered throughout the file.
        """
        if self._line_ending is None:
            raise AttributeError(
                'Attribute "line_ending" has not been set. Please ensure '
                'that either the `read()` method has been called')

        return self._line_ending

    @property
    def raw_contents(self) -> Union[List[str], None]:
        """A copy of the raw file content

        If the file was read using the :py:meth:`read` method, this attribute
        stores the original, unaltered contents of each line of the input
        file, and it returns a copy of this list of lines.  If the file was
        not read with the :py:meth:`read` method, this attribute stores a
        value of ``None``.
        """
        return copy.deepcopy(self._raw_contents)

    @property
    def trailing_newline(self) -> bool:
        """Whether the original file had a newline at the end
        of the file"""
        if self._trailing_newline is None:
            raise AttributeError(
                'Attribute "trailing_newline" has not been set. Please ensure '
                'that either the `read()` or `set_contents()` method has '
                'been called')

        return self._trailing_newline

    @trailing_newline.setter
    def trailing_newline(self, trailing_newline: Union[bool, None]) -> None:
        if trailing_newline is None:
            self._trailing_newline = None
        else:
            self._trailing_newline = bool(trailing_newline)

    def clean_contents(self,
                       remove_comments: bool = False,
                       skip_full_line_comments: bool = False,
                       strip: bool = False,
                       concat_lines: bool = False,
                       remove_blank_lines: bool = False
                       ) -> None:
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
        # Confirm that "contents" attribute hasn't been modified improperly
        self._check_contents(self.contents)

        # Store original file contents
        orig_contents = copy.deepcopy(self.contents)

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
            if remove_comments and (self.comment_chars is not None):
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

    def overwrite(self, prologue: str = '', epilogue: Optional[str] = None,
                  line_ending: str = '\n') -> None:
        """Write data in :py:attr:`contents` to the file specified by
        :py:attr:`path`

        Writes the lines of content in the :py:attr:`contents` attribute to
        the (previously-defined) file specified by the :py:attr:`path`
        attribute, suppressing warnings before overwriting the file.  This
        is useful for cases when the file contents are manually populated and
        it is desired to "dump" them to a file.  This method is also useful if
        a file's contents need to be updated periodically based on the results
        of another process.

        Parameters
        ----------
        prologue : str, optional
            Content written at beginning of file (default is ``''``)
        epilogue : str, optional
            Content written at end of file (default is to use the value of the
            ``line_ending`` argument if :py:attr:`trailing_newline` is
            ``True`` and ``''`` otherwise)
        line_ending : str, optional
            String written at the end of each line when writing file content
            (default is ``'\\n'``)
        """
        if self.path is None:
            raise AttributeError('Attribute "path" must be set to call '
                                 '"overwrite()" method')

        self.write(
            output_file = self.path,
            write_mode = 'w',
            warn_before_overwrite = False,
            prologue = prologue,
            epilogue = epilogue,
            line_ending = line_ending
        )

    def parse(self) -> None:
        """Parses the data in :py:attr:`contents` and stores it in class
        attributes

        This method by default does nothing.  However, it is intended that
        subclasses of :py:class:`TextFile` should override this method and
        define file-specific behavior in this method for extracting data from
        the file and storing it in custom object attributes.

        For example, if defining a CSV-parser, the :py:meth:`parse` method
        might parse data from the file and store it as a NumPy array.
        """
        return None

    def read(self, path: Optional[Union[str, pathlib.Path]] = None,
             parse: bool = True) -> None:
        """Read file from disk

        Calling this method reads the file specified by the :py:attr:`path`
        attribute from the disk, populating :py:attr:`contents` and
        :py:attr:`raw_contents`.  Additionally, the file hashes stored in
        the :py:attr:`hashes` attribute are updated (to make it easier to
        check if the file has been modified later).

        Parameters
        ----------
        path : str or pathlib.Path, optional
            Location of the text file in the file system  (default is ``None``)
        parse : bool, optional
            Whether to call the :py:meth:`parse` method after reading the
            file (default is ``True``)
        """
        # Mypy type annotation added because immediately after calling
        # `set_read_metadata()`, the "path" attribute cannot be `None`
        # or else an error would have been thrown
        self.set_read_metadata(path)
        self.path: pathlib.Path

        # Read file
        with open(self.path, 'r', encoding='utf_8') as fileID:
            self._raw_contents = fileID.readlines()

            # Store line endings
            self._line_ending = fileID.newlines

        # Store whether original file has a trailing newline
        self.trailing_newline = self._raw_contents[-1].endswith('\n')

        # Remove trailing newlines.  This is beneficial because if the
        # file is later cleaned and, for example, comments are removed,
        # this can result in an unpredictable mix of lines with trailing
        # newlines and lines without, so it's simpler to remove them all
        # at the beginning and add them when writing the file
        self._contents = [line.rstrip('\r\n') for line in self._raw_contents]

        # Optionally parse file contents
        if parse:
            self.parse()

    def set_contents(self, contents: List[str], trailing_newline: bool,
                     pass_by_reference: bool = False) -> None:
        """Add data to the :py:attr:`contents` list

        Allows users to manually fill the :py:attr:`contents` list with
        user-defined content.  The input list must be a list of strings,
        and the user can optionally choose whether to pass the input by
        reference or value.

        Parameters
        ----------
        contents : list
            List of strings which are to be assigned to the
            :py:attr:`contents` list
        trailing_newline : bool
            Whether the contents being added represent a file with a trailing
            newline (because the file wasn't read, the object has no way to
            determine whether the file has a trailing newline, so users must
            provide this information)
        pass_by_reference : bool, optional
            Whether to pass the ``contents`` argument by reference (default
            is ``False``)

        Notes
        -----
        If passing ``contents`` by reference, this means that if subsequent
        changes are made to the original ``contents`` object, they will be
        reflected in the :py:attr:`contents` attribute.  If passing by value,
        then a *copy* of the ``contents`` argument will be made, so changing
        the object outside the class instance will not affect the
        :py:attr:`contents` attribute.
        """
        # Verify that input matches required format
        self._check_contents(contents)

        # Store contents
        if pass_by_reference:
            self._contents = contents
        else:
            self._contents = copy.deepcopy(contents)

        # Store whether file has a trailing newline
        if not isinstance(trailing_newline, bool):
            raise TypeError(
                'Argument "trailing_newline" must be of type "bool"')

        self.trailing_newline = trailing_newline

    def update_contents(self) -> None:
        """Updates the :py:attr:`contents` list based on object attributes

        This method by default does nothing.  However, it is intended that
        subclasses of :py:class:`TextFile` should override this method and
        define file-specific behavior in this method for converting custom
        object attributes to lines of text in the file, and storing these
        data in :py:attr:`contents`.

        For example, if defining a CSV-parser, the class might have an
        attribute that stores numerical data in a NumPy array, and the
        :py:meth:`update_contents` method might convert the data in this array
        to comma-separated strings and store them in :py:attr:`contents`.
        """
        return None

    def write(self, output_file: Union[str, pathlib.Path],
              write_mode: str = 'w', warn_before_overwrite: bool = True,
              prologue: str = '', epilogue: Optional[str] = None,
              line_ending: str = '\n', update_contents: bool = True,
              ) -> None:
        """Write file to disk

        Calling this method writes the file contents stored in
        :py:attr:`contents` to the disk.

        Parameters
        ----------
        output_file : str or pathlib.Path
            Output file to which to write content
        write_mode : str, optional
            Any mode (such as ``'w'`` or ``'a'``) for the built-in
            ``open()`` function for writing files (default is ``'w'``)
        warn_before_overwrite : bool, optional
            Whether to throw an error if ``output_file`` already exists
            (default is ``True``)
        prologue : str, optional
            Content written at beginning of file (default is ``''``)
        epilogue : str, optional
            Content written at end of file (default is to use the value of the
            ``line_ending`` argument if :py:attr:`trailing_newline` is
            ``True`` and ``''`` otherwise)
        line_ending : str, optional
            String written at the end of each line when writing file content
            (default is ``'\\n'``)
        update_contents : bool, optional
            Whether to call the :py:meth:`update_contents` method before
            writing the file (default is ``True``)
        """
        # Update contents from file attributes
        if update_contents:
            self.update_contents()

        # Confirm that "contents" attribute hasn't been modified improperly
        self._check_contents(self.contents)

        # Convert output file to `pathlib.Path`
        output_file = pathlib.Path(output_file).expanduser().resolve()

        # Check before overwriting file
        if warn_before_overwrite and output_file.is_file():
            raise FileExistsError(
                f'Output file "{output_file}" already exists')

        # Set epilogue
        if epilogue is None:
            epilogue = line_ending if self.trailing_newline else ''

        # Write output file
        with open(output_file, write_mode, encoding='utf_8', newline='') \
                as fileID:
            fileID.write(prologue)
            fileID.write(line_ending.join(self.contents))
            fileID.write(epilogue)
