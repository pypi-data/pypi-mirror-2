#~ pyaeso is a python package that makes access to the Alberta, Canada's
#~ Electric System Operator's (AESO) Energy Trading System (ETS) easier.

#~ Copyright (C) 2010 Keegan Callin

#~ This program is free software: you can redistribute it and/or modify
#~ it under the terms of the GNU General Public License as published by
#~ the Free Software Foundation, either version 3 of the License, or
#~ (at your option) any later version.

#~ This program is distributed in the hope that it will be useful,
#~ but WITHOUT ANY WARRANTY; without even the implied warranty of
#~ MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#~ GNU General Public License for more details.

#~ You should have received a copy of the GNU General Public License
#~ along with this program.  If not, see
#~ <http://www.gnu.org/licenses/gpl-3.0.html>.

'''Access to the Alberta Interconnected Electric System Event log.  The
raw log is accessible at <http://ets.aeso.ca/ets_web/ip/Market/Reports/RealTimeShiftReportServlet>.
'''

# Standard library imports
import urllib2
import csv
from time import strptime
from time import mktime
from datetime import datetime

# Custom libraries
from aeso import AB_TZ
import pytz

def urlopen():
    '''Returns an open file-object connected to AESO's Alberta
    Interconnected Electric System (AIES) event log webservice.'''

    src = 'http://ets.aeso.ca/ets_web/ip/Market/Reports/RealTimeShiftReportServlet?contentType=csv'
    return urllib2.urlopen(src)


def parse_aieslog_file(f):
    '''Yields (:class:`datetime.datetime`, str) 2-tuples containing
    event datetime and description as extracted from file-like object
    `f`.  As always with pyaeso, datetimes are UTC offset-aware and
    should be converted to localized datetimes before being displayed
    to the user.

    .. versionadded:: 0.5

    Example Usage::
        >>> from aeso import aieslog
        >>> from aeso import AB_TZ
        >>>
        >>> from datetime import datetime
        >>> f = aieslog.urlopen()
        >>> for utc_dt, msg in aieslog.parse_aieslog_file(f):
        ...     # Convert UTC to Alberta timezone before printing
        ...     ab_dt = AB_TZ.normalize(utc_dt.astimezone(AB_TZ))
        ...     assert type(ab_dt) == datetime
        ...     assert type(msg) == str # Event description
        ...
        >>> f.close()
    '''

    num_extracted_rows = 0
    reader = csv.reader(f)
    for idx, cells in enumerate(reader):
        try:
            if len(cells) == 0:
                # Blank line.  Ignore and continue
                pass
            elif len(cells) == 2:
                dt_str = cells[0]
                entry = cells[1]

                struct_time = strptime(dt_str, "%m/%d/%Y %H:%M")
                timestamp = mktime(struct_time)
                dt = datetime.fromtimestamp(timestamp)
                ab_dt = AB_TZ.localize(dt)
                utc_dt = pytz.utc.normalize(ab_dt.astimezone(pytz.utc))

                num_extracted_rows += 1
                yield utc_dt, entry
            else:
                raise IndexError('Incorrect number of cells.')
        except (IndexError, ValueError), e:
            if num_extracted_rows > 0:
                raise
            else:
                continue
