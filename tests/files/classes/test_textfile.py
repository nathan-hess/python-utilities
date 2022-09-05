import filecmp
import pathlib
import shutil
import unittest

from pyxx.files import TextFile
from tests import CreateTempTestDir, SAMPLE_FILES_DIR


class Test_TextFile_Initialize(unittest.TestCase):
    def setUp(self):
        self.file = TextFile()

    def test_initialize_raw_contents(self):
        # Verifies that "_raw_contents" list is initialized correctly
        self.assertIsNone(self.file._raw_contents)

    def test_initialize_contents(self):
        # Verifies that "_contents" list is initialized correctly
        self.assertListEqual(self.file._contents, [])

    def test_initialize_trailing_newline(self):
        # Verifies that "_trailing_newline" list is initialized correctly
        self.assertIsNone(self.file._trailing_newline)

    def test_initialize_path(self):
        # Verifies that "path" attribute is initialized correctly
        with self.subTest(path_argument='true'):
            file = TextFile('test_file.txt')
            self.assertEqual(file._path, pathlib.Path('test_file.txt'))

        with self.subTest(path_argument='false'):
            self.assertIsNone(self.file._path)

    def test_initialize_comment_char(self):
        # Verifies that valid "comment_char" argument is initialized correctly
        test_cases_1 = [
            {'arg': '',   'stored_value': None},
            {'arg': (),   'stored_value': None},
            {'arg': None, 'stored_value': None},

        ]

        for test_case in test_cases_1:
            with self.subTest(comment_char=test_case['arg']):
                file = TextFile(comment_chars=test_case['arg'])
                self.assertIsNone(file._comment_chars)

        test_cases_2 = [
            {'arg': '#',        'stored_value': ('#',)},
            {'arg': '//',       'stored_value': ('//',)},
            {'arg': ('#',),     'stored_value': ('#',)},
            {'arg': (';', '#'), 'stored_value': (';', '#')},
        ]

        for test_case in test_cases_2:
            with self.subTest(comment_char=test_case['arg']):
                file = TextFile(comment_chars=test_case['arg'])
                self.assertEqual(
                    file._comment_chars,
                    test_case['stored_value']
                )

    def test_initialize_comment_char_invalid(self):
        # Verifies that invalid "comment_char" argument results in an
        # appropriate error
        with self.assertRaises(TypeError):
            TextFile(comment_chars=3)

        with self.assertRaises(TypeError):
            TextFile(comment_chars=('#', '//', 3, ';'))


class Test_TextFile_General(unittest.TestCase):
    def setUp(self):
        self.file = TextFile()

    def test_check_contents_invalid_type(self):
        # Verifies that `_check_contents()` method throws an error if input
        # is not a list or list elements aren't strings
        with self.assertRaises(TypeError):
            self.file._check_contents(3)

        with self.assertRaises(TypeError):
            self.file._check_contents(['abcdefg', 'hijklmno', 6.28, 'pqrstu'])

    def test_get_comment_chars(self):
        # Verifies that "comment_chars" property returns the value of the
        # non-public "_comment_chars" attribute, and that it is a tuple
        with self.subTest(test='value'):
            self.file._comment_chars = ('#', 'abc', 4.3)
            self.assertTupleEqual(self.file.comment_chars, ('#', 'abc', 4.3))

        with self.subTest(test='type'):
            file = TextFile(comment_chars='//')
            self.assertTrue(isinstance(file.comment_chars, tuple))

    def test_get_contents(self):
        # Verifies that "contents" property returns the non-public "_contents"
        # attribute by reference
        self.file._contents = ['line1', 'line2', 'line03']

        with self.subTest(test='value'):
            self.assertListEqual(self.file.contents, ['line1', 'line2', 'line03'])

        with self.subTest(test='pass_by_reference'):
            test_list = self.file.contents
            test_list[2] = 'myLine'

            self.assertListEqual(self.file._contents, ['line1', 'line2', 'myLine'])

    def test_get_raw_contents(self):
        # Verifies that "raw_contents" property returns the non-public
        # "_raw_contents" attribute by value
        self.file._raw_contents = ['line1', 'line2', 'line03']

        with self.subTest(test='value'):
            self.assertListEqual(
                self.file.raw_contents,
                ['line1', 'line2', 'line03'])

        with self.subTest(test='pass_by_value'):
            test_list = self.file.raw_contents
            test_list[2] = 'myLine'

            self.assertListEqual(
                self.file._raw_contents,
                ['line1', 'line2', 'line03'])

    def test_get_trailing_newline(self):
        # Verifies that "trailing_newline" property returns the non-public
        # "_trailing_newline" attribute or throws an error, as appropriate
        with self.subTest(value='set'):
            self.file._trailing_newline = True
            self.assertTrue(self.file.trailing_newline)

        with self.subTest(value='not_set'):
            self.file._trailing_newline = None
            with self.assertRaises(AttributeError):
                self.file.trailing_newline


