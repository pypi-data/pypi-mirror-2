# Copyright (c) 2010, Robert Escriva
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
#     * Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of Stirimango nor the names of its contributors may be
#       used to endorse or promote products derived from this software without
#       specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


'''The complete stirimango codebase resides in this single package with no
submodules or subpackages.

More mature releases may support other RDBMS using subpackages.
'''


import datetime
import getopt
import getpass
import os
import pkg_resources
import psycopg2
import re
import StringIO
import sys

from pysettings.modules import get_module


DATABASE_GETOPT_SHORT = 'd:h:p:U:Ws:'
DATABASE_GETOPT_LONG = ['dbname=', 'host=', 'port=', 'username=', 'password',
        'schema=']


def connect_to_database(optlist):
    '''Use the options list (from getopt) to connect to the database.
    '''
    options = {}
    password = False
    options['user'] = os.environ.get('LOGNAME') or os.environ.get('USER')
    for flag, value in optlist:
        if flag in ('-d', '--dbname'):
            options['database'] = value
        elif flag in ('-h', '--host'):
            options['host'] = value
        elif flag in ('-p', '--port'):
            options['port'] = value
        elif flag in ('-U', '--username'):
            options['user'] = value
        elif flag in ('-W', '--password'):
            password = True
    if options['user'] is None:
        del options['user']
    if password:
        options['password'] = getpass.getpass()
    return psycopg2.connect(**options)


def pack_db_diff(package_manager, database_manager):
    '''Return a dictionary keyed to migration ids.

    The value is a 2-tuple indicating presence of the migration in the package
    or database.
    '''
    database = database_manager
    packages = package_manager
    migrations = {}
    for mid in packages.migration_list():
        migrations[mid] = (True, False)
    for mid, app in database.migrations():
        package_side = migrations.get(mid, (False, False))[0]
        migrations[mid] = (package_side, True)
    return migrations


class StirimangoException(Exception):
    '''All stirimango exceptions inherit from this class.

    .. doctest::

       >>> raise StirimangoException('sample error message')
       Traceback (most recent call last):
       StirimangoException: sample error message
    '''

    def __init__(self, msg):
        super(StirimangoException, self).__init__(msg)
        self.msg = msg


class Usage(StirimangoException):
    '''This exception indicates an error caused by the user's usage.
    '''


class Migration(object):
    '''A single changeset to the database describing up and down diff actions.

    A :class:`migration` is keyed to its creation time (rounded to the nearest
    second) and a concise description of the migration.  Examples:

     * 2010-07-04 11:32:02 create_products_table
     * 2010-07-04 11:34:33 products_add_id_column

    The creation time provides an implicit ordering for migrations that is used
    when determining the order in which to apply migrations to the database.
    The concise description should contain ASCII alphanumeric characters
    (``a-zA-Z0-9``) and the underscore (``_``).
    '''

    def __init__(self, mid, contents):
        self._mid = mid
        globs = {'__builtins__': []}
        locs = globs.copy()
        exec(contents, globs, locs)
        self._long_description = locs.get('DESCRIPTION', '')
        self._forward = locs.get('FORWARD', '')
        self._backward = locs.get('BACKWARD', '')

    def __repr__(self):
        '''The representation of a migration.
        '''
        return 'Migration(%s)' % self.mid

    @property
    def mid(self):
        '''The id of the migration.

        This is the migration's filename minus the ``.py`` extension.
        '''
        return self._mid

    @property
    def long_description(self):
        '''A long description of the migration

        This is a string (possibly multiple lines long) that describes the
        purpose of the migration.  This string should be descriptive as it will
        be shown to the systems administrators who will be running the
        migrations.
        '''
        return self._long_description

    @property
    def forward(self):
        '''The SQL necessary to migrate forward.
        '''
        return self._forward

    @property
    def backward(self):
        '''The SQL necessary to migrate backward.
        '''
        return self._backward

    @property
    def created(self):
        return datetime.datetime.strptime(self._mid[:19],
                PackageManager.DATE_FORMAT)

    @property
    def description(self):
        return self._mid[20:]


