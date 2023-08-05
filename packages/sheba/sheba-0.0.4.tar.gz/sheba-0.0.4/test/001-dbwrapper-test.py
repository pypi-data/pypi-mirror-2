# Copyright 2010 Paul J. Davis <paul.joseph.davis@gmail.com>
# 
# This file is part of Sheba SQL Library, which is released under the
# MIT license.

from datetime import date, time, datetime

import t

def with_db(func):
    def _func():
        conn = t.dbwrapper.connect("sqlite3", ":memory:")
        try:
            func(conn, conn.cursor())
        finally:
            conn.close()
    _func.func_name = func.func_name
    return _func

def test_connect():
    def do_test(mod, modname):
        conn = t.dbwrapper.connect(modname, ":memory:")
        t.eq(isinstance(conn, t.dbwrapper.ConnectionWrapper), True)
        t.eq(conn.driver, mod)
        cursor = conn.cursor()
        t.eq(isinstance(cursor, t.dbwrapper.CursorWrapper), True)

    import sqlite3
    do_test(sqlite3, "sqlite3")
    
    import sqlite3.dbapi2 as dbapi2
    do_test(dbapi2, "sqlite3.dbapi2")

@with_db
def test_info(conn, cursor):
    t.ne(t.dbwrapper.DB_INFO['sqlite'], t.dbwrapper.DB_INFO['pgsql'])
    t.eq(conn.info(), t.dbwrapper.DBInfo('"', False, None))

@with_db
def test_execute(conn, cursor):
    cursor.execute('create table foo(a int, b date)')
    cursor.execute("insert into foo(a, b) values(1, '1954-06-07')")
    t.eq(cursor.rowcount, 1)
    t.eq(cursor.columns, None)
    cursor.execute("select * from foo")
    t.eq(len(cursor.columns), 2)

@with_db
def test_executemany(conn, cursor):
    cursor.execute("create table foo(a int);")
    cursor.executemany("insert into foo(a) values(?);", [(1,), (2,)])
    t.eq(cursor.rowcount, 2)

@with_db
def test_duplicate_column(conn, cursor):
    try:
        cursor.execute("select 1 as a, 2 as a")
    except t.dbwrapper.DuplicateColumnName, inst:
        t.eq(inst.column, "a")
        str(inst) # Doesn't raise

@with_db
def test_invalid_native_case(conn, cursor):
    try:
        t.dbwrapper.DB_INFO['sqlite'].native_case = "foo"
        cursor.execute("select 1 as a")
    except t.dbwrapper.InvalidNativeCase, inst:
        t.eq(inst.name, "foo")
        str(inst) # Doesn't raise
    finally:
        t.dbwrapper.DB_INFO['sqlite'].native_case = None

@with_db
def test_native_upper(conn, cursor):
    try:
        t.dbwrapper.DB_INFO['sqlite'].native_case = "upper"
        cursor.execute("select 1 as a")
        t.isin("A", cursor.columns)
    finally:
        t.dbwrapper.DB_INFO['sqlite'].native_case = None

@with_db
def test_native_lower(conn, cursor):
    try:
        t.dbwrapper.DB_INFO['sqlite'].native_case = "lower"
        cursor.execute("select 1 as A")
        t.isin("a", cursor.columns)
    finally:
        t.dbwrapper.DB_INFO['sqlite'].native_case = None

@with_db
def test_column(conn, cursor):
    cursor.execute("create table foo(a int);")
    cursor.execute("insert into foo(a) values(1);")
    cursor.execute("select * from foo;")
    col = cursor.columns["a"]
    t.eq(col.name, "a")
    t.eq(col.index, 0)
    # sqlite3 docs says it returns None for
    # everything except name. No idea why.
    t.eq(col.type, None)
    t.eq(col.display_size, None)
    t.eq(col.internal_size, None)
    t.eq(col.precision, None)
    t.eq(col.scale, None)
    t.eq(col.null_ok, None)

@with_db
def test_map_datetime(conn, cursor):
    cursor.columns = {
        "a": t.dbwrapper.Column(conn, 0, ['a', 'date'] + ([None]*5)),
        "b": t.dbwrapper.Column(conn, 1, ['b', 'time'] + ([None]*5)),
        "c": t.dbwrapper.Column(conn, 2, ['c', 'timestamp'] + ([None]*5))
    }
    ret = cursor._maprow(('1954-06-07', '12:17:38', '1954-06-07 12:17:38'))
    t.eq(ret['a'], date(1954, 6, 7))
    t.eq(ret['b'], time(12, 17, 38))
    t.eq(ret['c'], datetime(1954, 6, 7, 12, 17, 38))

@with_db
def test_no_map_non_string(conn, cursor):
    cursor.columns = {
        "a": t.dbwrapper.Column(conn, 0, ['a', 'date'] + ([None]*5))
    }
    ret = cursor._maprow((date(1954, 6, 7),))
    t.eq(ret['a'], date(1954, 6, 7))

@with_db
def test_fetchone(conn, cursor):
    cursor.execute("create table foo(a int);")
    cursor.execute("insert into foo values(1);")
    cursor.execute("select * from foo;")
    t.eq(cursor.fetchone(), {"a": 1})
    t.eq(cursor.fetchone(), None)

@with_db
def test_fetchall(conn, cursor):
    cursor.execute("create table foo(a int);")
    cursor.executemany("insert into foo values(?)", [(1,), (2,)])
    cursor.execute("select * from foo")
    t.eq(cursor.fetchall(), [{"a": 1}, {"a": 2}])

@with_db
def test_iter(conn, cursor):
    cursor.execute("create table foo(a int);")
    cursor.execute("insert into foo values(1);")
    cursor.execute("insert into foo values(1);")
    cursor.execute("select * from foo;")
    count = 0
    for row in iter(cursor):
        count += 1
        t.eq(row["a"], 1)
    t.eq(count, 2)
