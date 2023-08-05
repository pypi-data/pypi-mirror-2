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

from mod_python import apache
from mod_python import util
from pyano import *


class NewsInterface(Interface):

    title = 'Pyano Anonymous Usenet Interface'
    help = 'To use this, enter the newsgroups you wish to post to (comma separated), the from line you wish to have on the message (it is important that you read the part about from lines below), enter the subject of the message, enter the references line if replying to a post and you want it to thread (input the message ID of the post you are responding to, including the brackets &lt;&gt;, eg. &lt;asasfasf22228888765444@somewhere.com&gt;), and select if you want google to archive it or not.'

    def validate(self):
        groups = str(self.fs['newsgroups']).replace(' ','') # filter out whitespaces
        val_newsgroups(groups)
        orig = str(self.fs['from'])
        if orig:
            val_email(orig)
        refs = str(self.fs['references'])
        if refs:
            val_references(refs)
        mail2news = str(self.fs['mail2news']).replace(' ','')
        if mail2news:
            val_mail2news(mail2news)
        hashcash = str(self.fs['hashcash']).strip()
        if hashcash:
            val_hashcash(hashcash)
        try:
            checked = str(self.fs['archive'])
            no_archive = True
        except KeyError:
            no_archive = False
        subj = str(self.fs['subject'])
        if not subj:
            raise InputError('Subject required.')
        chain = parse_chain(self.fs,self.stats)
        n_copies = int(self.fs['copies'])
        val_n_copies(n_copies)
        msg = str(self.fs['message'])
        if not msg:
            raise InputError('Refusing to send empty message.')
        return groups, orig, subj, refs, mail2news, hashcash, no_archive, chain, n_copies, msg


    def header(self):
        return html_from_file(conf.news_header)


    def form(self,req):
        req.write('''
<h2>Web Interface</h2>

<form action="'''+str(req.uri)+'''" method="post" >
<table id="mixtable">
  <tr>
    <td><strong>*Newsgroup(s):</strong></td>
    <td><input class="line" name="newsgroups" value="" /></td>
  </tr>
  <tr>
    <td><strong>From:</strong></td>
    <td><input class="line" name="from" value="" /></td>
  </tr>
  <tr>
    <td><strong>*Subject:</strong></td>
    <td><input class="line" name="subject" value="" /></td>
  </tr>
  <tr>
    <td><strong>References:</strong></td>
    <td><input class="line" name="references" value="" /></td>
  </tr>
  <tr>
    <td><strong>Mail2News:</strong></td>
    <td><input class="line" name="mail2news" value="'''+conf.mail2news+'''" /></td>
  </tr>
  <tr>
    <td><strong>Hashcash:</strong></td>
    <td><input class="line" name="hashcash" value="" /></td>
  </tr>
  <tr>
    <td><strong>X-No-Archive:</strong></td>
    <td><input type="checkbox" name="archive" checked="checked" />
        (checked means Google will not archive this post)
    </td>
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
        newsgroups, orig, subj, refs, mail2news, hashcash, no_archive, chain, n_copies, msg = self.validate()
        send_news(newsgroups, orig, subj, refs, mail2news, hashcash, no_archive, chain, n_copies, msg)
        msg = 'Successfully sent message to '+newsgroups+' using '
        if chain:
            msg += 'remailer chain '+','.join(chain)+'.'
        else:
            msg += 'a random remailer chain.'
        return msg

    

def handler(req):
    return NewsInterface()(req)
