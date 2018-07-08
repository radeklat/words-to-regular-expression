import re
from typing import (
    Any,
    Callable,
    Type,
    List,
)
from unittest import TestCase

from src.formaters import (
    ALL_FORMATERS,
    BaseFormater,
    PythonFormater,
    PythonWordMatchFormater,
)
from src.prefix_tree.tree import PrefixTree


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
        self.assert_method_raises(BaseFormater.description, AssertionError)

    def test_it_asserts_code(self):
        self.assert_method_raises(BaseFormater.code, AssertionError)

    def test_it_abstracts_wrap_regexp(self):
        self.assert_method_raises(BaseFormater.wrap_regexp, NotImplementedError, None)


class OtherFormatersTestCase(TestCase):
    def test_formaters_are_listed(self):
        self.assertGreater(
            len(ALL_FORMATERS), 0, 'There should be some formaters available.'
        )

    def assert_method_returns_non_empty_string(self, method: Callable):
        self.assertGreater(len(method()), 0, "{} should return non-empty string.".format(
            method
        ))

    def test_it_has_description(self):
        for formatter in ALL_FORMATERS:
            self.assert_method_returns_non_empty_string(formatter.description)

    def test_it_has_code(self):
        for formatter in ALL_FORMATERS:
            self.assert_method_returns_non_empty_string(formatter.code)


class BaseTestCase(TestCase):
    INPUT_WORDS = ['hello', 'hi', 'hahaha']
    SAMPLE_TEXT = "hi. this is example hellous hello hihi hahahahah"

    def assert_formater_output(
            self,
            formater: Type[PythonFormater],
            expected_output: List[str]
    ):
        regexp = PrefixTree(self.INPUT_WORDS).to_regexp(formater)
        output_word = re.compile(regexp).findall(self.SAMPLE_TEXT)
        self.assertListEqual(expected_output, output_word)

    def assert_formater_output_matches_empty_string(
            self,
            formater: Type[PythonFormater],
    ):
        regexp = PrefixTree([]).to_regexp(formater)
        output_word = re.compile(regexp).findall('')
        self.assertListEqual([''], output_word)


class PythonFormaterTest(BaseTestCase):
    def test_it_generates_regexp_that_can_match_input_strings(self):
        expected_output = ['hi', 'hi', 'hello', 'hello', 'hi', 'hi', 'hahaha']
        self.assert_formater_output(PythonFormater, expected_output)

    def test_it_generates_regexp_that_can_match_empty_input(self):
        self.assert_formater_output_matches_empty_string(PythonFormater)


class PythonWordMatchingFormaterTest(BaseTestCase):
    def test_it_generates_regexp_that_can_match_input_words(self):
        expected_output = ['hi', 'hello']
        self.assert_formater_output(PythonWordMatchFormater, expected_output)

    def test_it_generates_regexp_that_can_match_empty_input(self):
        self.assert_formater_output_matches_empty_string(PythonWordMatchFormater)
