# Copyright 2010 Paul J. Davis <paul.joseph.davis@gmail.com>
# 
# This file is part of Sheba SQL Library, which is released under the
# MIT license.

import t

def test_ok():
    obj = {
        "name": "test",
        "desc": "A simple query",
        "type": "query",
        "dbs": "pgsql",
        "sql": "select * from scenes where actor = ${actor};"
    }
    s = t.Statement(obj)
    t.eq(s.name, "test")
    t.eq(s.desc, "A simple query")
    t.eq(s.type, "query")
    t.eq(s.dbs.keys(), ["pgsql"])
    t.eq(s.dbs["pgsql"].sql, "select * from scenes where actor = ${actor};")
    t.eq(s.dbs["pgsql"].tmpl.render(actor="foo"),
            "select * from scenes where actor = foo;")

def test_missing_name():
    obj = {"sql": "select * from scenes;"}
    t.raises(t.IncompleteStatementError, t.Statement, obj)

def test_missing_sql():
    obj = {"name": "test"}
    t.raises(t.IncompleteStatementError, t.Statement, obj)

def test_statement_error():
    obj = {"name": "test"}
    try:
        t.Statement(obj)
    except t.IncompleteStatementError, e:
        t.eq(e.name, "sql")
        str(e) # Doesn't raise

def test_defaults():
    obj = {"name": "test", "sql": "select * from scenes;"}
    s = t.Statement(obj)
    t.eq(s.name, "test")
    t.eq(s.desc, None)
    t.eq(s.type, "query")
    t.eq(s.dbs.keys(), [None])
    t.eq(s.dbs[None].sql, "select * from scenes;")
    t.eq(s.dbs[None].tmpl.render(), "select * from scenes;")

def test_multiple_dbs():
    obj = {
        "name": "test",
        "dbs": "pgsql sqlite",
        "sql": "select * from scenes;"
    }
    s = t.Statement(obj)
    t.eq(sorted(s.dbs.keys()), ["pgsql", "sqlite"])
    t.eq(s.dbs["pgsql"].sql, "select * from scenes;")
    t.eq(s.dbs["pgsql"], s.dbs["sqlite"])

def test_merge():
    obj1 = {"name": "test", "sql": "select * from scenes;"}
    obj2 = {"name": "test", "dbs": "sqlite", "sql": "select * from scenes2;"}
    s1 = t.Statement(obj1)
    s2 = t.Statement(obj2)
    t.eq(s1.name, s2.name)
    s1.merge(s2)
    t.eq(sorted(s1.dbs.keys()), [None, "sqlite"])
    t.eq(s1.dbs[None].sql, "select * from scenes;")
    t.eq(s1.dbs["sqlite"].sql, "select * from scenes2;")

def test_merge_desc():
    obj1 = {"name": "test", "sql": "select * from scenes;"}
    obj2 = {
        "name": "test",
        "desc": "I am a desc.",
        "dbs": "sqlite",
        "sql": "select * from scenes2;"
    }
    obj3 = {
        "name": "test",
        "desc": "Another desc",
        "sql": "select * from scenes3;"
        
    }
    s1 = t.Statement(obj1)
    s2 = t.Statement(obj2)
    s3 = t.Statement(obj3)
    t.eq(s1.desc, None)
    t.eq(s2.desc, "I am a desc.")
    t.eq(s3.desc, "Another desc")
    
    s1.merge(s2)
    t.eq(s1.desc, s2.desc)
    
    s3.merge(s2)
    t.ne(s3.desc, s2.desc)

def test_merge_errors():
    obj1 = {"name": "test", "sql": "select * from scenes;"}
    obj2 = {"name": "test2", "sql": "select * from actors;"}
    obj3 = {
        "name": "test",
        "type": "update",
        "sql": "insert into scenes values(${scene});"
    }
    obj4 = {"name": "test", "sql": "select * from scenes;"}
    s1 = t.Statement(obj1)
    s2 = t.Statement(obj2)
    s3 = t.Statement(obj3)
    s4 = t.Statement(obj4)
    
    t.raises(ValueError, s1.merge, s2) # Name difference
    t.raises(ValueError, s1.merge, s3) # Type difference
    t.raises(ValueError, s1.merge, s4) # Repeated database

@t.dbtest
def test_prepare(conn, cursor):
    obj = {"name": "test", "sql": "select * from scenes;"}
    s = t.Statement(obj)
    (sql, bound) = s.dbs[None].prepare(conn, {})
    t.eq(sql, "select * from scenes;")
    t.eq(bound, [])

@t.dbtest
def test_prepare_arg(conn, cursor):
    obj = {
        "name": "test",
        "sql": "select * from actors where name = ${name};"}
    s = t.Statement(obj)
    (sql, bound) = s.dbs[None].prepare(conn, {"name": "MR PRALINE"})
    t.eq(sql, "select * from actors where name = ?;")
    t.eq(bound, ["MR PRALINE"])

@t.dbtest
def test_prepare_multi_args(conn, cursor):
    obj = {"name": "test", "sql": "select ${n}, ${a};"}
    s = t.Statement(obj)
    (sql, bound) = s.dbs[None].prepare(conn, {"n": "f", "a": 10})
    t.eq(sql, "select ?, ?;")
    t.eq(bound, ["f", 10])
    
@t.dbtest
def test_prepare_repated_args(conn, cursor):
    obj = {"name": "test", "sql": "select ${n}, ${a}, ${a}, ${n}, ${a};"}
    s = t.Statement(obj)
    (sql, bound) = s.dbs[None].prepare(conn, {"n": "f", "a": 10})
    t.eq(sql, "select ?, ?, ?, ?, ?;")
    t.eq(bound, ["f", 10, 10, "f", 10])

@t.dbtest
def test_execute(conn, cursor):
    obj = {"name": "test", "sql": "select 1 as a;"}
    s = t.Statement(obj)
    s.execute(cursor, {})
    t.eq(cursor.next(), {"a": 1})

@t.dbtest
def test_bad_args(conn, cursor):
    obj = {"name": "test", "sql": "select 1 as a;"}
    s = t.Statement(obj)
    t.raises(TypeError, s.execute, cursor, [])

@t.dbtest
def test_missing_sql(conn, cursor):
    obj = {"name": "test", "dbs": "pgsql", "sql": "select 1 as a;"}
    s = t.Statement(obj)
    t.raises(KeyError, s.execute, cursor, {})

@t.dbtest
def test_bad_sql(conn, cursor):
    obj = {"name": "test", "sql": "select aasf"}
    s = t.Statement(obj)
    t.raises(t.DBError, s.execute, cursor, {})

@t.dbtest
def test_dberror(conn, cursor):
    obj = {"name": "test", "sql": "select a${name}"}
    s = t.Statement(obj)
    try:
        s.execute(cursor, {"name": "foo"})
    except t.DBError, e:
        t.eq(e.method, "query")
        t.eq(e.name, "test")
        t.eq(e.sql, "select a?")
        t.eq(e.bound, [("foo", "str")])
        t.ne(e.trace, None)
        str(e) # Doesn't raise