# Copyright 2010 Paul J. Davis <paul.joseph.davis@gmail.com>
# 
# This file is part of Sheba SQL Library, which is released under the
# MIT license.

import t

def test_connect():
    l = t.Library.from_file(t.yaml("conn-queries"))
    conn = t.sheba.connect(l, 'sqlite3', ':memory:')
    t.eq(isinstance(conn, t.Connection), True)