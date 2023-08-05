# Copyright 2010 Paul J. Davis <paul.joseph.davis@gmail.com>
# 
# This file is part of Sheba SQL Library, which is released under the
# MIT license.

import os

import sheba.dbwrapper as dbwrapper
from sheba.library import Library
from sheba.connection import Connection


def connect(yamlsrc, name=None, driver=None, args=None, kwargs=None):
    """\
    Create a connection object that pairs the database connection and
    a Library object.

    ``yamlsrc`` can be an instance of ``sheba.Library``, a string that
    refers to a file, or a raw YAML string. To decide if the string refers
    to a file, ``os.path.isfile(fname)`` is used. If that fails the string
    is passed directly to the YAML decoder.
    
    If ``name`` is not ``None`` it should refer to a connection info doc
    at the top of your YAML data. This section should describe the default
    parameters to use for your connection. For instance:
    
        name: testing
        type: connection
        driver: sqlite3
        args:
            - /var/lib/dbs/mywebapp.db
        kwargs:
            isolation_level: null
        ---
        name: get_user
        sql: |
            SELECT  name, email
            FROM    users
            WHERE   id = ${user_id}
    
    Any number of connection blocks can be specified in the YAML source as
    long as they are all specified before any of the SQL docs.
    
    If ``driver``, ``args`` or ``kwargs`` is specified they are used to
    replace anything found in the connection info block if ``name`` was
    not ``None``.
    """
    if isinstance(yamlsrc, Library):
        lib = yamlsrc
    elif os.path.exists(yamlsrc):
        lib = Library.from_file(yamlsrc)
    else:
        lib = Library(yamlsrc)
    
    
    if name is not None:
        info = lib.get_conn_info(name)
        driver = driver or info.driver
        args = args or info.args
        kwargs = kwargs or info.kwargs
    
    if args is None:
        args = tuple()
    if kwargs is None:
        kwargs = dict()
    
    conn = dbwrapper.connect(driver, *args, **kwargs)
    return Connection(lib, conn)