class Test_TextFile_Clean(unittest.TestCase):
    def setUp(self):
        self.file = TextFile()

        with open(SAMPLE_FILES_DIR / 'textfile_clean.txt', 'r') as fileID:
            contents = [line.rstrip('\r\n') for line in fileID.readlines()]
        self.file._contents = contents


class Test_TextFile_Clean_SingleComment(Test_TextFile_Clean):
    def setUp(self):
        super().setUp()
        self.file._comment_chars = ('#',)

    def test_clean_removeComments(self):
        # Verify that `TextFile.clean_contents()` correctly
        # removes line comments
        self.file.clean_contents(
            remove_comments=True,
            skip_full_line_comments=False,
            strip=False,
            concat_lines=False,
            remove_blank_lines=False
        )

        self.assertListEqual(
            self.file._contents,
            ['Line1 ', '', ' Li', 'Ln ', '', 'L5\\', 'Line6', 'Line7\\',
             'Li//ne8\\', 'line 9', '//lIne 10']
        )

    def test_clean_removeComments_skipFull(self):
        # Verify that `TextFile.clean_contents()` correctly removes line
        # comments, skipping full-line comments
        self.file.clean_contents(
            remove_comments=True,
            skip_full_line_comments=True,
            strip=False,
            concat_lines=False,
            remove_blank_lines=False
        )

        self.assertListEqual(
            self.file._contents,
            ['Line1 ', '#Li//ne2\t  ', ' Li', 'Ln ', '', 'L5\\', 'Line6',
             'Line7\\', 'Li//ne8\\', 'line 9', '//lIne 10']
        )

    def test_clean_removeCommentsBlank(self):
        # Verify that `TextFile.clean_contents()` correctly removes line
        # comments and blank lines
        self.file.clean_contents(
            remove_comments=True,
            skip_full_line_comments=False,
            strip=False,
            concat_lines=False,
            remove_blank_lines=True
        )

        self.assertListEqual(
            self.file._contents,
            ['Line1 ', ' Li', 'Ln ', 'L5\\', 'Line6', 'Line7\\',
             'Li//ne8\\', 'line 9', '//lIne 10']
        )

    def test_clean_removeCommentsBlank_skipFull(self):
        # Verify that `TextFile.clean_contents()` correctly removes line
        # comments and blank lines, skipping full-line comments
        self.file.clean_contents(
            remove_comments=True,
            skip_full_line_comments=True,
            strip=False,
            concat_lines=False,
            remove_blank_lines=True
        )

        self.assertListEqual(
            self.file._contents,
            ['Line1 ', '#Li//ne2\t  ', ' Li', 'Ln ', 'L5\\', 'Line6',
             'Line7\\', 'Li//ne8\\', 'line 9', '//lIne 10']
        )

    def test_clean_strip(self):
        # Verify that `TextFile.clean_contents()` correctly
        # strips whitespace from the beginning and end of lines
        self.file.clean_contents(
            remove_comments=False,
            skip_full_line_comments=False,
            strip=True,
            concat_lines=False,
            remove_blank_lines=False
        )

        self.assertListEqual(
            self.file._contents,
            ['Line1', '#Li//ne2', 'Li#ne\\3', 'Ln #4', '', 'L5\\', 'Line6',
             'Line7\\', 'Li//ne8\\', 'line 9', '//lIne 10']
        )

    def test_clean_concat(self):
        # Verify that `TextFile.clean_contents()` correctly
        # concatenates lines ending with backslashes
        self.file.clean_contents(
            remove_comments=False,
            skip_full_line_comments=False,
            strip=False,
            concat_lines=True,
            remove_blank_lines=False
        )

        self.assertListEqual(
            self.file._contents,
            ['Line1 ', '#Li//ne2\t  ', ' Li#ne\\3', 'Ln #4', '',
             'L5Line6', 'Line7Li//ne8line 9', '//lIne 10']
        )

    def test_clean_removeBlank(self):
        # Verify that `TextFile.clean_contents()` correctly
        # removes lines containing only whitespace
        self.file.clean_contents(
            remove_comments=False,
            skip_full_line_comments=False,
            strip=False,
            concat_lines=False,
            remove_blank_lines=True
        )

        self.assertListEqual(
            self.file._contents,
            ['Line1 ', '#Li//ne2\t  ', ' Li#ne\\3', 'Ln #4', 'L5\\',
             'Line6', 'Line7\\', 'Li//ne8\\', 'line 9', '//lIne 10']
        )

    def test_concat_removeComments_skipFull(self):
        # Verify that `TextFile.clean_contents()` correctly concatenates
        # lines ending with backslashes and removes comments, skipping
        # full-line comments
        self.file.clean_contents(
            remove_comments=True,
            skip_full_line_comments=True,
            strip=False,
            concat_lines=True,
            remove_blank_lines=False
        )

        self.assertListEqual(
            self.file._contents,
            ['Line1 ', '#Li//ne2\t  ', ' Li', 'Ln ', '',
             'L5Line6', 'Line7Li//ne8line 9', '//lIne 10']
        )

    def test_concat_removeComments(self):
        # Verify that `TextFile.clean_contents()` correctly concatenates
        # lines ending with backslashes and removes comments
        self.file.clean_contents(
            remove_comments=True,
            skip_full_line_comments=False,
            strip=False,
            concat_lines=True,
            remove_blank_lines=False
        )

        self.assertListEqual(
            self.file._contents,
            ['Line1 ', '', ' Li', 'Ln ', '', 'L5Line6',
             'Line7Li//ne8line 9', '//lIne 10']
        )


