# Copyright 2010 Paul J. Davis <paul.joseph.davis@gmail.com>
# 
# This file is part of Sheba SQL Library, which is released under the
# MIT license.

import types

import yaml

from statement import Statement

class ConnectionInfo(object):
    def __init__(self, obj):
        for k in "type name driver".split():
            if k not in obj:
                raise KeyError("Connection info missing required key: %s" % k)
        if obj["type"] != "connection":
            raise ValueError("Invalid connection info type: %s" % obj["type"])
        self.name = obj["name"]
        self.driver = obj["driver"]
        self.args = obj.get("args", tuple())
        self.kwargs = obj.get("kwargs", dict())
        
        if not isinstance(self.name, basestring):
            raise TypeError("Name must be a string")
        if not isinstance(self.driver, basestring):
            raise TypeError("Driver must be a string")
                

class Library(object):
    def __init__(self, library):
        self.conn_info = {}
        self.statements = {"query": {}, "update": {}}
        objiter = iter(yaml.load_all(library))
        self.add_conn_info(objiter)
        for obj in objiter:
            if obj is not None:
                self.add(Statement(obj))
        if len(self.statements["query"]) + len(self.statements["update"]) == 0:
            raise ValueError("YAML file does not define any SQL queries.")
    
    @staticmethod
    def from_file(path):
        with open(path, "rb") as handle:
            return Library(handle)
    
    def add_conn_info(self, iterable):
        for obj in iterable:
            if obj.get('type') != 'connection':
                if obj is not None:
                    self.add(Statement(obj))
                return
            info = ConnectionInfo(obj)
            if info.name in self.conn_info:
                raise ValueError("Duplicate conn info name: %s" % info.name)
            self.conn_info[info.name] = info
    
    def add(self, st):
        if st.type not in self.statements:
            raise ValueError("Unknown statement type: %s" % st.type)
        d = self.statements[st.type]
        if st.name in d:
            d[st.name].merge(st)
        else:
            d[st.name] = st
    
    def get_conn_info(self, name):
        if name not in self.conn_info:
            raise KeyError("No connection info for: %s" % name)
        return self.conn_info[name]
    
    def get_query(self, name):
        return self.statements["query"][name]
    
    def get_update(self, name):
        return self.statements["update"][name]
