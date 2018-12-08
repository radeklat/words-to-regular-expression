from w2re.formatters import (
    BaseFormatter,
    PythonFormatter,
    PythonWordMatchFormatter,
)
from w2re.prefix_tree.tree import PrefixTree
from w2re.utils import (
    iterable_to_regexp,
    stream_to_regexp,
)

__version__ = '3.1.0'

APPLICATION_NAME = 'w2re'
CHANGELOG_URL = 'https://github.com/radeklat/words-to-regular-expression/' \
                'blob/develop/CHANGELOG.md'
