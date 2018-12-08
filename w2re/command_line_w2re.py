#!/usr/bin/python
import argparse
import sys
from typing import (  # pylint: disable=unused-import; false positive
    Dict,
    Type,
)

from w2re import (
    APPLICATION_NAME,
    CHANGELOG_URL,
    __version__ as VERSION
)
from w2re.formatters import (  # pylint: disable=unused-import; false positive
    ALL_FORMATTERS,
    BaseFormatter,
)
from w2re.utils import stream_to_regexp

FORMATTERS_BY_CODE = {
    formatter.code(): formatter
    for formatter in ALL_FORMATTERS
}  # type: Dict[str, Type[BaseFormatter]]


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
        "%s:\t%s" % (key, formatter.description())
        for key, formatter in FORMATTERS_BY_CODE.items()
    )

    default_formatter_code = ALL_FORMATTERS[0].code()

    parser.add_argument(
        '-f',
        dest='formatter',
        default=default_formatter_code,
        metavar='<type>',
        choices=tuple(FORMATTERS_BY_CODE.keys()),
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

    parser.add_argument(
        '--version',
        dest='show_version',
        default=False,
        action='store_true',
        help='Show version information.'
    )

    args = parser.parse_args(mock_args)

    if args.show_version:
        print('{} {}\n\nFor changelog, see: {}'.format(
            APPLICATION_NAME, VERSION, CHANGELOG_URL
        ))
    else:
        print(stream_to_regexp(args.input, FORMATTERS_BY_CODE[args.formatter]), end='')


if __name__ == '__main__':  # pragma: no cover
    main()