class Test_TextFile_Clean_MultiComment(Test_TextFile_Clean):
    def setUp(self):
        super().setUp()
        self.file._comment_chars = ('//', '#')

    def test_clean_removeComments(self):
        # Verify that `TextFile.clean_contents()` correctly
        # removes line comments
        self.file.clean_contents(
            remove_comments=True,
            skip_full_line_comments=False,
            strip=False,
            concat_lines=False,
            remove_blank_lines=False
        )

        self.assertListEqual(
            self.file._contents,
            ['Line1 ', '', ' Li', 'Ln ', '', 'L5\\', 'Line6', 'Line7\\',
             'Li', 'line 9', '']
        )

    def test_clean_removeComments_skipFull(self):
        # Verify that `TextFile.clean_contents()` correctly removes line
        # comments, skipping full-line comments
        self.file.clean_contents(
            remove_comments=True,
            skip_full_line_comments=True,
            strip=False,
            concat_lines=False,
            remove_blank_lines=False
        )

        self.assertListEqual(
            self.file._contents,
            ['Line1 ', '#Li//ne2\t  ', ' Li', 'Ln ', '', 'L5\\', 'Line6',
             'Line7\\', 'Li', 'line 9', '//lIne 10']
        )

    def test_clean_removeCommentsBlank(self):
        # Verify that `TextFile.clean_contents()` correctly removes line
        # comments and blank lines
        self.file.clean_contents(
            remove_comments=True,
            skip_full_line_comments=False,
            strip=False,
            concat_lines=False,
            remove_blank_lines=True
        )

        self.assertListEqual(
            self.file._contents,
            ['Line1 ', ' Li', 'Ln ', 'L5\\', 'Line6', 'Line7\\',
             'Li', 'line 9']
        )

    def test_clean_removeCommentsBlank_skipFull(self):
        # Verify that `TextFile.clean_contents()` correctly removes line
        # comments and blank lines, skipping full-line comments
        self.file.clean_contents(
            remove_comments=True,
            skip_full_line_comments=True,
            strip=False,
            concat_lines=False,
            remove_blank_lines=True
        )

        self.assertListEqual(
            self.file._contents,
            ['Line1 ', '#Li//ne2\t  ', ' Li', 'Ln ', 'L5\\', 'Line6',
             'Line7\\', 'Li', 'line 9', '//lIne 10']
        )

    def test_clean_strip(self):
        # Verify that `TextFile.clean_contents()` correctly
        # strips whitespace from the beginning and end of lines
        self.file.clean_contents(
            remove_comments=False,
            skip_full_line_comments=False,
            strip=True,
            concat_lines=False,
            remove_blank_lines=False
        )

        self.assertListEqual(
            self.file._contents,
            ['Line1', '#Li//ne2', 'Li#ne\\3', 'Ln #4', '', 'L5\\',
             'Line6', 'Line7\\', 'Li//ne8\\', 'line 9', '//lIne 10']
        )

    def test_clean_concat(self):
        # Verify that `TextFile.clean_contents()` correctly
        # concatenates lines ending with backslashes
        self.file.clean_contents(
            remove_comments=False,
            skip_full_line_comments=False,
            strip=False,
            concat_lines=True,
            remove_blank_lines=False
        )

        self.assertListEqual(
            self.file._contents,
            ['Line1 ', '#Li//ne2\t  ', ' Li#ne\\3', 'Ln #4', '',
             'L5Line6', 'Line7Li//ne8line 9', '//lIne 10']
        )

    def test_clean_removeBlank(self):
        # Verify that `TextFile.clean_contents()` correctly
        # removes lines containing only whitespace
        self.file.clean_contents(
            remove_comments=False,
            skip_full_line_comments=False,
            strip=False,
            concat_lines=False,
            remove_blank_lines=True
        )

        self.assertListEqual(
            self.file._contents,
            ['Line1 ', '#Li//ne2\t  ', ' Li#ne\\3', 'Ln #4', 'L5\\',
             'Line6', 'Line7\\', 'Li//ne8\\', 'line 9', '//lIne 10']
        )

    def test_concat_removeComments_skipFull(self):
        # Verify that `TextFile.clean_contents()` correctly concatenates
        # lines ending with backslashes and removes comments, skipping
        # full-line comments
        self.file.clean_contents(
            remove_comments=True,
            skip_full_line_comments=True,
            strip=False,
            concat_lines=True,
            remove_blank_lines=False
        )

        self.assertListEqual(
            self.file._contents,
            ['Line1 ', '#Li//ne2\t  ', ' Li', 'Ln ', '',
             'L5Line6', 'Line7Li', '//lIne 10']
        )

    def test_concat_removeComments(self):
        # Verify that `TextFile.clean_contents()` correctly concatenates
        # lines ending with backslashes and removes comments
        self.file.clean_contents(
            remove_comments=True,
            skip_full_line_comments=False,
            strip=False,
            concat_lines=True,
            remove_blank_lines=False
        )

        self.assertListEqual(
            self.file._contents,
            ['Line1 ', '', ' Li', 'Ln ', '', 'L5Line6', 'Line7Li', '']
        )


