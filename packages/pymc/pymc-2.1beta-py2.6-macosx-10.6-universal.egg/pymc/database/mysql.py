"""
MySQL database backend

Store traces from tallyable objects in individual SQL tables.

Implementation Notes
--------------------
For each object, a table is created with the following format:

key (INT), trace (INT),  v1 (FLOAT), v2 (FLOAT), v3 (FLOAT) ...

The key is autoincremented each time a new row is added to the table.
trace denotes the chain index, and starts at 0.

Additional Dependencies
-----------------------
 * MySQL <http://www.mysql.com/downloads/>
 * mysql-python <http://sourceforge.net/projects/mysql-python>

Created by Chris Fonnesbeck on 2007-02-01.
Updated by CF 2008-07-13.
DB API changes, October 2008, DH.
"""

# TODO: Commit multiple tallies with single database call.
# TODO: Add support for integer valued objects.

from numpy import zeros, shape, squeeze, transpose
import base, pickle, ram, pymc, sqlite
import pdb
# Try importing pymysql
dbmod = None
try:
    import pymysql
    dbmod = pymysql
except ImportError:
    pass

if dbmod is None:
    try:
        import MySQLdb
        dbmod = MySQLdb
    except ImportError:
        pass


__all__ = ['Trace', 'Database', 'load']

class Trace(sqlite.Trace):
    """MySQL Trace class."""

    def _initialize(self, chain, length):
        """Initialize the trace. Create a table.
        """
        if self._getfunc is None:
            self._getfunc = self.db.model._funs_to_tally[self.name]


        # Determine size
        try:
            self._shape = shape(self._getfunc())
        except TypeError:
            self._shape = None

        self._vstr = ', '.join(sqlite.var_str(self._shape))

        # If the table already exists, exit now.
        if chain != 0:
            return

        # Create the variable name strings.
        vstr = ', '.join(v + ' FLOAT' for v in sqlite.var_str(self._shape))

        query = "create table %s (recid INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT, trace  int(5), %s )" % (self.name, vstr)

        self.db.cur.execute(query)



class Database(sqlite.Database):
    """MySQL database."""

    def __init__(self, dbname, dbuser='', dbpass='', dbhost='localhost', dbport=3306, dbmode='a'):
        """Open or create a MySQL database.

        :Parameters:
        dbname : string
          The name of the database file.
        dbuser : string
          The database user name.
        dbpass : string
          The database user password.
        dbhost : string
          The location of the database host.
        dbport : int
          The port number to use to reach the database host.
        dbmode : {'a', 'w'}
          File mode.  Use `a` to append values, and `w` to overwrite
          an existing database.
        """
        self.__name__ = 'mysql'
        self.dbname = dbname
        self.__Trace__ = Trace

        self.trace_names = []   # A list of sequences of names of the objects to tally.
        self._traces = {} # A dictionary of the Trace objects.
        self.chains = 0

        self._user = dbuser
        self._passwd = dbpass
        self._host = dbhost
        self._port = dbport
        self.mode = dbmode

        # Connect to database
        self.DB = dbmod.connect(user=self._user, passwd=self._passwd, host=self._host, port=self._port)
        self.cur = self.DB.cursor()

        # Try and create database with model name
        try:
            self.cur.execute('CREATE DATABASE %s' % self.dbname)
        except Exception:
            # If already exists, switch to database
            self.cur.execute('USE %s' % self.dbname)

            # If in write mode, remove existing tables.
            if self.mode == 'w':
                self.clean()


    def clean(self):
        """Deletes tables from database"""
        tables = get_table_list(self.cur)

        for t in tables:
            self.cur.execute('DROP TABLE %s' % t)

    def savestate(self, state):
        """Store a dictionnary containing the state of the Sampler and its
        StepMethods."""
        pass

    def getstate(self):
        """Return a dictionary containing the state of the Sampler and its
        StepMethods."""
        return {}


def load(dbname='', dbuser='', dbpass='', dbhost='localhost', dbport=3306):
    """Load an existing MySQL database.

    Return a Database instance.
    """
    db = Database(dbname=dbname, dbuser=dbuser, dbpass=dbpass, dbhost=dbhost, dbport=dbport, dbmode='a')
    db.DB = dbmod.connect(db=dbname, user=dbuser, passwd=dbpass, host=dbhost, port=dbport)
    db.cur = db.DB.cursor()

    # Get the name of the objects
    tables = get_table_list(db.cur)

    # Create a Trace instance for each object
    chains = 0
    for name in tables:
        db._traces[name] = Trace(name=name, db=db)
        setattr(db, name, db._traces[name])
        db.cur.execute('SELECT MAX(trace) FROM %s'%name)
        chains = max(chains, db.cur.fetchall()[0][0]+1)

    db.chains=chains
    db.trace_names = chains * [tables,]
    db._state_ = {}
    return db

# Copied form Django.
def get_table_list(cursor):
    """Returns a list of table names in the current database."""
    # Skip the sqlite_sequence system table used for autoincrement key
    # generation.
    cursor.execute("SHOW TABLES")
    return [row[0] for row in cursor.fetchall()]
