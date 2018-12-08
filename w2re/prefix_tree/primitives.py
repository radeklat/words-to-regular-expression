import re

from w2re.prefix_tree.letter_range_utils import collapse_letter_ranges


def get_stop_index(word, sliding_window_length):
    """ Stop index for two adjacent sliding windows.

    For blActgActgA it would be::

        blAct | gActg | A -> b | lActg | ActgA

    """
    return len(word) - sliding_window_length * 2 + 1


def add_brackets_around_string(word: str):
    """Adds square brackets for single character strings and round the rest.
    """
    if len(word) == 1 or (len(word) == 2 and word.startswith('\\')):
        return word

    return '(?:' + word + ')'


def compress(word, sliding_window_len=None):
    """
    This function uses sliding window of decreasing size to find repeated,
    non-overlapping and adjacent sub-strings.

    Example::

        BLACTGACTGA contains BL - 2x ACTG - A or BLA - 2x CTGA

    Note that the sub-string can be repeated more than 2x, so the function remembers
    first window and then next window, that can be repeated 1+ times, while
    counting the repetitions.

    The function also applies itself on the longest discovered sub-string
    recursively. So it discovers shorter sub-strings in sub-strings.

    :param word: Input string.
    :param sliding_window_len: Initial window size. Used by recursion. Do not set this
        yourself.
    :return: Compressed string.
    """
    if sliding_window_len is None:
        sliding_window_len = len(word) // 2

    if sliding_window_len <= 0 or len(word) <= 1:
        return word  # don't compress these

    stop_index = get_stop_index(word, sliding_window_len)
    i = 0
    compression_observed = False

    while i < stop_index:
        next_window_start = i + sliding_window_len  # there can be more than 2 windows
        first_window = word[i:next_window_start]
        repeat_count = 0

        while True:  # Repeat next windows until non-matching found
            next_window_end = next_window_start + sliding_window_len

            if next_window_end >= len(word) + 1:
                break  # next window overflows the string -> stop

            next_window = word[next_window_start:next_window_end]

            if first_window != next_window:
                break

            repeat_count += 1
            next_window_start = next_window_end

        if repeat_count > 0:
            compression_observed = True
            prefix = word[:i]

            repeated_block_len_end = i + sliding_window_len * (repeat_count + 1)
            suffix = word[repeated_block_len_end:]

            center = add_brackets_around_string(compress(first_window))

            new_word = prefix + center + '{' + str(repeat_count + 1) + '}'
            i = len(new_word) - 1  # skip the compressed part, investigate only the rest
            new_word += suffix
            word = new_word
            stop_index = get_stop_index(word, sliding_window_len)

        i += 1

    return word if compression_observed else compress(word, sliding_window_len - 1)


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
                return self._add_me(re.escape(letters[0]), False)

            # more letters, group in []
            return self._add_me(
                '[' + ''.join(collapse_letter_ranges(letters)) + ']', False
            )

        if not letters and len(strings) == 1:  # just one string
            return self._add_me(strings[0], True)

        # combination of letters and strings
        if len(letters) > 1:
            strings.insert(0, '[' + ''.join(collapse_letter_ranges(letters)) + ']')
        elif len(letters) == 1:
            strings.insert(0, letters[0])

        return self._add_me(self._non_matching_brackets('|'.join(strings)), False)


class PrefixTreeEdge:
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

    def to_regexp(self):
        from_below = self._target_node.to_regexp()

        if len(from_below) + len(self._label) <= 1:  # don't escape single characters
            return self._label + from_below

        return compress(re.escape(self._label)) + from_below
