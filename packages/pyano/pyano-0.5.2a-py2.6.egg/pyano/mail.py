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

from pyano import *

class MailInterface(Interface):
    
    title = 'Pyano Anonymous Email Web Interface'
    help = 'To use this, enter the address you wish to send e-mail, the from line you wish to have on the message (it is important that you read the part about from lines below), and the subject.'

    def validate(self):
        to = str(self.fs['to'])
        val_email(to)
        orig = str(self.fs['from'])
        if orig:
            val_email(orig)
        subj = str(self.fs['subject'])
        chain = parse_chain(self.fs,self.stats)
        n_copies = int(self.fs['copies'])
        val_n_copies(n_copies)
        msg = str(self.fs['message'])
        if not msg:
            raise InputError('Refusing to send empty message.')
        return to, orig, subj, chain, n_copies, msg


    def header(self):
        return html_from_file(conf.mail_header)
    

    def form(self,req):
        req.write('''
<h2>Web Interface</h2>

<form action="'''+str(req.uri)+'''" method="post" >
<table id="mixtable">
  <tr>
    <td><strong>*To:</strong></td>
    <td><input class="line" name="to" value="" /></td>
  </tr>
  <tr>
    <td><strong>From:</strong></td>
    <td><input class="line" name="from" value="" /></td>
  </tr>
  <tr>
    <td><strong>Subject:</strong></td>
    <td><input class="line" name="subject" value="" /></td>
  </tr>
  <tr>''')
        if self.stats:
            req.write('''   <td><strong>Chain:</strong></td>
    <td>
'''+html_chain(self.stats)+'''
    </td>
  </tr>''')
        req.write('''  <tr>
   <td><strong>Copies:</strong></td>
    <td>
'''+html_copies()+'''
    </td>
  </tr>

  <tr>
    <td><strong>*Message:</strong></td>
    <td><textarea name="message" rows="30" cols="70" ></textarea></td>
  </tr>
  <tr>
    <td></td>
    <td><input type="submit" value="Send" /><input type="reset" value="Reset" /></td>
  </tr>
</table>
</form>

''')
        
    def process(self):
        to, orig, subj, chain, n_copies, msg = self.validate() # check user input
        send_mail(to,orig,subj,chain,n_copies,msg) # try sending to mixmaster
        msg = 'Successfully sent message to '+to+' using '
        if chain:
            msg += 'remailer chain '+','.join(chain)+'.'
        else:
            msg += 'a random remailer chain.'
        return msg

    

def handler(req):
    return MailInterface()(req)

