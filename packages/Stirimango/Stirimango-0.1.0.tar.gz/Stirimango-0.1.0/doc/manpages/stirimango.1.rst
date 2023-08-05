============
 stirimango
============

------------------------------
database migrations for Python
------------------------------

:Author: Robert Escriva <me@robescriva.com>
:Date:   2010-07-05
:Copyright: 3-clause BSD
:Version: 0.1.0
:Manual section: 1
:Manual group: Stirimango Manual

SYNOPSIS
========

::

    stirimango init [<connection options>]

    stirimango backward [<connection options>] [--one]
                        [--until <migration>] <package>

    stirimango forward [<connection options>] [--one]
                       [--until <migration>] <package>

    stirimango status [<connection options>] <package>

    stirimango list <package>

DESCRIPTION
===========

.. include:: ../../README.rst

ACTIONS
=======

init
    Setup the database for use with Stirimango.  If the migration package is
    schema-safe, then the schema option may be used.

    This action must be performed before backward/forward migration.

backward
    Undo previous migrations.  Typically this action will remove columns/tables
    that were added by migrations.

    The action will be performed within a transaction, and so it will be
    all-or-nothing with respect to successful rollback of the migrations.

forward
    Apply migrations.  This action will typically (but not always) create
    columns/tables.

    The action will be performed within a transaction, and so it will be
    all-or-nothing with respect to successful application of the migrations.

status
    Check the status of the migrations.  This will display a complete list of
    migrations and indicate whether or not they have been applied to the
    database.

list
    List the migration ids for the migrations in a package, and a short
    description of each.

OPTIONS
=======

Common Postgresql connection options (correspond to options in the *psql(1)*
manpage):

-d <dbname>

--dbname <dbname>
    The Postgresql database name.

-h <hostname>

--host <hostname>
    The Postgresql host name.

-p <port>

--port <port>
    The Postgresql port/domain socket.

-U <username>

--username <username>
    The Postgresql username.  This defaults to the value of the `LOGNAME`
    environment variable and falls back to the `USER` environment variable.

-W

--password
    Prompt for the Postgresql database password.

-s <schemaname>

--schema <schemaname>
    The schema in which to perform the migrations.  It is good practice to write
    migrations that operate in the default schema.  This parameter changes the
    default schema (thus allowing the same package of migrations to be used for
    multiple schemas).

    This does not have a corresponding flag in *psql(1)*.

    .. note::

       This is *not* run as a parameterized query.  The schema name provided
       must be a valid schema name and must be from a trusted source (i.e.,
       don't allow untrusted users to control the schema name).

Stirimango options:

-n <number>

--number <number>
    The number of migrations to move forward or backward.  When moving forward,
    stirimango will apply up to this number of migrations in the order of their
    timestamps.  When moving backward, stirimango will remove up to this number
    of migrations in reverse order of their application.

-u <migration_id>

--until <migration_id>
    Migrate forward (respectively, backward) until the specified migration is
    applied to (respectively, removed from) the database.

PROBLEMS
========

This is designed for Postgresql.  If you don't use Postgresql, you will have
problems.

BUGS
====

There will be bugs.  Don't let that stop you from enjoying the milkshake.
