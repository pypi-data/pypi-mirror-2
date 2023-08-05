# Copyright 2010 Paul J. Davis <paul.joseph.davis@gmail.com>
# 
# This file is part of Sheba SQL Library, which is released under the
# MIT license.

import os
import shutil
import sqlite3
import subprocess as sp

import sheba
import sheba.dbwrapper as dbwrapper
from sheba.library import Library
from sheba.connection import Connection
from sheba.statement import IncompleteStatementError, DBError, Statement
import sheba.util as util

def testdir():
    return os.path.dirname(__file__)

def dbdata():
    return os.path.join(testdir(), "sql", "parrot-sketch.sql")

def srcdbname():
    return os.path.join(testdir(), "parrot.src.db")

def dbname():
    return os.path.join(testdir(), "parrot.db")

def yaml(name):
    return os.path.join(testdir(), "yaml", "%s.yaml" % name)

def dbtest(func):
    if not os.path.exists(srcdbname()):
        with open(dbdata(), "r") as handle:
            sql = handle.read()
        pipe = sp.Popen(['sqlite3', srcdbname()], stdin=sp.PIPE)
        pipe.communicate(input=sql)
        if pipe.wait() != 0:
            raise RuntimeError("Failed to init database.")
    def _func(*args, **kwargs):
        shutil.copy(srcdbname(), dbname())
        conn = dbwrapper.connect("sqlite3", dbname())
        try:
            func(conn, conn.cursor())
        finally:
            conn.close()
    _func.func_name = func.func_name
    return _func

def eq(a, b):
    assert a == b, "%r != %r" % (a, b)

def ne(a, b):
    assert a != b, "%r == %r" % (a, b)

def lt(a, b):
    assert a < b, "%r >= %r" % (a, b)

def gt(a, b):
    assert a > b, "%r <= %r" % (a, b)

def isin(a, b):
    assert a in b, "%r is not in %r" % (a, b)

def isnotin(a, b):
    assert a not in b, "%r is in %r" % (a, b)

def has(a, b):
    assert hasattr(a, b), "%r has no attribute %r" % (a, b)

def hasnot(a, b):
    assert not hasattr(a, b), "%r has an attribute %r" % (a, b)

def raises(exctype, func, *args, **kwargs):
    try:
        func(*args, **kwargs)
    except exctype:
        return
    func_name = getattr(func, "func_name", "<builtin_function>")
    mesg = "Function %s did not raise %s"
    raise AssertionError(mesg % (func_name, exctype.__name__))