class DatabaseManager(object):
    '''Track the status of migrations in the database.

    Conceptually, a database, or schema within a database, is a space that
    `stirimango` manipulates.  This object tracks what has been done (within the
    context of `stirimango`) to the database.
    '''

    class AlreadyInitialized(StirimangoException):
        '''The database/schema is already initialized.'''

        def __init__(self):
            super(DatabaseManager.AlreadyInitialized, self).\
                    __init__(_(self.__doc__))

    class NotInitialized(StirimangoException):
        '''The database/schema is not initialized.'''

        def __init__(self):
            super(DatabaseManager.NotInitialized, self).\
                    __init__(_(self.__doc__))

    class UnknownSchema(StirimangoException):
        '''No such schema exists.'''

        def __init__(self):
            super(DatabaseManager.UnknownSchema, self).\
                    __init__(_(self.__doc__))

    def __init__(self, connection):
        self.conn = connection
        self.cur = self.conn.cursor()
        self.cur.execute('BEGIN;')
        self._schema = 'public'

    def schema(self, schema):
        '''Change the cursor to use the provided schema name.

        .. warn::

           This is *not* run as a parameterized query.  The schema name provided
           must be a valid schema name and must be from a trusted source (i.e.,
           don't allow untrusted users to control the schema name).
        '''
        self.cur.execute('''
            SELECT nspname
            FROM pg_namespace
            WHERE nspname = %s;''', (schema,))
        rows = self.cur.fetchall()
        if len(rows) == 0:
            raise DatabaseManager.UnknownSchema()
        self.cur.execute('SET search_path TO "%s";' % schema)
        self._schema = schema

    def is_initialized(self):
        '''A boolean indicating whether the database is initialized.
        '''
        self.cur.execute('''
            SELECT tablename
            FROM pg_tables
            WHERE tablename = 'stirimango'
                AND schemaname = %s;''', (self._schema,))
        rows = self.cur.fetchall()
        return len(rows) > 0

    def init(self):
        '''Create the schema table in the database.

        This will raise a :exc:`DatabaseManager.AlreadyInitialized` in the event
        that the database has already been initialized.
        '''
        if self.is_initialized():
            raise DatabaseManager.AlreadyInitialized()
        sql = '''
            CREATE TABLE stirimango
            (
                created TIMESTAMP WITHOUT TIME ZONE NOT NULL,
                description VARCHAR(64) NOT NULL,
                applied TIMESTAMP WITHOUT TIME ZONE NOT NULL,
                PRIMARY KEY (created, description)
            );
            '''
        self.cur.execute(sql)

    def commit(self):
        '''Commit the current transaction to the database.

        It will also start a new transaction for further actions.
        '''
        self.cur.execute('COMMIT;')
        self.cur.execute('BEGIN;')

    def close(self):
        '''Close the database cursor and connection.
        '''
        self.cur.close()
        self.conn.close()

    def migrations(self):
        '''Return a list of (mid, application_time) tuples.
        '''
        if not self.is_initialized():
            raise DatabaseManager.AlreadyInitialized()
        sql = '''
            SELECT created, description, applied
            FROM stirimango;
            '''
        self.cur.execute(sql)
        def make_mid(created, desc):
            format = PackageManager.DATE_FORMAT
            return '%s_%s' % (created.strftime(format), desc)
        return [(make_mid(created, description), applied)
                for created, description, applied in self.cur.fetchall()]

    def forward(self, migration):
        self.cur.execute(migration.forward)
        self.cur.execute('''
            INSERT INTO stirimango (created, description, applied)
            VALUES (%s, %s, %s); ''',
            (migration.created, migration.description, datetime.datetime.now()))

    def backward(self, migration):
        self.cur.execute(migration.backward)
        self.cur.execute('''
            DELETE FROM stirimango WHERE created=%s AND description=%s;''',
            (migration.created, migration.description))


