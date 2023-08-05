# Copyright 2010 Paul J. Davis <paul.joseph.davis@gmail.com>
# 
# This file is part of Sheba SQL Library, which is released under the
# MIT license.


import sheba.dbwrapper as dbwrapper
from sheba.library import Library
from sheba.connection import Connection

def connect(lib, driver, *args, **kwargs):
    """\
    Open a LibraryConnection to the database.
    
    ``lib`` - An instance of sheba.Library to pair with the connection.
    ``driver`` - name of the DB-API 2.0 driver to use
    ``*args`` and ``**kwargs`` are passed to the driver's ``connect`` method
    """ 
    conn = dbwrapper.connect(driver, *args, **kwargs)
    return Connection(lib, conn)

