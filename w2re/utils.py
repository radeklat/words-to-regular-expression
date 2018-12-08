import os
from typing import (
    TextIO,
    Type,
    Iterable,
)

from w2re import PythonFormatter
from w2re.formatters import BaseFormatter
from w2re.prefix_tree.tree import PrefixTree


def stream_to_regexp(
        stream: TextIO,
        formatter: Type[BaseFormatter] = PythonFormatter
) -> str:
    lines_generator = (line for line in stream.read().split(os.linesep) if line)
    prefix_tree = PrefixTree(lines_generator)
    return prefix_tree.to_regexp(formatter)


def iterable_to_regexp(
        iterable: Iterable[str],
        formatter: Type[BaseFormatter] = PythonFormatter
) -> str:
    return PrefixTree(iterable).to_regexp(formatter)