class PackageManager(object):
    '''Track which migrations are available in a package.

    The set of migrations is a set of ``.py`` files within a Python package
    whose files follow a particular convention.  The Python files within the
    package have a filename matching the regular expression
    ``^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}_\w+.py$``.  Conceptually, this is
    the `datetime format string
    <http://docs.python.org/library/datetime.html#strftime-and-strptime-behavior>`_
    ``%Y-%m-%dT%H:%M:%S`` joined to a string of alphanumerics and underscores
    by a single underscore.
    '''

    DATE_FORMAT = '%Y-%m-%dT%H:%M:%S'
    MIGRATION_RE = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}_\w+.py$'

    class InvalidPackage(StirimangoException):
        '''The package specified is not a stirimango migrations package.'''

        def __init__(self):
            super(PackageManager.InvalidPackage, self).\
                    __init__(_(self.__doc__))

    def __init__(self, package):
        self.package_name = package
        self.package = get_module(package)
        self.provider = pkg_resources.get_provider(package)
        self.manager = pkg_resources.ResourceManager()
        self.config_values = {}
        for item in dir(self.package):
            if item.startswith('STIRIMANGO_'):
                self.config_values[item[11:]] = getattr(self.package, item)
        if self.config_values == {} and len(self.migration_list()) == 0:
            raise PackageManager.InvalidPackage()

    def migration_list(self):
        '''Return a list of migration ids in sorted order.

        .. doctest::

           >>> m = PackageManager('testdata.sample')
           >>> pprint(m.migration_list())
           ['2010-07-04T00:00:00_create_products_table',
            '2010-07-05T00:05:00_products_add_description_column',
            '2010-07-05T00:05:50_no_description',
            '2010-07-06T00:00:00_products_remove_description_column']
        '''
        ret = []
        for filename in self.provider.resource_listdir('.'):
            if re.match(PackageManager.MIGRATION_RE, filename):
                ret.append(filename[:-3])
        return ret

    def migrations(self):
        ret = []
        for migration in self.migration_list():
            get_resource_string = self.provider.get_resource_string
            contents = get_resource_string(self.manager, migration + '.py')
            ret.append(Migration(migration, contents))
        return ret


def main_init(argv, stdout=None, stderr=None):
    '''The main function for :func:`action_init`.

    :func:`main_init` parses argv and calls :func:`action_init`.
    '''
    try:
        optlist, args = getopt.getopt(argv, DATABASE_GETOPT_SHORT,
                DATABASE_GETOPT_LONG)
        if len(args) != 0:
            raise Usage(_('Extraneous arguments provided.'))
        connection = connect_to_database(optlist)
        schema = None
        for flag, value in optlist:
            if flag in ('-s', '--schema'):
                schema = value
        action_init(connection, schema, stdout, stderr)
        return 0
    except ( DatabaseManager.AlreadyInitialized
           , DatabaseManager.UnknownSchema
           , Usage
           ), ex:
        print >> stderr, ex.msg
        return 2


def action_init(connection, schema=None, stdout=None, stderr=None):
    '''Initialize the database/schema to have the required tables.
    '''
    stdout = stdout or sys.stdout
    stderr = stderr or sys.stderr
    schema = schema or 'public'
    manager = DatabaseManager(connection)
    if schema:
        manager.schema(schema)
    manager.init()
    manager.commit()
    manager.close()


def main_list(argv, stdout=None, stderr=None):
    '''The main function for :func:`action_list`.

    :func:`main_list` parses argv and calls :func:`action_list`.

    In the typical case, the argument will simply be passed through to
    :func:`action_list`.

    .. doctest::

       >>> ret = main_list(['testdata.sample'])
       2010-07-04T00:00:00_create_products_table
       <BLANKLINE>
           Create a table to hold products for sale.
       <BLANKLINE>
       2010-07-05T00:05:00_products_add_description_column
       <BLANKLINE>
           Add a column for describing the products to customers.
       <BLANKLINE>
       2010-07-05T00:05:50_no_description
       <BLANKLINE>
       2010-07-06T00:00:00_products_remove_description_column
       <BLANKLINE>
           Remove the `description` column in the `products` table.
       <BLANKLINE>
           The product descriptions will be stored somewhere else.
        >>> ret
        0

    If the user provides improper arguments, then the return value will be
    non-zero and an error message will be reported.

    .. doctest::

       >>> ret = main_list([])
       Provide the name of a single migrations package.
       >>> ret
       2
       >>> ret = main_list(['testdata.nonpackage'])
       The package specified is not a stirimango migrations package.
       >>> ret
       2
    '''
    try:
        if len(argv) != 1:
            raise Usage(_('Provide the name of a single migrations package.'))
        action_list(argv[0], stdout, stderr)
        return 0
    except (PackageManager.InvalidPackage, Usage), ex:
        print >> stderr, ex.msg
        return 2

