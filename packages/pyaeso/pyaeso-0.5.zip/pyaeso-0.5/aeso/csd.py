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

'''Access to current supply demand (CSD) data.  The raw report can be
accessed at <http://ets.aeso.ca/ets_web/ip/Market/Reports/CSDReportServlet>.'''

# Standard library imports
import urllib2
import csv
from time import strptime
from datetime import datetime
from decimal import Decimal

# Custom libraries
from aeso import AB_TZ
import pytz

def urlopen():
    '''Returns an open file-object connected to AESO's Current Supply
    Demand (CSD) webservice.

    .. versionadded:: 0.5'''
    src = 'http://ets.aeso.ca/ets_web/ip/Market/Reports/CSDReportServlet?contentType=csv'
    return urllib2.urlopen(src)


def _normalize_unit(unit):
    try:
        s = unit[unit.rindex('>') + 1:]
        while s.endswith('"'):
            s = s[0:-1]

        return s
    except ValueError:
        return unit


def parse_csd_file(f, reference_dt = None):
    '''Yields tuples extracted from file-like object `f` as returned by
    :func:`urlopen`.  Tuples may either be either a 3-tuple containing
    a power statistic or a 5-tuple containing generator output status.

    Three-tuples will contain the following data at the listed indices:

    0. (:class:`datetime.datetime`) - UTC and offset-aware time sample
       was taken.
    1. (str) - Data series name.
    2. (:class:`decimal.Decimal`) - Power in MW.

    AESO presently provides data series' with these names (2010-03-10):

    * Alberta Total Net Generation
    * Interchange
    * Alberta Internal Load (AIL)
    * Alberta Load Responsibility
    * Contingency Reserve Required
    * Dispatched Contingency Reserve (DCR)
    * Dispatched Contingency Reserve - Gen
    * Dispatched Contingency Reserve - Other
    * BC Interchange flow
    * SK Interchange flow

    These fields will appear at index one of a three-tuple.

    Five-tuples will contain the generator data at the listed indices:

    0. (:class:`datetime.datetime`) - UTC and offset-aware time sample
       was taken.
    1. (str) - Generator unit name.
    2. (:class:`decimal.Decimal`) - Generator Maximum Continuous Rating
       (MCR) in MW.
    3. (:class:`decimal.Decimal`) - Generator Total Net Generation
       (TNG) in MW.
    4. (:class:`decimal.Decimal`) - Dispatched (and accepted)
       Contingency Reserve (DCR) in MW.

    Generator data may contain "composite" units; For example, the
    "Coal" unit represents the generation output of all coal plangs in
    the province.

    .. versionadded:: 0.5

    Example Usage::
        >>> from aeso import csd
        >>> from aeso import AB_TZ
        >>> series = []
        >>> generators = []
        >>> f = csd.urlopen()
        >>> for cells in csd.parse_csd_file(f):
        ...     if len(cells) == 3:
        ...         series.append(cells)
        ...     else:
        ...         assert len(cells) == 5
        ...         utc_dt, unit, mcr, tng, dcr = cells
        ...         # MCR = Maximum Continuous Rating in MW
        ...         # TNG = Total Net Generation in MW
        ...         # DCR = Dispatched (and accepted) Contingency Reserve in MW
        ...         ab_dt = AB_TZ.normalize(utc_dt.astimezone(AB_TZ))
        ...         generators.append(cells)
        ...
        >>> f.close()
    '''

    utc_dt = None
    num_extracted_rows = 0
    reader = csv.reader(f)
    for idx, cells in enumerate(reader):
        try:
            if len(cells) == 0:
                # Blank line.  Ignore and continue
                pass
            elif len(cells) == 1:
                value = cells[0]
                if value.strip() == 'Current Supply Demand Report':
                    # Ignore report title
                    pass
                elif value.startswith('Last Update :'):
                    struct_time = strptime(cells[0], "Last Update : %b %d, %Y %H:%M")
                    dt = datetime(*struct_time[0:6])
                    #print cells[0], '=>', dt
                    try:
                        ab_dt = AB_TZ.localize(dt, is_dst = None)
                    except pytz.AmbiguousTimeError:
                        # Have reference time
                        if reference_dt is None:
                            raise
                        else:
                            with_dst_dt = AB_TZ.localize(dt, is_dst = True)
                            without_dst_dt = AB_TZ.localize(dt, is_dst = False)

                            if abs(without_dst_dt - reference_dt) <= abs(with_dst_dt - reference_dt):
                                ab_dt = AB_TZ.localize(dt, is_dst = False)
                            else:
                                ab_dt = AB_TZ.localize(dt, is_dst = True)

                    utc_dt = pytz.utc.normalize(ab_dt.astimezone(pytz.utc))
                else:
                    raise ValueError('Unexpected line data')

                num_extracted_rows += 1
            elif len(cells) == 2:
                if dt is None:
                    raise ValueError('No datetime set')
                unit = _normalize_unit(cells[0])

                if unit == 'TOTAL':
                    continue

                if cells[1] == '-':
                    value = ''
                else:
                    value = Decimal(cells[1])

                num_extracted_rows += 1
                yield utc_dt, unit, value
            elif len(cells) == 4:
                if dt is None:
                    raise ValueError('No datetime set')

                unit = _normalize_unit(cells[0])
                if unit == 'TOTAL':
                    continue
                mcr = Decimal(cells[1]) # Maximum continuous rating
                tng = Decimal(cells[2]) # total net generation
                dcr = Decimal(cells[3]) # Dispatched (and Accepted) Contingency Reserve

                num_extracted_rows += 1
                yield utc_dt, unit, mcr, tng, dcr
            else:
                raise IndexError('Incorrect number of cells.')
        except (IndexError, ValueError), e:
            if num_extracted_rows > 0:
                raise
            else:
                continue
