import re
from typing import Iterable
from unittest import TestCase

from hypothesis import (
    given,
)

from tests.helpers.hypothesis import (
    NON_EMPTY_TEXT_ITERABLES,
    SPECIAL_CHARACTER_STRINGS,
)
from w2re.formatters import PythonFormatter
from w2re.prefix_tree.tree import PrefixTree


def assert_strings_can_be_matched(
        self: TestCase,
        regexp: str,
        expected_strings: Iterable[str]
):
    matched_strings = set(re.findall(regexp, ' '.join(expected_strings)))

    self.assertEqual(
        set(expected_strings),
        matched_strings,
        msg="Expected: {}\nMatched: {}\nRegexp: {}".format(
            set(expected_strings), matched_strings, regexp
        )
    )


class PrefixTreeTest(TestCase):
    def setUp(self):
        self._tree = PrefixTree()

    def test_correctly_encodes_strings_with_special_characters(self):
        for input_string, expected_regexp in SPECIAL_CHARACTER_STRINGS.items():
            with self.subTest(input_string=input_string):
                tree = PrefixTree()
                tree.add(input_string)
                self.assertEqual(expected_regexp, tree._root_node.to_regexp())

    @given(NON_EMPTY_TEXT_ITERABLES)
    def test_accepts_individual_strings(self, expected_strings):
        for string in expected_strings:
            self._tree.add(string)

        assert_strings_can_be_matched(
            self, self._tree.to_regexp(PythonFormatter), expected_strings
        )

    @given(NON_EMPTY_TEXT_ITERABLES)
    def test_accepts_iterable_of_strings(self, expected_strings):
        self._tree.extend(expected_strings)
        assert_strings_can_be_matched(
            self, self._tree.to_regexp(PythonFormatter), expected_strings
        )

    @given(NON_EMPTY_TEXT_ITERABLES)
    def test_can_be_instantiated_with_initial_iterable_of_strings(self, expected_strings):
        self._tree = PrefixTree(expected_strings)
        assert_strings_can_be_matched(
            self, self._tree.to_regexp(PythonFormatter), expected_strings
        )

    def test_it_ignores_empty_strings(self):
        tree = PrefixTree([''])
        self.assertEqual(
            PythonFormatter._EMPTY_STRING_MATCH, tree.to_regexp(PythonFormatter)
        )
