import re
from typing import List


class PrefixTreeNode:
    def __init__(self, terminal_node=False):
        self._edges = None
        self.terminal_node = terminal_node

    def add(self, word: str, new_node: "PrefixTreeNode" = None):
        if not word:
            return

        first_letter = word[0]

        # no edge starting with the same letter, create a new branch
        if self._edges is None or first_letter not in self._edges:
            if self._edges is None:
                self._edges = {}

            self._edges[first_letter] = PrefixTreeEdge(word, True, new_node)
        else:
            self._edges[first_letter].add(word)

    @staticmethod
    def _non_matching_brackets(string: str) -> str:
        return '(?:' + string + ')'

    def _add_me(self, string: str, add_brackets: bool) -> str:
        if self.terminal_node:
            return (self._non_matching_brackets(string) if add_brackets else string) + '?'

        return string

    def to_regexp(self):
        if self._edges is None:  # target node is leaf
            return ''

        # not leaf, get sub-strings from children
        letters = []
        strings = []

        for edge in self._edges.values():
            sub_str = edge.to_regexp()
            if len(sub_str) == 1:  # just one letter received, more can be grouped in [XYZ]
                letters.append(sub_str)
            else:
                # strings received, can be grouped just with | symbol
                strings.append(sub_str)

        if letters and not strings:  # just letters
            if len(letters) == 1:  # just one letter
                return self._add_me(letters[0], False)

            # more letters, group in []
            return self._add_me(
                '[' + ''.join(PrefixTreeNode.compress_range(letters)) + ']', False
            )
        elif not letters and len(strings) == 1:  # just one string
            return self._add_me(strings[0], True)
        else:  # combination of letters and strings
            if len(letters) > 1:
                strings.insert(0, '[' + ''.join(letters) + ']')
            elif len(letters) == 1:
                strings.insert(0, letters[0])

            return self._add_me(self._non_matching_brackets('|'.join(strings)), False)

    @staticmethod
    def compress_range(letters: List[str]) -> List[str]:
        letters.sort()
        letters_out = []
        last_letter = letters[0]
        first_letter = letters[0]

        for letter in letters[1:]:
            if letter.isalnum() and ord(letter) == ord(last_letter) + 1:
                pass
            else:
                if first_letter != last_letter:
                    letters_out.append("%s-%s" % (first_letter, last_letter))
                else:
                    letters_out.append(re.escape(last_letter))

                first_letter = letter

            last_letter = letter

        if first_letter != last_letter:
            letters_out.append("%s-%s" % (first_letter, last_letter))
        else:
            letters_out.append(re.escape(last_letter))

        return letters_out


class PrefixTreeEdge(object):
    def __init__(self, label, terminal, new_node=None):
        self._target_node = new_node if new_node is not None else PrefixTreeNode(terminal)
        self._label = label

    def _split(self, word, position):
        new_node = PrefixTreeNode(True)
        new_node.add(self._label[position:], self._target_node)
        self._label = word
        self._target_node = new_node

    def _branch(self, word, position):
        new_node = PrefixTreeNode(False)  # create branching node, not terminal

        # create branch from the original label, use original node as end of the edge
        new_node.add(self._label[position:], self._target_node)

        # create branch from the new word, new node will be needed
        new_node.add(word[position:])
        self._label = word[:position]  # update label to the common part of both
        self._target_node = new_node  # update target node to point to the splitting one

    def add(self, word):
        # find branching
        for i in range(min(len(word), len(self._label))):
            if word[i] != self._label[i]:  # difference found, branch
                self._branch(word, i)
                return

        # no differences on the shortest length of both label and the new word
        if len(word) > len(self._label):
            # current edge is prefix of inputted word
            self._target_node.add(word[len(self._label):])
        elif len(word) < len(self._label):
            # current edge has inputted word as prefix, split it
            self._split(word, len(word))
        else:
            # current word and edge are the same, mark target node as terminal
            self._target_node.terminal_node = True

    def __str__(self):
        return self._label if self._label is not None else ""

    @staticmethod
    def compress(word, block_len=None):
        if block_len is None:
            block_len = len(word) // 2

        # don't compress blocks of two letters or less and single letter words
        if block_len <= 0 or len(word) < 2:
            return word

        compress_word = ''
        work_word = word
        min_work_word_len = block_len * 2

        while len(work_word) >= min_work_word_len:
            remainder_start = block_len
            repeat_cnt = 1

            window = work_word[:block_len]

            while True:
                if work_word.startswith(window, remainder_start):
                    remainder_start += block_len
                    repeat_cnt += 1
                else:
                    break

            if (repeat_cnt > 1 and block_len > 1) or repeat_cnt > 2:
                # there was a repetition of more than two letters
                if block_len == 2 and window.startswith("\\"):
                    compress_word += "[%s]{%s}" % (window, repeat_cnt)
                elif block_len > 1:
                    compress_word += "(?:%s){%s}" % (window, repeat_cnt)
                else:
                    compress_word += "%s{%s}" % (window, repeat_cnt)
                work_word = work_word[remainder_start:]
            else:
                compress_word += work_word[0]
                work_word = work_word[1:]

        compress_word += work_word

        return PrefixTreeEdge.compress(compress_word, block_len - 1)

    def to_regexp(self):
        from_below = self._target_node.to_regexp()

        if len(from_below) + len(self._label) <= 1:  # don't escape single characters
            return self._label + from_below

        return self.compress(re.escape(self._label)) + from_below
