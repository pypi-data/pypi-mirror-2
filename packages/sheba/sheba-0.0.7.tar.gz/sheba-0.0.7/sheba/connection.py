# Copyright 2010 Paul J. Davis <paul.joseph.davis@gmail.com>
# 
# This file is part of Sheba SQL Library, which is released under the
# MIT license.

from library import Library
from statement import Statement
from dbwrapper import ConnectionWrapper

class StatementWrapper(object):
    def __init__(self, st, conn):
        self.st = st
        self.conn = conn
    
    def __call__(self, *args, **kwargs):
        cursor = self.conn.cursor()
        self.st.execute(cursor, self._getargs(*args, **kwargs))
        if self.st.type == "update":
            return cursor.rowcount
        return cursor

    def run(self, *args, **kwargs):
        return self(*args, **kwargs)

    def _getargs(self, *args, **kwargs):
        stargs = {}
        if len(args) > 1:
            raise ValueError("Too many arguments. Expected a dict or nothing.")
        if len(args) == 1 and not isinstance(args[0], dict):
            raise TypeError("If an argument is supplied it must be a dict.")
        elif len(args):
            stargs = args[0]
        if len(kwargs):
            stargs.update(kwargs)
        return stargs
            

class StatementProxy(object):
    def __init__(self, fetch, conn):
        self.__fetch__ = fetch
        self.__conn__ = conn
    
    def __getattr__(self, name):
        return self.__wrap__(name)
    
    def __getitem__(self, name):
        return self.__wrap__(name)

    def __wrap__(self, name):
        return StatementWrapper(self.__fetch__(name), self.__conn__)

class Connection(object):
    def __init__(self, lib, conn):
        self.lib = lib
        self.conn = conn
        self.q = StatementProxy(self.lib.get_query, self.conn)
        self.u = StatementProxy(self.lib.get_update, self.conn)

    def close(self):
        self.conn.close()

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()
