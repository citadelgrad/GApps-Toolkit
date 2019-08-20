import gdata.apps.adminsettings.service
import database_connection


'''
>>> domain = "domain.com"
>>> email = "administrator@domain.com"
>>> password = "********"
>>> import gdata.apps.adminsettings.service
>>> c = gdata.apps.adminsettings.service.AdminSettingsService()
>>> c = gdata.apps.adminsettings.service.AdminSettingsService(email=email, domain=domain, password=password)
>>> service.ProgrammaticLogin()
>>> c.GetAdminSecondaryEmail()
'example@domain.com'

'''
