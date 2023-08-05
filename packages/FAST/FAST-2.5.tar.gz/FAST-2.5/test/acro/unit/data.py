#
# Unit Tests for the coopr.util package
#

import unittest
import os
import sys
sys.path.append("../../..")
import coopr.util


class spreadsheet(unittest.TestCase):

    def setUp(self):
        self.sheet = coopr.util.ExcelSpreadsheet("Book1.xls")

    def construct(self,filename):
        pass

    def tearDown(self):
        del self.sheet

    def test_get_range_OK(self):
        tmp = self.sheet.get_range("TheRange")
        self.failUnlessEqual( tmp[0] == (u'aa', u'bb', u'cc', u'dd'), True)
        self.failUnlessEqual( len(tmp), 5)

    def test_get_range_FAIL(self):
        try:
           tmp = self.sheet.get_range("BadRange")
        except ValueError:
           pass
        except Exception, err:
           self.fail("test_get_range_FAIL "+str(err))


if __name__ == "__main__":
   unittest.main()
