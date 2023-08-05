import unittest

from os.path import dirname
from os.path import join

import bz2
import sys

import doctest

# Custom libraries
import libtest
from aeso import AB_TZ
from aeso import aieslog

class TestAiesLog(unittest.TestCase):
    def test_parse_asset_list_file(self):
        test_file = join(dirname(__file__), 'res', 'RealTimeShiftReportServlet.csv.bz2')
        f = bz2.BZ2File(test_file)

        num_rows = 0
        for dt, entry in aieslog.parse_aieslog_file(f):
                num_rows += 1
                #print dt.astimezone(AB_TZ), entry
        f.close()
        self.assertEquals(num_rows, 29)


class TestAiesLogWebservice(unittest.TestCase):
    def test_parse_asset_list_file(self):
        f = aieslog.urlopen()
        rows = list(aieslog.parse_aieslog_file(f))
        f.close()
        self.assertTrue(len(rows) > 5)


loader = unittest.TestLoader()
remote_suites = [
    loader.loadTestsFromTestCase(TestAiesLogWebservice),
    doctest.DocTestSuite(aieslog),
]

local_suites = [
    loader.loadTestsFromTestCase(TestAiesLog),
]


if __name__ == '__main__':
    sys.exit(libtest.main(sys.argv[1:], local_suites, remote_suites))
