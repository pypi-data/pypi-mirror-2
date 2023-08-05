# Copyright 2010 Paul J. Davis <paul.joseph.davis@gmail.com>
# 
# This file is part of Sheba SQL Library, which is released under the
# MIT license.

import t

def test_basic():
    l = t.Library.from_file(t.yaml("basic"))
    s = l.get_query("test")
    t.eq(s.name, "test")
    t.eq(s.dbs[None].sql, "select 1 as a")
    t.eq(s.dbs["pgsql"].sql, 'select 1 as "a"')
    u = l.get_update("test2")
    t.eq(u.dbs[None].sql, "create table foo(a int);")

def test_no_name():
    try:
        t.Library.from_file(t.yaml("error-no-name"))
    except t.IncompleteStatementError, inst:
        t.eq(inst.name, "name")

def test_no_sql():
    try:
        t.Library.from_file(t.yaml("error-no-sql"))
    except t.IncompleteStatementError, inst:
        t.eq(inst.name, "sql")

def test_invalid_type():
    t.raises(ValueError, t.Library.from_file, t.yaml("error-type"))

def test_defaults():
    lib = t.Library.from_file(t.yaml("defaults-set"))
    s = lib.get_query("test")
    t.eq(s.name, "test")
    t.eq(s.desc, None)
    t.eq(s.type, "query")
    t.eq(s.dbs.keys(), [None])
    t.eq(s.dbs[None].sql, "select * from actors;")

def test_multiple_dbs():
    lib = t.Library.from_file(t.yaml("multiple-dbs"))
    s = lib.get_query("yay")
    t.eq(sorted(s.dbs.keys()), ["pgsql", "sqlite"])
    t.eq(s.dbs["pgsql"], s.dbs["sqlite"])

def test_merge():
    lib = t.Library.from_file(t.yaml("merge"))
    s = lib.get_query("test")
    t.eq(sorted(s.dbs.keys()), [None, "pgsql"])
    t.eq(s.dbs[None].sql, "select * from scenes;")
    t.eq(s.dbs["pgsql"].sql, "select * from scenes2;")

def test_merge_desc():
    lib = t.Library.from_file(t.yaml("merge-desc"))
    t.eq(lib.get_query("test").desc, "Some info")
    t.eq(lib.get_query("test2").desc, "Ignored second")

def test_merge_errors():
    t.raises(ValueError, t.Library.from_file, t.yaml("merge-error"))


