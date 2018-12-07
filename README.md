[![Master Build Status](https://travis-ci.org/radeklat/words-to-regular-expression.svg?branch=master)](https://travis-ci.org/radeklat/words-to-regular-expression)
[![Develop Build Status](https://travis-ci.org/radeklat/words-to-regular-expression.svg?branch=develop)](https://travis-ci.org/radeklat/words-to-regular-expression)

Compatible with Python 3.4+

# Purpose

This library and command line tool compresses multiple strings into one regular expression that can be used to find/match these strings later in larger piece of text.

## Example use

Input string are: `is`, `in`, `it`, `if`

Input text is [The Zen of Python](https://www.python.org/dev/peps/pep-0020/#id3)

Output regular expression is: `i[fnst]`

Output matches are ... finish this

# Installation

As simple as `pip install w2re`

# Usage guide

This project can be used as a library `w2re` or as a command line tool, also `w2re`.

# Features

## Collapsing of repeated sequences

For example `hahaha` will get transformed into `(?:ha){3}`.

This unfortunately does not produce a
range yet. E.g. _"subsubsection"_, _"subsection"_ and _"section"_ will become
_subs(?:ubsection|ection)_ rather than expected
_(?:sub){0,2}section_.

## Automatic escaping of regular expressions
  
For example _"test"_ and _"te*st"_ will become _te(?:st|\*st)_.

## Reading words from a file

**Support for the* `in` *operator.**