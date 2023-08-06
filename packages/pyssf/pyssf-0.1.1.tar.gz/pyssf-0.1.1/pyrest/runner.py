# 
# Copyright (C) 2010 Platform Computing
# 
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
# 
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
# 
'''
This module actually configures and runs the service.

Created on Aug 10, 2010

@author: tmetsch
'''
from pyrest import service, myexceptions
from pyrest.service import ResourceHandler, SecurityHandler
from web.wsgiserver import CherryPyWSGIServer
import web

# 
# Configures web.py and tells him which handlers should listen to which 
# entry-point.
# 
urls = ('/(.*)', 'ResourceHandler')

# 
# Turns debugging on of off - Default is False (off).
# 
web.config.debug = False

# 
# When using the build-in webserver of the web.py framework there is no need to
# change the following line. If the service is deployed in Apache using the
# mod_wsgi use the second line. Do not change the name of the attribute. Apache
# mod_wsgi will assume it is named application (lowercase).
# 
application = web.application(urls, globals())
#application = web.application(urls, globals()).wsgifunc()

# 
# When using the build-in webserver with SSL enabled uncomment the following
# lines
# 
CherryPyWSGIServer.ssl_certificate = "/home/tmetsch/scrap/CA/server/newcert.pem"
CherryPyWSGIServer.ssl_private_key = "/home/tmetsch/scrap/CA/server/newkey.pem"

class SimpleSecurityHandler(SecurityHandler):

    def authenticate(self, username, password):
        if username == 'foo' and password == 'bar':
            print username, password
        else:
            raise myexceptions.SecurityException()

service.AUTHENTICATION_ENABLED = True
service.SECURITY_HANDLER = SimpleSecurityHandler()

if __name__ == "__main__":
    application.run()
