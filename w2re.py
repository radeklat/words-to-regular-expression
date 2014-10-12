#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on 19.4.2013
@author: Radek Lát <radek.lat@gmail.com>
"""

import re
import sys
import argparse


def file_to_regexp(filename):
    """
    Reads strings from given file and constructs a compressed regular expression from it.
    :param str filename: File name of the input file. Each line should represent one word. Empty lines are ignored.
    :return: String with compressed regular expression or None if file could not be read.
    """
    try:
        f = open(filename, 'r')
        pt = PrefixTree([x for x in f.read().split('\n') if len(x) > 0])
        return pt.to_regexp()
    except FileNotFoundError:
        return None


def file_to_regexp_word_match(filename):
    """
    Reads strings from given file and constructs a compressed regular expression from it. This regular expression can
    be directly used for matching words in Python, using the :py:class:`re` module. Empty line in the input file are
    ignored.
    :param str filename: File name of the input file. Each line should represent one word.
    :return: String with compressed regular expression or None if file could not be read.
    """
    try:
        f = open(filename, 'r')
        pt = PrefixTree([x for x in f.read().split('\n') if len(x) > 0])
        return pt.to_regexp_word_match()
    except FileNotFoundError:
        return None

add_parenthesis = lambda string: '(?:' + string + ')'


class PrefixTree(object):
    """
    Prefix tree structure representation.
    """
    
    def __init__(self, data=None):
        """
        Constructor.
        :param data Iterable of initial items.
        """
        self.root = PrefixTreeNode()  # Root node of the trie.
        if data is not None:
            for item in data:
                self.add(item)
        
    def add(self, data):
        """
        Adds a word in the structure.
        :param data: A word to be put in the tree. Any object can be supplied but it will be converted to string.
        """
        word = str(data)
        
        if data is None or len(word) <= 0:
            return
        
        self.root.add(word)
        
    def extend(self, iterable):
        """
        Adds multiple word to the structure. Duplicates are ignored.
        :param iterable: Any valid iterable of objects. The :py:meth:`~PrefixTree.add` will be used on each of the
        input objects.
        """
        for item in iterable:
            self.add(item)
    
    def to_regexp(self):
        """
        :return Returns regular expression representation of the structure. If the structure is empty, returns
        regular expression matching empty string.
        """
        regexp = self.root.to_regexp()
        return regexp if len(regexp) > 0 else "\A\Z"
    
    def to_regexp_word_match(self):
        """
        :return Returns word matching regular expression representation of the structure. If the structure is empty,
        returns regular expression matching empty string.
        """
        regexp = self.to_regexp()
        return "((?:(?:\W+|\A)%s)+(?:\W+|\Z))" % regexp if regexp != "\A\Z" else regexp
    
    def compress(self, word):
        """
        :param word Any object. It will be converted to string.
        :return Input word in form of a compressed regular expression.
        """
        return PrefixTreeEdge.compress(self, str(word))


class PrefixTreeNode(object):
    """
    Prefix tree node representation.
    """
    
    def __init__(self, terminal=False):
        """
        :param terminal Is the node terminal node?
        """
        self.edges = None
        self.terminal = terminal
        
    def add(self, word, new_node=None):
        # no edge starting with the same letter, create a new branch
        if self.edges is None or word[0] not in self.edges:
            if self.edges is None:
                self.edges = {}

            self.edges[word[0]] = PrefixTreeEdge(word, True, new_node)
        else:
            self.edges[word[0]].add(word)

    def __add_me(self, string, parenthesis):
        if self.terminal:
            return (add_parenthesis(string) if parenthesis else string) + '?'
        else:
            return string

    def to_regexp(self):
        if self.edges is None:  # target node is leaf
            return ''
        
        #not leaf, get sub-strings from children
        letters = []
        strings = []
        
        for edge in self.edges.values():
            sub_str = edge.to_regexp()
            if len(sub_str) == 1:  # just one letter received, more can be grouped in [XYZ]
                letters.append(sub_str)
            else:
                strings.append(sub_str)  # strings received, can be grouped just with | symbol

        if len(letters) > 0 and len(strings) == 0:  # just letters
            if len(letters) == 1:  # just one letter
                return self.__add_me(letters[0], False)
            else:  # more letters, group in []
                return self.__add_me('[' + ''.join(PrefixTreeNode.compress_range(letters)) + ']', False)
        elif len(letters) == 0 and len(strings) == 1:  # just one string
            return self.__add_me(strings[0], True)
        else:  # combination of letters and strings
            if len(letters) > 1:
                strings.insert(0, '[' + ''.join(letters) + ']')
            elif len(letters) == 1:
                strings.insert(0, letters[0])
                
            return self.__add_me(add_parenthesis('|'.join(strings)), False)

    @classmethod
    def compress_range(cls, l):
        l.sort()
        l_out = []
        last_letter = l[0]
        first_letter = l[0]

        ord_range = lambda x, low, high: ord(low) <= ord(x.lower()) <= ord(high)

        for letter in l[1:]:
            if (ord_range(letter, 'a', 'z') or ord_range(letter, '0', '9')) and ord(letter) == ord(last_letter) + 1:
                pass
            else:
                if first_letter != last_letter:
                    l_out.append("%s-%s" % (first_letter, last_letter))
                else:
                    l_out.append(re.escape(last_letter))

                first_letter = letter

            last_letter = letter

        if first_letter != last_letter:
            l_out.append("%s-%s" % (first_letter, last_letter))
        else:
            l_out.append(re.escape(last_letter))

        return l_out


class PrefixTreeEdge(object):
    """
    Prefix tree edge representation.
    """

    def __init__(self, label, terminal, new_node=None):
        self.targetNode = new_node if new_node is not None else PrefixTreeNode(terminal)
        self.label = label
        
    def __split(self, word, position):
        new_node = PrefixTreeNode(True)
        new_node.add(self.label[position:], self.targetNode)
        self.label = word
        self.targetNode = new_node
        
    def __branch(self, word, position):
        new_node = PrefixTreeNode(False)  # create branching node, not terminal
        
        #create branch from the original label, use original node as end of the edge
        new_node.add(self.label[position:], self.targetNode)
        
        #create branch from the new word, new node will be needed
        new_node.add(word[position:])
        self.label = word[:position]  # update label to the common part of both
        self.targetNode = new_node  # update target node to point to the splitting one
        
    def add(self, word):
        #find branching
        for i in range(min(len(word), len(self.label))):
            if word[i] != self.label[i]:  # difference found, branch
                self.__branch(word, i)
                return
            
        #no differences on the shortest length of both label and the new word
        if len(word) > len(self.label):  # current edge is prefix of inputted word
            self.targetNode.add(word[len(self.label):])
        elif len(word) < len(self.label):  # current edge has inputted word as prefix, split it
            self.__split(word, len(word))
        else:  # current word and edge are the same, mark target node as terminal
            self.targetNode.terminal = True
    
    def __str__(self):
        return self.label if self.label is not None else ""

    @classmethod
    def compress(cls, word, block_len=None):
        if block_len is None:
            block_len = len(word) // 2
            
        #don't compress blocks of two letters or less and single letter words
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
                
            if (repeat_cnt > 1 and block_len > 1) or repeat_cnt > 2:  # there was a repetition of more than two letters
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
            
        return cls.compress(compress_word, block_len - 1)
    
    def to_regexp(self):
        from_below = self.targetNode.to_regexp()
        
        if len(from_below) + len(self.label) <= 1:  # don't escape single characters
            return self.label + from_below
        else:            
            return self.compress(re.escape(self.label)) + from_below 

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='w2re - Words to Regular Expression, ' +
                    'a script for converting a list of words into a compressed regular expression.'
    )

    OF_PY_REGEXP = 'pyre'
    OF_PY_REGEXP_WORDMATCH = 'pyrew'

    HELP = {
        OF_PY_REGEXP: 'Python regexp',
        OF_PY_REGEXP_WORDMATCH: 'Python word match regexp'
    }

    parser.add_argument(
        '-of', dest='output_format', default=OF_PY_REGEXP, metavar='<type>', choices=tuple(HELP.keys()),
        help='Output format. Possible value are: ' + ', '.join('%s (%s)' % (k, v) for k, v in HELP.items()) +
             '. Default value is %s.' % OF_PY_REGEXP
    )

    parser.add_argument(
        '-i', dest='input', default=None, metavar='<filename>',
        help='Input file. If none specified, stdin will be used instead.'
    )

    args = parser.parse_args()

    if args.input is not None:
        if args.output_format == OF_PY_REGEXP:
            print(file_to_regexp(args.input))
        elif args.output_format == OF_PY_REGEXP_WORDMATCH:
            print(file_to_regexp_word_match(args.input))
    else:
        pt = PrefixTree([x for x in sys.stdin.read().split('\n') if len(x) > 0])
        if args.output_format == OF_PY_REGEXP:
            print(pt.to_regexp())
        elif args.output_format == OF_PY_REGEXP_WORDMATCH:
            print(pt.to_regexp_word_match())