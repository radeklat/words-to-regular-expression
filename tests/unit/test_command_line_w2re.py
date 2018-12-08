import sys
from io import (
    StringIO,
    TextIOWrapper,
)
from tempfile import NamedTemporaryFile
from unittest import TestCase
from unittest.mock import (
    ANY,
    patch,
)

from w2re import (
    APPLICATION_NAME,
    CHANGELOG_URL,
    __version__ as VERSION,
)
from w2re.command_line_w2re import main
from w2re.formatters import (
    ALL_FORMATTERS,
    PythonFormatter,
)


class Main(TestCase):
    def setUp(self):
        mock_stream_to_regexp_patcher = patch('w2re.command_line_w2re.stream_to_regexp')
        self._mock_stream_to_regexp = mock_stream_to_regexp_patcher.start()
        self._mock_stream_to_regexp.return_value = ''
        self.addCleanup(mock_stream_to_regexp_patcher.stop)

    @patch('sys.stdout', new_callable=StringIO)
    def test_it_can_print_help(self, mock_stdout):
        with self.assertRaises(SystemExit) as exception_context:
            main(['-h'])

        self.assertEqual(0, exception_context.exception.code)
        self.assertIn("Words to Regular Expression", mock_stdout.getvalue())
        self._mock_stream_to_regexp.assert_not_called()

    def test_it_uses_python_formatter_by_default(self):
        main([])
        self._mock_stream_to_regexp.called_with([ANY, PythonFormatter])

    def test_it_accepts_valid_formatters(self):
        for formatter_class in ALL_FORMATTERS:
            formatter_code = formatter_class.code()
            main(['-f', formatter_code])
            self._mock_stream_to_regexp.called_with([ANY, formatter_class])
            self._mock_stream_to_regexp.reset()

    def test_it_refuses_unknown_formatters(self):
        with patch('sys.stderr', new_callable=StringIO):
            with self.assertRaises(SystemExit) as exception_context:
                main(['-f', 'sjaflksag'])

        self.assertNotEqual(0, exception_context.exception.code)
        self._mock_stream_to_regexp.assert_not_called()

    def test_it_opens_custom_file(self):
        with NamedTemporaryFile() as temp_file:
            main(['-i', temp_file.name])
            file_object = self._mock_stream_to_regexp.call_args[0][0]

            self.assertIsInstance(file_object, TextIOWrapper)
            self.assertEqual(temp_file.name, file_object.name)

    def test_it_uses_stdin_as_input_by_default(self):
        main([])
        self._mock_stream_to_regexp.called_with([sys.stdin, ANY])

    def test_it_prints_out_version(self):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            main(['--version'])

        output = mock_stdout.getvalue()

        self.assertIn(VERSION, output)
        self.assertIn(APPLICATION_NAME, output)
        self.assertIn(CHANGELOG_URL, output)


class MainIntegration(TestCase):
    @patch('sys.stdout', new_callable=StringIO)
    def test_it_converts_stream_to_regular_expression(self, mock_stdout):
        with NamedTemporaryFile() as temp_file:
            main(['-i', temp_file.name])

        self.assertEqual(PythonFormatter._EMPTY_STRING_MATCH, mock_stdout.getvalue())
