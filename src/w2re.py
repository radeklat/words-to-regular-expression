#!/usr/bin/python
import argparse
import os
import sys

from typing import (  # pylint: disable=unused-import; false positive
    Dict,
    TextIO,
    Type,
)

from src import APPLICATION_NAME
from src.formaters import (
    ALL_FORMATERS,
    BaseFormater,
)
from src.prefix_tree.tree import PrefixTree


def stream_to_regexp(stream: TextIO, formater: Type[BaseFormater]) -> str:
    lines_generator = (line for line in stream.read().split(os.linesep) if line)
    prefix_tree = PrefixTree(lines_generator)
    return prefix_tree.to_regexp(formater)


FORMATERS_BY_CODE = {
    formater.code(): formater
    for formater in ALL_FORMATERS
}  # type: Dict[str, Type[BaseFormater]]


APPLICATION_DESCRIPTION = (
    APPLICATION_NAME + ': Words to Regular Expression, script for converting '
    'a list of words into compressed regular expression. Empty lines are ignored.'
)


def main(mock_args=None):
    parser = argparse.ArgumentParser(
        description=APPLICATION_DESCRIPTION,
        formatter_class=argparse.RawTextHelpFormatter
    )

    formats_list = '\n'.join(
        "%s:\t%s" % (key, formater.description())
        for key, formater in FORMATERS_BY_CODE.items()
    )

    default_formatter_code = ALL_FORMATERS[0].code()

    parser.add_argument(
        '-f',
        dest='formater',
        default=default_formatter_code,
        metavar='<type>',
        choices=tuple(FORMATERS_BY_CODE.keys()),
        help="Output format. Default is '{}'. Possible value are:\n\n{}.".format(
            default_formatter_code, formats_list
        )
    )

    parser.add_argument(
        '-i',
        dest='input',
        default=sys.stdin,
        metavar='<filename>',
        type=argparse.FileType('r'),
        help='Input file. If none specified, stdin will be used instead.'
    )

    args = parser.parse_args(mock_args)

    print(stream_to_regexp(args.input, FORMATERS_BY_CODE[args.formater]), end='')


if __name__ == '__main__':  # pragma: no cover
    main()
