[![Master Build Status](https://travis-ci.org/radeklat/words-to-regular-expression.svg?branch=master)](https://travis-ci.org/radeklat/words-to-regular-expression)
[![Develop Build Status](https://travis-ci.org/radeklat/words-to-regular-expression.svg?branch=develop)](https://travis-ci.org/radeklat/words-to-regular-expression)

Compatible with Python 3.4+

# Purpose

This library and command line tool compresses multiple strings into one regular expression that can be used to find/match these strings later in larger piece of text.

# Installation

As simple as `pip install w2re`

## Example use

Input string are: `is`, `in`, `it`, `if`, `the`, `than`

As a library:

```python
from w2re import iterable_to_regexp                                         
    
iterable_to_regexp(['is', 'in', 'it', 'if', 'the', 'than'])
```                 

    '(?:i[fnst]|th(?:e|an))'
    
As command line tool:

```bash
echo -e "is\nin\nit\nif\nthe\nthan" | w2re
```
    
    (?:i[fnst]|th(?:e|an))
    
Input text is [The Zen of Python](https://www.python.org/dev/peps/pep-0020/#id3)

Counting words:

```python
from collections import Counter
from re import findall

from requests import get
from w2re import iterable_to_regexp

Counter(
    findall(
        iterable_to_regexp(['is', 'in', 'it', 'if', 'the', 'than']),
        get('https://raw.githubusercontent.com/python/peps/master/pep-0020.txt').text
    )
).most_common()                    
```

    [('is', 15), ('it', 12), ('in', 11), ('than', 8), ('the', 7), ('if', 2)]

# Features

## Collapsing multiple strings from command line input

This is very useful if you need to search for multiple strings and are not sure how to write the correct regexp (or like me, are lazy and write libraries for it instead).

Terminate your input with EOF (Ctrl+D on empty line in Linux).

```bash
w2re
i am searching for this
and this
and this as well
```

    (?:i\ am\ searching\ for\ this|and\ this(?:\ as\ wel{2})?)

## Collapsing of repeated sequences

```bash
echo 'hahaha' | w2re
```

    (?:ha){3}

This unfortunately does not produce a range yet. E.g. `subsubsection`, `subsection` and `section` will become `s(?:ection|ubs(?:ection|ubsection))` rather than expected `(?:sub){0,2}section`.

## Automatic escaping of regular expressions
  
```bash
echo '* test: ...' | w2re
```

    \*\ test\:\ \.{3}

## Reading words from a file on command line

    w2re -i /usr/share/dict/words

## Command line filter

    head -n 10 /usr/share/dict/words | w2re
    
    A(?:\'s|MD(?:\'s)?|OL(?:\'s)?|WS(?:\'s)?|achen(?:\'s)?)

## Reading words from iterable

```python
import w2re                                         
    
w2re.iterable_to_regexp(['is', 'in', 'it', 'if', 'the', 'than'])
``` 

    '(?:i[fnst]|th(?:e|an))'
        
## Reading words from stream

```python
import w2re                 
import io                        
    
w2re.stream_to_regexp(io.StringIO('is\nin\nit\nif\nthe\nthan'))
``` 

    '(?:i[fnst]|th(?:e|an))'

## Multiple output formats

### `w2re.PythonFormatter`

Standard Python formatted regular expression, based on the [re](https://docs.python.org/3/library/re.html) module. This is the default formatter for command line and library.

```python
import w2re                                         
    
w2re.iterable_to_regexp(['is', 'in', 'it', 'if', 'the', 'than'], w2re.PythonFormatter)
```

    '(?:i[fnst]|th(?:e|an))'

### `w2re.PythonWordMatchFormatter`

Standard Python formatted regular expression, based on the [re](https://docs.python.org/3/library/re.html) module. Suitable for matching whole words, rather than strings. Unlike `PythonFormatter`, it won't match `Python` in `Pythonista`.

```python
import w2re                                         
    
w2re.iterable_to_regexp(['is', 'in', 'it', 'if', 'the', 'than'], w2re.PythonWordMatchFormatter)
```

    '(?:\\W+|\\A)((?:i[fnst]|th(?:e|an)))(?=\\W+|\\Z)'
    
### `w2re.BaseFormatter`

Base class for implementation of custom formatters. See the [w2re.formatters](https://github.com/radeklat/words-to-regular-expression/blob/develop/w2re/formatters.py) module.