import gdata.apps.adminsettings.service
import database_connection


'''
>>> domain = "oetahiti.com"
>>> email = "administrator@oetahiti.com"
>>> password = "********"
>>> import gdata.apps.adminsettings.service
>>> c = gdata.apps.adminsettings.service.AdminSettingsService()
>>> c = gdata.apps.adminsettings.service.AdminSettingsService(email=email, domain=domain, password=password)
>>> service.ProgrammaticLogin()
>>> c.GetAdminSecondaryEmail()
'goleksiak@oeh.com'

'''