class Test_TextFile_Populate(unittest.TestCase):
    def setUp(self):
        self.file = TextFile()

    def test_invalid_format(self):
        # Verifies that errors are thrown if the `contents` argument does not
        # match required format
        with self.subTest(issue='not_list'):
            with self.assertRaises(TypeError):
                self.file.populate_contents('myContents', True)

        with self.subTest(issue='items_not_str'):
            with self.assertRaises(TypeError):
                self.file.populate_contents(['myContents', 4], True)

    def test_invalid_trailing_newline(self):
        # Verifies that errors are thrown if the `trailing_newline` argument
        # is not valid
        with self.assertRaises(TypeError):
            self.file.populate_contents(['line1', 'line2'], '\n')

    def test_populate_trailing_newline(self):
        # Verifies that `populate_contents()` stores "trailing_newline"
        # attribute correctly
        with self.subTest(trailing_newline=True):
            self.file.populate_contents(['line1', 'line2'], True)
            self.assertTrue(self.file._trailing_newline)

        with self.subTest(trailing_newline=False):
            self.file.populate_contents(['line1', 'line2'], False)
            self.assertFalse(self.file._trailing_newline)

    def test_populate_contents_reference(self):
        # Verifies that `populate_contents()` stores data correctly
        # when passing argument by reference
        contents = ['line1', 'line2', '', '# data']

        with self.subTest(time='before_edit'):
            self.file.populate_contents(
                contents=contents,
                trailing_newline=True,
                pass_by_reference=True)

            self.assertListEqual(
                self.file._contents,
                ['line1', 'line2', '', '# data'])

        contents[2] = 'myModification'

        with self.subTest(time='after_edit'):
            self.assertListEqual(
                self.file._contents,
                ['line1', 'line2', 'myModification', '# data'])

    def test_populate_contents_value(self):
        # Verifies that `populate_contents()` stores data correctly
        # when passing argument by value
        contents = ['line1', 'line2', '', '# data']

        with self.subTest(time='before_edit'):
            self.file.populate_contents(
                contents=contents,
                trailing_newline=True,
                pass_by_reference=False)

            self.assertListEqual(
                self.file._contents,
                ['line1', 'line2', '', '# data'])

        contents[2] = 'myModification'

        with self.subTest(time='after_edit'):
            self.assertListEqual(
                self.file._contents,
                ['line1', 'line2', '', '# data'])


