#Used to make the database connection
from storm.locals import *

class DBError(Exception):
    '''Base Error class'''
    def __init__(self,message):
        self.message = message

    def __str__(self):
        return repr(self.message)

class DBConnectionError(DBError):
    pass

# STORM ORM database schema
class AccessAccounts(object):
    ''' access_accounts table mapping object '''
    __storm_table__ = "access_accounts"
    id = Int(primary=True)
    domain = Unicode()
    email = Unicode()
    password = Unicode()

    def __init__(self, email = None, password = None):
        self.domain = Unicode(email.split('@')[1])
        self.email = Unicode(email)
        self.password = Unicode(password)

#Database connection parameters
sql_schema='sqlite'
sql_username='scott'
sql_pwd=''
sql_host='localhost'
sql_port=''
sql_db_name='/Users/scott/gtools/google_sync.db'

try:
    #database = create_database("sqlite:/Users/scott/gtools/google_sync.db")
    database = create_database("%s:%s" % (sql_schema,sql_db_name))
    store = Store(database)
except Exception, err:
    raise  DBConnectionError("Could not connect to %s with user %s. Traceback: (%s, %s)" %
                                (sql_schema.upper(), sql_db_name, err.__class__, err))