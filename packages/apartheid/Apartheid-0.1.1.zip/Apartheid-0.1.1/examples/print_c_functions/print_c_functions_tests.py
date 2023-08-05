"""
    Print C Functions Tests
    ~~~~~~~~~~~

    Tests the Print C Functions example.

    :copyright: (c) 2010 by Shawn Presser.
    :license: MIT, see LICENSE for more details.
"""
import unittest
import print_c_functions

class PrintCFunctionsTestCase(unittest.TestCase):
    def test_print_functions(self):

        print_c_functions.print_functions('\n'.join(
            ['#include <stdio.h>',
             '#include <stdlib.h>',
             'int i = 42;',
             'int add(int a, int b)',
             '{',
             '  return a + b;',
             '}']))
