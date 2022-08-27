import pathlib


# Define variables available to all tests
PROJECT_TEST_DIR = pathlib.Path(__file__).resolve().parent
SAMPLE_FILES_DIR = PROJECT_TEST_DIR / '_sample_files'
TEST_TMP_DIR = PROJECT_TEST_DIR / 'tmp'


# Import and run tests
from .arrays import *
from .files import *
from .strings import *
