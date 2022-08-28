"""
Base class for processing files of any type (text or binary)
"""

import pathlib
from typing import Union

from pyxx.arrays.functions.convert import convert_to_tuple
from pyxx.files.functions.hash import compute_file_hash
from pyxx.files.exceptions import UntrackedFileError


class File:
    """Base class for processing files of any type (text or binary)

    This class is intended to represent an arbitrary file (which can but does
    not necessarily exist).  After creating a new instance of this class, it
    is possible to perform operations such as calculating file hashes and
    tracking whether the file has been modified.
    """

    def __init__(self, file: Union[str, pathlib.Path]):
        """Define an arbitrary file

        Creates an object that represents and can be used to process a file of
        any type (text or binary).

        Parameters
        ----------
        file : str or pathlib.Path
            File that the object is to represent
        """
        # File path
        self._file = pathlib.Path(file)

        # File hashes
        self._hashes: dict = {}

    def __repr__(self):
        # Display class
        representation = f'{__class__}\n'

        # Display path and filename
        representation += f'--> File: {str(self._file)}\n'

        # Display file hashes
        if len(self._hashes) > 0:
            header = '--> File hash:' \
                if len(self._hashes) == 1 else '--> File hashes:'
            representation += self.__file_hash_str(header, 4)

        return representation[:-1]

    def __str__(self):
        return str(self._file)

    def __file_hash_str(self, header: str, indent: int = 0):
        file_hash_str = f'{header}\n'

        for i in self._hashes.items():
            file_hash_str += f'{" " * indent}{i[0]}: {i[1]}\n'

        return file_hash_str

    @property
    def file(self):
        """Returns the file path and filename"""
        return self._file

    @property
    def hashes(self):
        """Returns a dictionary containing any file hashes previously
        computed for the file"""
        return self._hashes

    def compute_file_hashes(self,
            hash_functions: Union[tuple, str] = ('md5', 'sha256'),  # noqa : E128
            store: bool = False):                                   # noqa : E128
        """Computes hashes of the file

        Computes and returns the hashes of the file, with the option to
        populate the :py:attr:`hashes` dictionary with their values.

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
        """
        if not self.file.exists():
            raise FileNotFoundError(
                f'Cannot compute hash for non-existent file "{self.file}"'
            )

        # Ensure that inputs such as `hash_functions=('md5')` are still
        # interpreted as a tuple, not a string
        hash_functions = convert_to_tuple(hash_functions)

        # Compute file hash(es)
        output = {}
        for func in hash_functions:
            hash_name, file_hash = compute_file_hash(self.file, func)
            output[hash_name] = file_hash

            if store:
                self._hashes[hash_name] = file_hash

        return output

    def has_changed(self):
        """Returns whether the file has changed since the last time file
        hashes were computed

        Returns
        -------
        bool
            Whether file has changed since the last time file hashes
            were computed
        """
        if len(self.hashes) == 0:
            raise UntrackedFileError(
                'File hashes have not yet been computed. Cannot '
                'evaluate whether file has changed')

        # Compute hashes of current file
        current_hashes = self.compute_file_hashes(tuple(self.hashes.keys()),
                                                  store=False)

        # Check whether current file hashes match those stored
        for key, value in self.hashes.items():
            if current_hashes[key] != value:
                return True

        return False

    def store_file_hashes(self,
            hash_functions: Union[tuple, str] = ('md5', 'sha256')):  # noqa : E128
        """Computes and stores hashes of the file

        Computes given hashes of the file and populates the
        :py:attr:`hashes` dictionary with their values.

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
        """
        _ = self.compute_file_hashes(hash_functions, store=True)
