import pathlib
import shutil
import unittest

from pyxx.files import File
from pyxx.files.exceptions import NoFileSpecifiedError, UntrackedFileError
from tests import CreateTempTestDir, SAMPLE_FILES_DIR


class Test_File(unittest.TestCase):
    def setUp(self):
        self.file_pathlib = SAMPLE_FILES_DIR / 'hashes.txt'
        self.file_str = str(self.file_pathlib)

        self.file_from_pathlib = File(self.file_pathlib)
        self.file_from_str = File(self.file_str)
        self.file_empty = File()

        # Known file hashes
        self.hashes = {
            'md5': 'b8c4707ddd8e71744899222680a08060',
            'sha1': '7baba1d3b8b4ff88995d97c2321a7dca5de91460',
            'sha224': '40769b9535d5ec2a18b37f8b666c198a8b78668f192f1885def71792',
            'sha256': 'cc7d0f19c158e4141585c57e5278320bc60f049e5ec18ec472668660f0d4aaa7',
            'sha384': '11723482eaa0a8cbffc201cc7cd6085fd6beb9f7505fa26f1c223782cf3634ae4bd0bc65d27131f5173ff7519600630c',
            'sha512': 'a8b65a414cba9df08d5fc5f9a476e43d29ef636621011e222830182dc396f4cd4618a49b5e8c21a5dbd8706fe5cd174a118d24969d6d49f614272a2e3841c515',
        }

        self.test_files = {
            'pathlib': self.file_from_pathlib,
            'str': self.file_from_str,
        }

    def test_file_repr_empty(self):
        # Verifies that the file object string representation is computed
        # correctly if `path` attribute has not been assigned a value
        self.assertEqual(
            self.file_empty.__repr__(),
            "<class 'pyxx.files.classes.file.File'>")

    def test_file_repr_before(self):
        # Verifies that file object descriptor is computed correctly before
        # computing file hashes
        for source, file in self.test_files.items():
            with self.subTest(source=source):
                self.assertEqual(
                    file.__repr__(),
                    f"<class 'pyxx.files.classes.file.File'>\n--> File path: {self.file_str}"
                )

    def test_file_repr_after_single(self):
        # Verifies that file object descriptor is computed correctly after
        # computing file hashes
        for source, file in self.test_files.items():
            with self.subTest(source=source):
                file.compute_file_hashes('sha512', store=True)
                self.assertEqual(
                    file.__repr__(),
                    (f"<class 'pyxx.files.classes.file.File'>\n"
                    f"--> File path: {self.file_str}\n"
                    f"--> File hash:\n"
                    f"    sha512: {self.hashes['sha512']}")
                )

    def test_file_repr_after_multiple(self):
        # Verifies that file object descriptor is computed correctly after
        # computing file hashes
        for source, file in self.test_files.items():
            with self.subTest(source=source):
                file.compute_file_hashes(('md5', 'sha256'), store=True)
                self.assertEqual(
                    file.__repr__(),
                    (f"<class 'pyxx.files.classes.file.File'>\n"
                    f"--> File path: {self.file_str}\n"
                    f"--> File hashes:\n"
                    f"    md5: {self.hashes['md5']}\n"
                    f"    sha256: {self.hashes['sha256']}")
                )

    def test_file_str(self):
        # Verifies that path and filename is correctly returned
        # as a string
        for source, file in self.test_files.items():
            with self.subTest(source=source):
                self.assertEqual(
                    str(file),
                    f'<class \'pyxx.files.classes.file.File\'> path="{self.file_str}"'
                )

        with self.subTest(source='empty'):
            self.assertEqual(
                str(self.file_empty),
                f'<class \'pyxx.files.classes.file.File\'> path="None"'
            )

    def test_hashes_getter(self):
        # Verifies that getting the "hashes" attribute correctly retrieves
        # the file hashes
        for source, file in self.test_files.items():
            with self.subTest(source=source):
                file._hashes = {'hash1': 'abcd', 'hash2': 'efghij'}
                self.assertDictEqual(
                    file.hashes,
                    {'hash1': 'abcd', 'hash2': 'efghij'})

    def test_file_setter(self):
        # Verifies that setting the "path" attribute correctly sets the
        # path and clears file hashes
        for source, file in self.test_files.items():
            with self.subTest(source=source):
                # Make sure hashes dictionary is populated
                file._hashes = {'hash1': 'abcdefg'}
                self.assertGreater(len(file._hashes), 0)

                # Set new file
                file.path = 'newFile.rst'
                self.assertEqual(file._path, pathlib.Path('newFile.rst'))
                self.assertTrue(isinstance(file._path, pathlib.Path))
                self.assertDictEqual(file._hashes, {})

    def test_file_getter(self):
        # Verifies that getting the "path" attribute correctly retrieves
        # the file path
        for source, file in self.test_files.items():
            with self.subTest(source=source):
                self.assertEqual(file.path, pathlib.Path(self.file_str))

    def test_clear_hashes(self):
        # Verifies that file hashes are cleared by the
        # `File.clear_file_hashes()` method
        for source, file in self.test_files.items():
            with self.subTest(source=source):
                file.clear_file_hashes()
                self.assertDictEqual(file._hashes, {})

    def test_no_path_attribute(self):
        # Verifies that an error is thrown if attempting to compute file
        # hashes without the "path" attribute set
        with self.assertRaises(NoFileSpecifiedError):
            self.file_empty.compute_file_hashes()

    def test_compute_no_file(self):
        # Verifies that an error is thrown if attempting to compute file
        # hashes for a non-existent file
        file = File('non_existent_file.docx')

        with self.assertRaises(FileNotFoundError):
            file.compute_file_hashes()

    def test_compute_directory(self):
        # Verifies that an error is thrown if attempting to compute file
        # hashes for a directory
        file = File(SAMPLE_FILES_DIR)

        with self.assertRaises(IsADirectoryError):
            file.compute_file_hashes()

    def test_compute_store_hashes(self):
        # Verifies that file hashes are computed and stored correctly
        hashes_dict = {
            'md5': self.hashes['md5'],
            'sha384': self.hashes['sha384'],
            'sha256': self.hashes['sha256'],
        }

        for source, file in self.test_files.items():
            with self.subTest(source=source):
                hashes = file.compute_file_hashes(
                    ('md5', 'sha384', 'sha256'), store=True)
                self.assertDictEqual(file._hashes, hashes_dict)
                self.assertDictEqual(hashes, hashes_dict)
            hashes.clear()

    def test_no_store_hashes(self):
        # Verifies that no file hashes are stored if user does not set the
        # "store" argument to `True`
        for source, file in self.test_files.items():
            with self.subTest(source=source):
                file.compute_file_hashes(('md5', 'sha384', 'sha256'))
                self.assertDictEqual(file._hashes, {})

    def test_hashes_copy(self):
        # Verifies that "hashes" attribute returns a copy so that manipulating
        # the returned variable does not affect the stored hashes
        hashes_dict = {
            'md5': self.hashes['md5'],
            'sha256': self.hashes['sha256'],
        }

        for source, file in self.test_files.items():
            with self.subTest(source=source):
                file.store_file_hashes()

                hashes = file.hashes
                hashes['md5'] = 'modified_hash'

                self.assertDictEqual(file.hashes, hashes_dict)
                hashes.clear()

    def test_has_changed_no_stored(self):
        # Verifies that an error is thrown if attempting to evaluate whether
        # a file has been changed, but the hashes of the file were not
        # previously computed
        for source, file in self.test_files.items():
            with self.subTest(source=source):
                with self.assertRaises(UntrackedFileError):
                    file.has_changed()

    def test_has_changed(self):
        # Verifies that changes in file are correctly identified
        with CreateTempTestDir() as TMP_DIR:
            # Create sample file
            test_file = TMP_DIR / 'test_file.txt'
            shutil.copyfile(self.file_str, test_file)

            # Compute hashes of sample file
            file = File(test_file)
            file.store_file_hashes()
            self.assertFalse(file.has_changed())

            # Modify file
            with open(test_file, 'a', encoding='utf_8') as fileID:
                fileID.write('abcdefg')
            self.assertTrue(file.has_changed())

            # Compute hashes again
            file.store_file_hashes()
            self.assertFalse(file.has_changed())

    def test_set_read_metadata_path_none(self):
        # Verifies that `set_read_metadata()` throws an error if no path
        # is provided
        with self.assertRaises(AttributeError):
            self.file_empty.set_read_metadata()

    def test_set_read_metadata_path_attr(self):
        # Verifies that `set_read_metadata()` correctly reads a file and
        # stores file hashes if the path is provided as an attribute
        self.assertDictEqual(self.file_empty.hashes, {})

        self.file_empty._path = self.file_pathlib
        self.file_empty.set_read_metadata()

        with self.subTest(check='path'):
            self.assertEqual(self.file_empty.path, self.file_pathlib)

        with self.subTest(check='hashes'):
            self.assertDictEqual(
                self.file_empty.hashes,
                {
                    'md5': self.hashes['md5'],
                    'sha256': self.hashes['sha256'],
                }
            )

    def test_set_read_metadata_path_arg(self):
        # Verifies that `set_read_metadata()` correctly reads a file and
        # stores file hashes if the path is provided as an argument
        self.assertDictEqual(self.file_empty.hashes, {})

        self.file_empty.set_read_metadata(self.file_pathlib)

        with self.subTest(check='path'):
            self.assertEqual(self.file_empty.path, self.file_pathlib)

        with self.subTest(check='hashes'):
            self.assertDictEqual(
                self.file_empty.hashes,
                {
                    'md5': self.hashes['md5'],
                    'sha256': self.hashes['sha256'],
                }
            )

    def test_set_read_metadata_path_arg_attr(self):
        # Verifies that `set_read_metadata()` correctly gives priority to
        # a path provided as an argument (over stored attribute)
        self.assertDictEqual(self.file_empty.hashes, {})

        self.file_empty._path = SAMPLE_FILES_DIR / 'textfile_write.txt'
        self.file_empty.set_read_metadata(self.file_pathlib)

        with self.subTest(check='path'):
            self.assertEqual(self.file_empty.path, self.file_pathlib)

        with self.subTest(check='hashes'):
            self.assertDictEqual(
                self.file_empty.hashes,
                {
                    'md5': self.hashes['md5'],
                    'sha256': self.hashes['sha256'],
                }
            )

    def test_store_hashes(self):
        # Verifies that file hashes are stored correctly
        for source, file in self.test_files.items():
            with self.subTest(source=source):
                file.store_file_hashes(('md5', 'sha384', 'sha256'))
                self.assertDictEqual(
                    file.hashes,
                    {
                        'md5': self.hashes['md5'],
                        'sha384': self.hashes['sha384'],
                        'sha256': self.hashes['sha256'],
                    }
                )

    def test_track_new_file(self):
        # Verifies that the "track_new_file()" method stores the file path
        # and file hashes
        hashes_dict = {
            'md5': self.hashes['md5'],
            'sha384': self.hashes['sha384'],
            'sha256': self.hashes['sha256'],
        }

        file = File()
        file.track_new_file(
            path=self.file_str,
            hash_functions=('md5', 'sha256', 'sha384')
        )

        with self.subTest(attribute='path'):
            self.assertEqual(file._path, pathlib.Path(self.file_str))

        with self.subTest(attribute='hashes'):
            self.assertDictEqual(file._hashes, hashes_dict)

    def test_track_new_file_invalid(self):
        # Verifies that an error is thrown if attempting to call the
        # "track_new_file()" method with "None" as the "path" argument
        test_files = {
            'pathlib': self.file_from_pathlib,
            'str': self.file_from_str,
            'empty': self.file_empty,
        }

        for source, file in test_files.items():
            with self.subTest(source=source):
                with self.assertRaises(TypeError):
                    file.track_new_file(path=None)
