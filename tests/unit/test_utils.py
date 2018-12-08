from unittest import TestCase

from hypothesis import given

from tests.helpers.hypothesis import NON_EMPTY_TEXT_ITERABLES
from tests.unit.prefix_tree.test_tree import assert_strings_can_be_matched
from w2re import PythonFormatter
from w2re.utils import iterable_to_regexp


class IterableToRegexp(TestCase):
    @given(NON_EMPTY_TEXT_ITERABLES)
    def test_generates_correct_regexp_from_iterable_of_strings(self, expected_strings):
        assert_strings_can_be_matched(
            self, iterable_to_regexp(expected_strings, PythonFormatter), expected_strings
        )

    def test_it_ignores_empty_strings(self):
        self.assertEqual(
            PythonFormatter._EMPTY_STRING_MATCH, iterable_to_regexp([''], PythonFormatter)
        )

    def test_it_defaults_to_python_formatter(self):
        self.assertEqual(
            PythonFormatter._EMPTY_STRING_MATCH, iterable_to_regexp([''])
        )
