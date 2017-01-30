# coding: utf-8
"""
module to check if a string is a regex or plain text
"""

import re
import ast

#NO_SPECIAL_CHARS = re.compile(r'^[^.\^$*+?{}\\()]+$')
#SPECIAL_CHAR = re.compile(r'(?<!\\)[\^.$*+?\[\](){}]|\\[AbBdDsSwWZ]')
RE_DOT = re.compile(r'(?<!\\)[.?*]')
RE_ESCAPE = re.compile(r'\\(.)')

def unescape(string):
    r"""
    remove backslash escapes for string matching.
    this may well not be working for all double escape scenarios 

    somewhat working, but still has issues with i.e. '\n'

    >>> unescape('asdf \.\?\(dkdk\)\*')
    'asdf .?(dkdk)*'
    >>> unescape(re.escape('asdf .?(dfkdk*\\w+{4}(?P<dkdk>alskdjf\\)'))
    'asdf .?(dfkdk*\\w+{4}(?P<dkdk>alskdjf\\)'
    >>> unescape(re.escape('asdf\n'))
    'asdf\n'
    """
    print(string)
    return RE_ESCAPE.sub(r'\1', string)


def is_plain(string):
    r"""
    test if given string is a plain text or a regular expression.

    in general, plain text strings (with the exception of `.` will match themselves,
        while regular expressions won't.
    it is very likely that there are regex 'quines' that will match themselves,
        but these seem very unlikely to occur in the wild by accident.

    >>> is_plain('asdf ~=\t-_0230#!@"%&`你好><,/;:')
    True
    >>> is_plain('asdf\ndkdkdk\ndkasdflkj\n\rlsdl')
    True
    >>> is_plain('asdf\^\.\$\*\+\?\[\]\(\)\{\}\\w')  # TODO: r'\\'
    True

    >>> is_plain('a.b')
    False
    >>> is_plain('a\db')
    False
    >>> is_plain('a(bcd|efg)')
    False
    >>> is_plain('asdf|dkdkd')
    False
    >>> is_plain('a[bc]d')
    False
    >>> is_plain('a(?:asdf)')
    False
    >>> is_plain('a(?P<xxx>asdf)')
    False
    >>> is_plain('^asdf$')
    False
    >>> is_plain('asdf?')
    False
    >>> is_plain('asdf*')
    False
    >>> is_plain('asdf{4}')
    False
    """
    # escapes don't match themselves...
    target = unescape(string)
    pattern = r'^(?:%s)$' % (string, )
    matches_itself = bool(re.match(pattern, target, flags=re.U | re.M))
    no_dot = not bool(RE_DOT.search(string))
    return matches_itself and no_dot
