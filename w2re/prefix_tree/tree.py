from typing import Optional, Iterable, Type

from w2re.prefix_tree.primitives import PrefixTreeNode
from w2re.formatters import BaseFormatter


class PrefixTree:
    def __init__(self, words: Optional[Iterable[str]] = None) -> None:
        self._root_node = PrefixTreeNode()

        if words is not None:
            self.extend(words)

    def add(self, word: str):
        self._root_node.add(word)

    def extend(self, words: Iterable[str]):
        for word in words:
            self.add(word)

    def to_regexp(self, formatter: Type[BaseFormatter]) -> str:
        """
        :return Returns regular expression representation of the structure.
        If the structure is empty, returns regular expression matching
        empty string.
        """
        return formatter.wrap_regexp(self._root_node)
