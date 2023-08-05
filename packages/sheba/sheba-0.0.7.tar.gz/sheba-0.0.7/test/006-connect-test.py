# Copyright 2010 Paul J. Davis <paul.joseph.davis@gmail.com>
# 
# This file is part of Sheba SQL Library, which is released under the
# MIT license.

import t
from textwrap import dedent

def test_library():
    yaml = dedent("""\
        name: test
        sql: SELECT 'x' as "foo"
        """)
    lib = t.Library(yaml)
    conn = t.sheba.connect(lib, driver='sqlite3', args=(":memory:",))
    t.eq(isinstance(conn, t.Connection), True)

def test_raw_yaml():
    yaml = dedent("""\
        name: test
        sql: SELECT 'x' as "foo"
        """)
    conn = t.sheba.connect(yaml, driver='sqlite3', args=(":memory:",))
    t.eq(isinstance(conn, t.Connection), True)

def test_file_name():
    args = tuple([":memory:"])
    conn = t.sheba.connect(t.yaml("conn-queries"), driver='sqlite3', args=args)
    t.eq(isinstance(conn, t.Connection), True)

def test_kwargs():
    kw = {"database": ":memory:"}
    conn = t.sheba.connect(t.yaml("conn-queries"), driver='sqlite3', kwargs=kw)
    t.eq(isinstance(conn, t.Connection), True)

def test_conn_info():
    conn = t.sheba.connect(t.yaml("with-conn-info"), name="dev")
    t.eq(isinstance(conn, t.Connection), True)

def test_alternate_conn_info():
    conn = t.sheba.connect(t.yaml("with-conn-info"), name="prod")
    t.eq(isinstance(conn, t.Connection), True)