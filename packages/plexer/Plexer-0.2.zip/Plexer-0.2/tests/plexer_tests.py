"""
    Plexer Tests
    ~~~~~~~~~~~

    Tests the Plexer lexer.

    :copyright: (c) 2010 by Shawn Presser.
    :license: MIT, see LICENSE for more details.
"""
import os
import sys
import unittest
import plexer
from plexer import TYPE

example_path = os.path.join(os.path.dirname(__file__), '..', 'examples')
sys.path.append(os.path.join(example_path, 'print_c_includes'))

class BasicFunctionalityTestCase(unittest.TestCase):

    def test_parse_includes(self):
        lines = plexer.tokenize_lines(
            '#include <stdio.h>\n#include "myfile.h"\n',
            lexer=plexer.lexers['c'])
        assert len(lines) == 2
        assert lines[0][0]['value'] == '#include'

        # #include <name.h>
        include_global = [
            TYPE.IDENTIFIER, TYPE.WHITESPACE, TYPE.SPECIAL,
            TYPE.IDENTIFIER, TYPE.SPECIAL, TYPE.IDENTIFIER, TYPE.SPECIAL]

        # #include "name.h"
        include_local = [
            TYPE.IDENTIFIER, TYPE.WHITESPACE, TYPE.STRING]

        verify_token_types = [

            # #include <stdio.h>
            include_global,

            # #include "myfile.h"
            include_local]

        for i in range(len(lines)):
            line = lines[i]
            for j in range(len(line)):
                token = line[j]
                assert token['type'] == verify_token_types[i][j]

def suite():
    import print_c_includes_tests 
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(BasicFunctionalityTestCase))
    suite.addTest(unittest.makeSuite(print_c_includes_tests.BasicFunctionalityTestCase))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
