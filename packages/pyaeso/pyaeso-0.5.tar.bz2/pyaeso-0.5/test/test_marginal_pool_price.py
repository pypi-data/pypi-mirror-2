import unittest
from datetime import date
from datetime import datetime
from datetime import timedelta
from os.path import join
from os.path import dirname
from StringIO import StringIO
from shutil import copyfileobj
import sys
from bz2 import BZ2File


# 3rd Party Required Libraries
import pytz

# Custom Libraries
from pyaeso import ets
from pyaeso.ets import _filter_mpp_headers

AESO_BUG_1_CANARY = '''"09/01/2004 01","24:15","11.02"
"09/01/2004 01","24:00","11.04"
"08/31/2004 24","24:00","11.02"
"08/31/2004 24","24:00","72.50"
'''

def ab_to_utc(naive_dt, is_dst = None):
    '''Localizes a naive_dt object to the Alberta timezone, then returns
    the UTC equivalent.'''

    ab_dt = ets.ALBERTA_TZ.localize(naive_dt, is_dst = is_dst)
    utc_dt = pytz.utc.normalize(ab_dt.astimezone(pytz.utc))
    return utc_dt


class TestMarginalPoolPriceServiceBehaviour(unittest.TestCase):
    def assert_expected_start_end_behaviour(self, start_date, end_date):
        DATE_FORMAT = '%m/%d/%Y'

        f = ets.urlopen_marginal_pool_price(start_date, end_date)
        text = f.read()
        self.assertTrue(start_date.strftime(DATE_FORMAT) in text, 'start date should have been included in report')
        self.assertFalse(end_date.strftime(DATE_FORMAT) in text, 'end date should not have been included in report')
        f.close()


    def test_start_and_end(self):
        self.assert_expected_start_end_behaviour(date(2004, 8, 31), date(2004, 9, 1))
        self.assert_expected_start_end_behaviour(date(2004, 1, 1), date(2004, 1, 31))
        self.assert_expected_start_end_behaviour(date(2004, 1, 1), date(2004, 1, 31))

        # Try some sample dates.
        self.assert_expected_start_end_behaviour(date(2009, 12, 11), date(2010, 1, 10))
        self.assert_expected_start_end_behaviour(date(2009, 11, 10), date(2009, 12, 10))
        self.assert_expected_start_end_behaviour(date(2009, 10, 10), date(2009, 11, 9))
        self.assert_expected_start_end_behaviour(date(2009, 10, 1), date(2009, 10, 9))

    def test_reversed_start_and_end(self):
        start_date = date(2004, 8, 31)
        end_date = date(2004, 9, 1)

        f = ets.urlopen_marginal_pool_price(end_date, start_date)
        text = f.read()
        self.assertTrue('Report end date must be after begin date.' in text, 'expected error text did not appear.')
        f.close()


    def test_aeso_bug_1(self):
        '''Hour "24" is used alternatively to mean the end of one day
        and the beginning of another.  That is, 2004-31-08 24:00 and
        2004-09-01 24:00 can be used to refer to the same instant.
        Observe the following:

        "09/01/2004 02","01:20","11.03"
        "09/01/2004 02","01:00","20.01"
        "09/01/2004 01","24:26","11.02"
        "09/01/2004 01","24:17","11.02"
        "09/01/2004 01","24:15","11.02" <===
        "09/01/2004 01","24:00","11.04" <=== Where does 24 start and end?
        "08/31/2004 24","24:00","11.02" <===
        "08/31/2004 24","24:00","72.50" <===
        "08/31/2004 24","24:00","11.04"
        "08/31/2004 24","23:00","11.04"
        "08/31/2004 23","22:52","11.04"
        '''
        start_date = date(2004, 8, 31)
        end_date = date(2004, 9, 2)

        f = ets.urlopen_marginal_pool_price(start_date, end_date)
        text = f.read()
        self.assertTrue(AESO_BUG_1_CANARY in text, 'expected aeso_bug_1 canary to sing.')


    def test_dump(self):
        DATE_FORMAT = '%m/%d/%Y'

        start_date = date(2009, 10, 1)
        end_date = date(2010, 1, 10)

        buff = StringIO()
        ets.dump_marginal_pool_price(buff, start_date, end_date)
        text = buff.getvalue()
        buff.seek(0)

        # Make sure all dates are represented in data
        d = start_date
        while d <= end_date:
            #self.assertTrue(d.strftime(DATE_FORMAT) in text, 'Data missing for {0}'.format(d))
            self.assertTrue(d.strftime(DATE_FORMAT) in text, 'Data missing for ' + str(d))
            d += timedelta(1)


