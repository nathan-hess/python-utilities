import unittest

from pyxx.files import compute_file_hash
from tests import SAMPLE_FILES_DIR


class Test_FileHash(unittest.TestCase):
    def setUp(self):
        # File for which to compute hashes
        self.file = SAMPLE_FILES_DIR / 'hashes.txt'

        # Known file hashes for `self.file`
        self.hashes = {
            'md5': 'b8c4707ddd8e71744899222680a08060',
            'sha1': '7baba1d3b8b4ff88995d97c2321a7dca5de91460',
            'sha224': '40769b9535d5ec2a18b37f8b666c198a8b78668f192f1885def71792',
            'sha256': 'cc7d0f19c158e4141585c57e5278320bc60f049e5ec18ec472668660f0d4aaa7',
            'sha384': '11723482eaa0a8cbffc201cc7cd6085fd6beb9f7505fa26f1c223782cf3634ae4bd0bc65d27131f5173ff7519600630c',
            'sha512': 'a8b65a414cba9df08d5fc5f9a476e43d29ef636621011e222830182dc396f4cd4618a49b5e8c21a5dbd8706fe5cd174a118d24969d6d49f614272a2e3841c515',
        }

    def test_md5(self):
        # Verifies that MD5 hash of a file is computed correctly
        for hash in ('md5', 'md_5', 'MD-5', 'mD-_5', 'MD5'):
            with self.subTest(hash=hash):
                self.assertTupleEqual(compute_file_hash(self.file, hash),
                                      ('md5', self.hashes['md5']))

    def test_sha1(self):
        # Verifies that SHA-1 hash of a file is computed correctly
        for hash in ('sha1', 'sha_1', 'SHA-1', 'sHa-_1'):
            with self.subTest(hash=hash):
                self.assertTupleEqual(compute_file_hash(self.file, hash),
                                      ('sha1', self.hashes['sha1']))

    def test_sha224(self):
        # Verifies that SHA-224 hash of a file is computed correctly
        for hash in ('sha224', 'sha_224', 'SHA-224', 'sHa-_224'):
            with self.subTest(hash=hash):
                self.assertTupleEqual(compute_file_hash(self.file, hash),
                                      ('sha224', self.hashes['sha224']))

    def test_sha384(self):
        # Verifies that SHA-384 hash of a file is computed correctly
        for hash in ('sha384', 'sha_384', 'SHA-384', 'sHa-_384'):
            with self.subTest(hash=hash):
                self.assertTupleEqual(compute_file_hash(self.file, hash),
                                      ('sha384', self.hashes['sha384']))

    def test_sha512(self):
        # Verifies that SHA-512 hash of a file is computed correctly
        for hash in ('sha512', 'sha_512', 'SHA-512', 'sHa-_512'):
            with self.subTest(hash=hash):
                self.assertTupleEqual(compute_file_hash(self.file, 'sHa-_512'),
                                      ('sha512', self.hashes['sha512']))

    def test_hash_default(self):
        # Verifies that hash of a file is computed correctly and equal
        # to the SHA-256 hash using the default `hash_function` argument
        self.assertTupleEqual(compute_file_hash(self.file),
                              ('sha256', self.hashes['sha256']))
