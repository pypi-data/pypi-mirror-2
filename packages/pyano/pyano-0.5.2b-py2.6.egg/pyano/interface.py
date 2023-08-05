###############################################################################
# This file is part of Pyano.                                                 #
#                                                                             #
# Pyano is a web interface for the mixmaster remailer, written for mod_python #
# Copyright (C) 2010  Sean Whitbeck <sean@neush.net>                          #
#                                                                             #
# Pyano is free software: you can redistribute it and/or modify               #
# it under the terms of the GNU General Public License as published by        #
# the Free Software Foundation, either version 3 of the License, or           #
# (at your option) any later version.                                         #
#                                                                             #
# Pyano is distributed in the hope that it will be useful,                    #
# but WITHOUT ANY WARRANTY; without even the implied warranty of              #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the               #
# GNU General Public License for more details.                                #
#                                                                             #
# You should have received a copy of the GNU General Public License           #
# along with this program.  If not, see <http://www.gnu.org/licenses/>.       #
###############################################################################

from mod_python import util
from mod_python import apache
from pyano import *

class Interface:
    
    def __call__(self,req):
        parse_config( req.get_options()['config_file'] )

        req.content_type = 'text/html'
        req.send_http_header()
        self.fs = util.FieldStorage(req,keep_blank_values=True)

        try:
            self.stats = get_stats()
            try:
                req.write( self.header() )
            except:
                req.write( html_header (self.title) )
        
            if len(self.fs) == 0: # before user submission
                req.write(html_preamble())
                self.form(req)
                req.write(html_help(self.help))

            else: # process user submission
                check_ip(req.get_remote_host(apache.REMOTE_NOLOOKUP))  # make sure user is not spamming
                msg = self.process()
                # if we get this far: Succes!
                req.write(html_success(msg))
                req.write(html_back())

        except InputError as ie: # Invalid user input
            req.write(html_error(str(ie)))
            req.write(html_back())
        
        except SecurityError as he: # User has been permanently or temporarily banned
            req.write(html_error(str(he)))
            req.write(html_back())
        
        except MixError as me: # Error interacting with mixmaster process
            req.write(html_error(str(me)))
            req.write(html_back())

        except ConfigError as ce: # Error parsing configuration
            req.write(html_error(str(ce)))
            req.write(html_back())

        except Exception as ex: # Catch all remaining errors
            req.write('<h2>Unhandled Error!</h2>')
            req.write('<p>'+str(ex)+'</p>')
            req.write(html_back())

        try:
            req.write( html_from_file(conf.footer) )
        except:
            req.write( html_copyright() )

        req.write('\n\n</body>\n\n</html>\n')

        return apache.OK

