[![Master Build Status](https://travis-ci.org/radeklat/words-to-regular-expression.svg?branch=master)](https://travis-ci.org/radeklat/words-to-regular-expression)
[![Develop Build Status](https://travis-ci.org/radeklat/words-to-regular-expression.svg?branch=develop)](https://travis-ci.org/radeklat/words-to-regular-expression)

Python 3.4+

Overview
========

PrefixTree is a data structure, that stores string values in form of a prefix
tree (also known as trie or radix tree).

This struture is not intended to be
used as an efficient storage of data. The main purpose is generating compressed
regular expressions that will allow you to use strings operations for thousands
of words in one quick pass over the target string. Here are some of the
features:

**Colapsing of repeated sequences**

For example _"subsubsection"_ will get transformed into _(?:sub){2}section_.

This unfortunately does not produce a
range yet. E.g. _"subsubsection"_, _"subsection"_ and _"section"_ will become
_s(?:ection|ubs(?:ection|ubsection))_ rather than expected
_(?:sub){0,2}section_.

**Automatic escaping of regular expressions.**
  
For example _"test"_ and _"te*st"_ will become _te(?:st|\*st)_.

**Reading words from a file.**

**Support for the* `in` *operator.**