class Test_TextFile_Read(unittest.TestCase):
    def setUp(self):
        self.test_file = SAMPLE_FILES_DIR / 'textfile_read.txt'
        self.test_file_no_trailing_newline \
            = SAMPLE_FILES_DIR / 'textfile_read_no_trailing_newline.txt'

    def test_missing_path(self):
        # Verifies that an error is thrown if no file path is specified
        file = TextFile()
        with self.assertRaises(AttributeError):
            file.read()

    def test_set_path(self):
        # Verifies that logic to set path matches expectations
        with self.subTest(path='argument_only'):
            file1 = TextFile()
            file1.read(self.test_file)
            self.assertEqual(file1.path, self.test_file)

        with self.subTest(path='attribute_only'):
            file2 = TextFile(self.test_file)
            file2.read()
            self.assertEqual(file2.path, self.test_file)

        with self.subTest(path='argument_and_attribute'):
            file3 = TextFile('myFile.txt')
            file3.read(self.test_file)
            self.assertEqual(file3.path, self.test_file)

    def test_populate_hashes(self):
        # Verifies that reading a file populates the "hashes" dictionary
        file = TextFile(self.test_file)

        self.assertDictEqual(file.hashes, {})
        file.read()

        self.assertDictEqual(
            file.hashes,
            {'md5': '71261fa22b3680e252a89f78036dfa29',
             'sha256': 'e3f871fedca04c49ffbe6e1f1791cbb781c830d4b137acf9869c147a35b70903'}
        )

    def test_read_contents(self):
        # Verifies that data are read correctly for a file with a
        # trailing newline
        file = TextFile(self.test_file)
        file.read()

        with self.subTest(data='trailing_newline'):
            self.assertTrue(file._trailing_newline)

        with self.subTest(data='contents'):
            self.assertListEqual(
                file._contents,
                ['Line1', '# commented line', 'line4  ', '4595  # 9945'])

        with self.subTest(data='raw_contents'):
            self.assertListEqual(
                file._raw_contents,
                ['Line1\n', '# commented line\n', 'line4  \n', '4595  # 9945\n'])

    def test_read_contents_no_trailing_newline(self):
        # Verifies that data are read correctly for a file without a
        # trailing newline
        file = TextFile(self.test_file_no_trailing_newline)
        file.read()

        with self.subTest(data='trailing_newline'):
            self.assertFalse(file._trailing_newline)

        with self.subTest(data='contents'):
            self.assertListEqual(
                file._contents,
                ['Line1', '# commented line', 'line4  ', '4595  # 9945'])

        with self.subTest(data='raw_contents'):
            self.assertListEqual(
                file._raw_contents,
                ['Line1\n', '# commented line\n', 'line4  \n', '4595  # 9945'])


