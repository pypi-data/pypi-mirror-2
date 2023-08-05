# Copyright 2010 Paul J. Davis <paul.joseph.davis@gmail.com>
# 
# This file is part of Sheba SQL Library, which is released under the
# MIT license.

import types

import yaml

from statement import Statement

class Library(object):
    def __init__(self, library):
        self.statements = {"query": {}, "update": {}}
        for obj in yaml.load_all(library):
            self.add(Statement(obj))
    
    @staticmethod
    def from_file(path):
        with open(path, "rb") as handle:
            return Library(handle)
    
    def add(self, st):
        if st.type not in self.statements:
            raise ValueError("Unknown statement type: %s" % st.type)
        d = self.statements[st.type]
        if st.name in d:
            d[st.name].merge(st)
        else:
            d[st.name] = st
    
    def get_query(self, name):
        return self.statements["query"][name]
    
    def get_update(self, name):
        return self.statements["update"][name]
