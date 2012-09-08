#!/usr/bin/env python
'''
Required python libraries:
    - Google gdata: http://code.google.com/apis/gdata/
    - Storm ORM: https://storm.canonical.com/FrontPage
'''

from storm.locals import *
import gdata.apps.service

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

# Pull domain, username, & password from database
domains = store.find(AccessAccounts,AccessAccounts.id > 0)

for g in domains:
    print "Setting password change field for the %s domain." % (g.domain)
    service = gdata.apps.service.AppsService(email=g.email, domain=g.domain, password=g.password)
    service.ProgrammaticLogin()
    userlist = service.RetrieveAllUsers()
    
    for i in userlist.entry:
        no_update = ('administrator', 'warrior', 'cacha1')
        if not i.login.user_name in no_update:
            try: 
                userobj = service.RetrieveUser(i.login.user_name)
                userobj.login.change_password='true'
                service.UpdateUser(i.login.user_name, userobj)
                print i.login.user_name + " must change password at next login."
            except gdata.apps.service.AppsService, e:
                print e
    
    print "Done running Password reset script."
    
    
'''
How to connect to STORM ORM and Get/Set records.

>>> from storm.locals import *
>>> class AccessAccounts(object):
...     #access_accounts table mapping object
...     __storm_table__ = "access_accounts"
...     id = Int(primary=True)
...     domain = Unicode()
...     email = Unicode()
...     password = Unicode()
... 
>>> database = create_database("sqlite:/Users/scott/gtools/google_sync.db")
>>> store = Store(database)
>>> t = AccessAccounts()
>>> t.domain = u'oetahiti.com'
>>> t.email = u'administrator@oetahiti.com'
>>> t.password = u'********'
>>> store.add(t)
<__main__.AccessAccounts object at 0x100769ed0>
>>> p = store.find(AccessAccounts, AccessAccounts.email == u'administrator@oetahiti.com').one()
>>> print "%r, %r" % (p.id, p.email)
1, u'administrator@oetahiti.com'
>>> store.get(AccessAccounts,1).email
u'administrator@oetahiti.com'
>>> store.get(AccessAccounts,1).password
u'bac6eg5F'
>>> store.flush
<bound method Store.flush of <storm.store.Store object at 0x100652350>>
>>> store.flush()
>>> store.commit()

-------------------------------------

How to set an account to change their password at next login?
>>> import atom
>>> import gdata.auth
>>> import gdata.contacts
>>> import gdata.contacts.service
>>> import gdata.data
>>> import gdata.contacts.data
>>> import gdata.contacts.client
>>> 
>>> import gdata.apps.service
>>> import gdata.apps.groups.service
>>> 
>>> domain = "oetahiti.com"
>>> email = "administrator@oetahiti.com"
>>> password = "********"
>>> service = gdata.apps.service.AppsService(email=email, domain=domain, password=password)
>>> service.ProgrammaticLogin()
>>> 
>>> a= service.RetrieveUser('test2')
>>> a.login.user_name
'test2'
>>> a.login.change_password
'false'
>>> a.login.change_password='true'
>>> service.UpdateUser('test2', a)
<gdata.apps.UserEntry object at 0x6d8fd0>
>>> 

'''