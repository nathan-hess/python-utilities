import pathlib
import os
import shutil


# Define variables available to all tests
PROJECT_TEST_DIR = pathlib.Path(__file__).resolve().parent
SAMPLE_FILES_DIR = PROJECT_TEST_DIR / '_sample_files'
TEST_TMP_DIR = PROJECT_TEST_DIR / 'tmp'


# Define context managers to facilitate testing
class CreateTempTestDir:
    """Sets up temporary folder for reading/writing test files"""
    def __enter__(self):
        # Set test directory name
        index = 0
        while (test_dir := (TEST_TMP_DIR / f'test{index}')).exists():
            index += 1

        self.test_dir = test_dir

        # Create test directory
        os.makedirs(self.test_dir)

        return self.test_dir

    def __exit__(self, *args, **kwargs):
        shutil.rmtree(self.test_dir)


# Import and run tests
from .arrays import *
from .files import *
from .strings import *
