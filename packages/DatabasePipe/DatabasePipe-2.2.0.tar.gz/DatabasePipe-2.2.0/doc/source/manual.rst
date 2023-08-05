++++++
Manual
++++++

.. warning:: This package currently only supports PostgreSQL using psycopg2.

.. warning:: This documentation is not up-to-date or correct.

Chapter 1. Introducing the Database Package
+++++++++++++++++++++++++++++++++++++++++++

The Database package is two things:

Database Abstraction Layer
    The simplest possible wrapper over the DB-API to allow you to write code 
    which is reasonably portable across SQLite, PostgreSQL and MySQL

Service
    A service object for the Flows framework to provide a connection pool and
    per-request connections

Let's look at each in turn.

The ``Database`` package has its roots in Lemon, and then the Python Web
Modules and is designed for people who like writing SQL directly to work with
databases rather than using object-relational mappers or other higher-level
abstractions.

Database Abstraction Layer
==========================

How does the Database package improve on the DB-API?
----------------------------------------------------

The Python DB-API 2.0 allows you to write SQL statements and retrieve results
but there are a couple of areas where it could be extended for real-world use:

* the majority of tables commonly have autoincrementing integer primary keys so it
  would be nice to be able to deal with auto-incrementing fields in a
  consistent way across databases, namely have the database API return the
  ``id`` of a newly-inserted row

* ability to change the response format to lists of dictionaries or lists of
  objects rather than just lists of lists (or rather tuples of tuples)

* ability to have the DB-API automatically manage the param style so that
  carefully written SQL will work on all databases, regardless of whether they
  are expecting ``%s``, ``?`` or some other marker for substitutions.

* Ability to embed a converter to correct with driver-specific issues such as 
  the ``psycopg2`` module's use of Unicode 

In addition, it would be nice to be able to:

* have an API which made simple inserts, queries and updates against one record
  trivially simple and not require any SQL

* ability to pool database connections to improve latency

The Database package provides all these features.

Why not use an even higher-level abstraction like SQLAlchemy?
-------------------------------------------------------------

Here are some reasons:

* If you already know SQL and aren't likely to need cross-database support then
  there is little point in investing the time to learn the higher-level
  abstraction's APIs when they won't give you the same control as direct SQL
  anyway

* The Database package is only a few hundred lines of code so any problems will
  be much easier to track down

If these two reasons don't apply you might be better off with the higher level
abstraction.

The Helpers
-----------

The Database package's functionality is implemented as a series of simple helpers:

.. autofunction:: databasepipe.helper.query

.. autofunction:: databasepipe.helper.update_record

.. autofunction:: databasepipe.helper.insert_record

.. autofunction:: databasepipe.helper.page_data

Services
========

Although the helpers do their jobs perfectly well it can quickly become tedious to 
keep specifying the ``connection``, ``paramstyle`` and ``database_type`` arguments 
when they are likely to be the same for a particular web request.

To solve this problem you can use a *service* to keep track of these values and 
apply them for you.

An Example
----------

Here's an example where we use the ``start_flow()`` function to create a
``DatabaseConnectionService`` to connect to an SQLite database storing its data
in memory. The ``start_flow()`` function will call the ``run()`` function with
a single argument which has a ``database`` attribute. This object has a number
of helpers attached and will automatically connect to the database the first
time one of its helpers is called. It will then re-use that same connection for
all subsequent helper calls from that ``flow`` object. At the end of the
``run()`` function, the ``start_flow()`` function will close any open
connections, committing any outstanding changes unless an error occurred, in
which case it will rollback all the changes that were made with that ``flow``
object so that the database is not left in an inconsistent state.

Here's our configuration using an in-memory SQLite database:

.. sourcecode :: pycon

    >>> option = {'database': {'plugin': u'sqlite3', 'database': u':memory:'}}

Here's some sample code:

.. sourcecode :: pycon

    >>> from databasepipe.service.connection import DatabasePipe
    >>> from pipestack.app import App, pipe
    >>> from pipestack.ensure import ensure
    >>>
    >>> class TestApp(App):
    ...     pipes = [
    ...         pipe('database', DatabasePipe),
    ...     ]
    >>>
    >>> @ensure('database')
    ... def run(bag):
    ...     print bag.database.query('SELECT 1 AS Res;')
    ... 
    >>> app = TestApp(option=option)
    >>> app.start_flow(
    ...     run=run,
    ... )
    [{'Res': 1}]

Database Drivers
----------------

Every database engine (eg PostgreSQL, MySQL, MS SQL Server etc) is different
and each different engine often has different drivers (eg for PostgreSQL you
could use ``psycopg`` or ``psycopg2``).

The Database package supports the concept of *plugins* so that different
engines and drivers can be supported without changing the API. The plugins
each have a name which usually reflects the underlying database driver (eg
``psycopg2`` etc) but can actually be named whatever you like.

To use a database you must specify the plugin you wish to use. If you are
using a connection service, the Database package will load the plugin to
determine the engine and driver you are using.

Connection Pool
--------------- 

When running a web application it can sometimes be useful to keep a pool of
database connections open and give them out as they are needed by different
requests. This saves the web application having to connect and disconnect from
the database on every request.

Once you are using the structure shown in the previous example, this is just a
case of importing, configuring and using a ``DatabaseConnectionPoolService``
instead of a ``DatabaseConnectionService``:

.. sourcecode :: pycon

    >>> option = {'database': {'plugin': u'sqlite3', 'database': u':memory:', 'pool': u'true'}}

Configuration stages:

* Core DBUtils options first (eg  pool, plugin, maxshared)
* Plugin options handled next (eg creator, fetch_converter, execute_converter, database, port, username etc)


Service Extensions
------------------

* Converters
* Extra helpers

