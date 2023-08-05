# Copyright 2010 Paul J. Davis <paul.joseph.davis@gmail.com>
# 
# This file is part of Sheba SQL Library, which is released under the
# MIT license.

import datetime
import t

ddate = datetime.date
dtime = datetime.time
ddtime = datetime.datetime

FMT_ERROR = t.util.DatetimeFormatError
pdate = t.util.parse_iso8601_date
ptime = t.util.parse_iso8601_time
pdtime = t.util.parse_iso8601_datetime

def test_fmt_error():
    try:
        pdate("afadsfa")
    except FMT_ERROR, e:
        t.eq(e.mesg, "Invalid date: 'afadsfa'")
        str(e) # Doesn't raise.

def test_utc():
    u = t.util.UTC()
    t.eq(u.utcoffset(1), datetime.timedelta(0))
    t.eq(u.tzname(0), "UTC")
    t.eq(u.dst(1), datetime.timedelta(0))

def test_parse_date():
    t.eq(pdate("1954-06-07"), ddate(1954, 6, 7))
    t.eq(pdate("19540607"), ddate(1954, 6, 7))
    t.eq(pdate("1954-06"), ddate(1954, 6, 1))
    # Bug in Python?
    # t.eq(pdate("1954W23"), ddate(1954, 6, 7))
    t.eq(pdate("1954W23-1"), ddate(1954, 6, 7))
    t.eq(pdate("1954W231"), ddate(1954, 6, 7))
    t.eq(pdate("1954-158"), ddate(1954, 6, 7))
    # Disallowing %Y%j because it parsers YYYYMM
    # t.eq(pdate("1954158"), ddate(1954, 6, 7))

def test_date_errors():
    # Disallowed by iso8601 to avoid confusion with YYMMDD
    t.raises(FMT_ERROR, pdate, "195406")

    t.raises(FMT_ERROR, pdate, "foo")
    t.raises(FMT_ERROR, pdate, "1954-0607")
    t.raises(FMT_ERROR, pdate, "195406-07")
    t.raises(FMT_ERROR, pdate, "1954")

def test_parse_time():
    t.eq(ptime("11:11:00"), dtime(11, 11, 0))
    t.eq(ptime("111100"), dtime(11, 11, 0))
    t.eq(ptime("111200.01"), dtime(11, 12, 0, 10000))
    t.eq(ptime("111200Z"), dtime(11, 12, 0, 0, t.util.UTC()))

def test_time_errors():
    t.raises(FMT_ERROR, ptime, "11:1100")
    t.raises(FMT_ERROR, ptime, "1111:00")
    t.raises(ValueError, ptime, "11:11:00+05")

def test_parse_datetime():
    expect = ddtime(1954, 6, 7, 11, 11, 0, 0, t.util.UTC())
    t.eq(pdtime("1954-06-07T11:11:00Z"), expect)
    t.eq(pdtime("1954-06-07 11:11:00"), ddtime(1954, 6, 7, 11, 11))

def test_datetime_errors():
    t.raises(FMT_ERROR, pdtime, "adf")
