Sheba SQL
=========

SQL management for people that don't mind SQL.

Motivation
----------

I can write SQL faster than I can figure out the various library and ORM
abstraction layers. Writing SQL directly in code is pretty disgusting. So
I stole an idea from the `Axamol SQL Library`_ and along with a couple updates
have created this library.

What is it?
-----------

First, we'll consider some basic query definitions::

    >>> queries = """
    ... name: create_roles_table
    ... type: update
    ... sql: |
    ...     CREATE  TABLE roles
    ...     (
    ...         scene   text,
    ...         name    text,
    ...         actor   text,
    ...         UNIQUE(scene, name)
    ...     )
    ... ---
    ... name: add_role
    ... type: update
    ... sql: | 
    ...     INSERT
    ...     INTO    roles(scene, name, actor)
    ...     VALUES  (${scene}, ${name}, ${actor})
    ... ---
    ... name: list_roles
    ... sql: |
    ...     SELECT  name,
    ...             actor
    ...     FROM    roles
    ...     ORDER   BY
    ...             name ASC
    ... ---
    ... name: get_role_attr
    ... sql: |
    ...     SELECT  ${col | ident}
    ...     FROM    roles
    ...     WHERE   name = ${name}
    ... """
    >>>

This is a YAML_ file that defines a couple queries for working with a simple
table that lists scenes, roles, and actors. Generally, you'll want to define
your queries in a file in your Python package and use the static method
``sheba.Library.from_file(path)`` to load the queries. 

Now, to use these in some code::

    >>> import sheba
    >>> lib = sheba.Library(queries)
    >>> conn = sheba.connect(lib, 'sqlite3', ':memory:')

Now that we have a connection, lets create the roles table::

    >>> conn.u.create_roles_table()
    -1

The ``-1`` is due to DDL statements not returning row information. I could
technically create a third class of statement types so avoid this, but in
the not doctest world you can just ignore that return value.

Next we'll insert a couple rows::

    >>> conn.u.add_role(scene="Parrot Sketch", name="MR PRALINE", actor="John Cleese")
    1
    >>> conn.u.add_role(scene="Parrot Sketch", name="SHOP OWNER", actor="Machale Palin")
    1
    >>> conn.u.add_role(scene="Parrot Sketch", name="DEAD PARROT", actor="Fake Parrot")
    1

Yep, it's that simple. And lastly, we'll list the roles in the table:

    >>> for row in conn.q.list_roles():
    ...     print "Name: %(name)s Actor: %(actor)s" % row
    ...
    Name: DEAD PARROT Actor: Fake Parrot
    Name: MR PRALINE Actor: John Cleese
    Name: SHOP OWNER Actor: Machale Palin

As they say, "Wicked awesome."

Possible Query Attributes
-------------------------

The example above only used ``name``, ``type``, and ``sql``. Only ``name`` and
``sql`` are absolutely required. The full list of attributes is:

* ``name`` - The name used to reference this query from Python
* ``desc`` - An explanation of the query for documentation.
* ``type`` - ``query`` or ``update``. Defaults to ``query``.
* ``dbs`` - A list of database names that this SQL will work with. The default
            value is None which is interpreted as "Use this query when no SQL
            has been defined for the current connections database connection."
* ``sql`` - The actual query. SQL is passed through Mako with access to
            any parameter names that were provide to the query. To bind
            a parameter in a query, simply print the value with standard
            Mako syntax like ${my_parameter_name}. Sheba will automatically
            replace it with the proper bind variable syntax and pass the
            supplied value onto the database connection.

.. note::

    It may appear at first glance that the dynamic queries are writing
    parameter values directly into the SQL. They are *NOT*. The actual
    values passed along into the template context are UUID's that will
    be replaced with bind parameters syntax appropriate to your database
    driver. If you're asking yourself, "What if I do want the actual value?"
    you should go fix all of your SQL injection vulnerabilities.

Identifiers in SQL
------------------

If you're feeling particularly precocious there's support for dynamically
setting identifier names in SQL statements.

Given the following YAML query::

    name: get_role_attr
    sql: |
        SELECT ${col | ident}
        FROM    roles
        WHERE   name = ${name}

You can then execute this query like such::

    >>> for row in conn.q.get_role_attr({"col": "actor", "name": "MR PRALINE"}):
    ...     print "%(actor)s" % row
    ...
    John Cleese

License
-------

Released under the MIT license. See the LICENSE file for more details.

.. _`Axamol SQL Library`: http://www.slamb.org/projects/axamol/sql-library/
.. _YAML: http://yaml.org/
