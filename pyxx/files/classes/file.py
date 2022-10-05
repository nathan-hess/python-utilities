"""Base class for processing files of any type (text or binary)
"""

import copy
import pathlib
from typing import Dict, Optional, Union

from pyxx.arrays.functions.convert import convert_to_tuple
from pyxx.files.functions.hash import compute_file_hash
from pyxx.files.exceptions import NoFileSpecifiedError, UntrackedFileError


class File:
    """Base class for processing files of any type (text or binary)

    This class is intended to represent an arbitrary file (which can but does
    not necessarily exist).  After creating a new instance of this class, it
    is possible to perform operations such as calculating file hashes and
    tracking whether the file has been modified.
    """

    def __init__(self, path: Optional[Union[str, pathlib.Path]] = None):
        """Define an arbitrary file

        Creates an object that represents and can be used to process a file of
        any type (text or binary).

        Parameters
        ----------
        path : str or pathlib.Path
            Path describing the location in the file system of the file that
            the object is to represent
        """
        # Initialize dictionary to store file hashes
        self._hashes: Dict[str, str] = {}

        # Store file path
        self.path = path

    def __repr__(self):
        # Display class
        representation = f'{__class__}\n'

        # Display path
        if self.path is not None:
            representation += f'--> File path: {str(self.path)}\n'

        # Display file hashes
        if len(self._hashes) > 0:
            header = '--> File hash:' \
                if len(self._hashes) == 1 else '--> File hashes:'
            representation += self.__file_hash_str(header, 4)

        return representation[:-1]

    def __str__(self):
        return f'{__class__} path="{self.path}"'

    def __file_hash_str(self, header: str, indent: int = 0):
        file_hash_str = f'{header}\n'

        for i in self._hashes.items():
            file_hash_str += f'{" " * indent}{i[0]}: {i[1]}\n'

        return file_hash_str

    @property
    def hashes(self):
        """A copy of the dictionary containing any file hashes previously
        computed for the file specified by the :py:attr:`path` attribute"""
        return copy.deepcopy(self._hashes)

    @property
    def path(self):
        """Path describing the location of the file on the disk

        Assigning a value to this attribute (regardless whether it matches the
        current value or is a different path) will save the value as a
        ``pathlib.Path`` and **will automatically clear any saved file
        hashes**.
        """
        return self._path

    @path.setter
    def path(self, path: Optional[Union[str, pathlib.Path]]):
        # Clear any existing file hashes
        self.clear_file_hashes()

        # Store file path
        self._path = None if path is None else pathlib.Path(path)

    def clear_file_hashes(self):
        """Clears any stored file hashes"""
        self._hashes.clear()

    def compute_file_hashes(self,
            hash_functions: Union[tuple, str] = ('md5', 'sha256'),  # noqa : E128
            store: bool = False):                                   # noqa : E128
        """Computes hashes of the file specified by the :py:attr:`path`
        attribute

        Computes and returns the hashes of the file specified by the
        :py:attr:`path` attribute, with the option to populate the
        :py:attr:`hashes` dictionary with their values.

        Parameters
        ----------
        hash_functions : tuple or str, optional
            Tuple of strings (or individual string) specifying which hash(es)
            to compute. Any hash functions supported by ``hashlib`` can be
            used. Default is ``('md5', 'sha256')``
        store : bool, optional
            Whether to store the computed hashes in the :py:attr:`hashes`
            dictionary (default is ``False``)

        Returns
        -------
        dict
            A dictionary containing the file hashes specified by
            ``hash_functions``

        See Also
        --------
        pyxx.files.compute_file_hash :
            Function used to compute file hashes

        Notes
        -----
        Prior to calling this method, the :py:attr:`path` attribute must be
        defined.  To simultaneously set the :py:attr:`path` attribute and store
        file hashes, use :py:meth:`track_new_file`.
        """
        # Check that `path` attribute is defined
        if self.path is None:
            raise NoFileSpecifiedError(
                'Attribute "path" must be defined to compute file hashes')

        # Check that file exists
        if not self.path.exists():
            raise FileNotFoundError(
                f'Cannot compute hash for non-existent file "{self.path}"')

        if not self.path.is_file():
            raise IsADirectoryError(
                f'Cannot compute hash for a directory ("{self.path}")')

        # Ensure that inputs such as `hash_functions=('md5')` are still
        # interpreted as a tuple, not a string
        hash_functions = convert_to_tuple(hash_functions)

        # Compute file hash(es)
        output = {}
        for func in hash_functions:
            hash_name, file_hash = compute_file_hash(self.path, func)
            output[hash_name] = file_hash

            if store:
                self._hashes[hash_name] = file_hash

        return output

    def has_changed(self):
        """Returns whether the file specified by the :py:attr:`path`
        attribute has changed since the last time file hashes were computed

        Returns
        -------
        bool
            Whether file has changed since the last time file hashes
            were computed
        """
        if len(self._hashes) == 0:
            raise UntrackedFileError(
                'File hashes have not yet been computed. Cannot '
                'evaluate whether file has changed')

        # Compute hashes of current file
        current_hashes = self.compute_file_hashes(tuple(self._hashes.keys()),
                                                  store=False)

        # Check whether current file hashes match those stored
        for key, value in self._hashes.items():
            if current_hashes[key] != value:
                return True

        return False

    def store_file_hashes(self,
            hash_functions: Union[tuple, str] = ('md5', 'sha256')):  # noqa : E128
        """Computes and stores hashes of the file specified by the
        :py:attr:`path` attribute

        Computes given hashes of the file specified by the :py:attr:`path`
        attribute and populates the :py:attr:`hashes` dictionary with their
        values.

        Parameters
        ----------
        hash_functions : tuple or str, optional
            Tuple of strings (or individual string) specifying which hash(es)
            to compute. Any hash functions supported by ``hashlib`` can be
            used. Default is ``('md5', 'sha256')``

        See Also
        --------
        pyxx.files.compute_file_hash :
            Function used to compute file hashes
        track_new_file :
            Use this method if you want to store file hashes but the
            :py:attr:`path` attribute isn't yet defined

        Notes
        -----
        Prior to calling this method, the :py:attr:`path` attribute must be
        defined.  To simultaneously set the :py:attr:`path` attribute and store
        file hashes, use :py:meth:`track_new_file`.
        """
        _ = self.compute_file_hashes(hash_functions, store=True)

    def track_new_file(self, path: Union[str, pathlib.Path],
            hash_functions: Union[tuple, str] = ('md5', 'sha256')):  # noqa : E128
        """Shortcut for simultaneously modifying the :py:attr:`path` attribute
        and storing file hashes

        This method functions as a "shortcut," both modifying the
        :py:attr:`path` attribute and storing an optionally user-specified
        list of file hashes in the :py:attr:`hashes` attribute.  The
        intention of this method is that if a :py:class:`File` instance is
        tracking a given file, and user wants to switch to tracking another
        file, this provides a convenient way to do so with a single line
        of code.

        Parameters
        ----------
        file : str or pathlib.Path
            File that the object is to represent
        hash_functions : tuple or str, optional
            Tuple of strings (or individual string) specifying which hash(es)
            to compute. Any hash functions supported by ``hashlib`` can be
            used. Default is ``('md5', 'sha256')``

        See Also
        --------
        pyxx.files.compute_file_hash :
            Function used to compute file hashes
        """
        # Store the file path and name
        if path is None:
            raise TypeError('Argument "path" cannot be "None" when calling '
                            '"track_file()" method')

        self.path = path

        # Compute and store file hashes
        self.store_file_hashes(hash_functions)
