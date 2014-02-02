#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 19.4.2013
@author: Radek Lát
@todo: Counting prefix tree
@todo: Make removing items possible
'''

import re

def file_to_regexp(filename):
    '''
    Reads strings from given file and constructs a compressed regular expression
    from it.
    @param filename: File name of the input file. Each line should represent one
    word.
    @type filename: String
    @return: String with compressed regular expression or None if file could not
    be read.
    '''
    try:
        f = open(filename, 'r')
        pt = PrefixTree(f.read().split('\n'))
        return pt.to_regexp()
    except FileNotFoundError:
        return None

def file_to_regexp_word_match(filename):
    '''
    Reads strings from given file and constructs a compressed regular expression
    from it. This regular expression can be directly used for matching words in
    Python.
    @param filename: File name of the input file. Each line should represent one
    word.
    @type filename: String
    @return: String with compressed regular expression or None if file could not
    be read.
    '''
    try:
        f = open(filename, 'r')
        pt = PrefixTree(f.read().split('\n'))
        return pt.to_regexp_word_match()
    except FileNotFoundError:
        return None

class PrefixTree(object):
    '''
    Prefix tree structure representation.
    '''
    
    def __init__(self, data=()):
        '''
        Constructor.
        '''
        
        self.root = PrefixTreeNode()
        '''
        Root node of the trie.
        '''
        
        for item in data:
            self.add(item)
        
    def add(self, data, **kwargs):
        '''
        Adds a word in the structure.
        @param data: Word to be put in the tree. It always gets converted to
        string.
        @param **kwargs: Any additional parameters, that will be added to the
        end node. This node can be retrieved later using find() method. Any
        parameters that could conflict with existing methods or parameters
        will be ignored.
        '''
        word = str(data)
        
        if data == None or len(word) <= 0:
            return
        
        self.root.add(word, args=kwargs)
        
    def extend(self, iterable):
        for item in iterable:
            self.add(item)
        
    def __contains__(self, data):
        search_word = str(data)
                
        if data == None or len(search_word) <= 0:
            return True
        
        return search_word in self.root
    
    def find(self, data):
        '''
        Finds data in the tree.
        @return: Terminal node if found, None otherwise.
        '''
        search_word = str(data)
                
        if data == None or len(search_word) <= 0:
            return None
        
        return self.root.find(search_word)
    
    def to_regexp(self):
        regexp = self.root.to_regexp()
        return regexp if len(regexp) > 0 else "\A\Z"
    
    def to_regexp_word_match(self):
        regexp = self.to_regexp()
        return "((?:(?:\W+|\A)%s)+(?:\W+|\Z))" % regexp if regexp != "\A\Z" else regexp
    
    def compress(self, word):
        return PrefixTreeEdge.compress(self, word)
    
class PrefixTreeNode(object):
    '''
    Prefix tree node representation.
    '''
    
    FORBIDDEN_ARGS = None

    def __init__(self, terminal=False, args={}):
        if self.FORBIDDEN_ARGS == None:
            self.FORBIDDEN_ARGS = self.__dict__.keys()
            
        self.edges = None
        self.terminal = terminal
        self.update_args(args)
        
    def add(self, word, new_node=None, args={}):
        #no edge starting with the same letter, create a new branch        
        if self.edges == None or word[0] not in self.edges:
            if self.edges == None:
                self.edges = {}

            self.edges[word[0]] = PrefixTreeEdge(word, True, new_node, args)
        else:
            self.edges[word[0]].add(word, args)
            
    def update_args(self, args):
        for key, value in args.items():
            if key not in self.FORBIDDEN_ARGS:
                self.__dict__[key] = value
            
    def __contains__(self, word):
        if len(word) == 0: #last one, am I terminal?
            return self.terminal
        
        #if successor does not exist        
        if self.edges == None or word[0] not in self.edges:
            return False
            
        return word in self.edges[word[0]]
    
    def find(self, word):
        if len(word) == 0: #last one, am I terminal?
            return self if self.terminal else None
        
        #if successor does not exist        
        if self.edges == None or word[0] not in self.edges:
            return None
            
        return self.edges[word[0]].find(word)
    
    def __str__(self):
        pass
    
    def __add_parenthesis(self, string):
        return '(?:' + string + ')'
    
    def __add_me(self, string, parenthesis):        
        if self.terminal:
            return (self.__add_parenthesis(string) if parenthesis else string) + '?'
        else:
            return string
        
    @classmethod
    def compress_range(self, l):
        l.sort()
        l_out = []
        last_letter = l[0]
        first_letter = l[0]
        
        for letter in l[1:]:
            if (((ord(letter.lower()) >= ord('a') and ord(letter.lower()) <= ord('z')) or 
            (ord(letter) >= ord('0') and ord(letter <= ord('9')))) and ord(letter) == ord(last_letter) + 1):
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
    
    def to_regexp(self):
        if self.edges == None: #target node is leaf
            return ''
        
        #not leaf, get substrings from children
        letters = []
        strings = []
        
        for edge in self.edges.values():
            sub_str = edge.to_regexp()
            if len(sub_str) == 1: #just one letter received, more can be grouped in [XYZ]
                letters.append(sub_str)
            else:
                strings.append(sub_str) #strings received, can be grouped just with | symbol

        if len(letters) > 0 and len(strings) == 0: #just letters
            if len(letters) == 1: #just one letter
                return self.__add_me(letters[0], False)
            else: #more letters, group in []
                return self.__add_me('[' + ''.join(self.compress_range(letters)) + ']', False)
        elif len(letters) == 0 and len(strings) == 1: #just one string
            return self.__add_me(strings[0], True)
        else: #combination of letters and strings
            if len(letters) > 1:
                strings.insert(0, '[' + ''.join(letters) + ']')
            elif len(letters) == 1:
                strings.insert(0, letters[0])
                
            return self.__add_me(self.__add_parenthesis('|'.join(strings)), False)
    
    
class PrefixTreeEdge(object):
    '''
    Prefix tree edge representation.
    '''

    def __init__(self, label, terminal, new_node=None, args={}):
        self.targetNode = new_node if new_node != None else PrefixTreeNode(terminal, args)
        self.label = label
        
    def __split(self, word, position, args):
        new_node = PrefixTreeNode(True, args)
        new_node.add(self.label[position:], self.targetNode)
        self.label = word
        self.targetNode = new_node
        
    def __branch(self, word, position, args):
        new_node = PrefixTreeNode(False) #create branching node, not terminal
        
        #create branch from the original label, use original node as end of the edge
        new_node.add(self.label[position:], self.targetNode)
        
        #create branch from the new word, new node will be needed
        new_node.add(word[position:], args=args)
        self.label = word[:position] #update label to the common part of both
        self.targetNode = new_node #update target node to point to the splitting one
        
    def add(self, word, args):
        #find branching
        for i in range(min(len(word), len(self.label))):
            if word[i] != self.label[i]: #difference found, branch
                self.__branch(word, i, args)
                return
            
        #no differences on the shortest length of both label and the new word
        if len(word) > len(self.label): #current edge is prefix of inputed word
            self.targetNode.add(word[len(self.label):], args=args)
        elif len(word) < len(self.label): #current edge has inputed word as prefix, split it
            self.__split(word, len(word), args)
        else: #current word and edge are the same, mark target node as terminal
            self.targetNode.terminal = True
            self.targetNode.update_args(args)
    
    def __str__(self):
        return self.label if self.label != None else ""
    
    def __contains__(self, word):
        return word[len(self.label):] in self.targetNode if word.startswith(self.label) else False
    
    def find(self, word):
        return self.targetNode.find(word[len(self.label):]) if word.startswith(self.label) else None
    
    @classmethod
    def compress(self, word, block_len=None):
        if block_len == None:
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
                
            if (repeat_cnt > 1 and block_len > 1) or repeat_cnt > 2: #there was a repetition of more than two letters
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
            
        return self.compress(compress_word, block_len - 1)
    
    def to_regexp(self):
        from_below = self.targetNode.to_regexp()
        
        if len(from_below) + len(self.label) <= 1: #don't escape single characters
            return self.label + from_below
        else:            
            return self.compress(re.escape(self.label)) + from_below 

