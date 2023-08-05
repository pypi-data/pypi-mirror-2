# Copyright 2010 Paul J. Davis <paul.joseph.davis@gmail.com>
# 
# This file is part of Sheba SQL Library, which is released under the
# MIT license.

import pickle
import pprint
import sys
import traceback
import uuid

from mako.template import Template
from mako.exceptions import text_error_template

import dbwrapper

class IncompleteStatementError(KeyError):
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return "Missing required field: %s" % self.name

class RenderError(RuntimeError):
    def __init__(self, mesg):
        self.mesg = mesg
    def __str__(self):
        return self.mesg

class DBError(Exception):
    def __init__(self, method, name, sql, args, exc_info=None):
        self.method = method
        self.name = name
        self.sql = sql
        self.bound = []
        for a in args:
            self.bound.append((a, a.__class__.__name__))
        self.trace = None
        if exc_info is not None:
            self.trace = traceback.format_exc()

    def __str__(self):
        info = [
            'Statement: %s' % self.name,
            'Method: %s' % self.method,
            'SQL:\n%s' % self.sql,
            'Bound:\n%s' % pprint.pformat(self.args)
        ]
        if self.trace:
            info.append("Cause:\n%s" % self.trace)
        return '\n'.join(info)        

class DBStatement(object):
    
    PARAM_STYLES = {
        'qmark': '?',
        'format': '%s',
        'pyformat': '%s'
    }
    
    def __init__(self, sql):
        self.sql = sql
        self.tmpl = Template(sql)

    def escape(self, conn, name):
        """\
        Escape a value to be used as an identifier.
        """
        info = dbwrapper.DB_INFO.get(conn.dbdesc())
        if not info:
            raise KeyError("No database info for: %s" % conn.dbdesc())
        
        if info.native_case == "upper":
            name = name.upper()
        elif info.native_case == "lower":
            name = name.lower()
        
        bsEscape = info.backslash_esc
        idQuote = info.ident_quote

        ret = [idQuote]
        for c in name:
            if c == idQuote:
                ret.extend([idQuote, idQuote])
            elif c == '\\' and bsEscape:
                ret.append('\\\\')
            else:
                ret.append(c)
        ret.append(idQuote)
        return ''.join(ret)

    def prepare(self, conn, args):
        # Make uuids for access in the template.
        argids = dict((k, uuid.uuid4().hex) for k in args)
        identids = dict((k, uuid.uuid4().hex) for k in argids)
        def ident(aid):
            for name, argid in argids.iteritems():
                if argid == aid:
                    return identids[name]
            raise KeyError("Unknown argument: %s" % aid)

        try:
            sql = self.tmpl.render(ident=ident, **argids)
        except:
            mesg = text_error_template().render()
            raise RenderError(mesg)

        # Replace identifiers
        for name, identid in identids.iteritems():
            if sql.find(identid) < 0:
                continue
            if not isinstance(args[name], basestring):
                raise TypeError("Identifier arguments must be strings.")
            sql = sql.replace(identid, self.escape(conn, args[name]))

        # Figure out the list of parameters to bind
        poslist = []
        for key, argid in argids.iteritems():
            pos = sql.find(argid)
            while pos >= 0:
                poslist.append((pos, key))
                pos = sql.find(argid, pos+1)
        poslist.sort()

        # Build the args list that will get sent to the db
        bound = []
        for p in poslist:
            bound.append(args[p[1]])

        # Repalce argids in the query with the bind parmeter syntax
        syntax = self.PARAM_STYLES[conn.driver.paramstyle]
        for argid in argids.itervalues():
            sql = sql.replace(argid, syntax)

        return (sql, bound)

class Statement(object):
    
    def __init__(self, obj):
        try:
            self.name = obj["name"]
            self.desc = obj.get("desc", None)
            self.type = obj.get("type", "query")

            dbst = DBStatement(obj["sql"])

            self.dbs = {}
            dbs = obj.get("dbs", [None])
            if isinstance(dbs, basestring):
                dbs = dbs.split()
            dbs = set(dbs)
            for db in dbs:
                self.dbs[db] = dbst

        except KeyError, inst:
            raise IncompleteStatementError(inst.args[0])
    
    def merge(self, st):
        if st.name != self.name:
            raise ValueError("Mismatched statement name: %s" % st.name)
        if st.type != self.type:
            raise ValueError("Mismatched statement type: %s" % st.type)
        if st.desc and not self.desc:
            self.desc = st.desc
        for db, info in st.dbs.iteritems():
            if db in self.dbs:
                raise ValueError("SQL for db already defined: %s" % db)
            self.dbs[db] = info
        return self

    def execute(self, cursor, args):
        if not isinstance(args, dict):
            raise TypeError("Expected a dict instance: %r" % args)
        dbdesc = cursor.connection.dbdesc()
        if dbdesc not in self.dbs:
            if None in self.dbs:
                dbdesc = None
            else:
                raise KeyError("No SQL for database: %s" % dbdesc)
        (sql, bound) = self.dbs[dbdesc].prepare(cursor.connection, args)
        try:
            cursor.execute(sql, bound)
        except:
            raise DBError(self.type, self.name, sql, bound, sys.exc_info())
