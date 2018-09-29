import re
import sre_constants
from unittest import TestCase

from hypothesis import (
    given,
)

from src.formaters import PythonFormater
from src.prefix_tree.tree import PrefixTree
from tests.helpers.hypothesis import (
    NON_EMPTY_TEXT_ITERABLES,
    SPECIAL_CHARACTER_STRINGS,
)


class PrefixTreeTest(TestCase):
    def setUp(self):
        self._tree = PrefixTree()

    def assert_strings_can_be_matched(self, expected_strings):
        example_input = ' '.join(expected_strings)

        regexp = self._tree.to_regexp(PythonFormater)
        try:
            compiled_regexp = re.compile(regexp)
        except sre_constants.error as ex:
            print("Strings {} compiled into invalid regular expression '{}'.".format(
                expected_strings, regexp
            ), ex)
            raise ex

        matched_strings = set(compiled_regexp.findall(example_input))

        self.assertEqual(
            set(expected_strings),
            matched_strings,
            msg="Expected: {}\nMatched: {}\nRegexp: {}".format(
                set(expected_strings), matched_strings, regexp
            )
        )

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

        self.assert_strings_can_be_matched(expected_strings)

    @given(NON_EMPTY_TEXT_ITERABLES)
    def test_accepts_iterable_of_strings(self, expected_strings):
        self._tree.extend(expected_strings)
        self.assert_strings_can_be_matched(expected_strings)

    @given(NON_EMPTY_TEXT_ITERABLES)
    def test_can_be_instantiated_with_initial_iterable_of_strings(self, expected_strings):
        self._tree = PrefixTree(expected_strings)
        self.assert_strings_can_be_matched(expected_strings)
