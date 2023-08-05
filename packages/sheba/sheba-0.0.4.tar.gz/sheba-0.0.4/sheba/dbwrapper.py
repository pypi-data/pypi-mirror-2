# Copyright 2002-2005 Scott Lamb <slamb@slamb.org>
# Copyright 2008-2010 Paul J. Davis <paul.joseph.davis@gmail.com>
# 
# This file is part of Sheba SQL Library, which is released under the
# MIT license.

"""\
Wrapper around DB-API 2.0-compliant drivers which provides a sane,
database-independent interface.
"""

import re
import datetime
import logging

import util

class DBInfo(object):
    def __init__(self, ident_quote, backslash_esc, native_case):
        self.ident_quote = ident_quote
        self.backslash_esc = backslash_esc
        self.native_case = native_case
    
    def __eq__(self, other):
        if self.ident_quote == other.ident_quote or \
                self.backslash_esc == other.backslash_esc or \
                self.native_case == other.native_case:
            return True

DB_INFO = dict(
    db2=DBInfo('"', True, "upper"),
    informix=DBInfo('"', False, "upper"),
    mssql=DBInfo('"', False, None),
    mysql=DBInfo("`", False, None),
    oracle=DBInfo('"', False, "upper"),
    pgsql=DBInfo('"', True, "lower"),
    sqlite=DBInfo('"', False, None)
)

DB_ALIASES = {
    'pygresql': 'pgsql',
    'psycopg2': 'pgsql',
    'sqlite3': 'sqlite',
    'sqlite3.dbapi2': 'sqlite',
}

class DuplicateColumnName(Exception):
    def __init__(self, column):
        self.column = column
    def __str__(self):
        return 'Duplicate column name "%s" (after case folding)' % (self.column)

class InvalidNativeCase(ValueError):
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return 'Invalid native case "%s"' % self.name

class Column(object):
    def __init__(self, connection, index, description):
        self.index = index
        self.name = description[0]
        self.type = description[1]
        self.display_size = description[2]
        self.internal_size = description[3]
        self.precision = description[4]
        self.scale = description[5]
        self.null_ok = description[6]

class CursorWrapper(object):
    """A ResultSet class that allows access by column name."""

    TIME_FUNCS = {
        'date': util.parse_iso8601_date,
        'time': util.parse_iso8601_time,
        'timestamp': util.parse_iso8601_datetime
    }

    def __init__(self, connection):
        self.cursor = connection.conn.cursor()
        self.connection = connection
        self.columns = None

    def __getattr__(self, name):
        # Unknown attributes are retrieved from the cursor
        return getattr(self.cursor, name)

    def __iter__(self):
        return self

    def next(self):
        ret = self.fetchone()
        if ret is None:
            raise StopIteration()
        return ret

    def execute(self, operation, *args, **kwargs):
        return self._exec(self.cursor.execute, operation, args, kwargs)

    def executemany(self, operation, *args, **kwargs):
        return self._exec(self.cursor.executemany, operation, args, kwargs)

    def fetchone(self):
        return self._maprow(self.cursor.fetchone())

    def fetchall(self):
        return [d for d in self]

    def _exec(self, executefunc, operation, args, kwargs):
        """\
        Executes a statement, producing better column information for queries.
        """
        if len(args) > 0:
            executefunc(operation, *args)
        else:
            executefunc(operation, **kwargs)

        # Produce sane column info
        columns = None
        cursor = self.cursor
        if cursor.description is not None: # DQL only
            columns = {}
            for i in range(len(cursor.description)):
                column = Column(self.connection, i, cursor.description[i])
                folded = self._fold(column.name)
                if folded in columns:
                    raise DuplicateColumnName(folded)
                columns[folded] = column
        self.columns = columns
        return self

    def _fold(self, name):
        native = DB_INFO[self.connection.dbdesc()].native_case
        if native is None:
            return name
        elif native == "upper":
            return name.upper()
        elif native == "lower":
            return name.lower()
        else:
            raise InvalidNativeCase(native)

    def _maprow(self, row):
        """\
        Creates a dictionary representation of a row.
        """
        if row is None:
            return None
        ret = {}
        for col in self.columns.itervalues():
            ret[col.name] = self._convert(col.type, row[col.index])
        return ret

    def _convert(self, ctype, value):
        if ctype not in self.TIME_FUNCS:
            return value
        if not isinstance(value, basestring):
            return value
        return self.TIME_FUNCS[ctype](value)

class ConnectionWrapper(object):
    def __init__(self, driver, conn):
        self.driver = driver
        self.conn = conn
        self.paramstyle = driver.paramstyle
        self.threadsafety = driver.threadsafety

    def __getattr__(self, name):
        return getattr(self.conn, name)

    def cursor(self):
        return CursorWrapper(self)

    def dbdesc(self):
        name = self.driver.__name__.lower()
        while name in DB_ALIASES:
            name = DB_ALIASES[name]
        return name

    def info(self):
        return DB_INFO.get(self.dbdesc(), None)

def connect(driver_name, *args, **keyword_args):
    """\
    Returns a wrapped database connection.

    ``driver`` is the name of the DBAPI-2.0 module to wrap. All other
    arguments are passed through to its connect function.
    """
    driver = __import__(driver_name)
    for p in driver_name.split(".")[1:]:
        driver = getattr(driver, p)
    return ConnectionWrapper(driver, driver.connect(*args, **keyword_args))
