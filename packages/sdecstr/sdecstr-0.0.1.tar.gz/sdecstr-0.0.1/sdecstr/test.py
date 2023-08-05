#!/usr/bin/env python
import unittest
from doctest import DocFileSuite, REPORT_ONLY_FIRST_FAILURE

from decimal import Decimal
from sdecstr import SDecStr


class SDecStrTests(unittest.TestCase):
    """ Test various scenarious of the SDecStr class """
    
    test_cases = [('1.00', '1000000000001.00'),
                  ('-1.00', '0999999999999.00'),
                  ('2.00', '1000000000002.00'),
                  ('-2.00', '0999999999998.00'),
                  ('99.00', '1000000000099.00'),
                  ('-99.00', '0999999999901.00'),
                  ('100.00', '1000000000100.00'),
                  ('-100.00', '0999999999900.00'),
                  ('-2837395.00', '0999997162605.00')]

    def testconversion(self):
        """ Convert all test cases to Signed Decimal String and back """
        for i, j in self.test_cases:
            sdstr = SDecStr(Decimal(i))
            s = sdstr.sdstr(16,2)
            self.assertEqual(s, j)
            sdstr = SDecStr(j)
            self.assertEqual(str(sdstr), i)


def test_suite():
    suite = DocFileSuite('sdecstr.txt', 'sa.txt',
                         optionflags = REPORT_ONLY_FIRST_FAILURE)
    return suite


if __name__ == '__main__':
    """ Run all tests """

    unittest.TextTestRunner().run(test_suite())
    unittest.main()