class Test_TextFile_Write(unittest.TestCase):
    def setUp(self):
        self.file = TextFile()
        self.file._contents = ['line1', 'line02', 'line3']
        self.file._trailing_newline = True

    def test_check_content(self):
        # Verifies that file won't be written if contents don't follow
        # expected format
        with CreateTempTestDir() as TEST_DIR:
            with self.subTest(issue='not_list'):
                self.file._contents = 'myContents'
                with self.assertRaises(TypeError):
                    self.file.write(TEST_DIR / 'output.txt')

            with self.subTest(issue='items_not_str'):
                self.file._contents = ['myContents', 4]
                with self.assertRaises(TypeError):
                    self.file.write(TEST_DIR / 'output.txt')

    def test_no_overwrite(self):
        # Verifies that warning can be generated before overwriting output file
        with CreateTempTestDir() as TEST_DIR:
            output_file = TEST_DIR / 'output.txt'
            with open(output_file, 'w', encoding='utf_8') as fileID:
                fileID.write('myOutputFile')

            with self.assertRaises(FileExistsError):
                self.file.write(output_file)

    def test_write_default(self):
        # Test writing file with default settings
        with self.subTest(trailing_newline='true'):
            with CreateTempTestDir() as TEST_DIR:
                output_file = TEST_DIR / 'output.txt'
                self.file.write(output_file)

                self.assertTrue(filecmp.cmp(
                    output_file,
                    SAMPLE_FILES_DIR / 'textfile_write.txt',
                    shallow=False))

        with self.subTest(trailing_newline='false'):
            self.file._trailing_newline = False

            with CreateTempTestDir() as TEST_DIR:
                output_file = TEST_DIR / 'output.txt'
                self.file.write(output_file)

                self.assertTrue(filecmp.cmp(
                    output_file,
                    SAMPLE_FILES_DIR / 'textfile_write_no_newline.txt',
                    shallow=False))

    def test_write_custom(self):
        # Test writing file with customized prologue, epilogue, and line endings
        with self.subTest(trailing_newline='true'):
            with CreateTempTestDir() as TEST_DIR:
                output_file = TEST_DIR / 'output.txt'
                self.file.write(
                    output_file,
                    prologue='My file prologue@',
                    epilogue='[[myEpilogue]]',
                    line_ending='!!!')

                self.assertTrue(filecmp.cmp(
                    output_file,
                    SAMPLE_FILES_DIR / 'textfile_write_custom.txt',
                    shallow=False))

        with self.subTest(trailing_newline='false'):
            self.file._trailing_newline = False

            with CreateTempTestDir() as TEST_DIR:
                output_file = TEST_DIR / 'output.txt'
                self.file.write(
                    output_file,
                    prologue='My file prologue@',
                    epilogue='[[myEpilogue]]',
                    line_ending='!!!')

                self.assertTrue(filecmp.cmp(
                    output_file,
                    SAMPLE_FILES_DIR / 'textfile_write_custom_no_newline.txt',
                    shallow=False))

    def test_write_append(self):
        # Tests appending to an output file
        with CreateTempTestDir() as TEST_DIR:
            output_file = TEST_DIR / 'output.txt'
            shutil.copyfile(
                src=SAMPLE_FILES_DIR / 'textfile_write_append_before.txt',
                dst=output_file)

            self.file.write(
                output_file,
                write_mode='a',
                warn_before_overwrite=False)

            self.assertTrue(filecmp.cmp(
                output_file,
                SAMPLE_FILES_DIR / 'textfile_write_append_after.txt',
                shallow=False))

    def test_overwrite(self):
        # Tests overwriting a file
        file = TextFile()
        file._contents = ['overwrite', '12345', 'sample file', 'python']
        file._trailing_newline = True

        with CreateTempTestDir() as TEST_DIR:
            output_file = TEST_DIR / 'output.txt'
            shutil.copyfile(
                src=SAMPLE_FILES_DIR / 'textfile_write.txt',
                dst=output_file)

            file.path = output_file
            file.overwrite()

            self.assertTrue(filecmp.cmp(
                output_file,
                SAMPLE_FILES_DIR / 'textfile_overwrite.txt',
                shallow=False))

    def test_overwrite_no_path(self):
        # Verifies that an error is thrown if attempting to call "overwrite()"
        # method without first defining "path" attribute
        with CreateTempTestDir() as TEST_DIR:
            output_file = TEST_DIR / 'output.txt'
            shutil.copyfile(
                src=SAMPLE_FILES_DIR / 'textfile_write.txt',
                dst=output_file)

            with self.assertRaises(AttributeError):
                self.file.overwrite()


