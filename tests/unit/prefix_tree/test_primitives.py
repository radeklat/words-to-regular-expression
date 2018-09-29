from unittest import TestCase

from src.prefix_tree.primitives import (
    compress,
)


class Compress(TestCase):
    def test_compresses_strings_correctly(self):
        samples = [
            ['abxbxaabxbxa', '(?:a(?:bx){2}a){2}', 'nested repetition'],
            ['blact', 'blact', 'no compression possible'],
            ['blactgactga', 'bl(?:actg){2}a', '2 overlapping substrings'],
            ['blactgactgactga', 'bl(?:actg){3}a', '3 overlapping substrings'],
            ['bactactgactactb', 'b(?:act){2}g(?:act){2}b', 'multiple repetitions'],
            # TODO: optimize to a{7}
            ['aaaaaaa', '(?:(?:a){3}){2}a', 'single letter 7 times'],
            # TODO: optimize to (?:\\ª){8}
            ['\\ª\\ª\\ª\\ª\\ª\\ª\\ª\\ª', '(?:(?:(?:\\ª){2}){2}){2}', 'escaped string'],
        ]

        for string, expected_regexp, name in samples:
            with self.subTest(string=string, test=name):
                self.assertEqual(expected_regexp, compress(string))