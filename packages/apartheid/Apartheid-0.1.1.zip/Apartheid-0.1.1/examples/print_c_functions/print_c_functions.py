# -*- coding: utf-8 -*-
"""
    Print C Functions
    ~~~~~~

    Parses a C file and prints any functions.

    :copyright: (c) 2010 by Shawn Presser.
    :license: MIT, see LICENSE for more details.
"""
from apartheid import parse

def print_functions(s):
    pass

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print "Usage: print_c_functions.py myfile.c"
    else:
        try:
            print_functions(open(sys.argv[1], 'r').read())
        except IOError:
            print "Could not open file '" + sys.argv[1] + "' for reading."

