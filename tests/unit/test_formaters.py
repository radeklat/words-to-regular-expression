from typing import Callable
from unittest import TestCase

from src.formaters import BaseFormater, ALL_FORMATERS


class BaseFormatterTestCase(TestCase):
    def test_it_asserts_description(self):
        with self.assertRaises(AssertionError):
            BaseFormater.description()

    def test_it_asserts_code(self):
        with self.assertRaises(AssertionError):
            BaseFormater.code()


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