class TestMarginalPoolPrice(unittest.TestCase):
    def assertMppDtEquals(self, cells, naive_ab_dt, is_dst = None):
        self.assertEquals(ets._marginal_pool_price_dt(cells), ab_to_utc(naive_ab_dt, is_dst))


    def test_parse(self):
        test_report = join(dirname(__file__), 'res', 'marginal_pool_price_sample.csv.bz2')
        start_date = date(2009, 1, 1)
        end_date = date(2010, 1, 10)

        # Creates a new test file resource
        #~ f = BZ2File(test_report, 'w')
        #~ ets.dump_marginal_pool_price(f, start_date, end_date)
        #~ f.close()

        f = BZ2File(test_report)
        rows = list(ets.parse_marginal_pool_price_file(f))
        f.close()

        for i in xrange(1, len(rows)):
            #self.assertTrue(rows[i].t <= rows[i-1].t, 'Expected time on row {0} to be after row {1} ({2} vs {3})'.format(i, i + 1, rows[i - 1], rows[i]))
            self.assertTrue(rows[i].t <= rows[i-1].t, 'Expected time on row ' + str(i) + ' to be after row ' + str(i+1) + ' (' + repr(rows[i-1]) + ' vs ' + repr(rows[i]) + ')')


    def test_date_handling(self):
        utc_offset = 7

        # aeso_bug_1 compensation
        self.assertMppDtEquals(("09/01/2004 01","24:15","11.02"), datetime(2004, 9, 1, 0, 15))
        self.assertMppDtEquals(("09/01/2004 01","24:00","11.04"), datetime(2004, 9, 1, 0, 0))
        self.assertMppDtEquals(("08/31/2004 24","24:00","11.02"), datetime(2004, 9, 1, 0, 0))
        self.assertMppDtEquals(("08/31/2004 24","24:00","72.50"), datetime(2004, 9, 1, 0, 0))

        # DST tests
        self.assertMppDtEquals(("11/01/2009 04","03:00","28.44"), datetime(2009, 11, 1, 3, 0))
        self.assertMppDtEquals(("11/01/2009 03","02:55","28.44"), datetime(2009, 11, 1, 2, 55))
        self.assertMppDtEquals(("11/01/2009 03","02:39","28.70"), datetime(2009, 11, 1, 2, 39))
        self.assertMppDtEquals(("11/01/2009 03","02:00","29.39"), datetime(2009, 11, 1, 2, 0))
        self.assertMppDtEquals(("11/01/2009 02*","01:31*","30.06"), datetime(2009, 11, 1, 1, 31), False)
        self.assertMppDtEquals(("11/01/2009 02*","01:14*","31.55"), datetime(2009, 11, 1, 1, 14), False)
        self.assertMppDtEquals(("11/01/2009 02*","01:00*","32.25"), datetime(2009, 11, 1, 1, 0), False)
        self.assertMppDtEquals(("11/01/2009 02","01:56","32.25"), datetime(2009, 11, 1, 1, 56), True)
        self.assertMppDtEquals(("11/01/2009 02","01:05","35.67"), datetime(2009, 11, 1, 1, 5), True)
        self.assertMppDtEquals(("11/01/2009 02","01:01","32.00"), datetime(2009, 11, 1, 1, 1), True)
        self.assertMppDtEquals(("11/01/2009 02","01:00","31.50"), datetime(2009, 11, 1, 1, 0), True)
        self.assertMppDtEquals(("11/01/2009 01","24:54","31.55"), datetime(2009, 11, 1, 0, 54))
        self.assertMppDtEquals(("11/01/2009 01","24:48","29.59"), datetime(2009, 11, 1, 0, 48))


if __name__ == '__main__':
    unittest.main()
