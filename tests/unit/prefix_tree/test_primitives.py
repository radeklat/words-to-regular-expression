from unittest import TestCase

from src.prefix_tree.primitives import compress


class Compress(TestCase):
    def test_compresses_strings_correctly(self):
        samples = [
            ['\\ª\\ª\\ª\\ª\\ª\\ª\\ª\\ª', '(?:(?:[\\ª]){2}){2}'],
            ['a', 'a'],
            ['aa', 'aa'],
            ['aaa', 'a{3}'],
            ['aaaa', '(?:aa){2}'],
            ['aaaaa', '(?:aa){2}a'],
            ['aaaaaa', '(?:a{3}){2}'],
            ['aaaaaaa', '(?:a{3}){2}a'],
            ['aaaaaaaa', '(?:(?:aa){2}){2}'],
            ['aaaaaaaaa', '(?:(?:aa){2}){2}a'],
        ]

        for string, expected_regexp in samples:
            with self.subTest(string=string):
                self.assertEqual(expected_regexp, compress(string))