def action_list(package_name, stdout=None, stderr=None):
    '''List migrations available in a package.

    Argv should be a list containing a single string which is the package name.

    In the typical case, migrations will be listed in chronological order:

    .. doctest::

       >>> action_list('testdata.sample')
       2010-07-04T00:00:00_create_products_table
       <BLANKLINE>
           Create a table to hold products for sale.
       <BLANKLINE>
       2010-07-05T00:05:00_products_add_description_column
       <BLANKLINE>
           Add a column for describing the products to customers.
       <BLANKLINE>
       2010-07-05T00:05:50_no_description
       <BLANKLINE>
       2010-07-06T00:00:00_products_remove_description_column
       <BLANKLINE>
           Remove the `description` column in the `products` table.
       <BLANKLINE>
           The product descriptions will be stored somewhere else.

    If there are constants defined in the package that provide information to
    stirimango, but the package contains no migrations, stirimango will
    acknowledge this as well:

    .. doctest::

       >>> action_list('testdata.emptypackage')
       The package specified has no migrations.

    When the package contains no indication that it was created for stirimango,
    the list function will indicate such with a :exc:`Usage` exception:

    .. doctest::

       >>> action_list('testdata.nonpackage')
       Traceback (most recent call last):
       InvalidPackage: The package specified is not a stirimango migrations package.

    An :exc:`ImportError` is generated when the package does not exist:

    .. doctest::

       >>> action_list('testdata.noexist')
       Traceback (most recent call last):
       ImportError: No module named noexist
    '''
    stdout = stdout or sys.stdout
    stderr = stderr or sys.stderr
    manager = PackageManager(package_name)
    migrations = manager.migrations()
    migration_strings = []
    for migration in migrations:
        sio = StringIO.StringIO()
        print >> sio, migration.mid,
        long_desc = migration.long_description.split(os.linesep)
        while len(long_desc) and long_desc[0] == '':
            long_desc = long_desc[1:]
        while len(long_desc) and long_desc[-1] == '':
            long_desc.pop()
        if long_desc != []:
            print >> sio
            for line in long_desc:
                print >> sio
                print >> sio, '    %s' % line,
        migration_strings.append(sio.getvalue())
    if migration_strings:
        print >> stdout, '\n\n'.join(migration_strings)
    else:
        print >> stdout, _('The package specified has no migrations.')


def main_status(argv, stdout=None, stderr=None):
    '''The main function for :func:`action_status`.

    :func:`main_status` parses argv and calls :func:`action_status`.
    '''
    try:
        optlist, args = getopt.getopt(argv, DATABASE_GETOPT_SHORT,
                DATABASE_GETOPT_LONG)
        if len(args) != 1:
            raise Usage(_('Provide the name of a single migrations package.'))
        connection = connect_to_database(optlist)
        schema = None
        for flag, value in optlist:
            if flag in ('-s', '--schema'):
                schema = value
        action_status(args[0], connection, schema, stdout, stderr)
        return 0
    except ( DatabaseManager.UnknownSchema
           , Usage
           ), ex:
        print >> stderr, ex.msg
        return 2


def action_status(package_name, connection, schema=None, stdout=None,
        stderr=None):
    '''Display the status of the database.
    '''
    stdout = stdout or sys.stdout
    stderr = stderr or sys.stderr
    schema = schema or 'public'
    packman = PackageManager(package_name)
    dbman = DatabaseManager(connection)
    if schema:
        dbman.schema(schema)
    if not dbman.is_initialized():
        raise Usage(_('The database is not initialized.'))
    print ' %s' % _('Migrations Package')
    print ' | %s' % _(' Database')
    print ' V  V'
    mapping = {True: u'\u2713', False: ' '}
    for mid, (pack, db) in sorted(pack_db_diff(packman, dbman).items()):
        print '[%s][%s]' % (mapping[pack], mapping[db]), mid
    dbman.close()


def main_forward(argv, stdout=None, stderr=None):
    '''The main function for :func:`action_forward`.

    :func:`main_forward` parses argv and calls :func:`action_forward`.
    '''
    try:
        optlist, args = getopt.getopt(argv, DATABASE_GETOPT_SHORT + 'n:u:',
                DATABASE_GETOPT_LONG + ['number=', 'one='])
        if len(args) != 1:
            raise Usage(_('Provide the name of a single migrations package.'))
        connection = connect_to_database(optlist)
        schema = None
        number = None
        until = None
        for flag, value in optlist:
            if flag in ('-s', '--schema'):
                schema = value
            elif flag in ('-n', '--number'):
                try:
                    number = int(value)
                except ValueError, ex:
                    raise Usage(_('%s needs an integer') % flag)
            elif flag in ('-u', '--until'):
                until = value
        action_forward(args[0], connection, number, until, schema, stdout,
                stderr)
        return 0
    except ( DatabaseManager.UnknownSchema
           , Usage
           ), ex:
        print >> stderr, ex.msg
        return 2