class Test_TextFile_Integration(unittest.TestCase):
    def test_read_clean(self):
        # Tests reading and cleaning contents of a file
        file = TextFile(comment_chars='#')
        file.read(SAMPLE_FILES_DIR / 'textfile_read.txt')

        with self.subTest(check='path'):
            self.assertEqual(
                file.path,
                SAMPLE_FILES_DIR / 'textfile_read.txt')

        with self.subTest(check='before_clean'):
            self.assertListEqual(
                file.contents,
                ['Line1', '# commented line', 'line4  ', '4595  # 9945'])

            self.assertListEqual(
                file.raw_contents,
                ['Line1\n', '# commented line\n', 'line4  \n', '4595  # 9945\n'])

        # Remove inline comments
        file.clean_contents(
            remove_comments=True,
            skip_full_line_comments=True,
            strip=False,
            concat_lines=True,
            remove_blank_lines=True
        )

        with self.subTest(check='after_clean_inline_comments'):
            self.assertListEqual(
                file.contents,
                ['Line1', '# commented line', 'line4  ', '4595  '])

            self.assertListEqual(
                file.raw_contents,
                ['Line1\n', '# commented line\n', 'line4  \n', '4595  # 9945\n'])

        # Strip whitespace
        file.clean_contents(
            remove_comments=False,
            skip_full_line_comments=False,
            strip=True,
            concat_lines=False,
            remove_blank_lines=False
        )

        with self.subTest(check='after_clean_strip'):
            self.assertListEqual(
                file.contents,
                ['Line1', '# commented line', 'line4', '4595'])

            self.assertListEqual(
                file.raw_contents,
                ['Line1\n', '# commented line\n', 'line4  \n', '4595  # 9945\n'])

        # Remove remaining comments
        file.clean_contents(
            remove_comments=True,
            skip_full_line_comments=False,
            strip=True,
            concat_lines=False,
            remove_blank_lines=False
        )

        with self.subTest(check='after_clean_comments'):
            self.assertListEqual(
                file.contents,
                ['Line1', '', 'line4', '4595'])

            self.assertListEqual(
                file.raw_contents,
                ['Line1\n', '# commented line\n', 'line4  \n', '4595  # 9945\n'])

        # Remove blank lines
        file.clean_contents(
            remove_comments=True,
            skip_full_line_comments=False,
            strip=True,
            concat_lines=True,
            remove_blank_lines=True
        )

        with self.subTest(check='after_clean_comments'):
            self.assertListEqual(
                file.contents,
                ['Line1', 'line4', '4595'])

            self.assertListEqual(
                file.raw_contents,
                ['Line1\n', '# commented line\n', 'line4  \n', '4595  # 9945\n'])
