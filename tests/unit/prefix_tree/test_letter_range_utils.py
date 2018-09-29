from unittest import TestCase

from src.prefix_tree.letter_range_utils import collapse_letter_ranges


class CollapseLettersIntoRangesTest(TestCase):
    def assert_collapses_letters_into(self, input_letters, expected_output):
        output = collapse_letter_ranges(input_letters)
        self.assertEqual(expected_output, output)

    def test_one_letter_is_not_collapsed(self):
        input_letters = ['i']
        self.assert_collapses_letters_into(input_letters, input_letters)

    def test_no_range_is_not_collapsed_and_sorted(self):
        input_letters = ['i', 'e', 'a']
        self.assert_collapses_letters_into(input_letters, sorted(input_letters))

    def test_two_consecutive_are_not_collapsed(self):
        input_letters = ['a', 'b', 'd', 'e']
        self.assert_collapses_letters_into(input_letters, input_letters)

    def test_three_consecutive_are_collapsed(self):
        input_letters = ['a', 'b', 'c', 'f', 'h', 'i', 'j']
        self.assert_collapses_letters_into(input_letters, ['a-c', 'f', 'h-j'])

    def test_three_consecutive_non_alphanumeric_are_not_collapsed(self):
        input_letters = ['<', '=', '>']
        self.assert_collapses_letters_into(input_letters, input_letters)

    def test_hyphen_is_first(self):
        self.assert_collapses_letters_into(['a', 'b', 'c', '-'], ['-', 'a-c'])

    def test_special_characters_are_escaped(self):
        samples = {
            '[': ['\['],
            ']': ['\]'],
            '[]': ['\[', '\]'],
            '][': ['\[', '\]'],
            '\\': ['\\\\'],
        }

        for input_string, expected_output in samples.items():
            input_letters = list(input_string)
            with self.subTest(input_letters=input_letters, expected_output=expected_output):
                self.assert_collapses_letters_into(input_letters, expected_output)

    def test_unfinished_alnum_ranges(self):
        samples = [
            ['˒', '0'],
            ['!', '0']
        ]

        for input_letters in samples:
            with self.subTest(input_letters=input_letters):
                self.assert_collapses_letters_into(input_letters, input_letters)