def action_forward(package_name, connection, number=None, until=None,
        schema=None, stdout=None, stderr=None):
    '''Move the migrations forward.
    '''
    stdout = stdout or sys.stdout
    stderr = stderr or sys.stderr
    schema = schema or 'public'
    if number is not None and until is not None:
        raise Usage(_('Specify either --number or --until, but not both.'))
    packman = PackageManager(package_name)
    dbman = DatabaseManager(connection)
    if schema:
        dbman.schema(schema)
    if not dbman.is_initialized():
        raise Usage(_('The database is not initialized.'))
    diff = pack_db_diff(packman, dbman)
    unapplied_migrations = sorted([mid for mid, (pack, db) in diff.items()
                                       if not db])
    if number is not None:
        unapplied_migrations = unapplied_migrations[:number]
    elif until is not None:
        if until not in unapplied_migrations:
            raise Usage(_('--until must specify an unapplied migration.'))
        offset = unapplied_migrations.index(until)
        unapplied_migrations = unapplied_migrations[:offset + 1]
    migrations = dict([(m.mid, m) for m in packman.migrations()])
    for mid in unapplied_migrations:
        try:
            dbman.forward(migrations[mid])
        except psycopg2.DatabaseError, ex:
            message = str(ex)
            while message.endswith('\n'):
                message = message[:-1]
            dbman.close()
            raise Usage(message)
    if not len(unapplied_migrations):
        print >> stderr, _('All migrations were already applied.')
    dbman.commit()
    dbman.close()


def main_backward(argv, stdout=None, stderr=None):
    '''The main function for :func:`action_backward`.

    :func:`main_backward` parses argv and calls :func:`action_backward`.
    '''
    try:
        optlist, args = getopt.getopt(argv, DATABASE_GETOPT_SHORT + 'n:u:',
                DATABASE_GETOPT_LONG + ['number=', 'one='])
        if len(args) != 1:
            raise Usage(_('Provide the name of a single migrations package.'))
        connection = connect_to_database(optlist)
        schema = None
        number = None
        until = None
        for flag, value in optlist:
            if flag in ('-s', '--schema'):
                schema = value
            elif flag in ('-n', '--number'):
                try:
                    number = int(value)
                except ValueError, ex:
                    raise Usage(_('%s needs an integer') % flag)
            elif flag in ('-u', '--until'):
                until = value
        action_backward(args[0], connection, number, until, schema, stdout,
                stderr)
        return 0
    except ( DatabaseManager.UnknownSchema
           , Usage
           ), ex:
        print >> stderr, ex.msg
        return 2


def action_backward(package_name, connection, number=None, until=None,
        schema=None, stdout=None, stderr=None):
    '''Move the migrations backward.
    '''
    stdout = stdout or sys.stdout
    stderr = stderr or sys.stderr
    schema = schema or 'public'
    if number is not None and until is not None:
        raise Usage(_('Specify either --number or --until, but not both.'))
    packman = PackageManager(package_name)
    dbman = DatabaseManager(connection)
    if schema:
        dbman.schema(schema)
    if not dbman.is_initialized():
        raise Usage(_('The database is not initialized.'))
    diff = pack_db_diff(packman, dbman)
    applied_migrations = sorted([mid for mid, (pack, db) in diff.items()
                                     if db], reverse=True)
    if number is not None:
        applied_migrations = applied_migrations[:number]
    elif until is not None:
        if until not in applied_migrations:
            raise Usage(_('--until must specify an applied migration.'))
        offset = applied_migrations.index(until)
        applied_migrations = applied_migrations[:offset + 1]
    migrations = dict([(m.mid, m) for m in packman.migrations()])
    if set(applied_migrations) - set(migrations.keys()) != set([]):
        err = _('There are migrations in the db that are not in the package')
        raise Usage(err)
    for mid in applied_migrations:
        try:
            dbman.backward(migrations[mid])
        except psycopg2.DatabaseError, ex:
            message = str(ex)
            while message.endswith('\n'):
                message = message[:-1]
            dbman.close()
            raise Usage(message)
    if not len(applied_migrations):
        print >> stderr, _('No migrations were available to rollback.')
    dbman.commit()
    dbman.close()
