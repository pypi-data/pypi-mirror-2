"""
    Apartheid Tests
    ~~~~~~~~~~~

    Tests Apartheid.

    :copyright: (c) 2010 by Shawn Presser.
    :license: MIT, see LICENSE for more details.
"""
import os
import sys
import unittest
from apartheid import ParseError, parse

example_path = os.path.join(os.path.dirname(__file__), '..', 'examples')
sys.path.append(os.path.join(example_path, 'print_c_functions'))

class ApartheidBasicTestCase(unittest.TestCase):
    def test_parse_c_include(self):
        elems = parse('#include "foo.h"')
        assert len(elems) == 1
        assert elems[0].name == 'include'
        assert elems[0].file == 'foo.h'
        assert str(elems[0]) == '#include "foo.h"'

def suite():
    from print_c_functions_tests import PrintCFunctionsTestCase
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ApartheidBasicTestCase))
    suite.addTest(unittest.makeSuite(PrintCFunctionsTestCase))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
