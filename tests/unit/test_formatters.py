import re
from typing import (
    Any,
    Callable,
    Iterable,
    Type,
)
from unittest import TestCase

from hypothesis import (
    given,
)

from w2re.formatters import (
    ALL_FORMATTERS,
    BaseFormatter,
    PythonFormatter,
    PythonWordMatchFormatter,
)
from w2re.prefix_tree.tree import PrefixTree
from tests.helpers.hypothesis import (
    LISTS_OF_WORDS,
    NON_ALPHANUMERIC_STRING,
    NON_EMPTY_TEXT_ITERABLES,
    SPECIAL_CHARACTER_STRINGS,
)


class BaseFormatterTestCase(TestCase):
    def assert_method_raises(
            self,
            method: Callable,
            exception_class: Type[Exception],
            *args: Any
    ):
        with self.assertRaises(exception_class):
            method(*args)

    def test_it_asserts_description(self):
        self.assert_method_raises(BaseFormatter.description, AssertionError)

    def test_it_asserts_code(self):
        self.assert_method_raises(BaseFormatter.code, AssertionError)

    def test_it_abstracts_wrap_regexp(self):
        self.assert_method_raises(BaseFormatter.wrap_regexp, NotImplementedError, None)


class OtherFormattersTestCase(TestCase):
    def test_formatters_are_listed(self):
        self.assertGreater(
            len(ALL_FORMATTERS), 0, 'There should be some formatters available.'
        )

    def assert_method_returns_non_empty_string(self, method: Callable):
        self.assertGreater(len(method()), 0, "{} should return non-empty string.".format(
            method
        ))

    def test_it_has_description(self):
        for formatter in ALL_FORMATTERS:
            self.assert_method_returns_non_empty_string(formatter.description)

    def test_it_has_code(self):
        for formatter in ALL_FORMATTERS:
            self.assert_method_returns_non_empty_string(formatter.code)


class BaseTestCase(TestCase):
    _Formatter = BaseFormatter  # type: Type[BaseFormatter]

    def setUp(self):
        assert self._Formatter != BaseFormatter, \
            '_Formatter must be overwritten in sub-classes.'

    def check_formatter_output(self, expected_strings: Iterable[str], delimiter: str = ' '):
        sample_input = delimiter.join(expected_strings)
        regexp = PrefixTree(expected_strings).to_regexp(self._Formatter)

        output_strings = sorted(set(re.compile(regexp).findall(sample_input)))

        self.assertEqual(
            sorted(set(expected_strings)),
            output_strings,
            msg="Regexp: {}\nInput: '{}'".format(regexp, sample_input)
        )

    def check_formatter_output_matches_empty_string(self):
        regexp = PrefixTree([]).to_regexp(self._Formatter)
        output_word = re.compile(regexp).findall('')
        self.assertListEqual([''], output_word)


class PythonFormatterTest(BaseTestCase):
    _Formatter = PythonFormatter

    def test_it_generates_regexps_that_can_match_special_characters(self):
        self.check_formatter_output(list(SPECIAL_CHARACTER_STRINGS.keys()))

    @given(NON_EMPTY_TEXT_ITERABLES)
    def test_it_generates_regexp_that_can_match_input_strings(self, strings):
        self.check_formatter_output(strings)

    def test_it_generates_regexp_that_can_match_empty_input(self):
        self.check_formatter_output_matches_empty_string()


class PythonWordMatchingFormatterTest(BaseTestCase):
    _Formatter = PythonWordMatchFormatter

    @given(LISTS_OF_WORDS, NON_ALPHANUMERIC_STRING)
    def test_it_generates_regexp_that_can_match_input_words(self, words, delimiter):
        self.check_formatter_output(words, delimiter)

    def test_it_generates_regexp_that_can_match_empty_input(self):
        self.check_formatter_output_matches_empty_string()
