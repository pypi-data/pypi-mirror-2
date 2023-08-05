# Copyright 2002-2005 Scott Lamb <slamb@slamb.org>
# Copyright 2008-2010 Paul J. Davis <paul.joseph.davis@gmail.com>
# 
# This file is part of Sheba SQL Library, which is released under the
# MIT license.

import datetime
import re

# Disallowing %Y%j because it parses YYYYMM wrong
DATES = "%Y-%m-%d %Y%m%d %Y-%m %YW%W %YW%W-%w %YW%W%w %Y-%j".split()
TIMES = "%H:%M:%S.%f %H%M%S.%f %H:%M:%S %H%M%S %H:%M %H%M %H".split()

class DatetimeFormatError(Exception):
    def __init__(self,mesg):
        self.mesg = mesg
    def __str__(self):
        return self.mesg

class UTC(datetime.tzinfo):
    """UTC"""

    def utcoffset(self, dt):
        return datetime.timedelta(0)

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        return datetime.timedelta(0)


def _parse(val, formats, errmsg):
    for fmt in formats:
        try:
            return datetime.datetime.strptime(val, fmt)
        except ValueError:
            pass
    raise DatetimeFormatError(errmsg % val)
    
def parse_iso8601_date(val):
    d = _parse(val, DATES, "Invalid date: %r")
    return datetime.date(year=d.year, month=d.month, day=d.day)

def parse_iso8601_time(val):
    time, tzinfo = val, None
    if time.strip().endswith("Z"):
        time, tzinfo = val.rstrip("Z"), UTC()
    elif val.find("+") >= 0 or val.find("-") >= 0:
        raise ValueError("Arbitrary timezones are not supported.")
    else:
        time, tzinfo = val, None

    time = _parse(time, TIMES, "Invalid time: %r")
    r = datetime.time(time.hour, time.minute, time.second, time.microsecond)
    if tzinfo:
        return r.replace(tzinfo=tzinfo)
    return r

def parse_iso8601_datetime(val):
    if val.find("T") < 0 and val.find(" ") < 0:
        raise DatetimeFormatError("Invalid datetime: %r" % val)
    if val.find("T") >= 0:
        date, time = val.split("T", 1)
    else:
        date, time = val.split(" ", 1)
    date = parse_iso8601_date(date)
    time = parse_iso8601_time(time)
    return datetime.datetime.combine(date, time)
