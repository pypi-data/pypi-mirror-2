# Copyright 2010 Paul J. Davis <paul.joseph.davis@gmail.com>
# 
# This file is part of Sheba SQL Library, which is released under the
# MIT license.

import t

def with_conn(func):
    @t.dbtest
    def _func(dbconn, cursor):
        lib = t.Library.from_file(t.yaml("conn-queries"))
        conn = t.Connection(lib, dbconn)
        try:
            func(conn)
        finally:
            conn.close()
    _func.func_name = func.func_name
    return _func

@with_conn
def test_query(conn):
    t.eq(conn.q.list_roles().fetchall(), [
        {"name": "MR PRALINE", "actor": "John Cleese"},
        {"name": "SHOP OWNER", "actor": "Machale Palin"}
    ])

@with_conn
def test_query_by_item_access(conn):
    t.eq(conn.q["list_roles"].run().fetchall(), [
        {"name": "MR PRALINE", "actor": "John Cleese"},
        {"name": "SHOP OWNER", "actor": "Machale Palin"}
    ])

@with_conn
def test_update(conn):
    t.eq(conn.u.add_role(
        scene='The Parrot Sketch', name='DEAD PARROT', actor='Fake Parrot'
    ), 1)

@with_conn
def test_dict_arg(conn):
    t.eq(conn.u.add_role({
        "scene": "The Parrot Sketch",
        "name": "PARROT",
        "actor": "Walter Matthau"
    }), 1)

@with_conn
def test_too_many_ags(conn):
    t.raises(ValueError, conn.q.list_roles, 1, 2)

@with_conn
def test_args_is_dict(conn):
    t.raises(TypeError, conn.q.list_roles, [])

@with_conn
def test_no_query(conn):
    t.raises(KeyError, getattr, conn.q, "no_query_named_this")

def count_roles(cursor):
    cursor.execute("select count(*) from roles")
    ret = cursor.fetchone()
    if isinstance(ret, dict):
        return ret.values()[0]
    else:
        return ret[0]

@with_conn
def test_commit(conn):
    c2 = t.sqlite3.connect(t.dbname())
    cursor = c2.cursor()

    t.eq(count_roles(cursor), 2)
    conn.u.add_role(scene="Foo", name="PARROT", actor='Birdy')
    t.eq(count_roles(cursor), 2)
    t.eq(count_roles(conn.conn.cursor()), 3)
    conn.commit()
    t.eq(count_roles(conn.conn.cursor()), 3)
    t.eq(count_roles(cursor), 3)

@with_conn
def test_rollback(conn):
    c2 = t.sqlite3.connect(t.dbname())
    cursor = c2.cursor()
    
    t.eq(count_roles(cursor), 2)
    conn.u.add_role(scene="Foo", name="PARROT", actor="Big Bird")
    t.eq(count_roles(cursor), 2)
    t.eq(count_roles(conn.conn.cursor()), 3)
    conn.rollback()
    t.eq(count_roles(conn.conn.cursor()), 2)
    t.eq(count_roles(cursor), 2)
