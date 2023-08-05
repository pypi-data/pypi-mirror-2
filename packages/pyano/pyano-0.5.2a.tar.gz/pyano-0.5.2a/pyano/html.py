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

from config import conf
from stats import uptime_sort, format_stats

NONE = ''
RANDOM = 'RANDOM'


def html_from_file(file):
    with open(file,'r') as f:
        return f.read()


def html_header(title):
    return '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">

<head>
  <title>'''+title+'''</title>
</head>

<body>

<h1>'''+title+'''</h1>


'''


def html_copyright():
    return '''
<div id="copyright">
<a href="http://pyanon.sourceforge.net">Pyano</a> - &copy; Sean Whitbeck 2010
</div>
'''


def html_error(msg):
    return '''<h2>Error!</h2>

<p>
'''+msg+'''
</p>
'''


def html_preamble():
    return '''<p>
Use this mixmaster web interface to send anonymous emails. If no remailers are selected
in the chain, then mixmaster will automatically select a remailer chain for you. If you intend
on using the <em>From</em> field please read the instructions <a href="#from">here</a>. For
more detailed instructions, refer to the <a href="#help">help</a> section below.
</p>
<p>
Fields marked with <strong>*</strong> are mandatory.
</p>
'''

def html_help( msg ):
    return '''<h2><a name="help">Help</a></h2>

<p>
The mixmaster interface is a completely anonymous solution. 
Messages sent via this interface cannot even be traced back to matterhorn. 
Use it responsibly. If you spam through it, you risk getting banned.
</p>

<p>
This interface wraps your message in layers of PGP encryption. 
Each remailer in the chain unwraps one layer then sends to the next one. 
In this way no one remailer knows the source, destination, and contents. 
The longer the chain you use, the more guaranteed the anonymity. 
However, this comes at the cost of reliabiltyy. Indeed, remailers can be unreliable 
and there is no guarantee that every message sent will arrive at it's destination. Increasing
the number of copies increases the reliability.
</p>

<p>
'''+msg+''' Choose your remailers. Enter the message body, then click send. 
A sent page will appear to inform you on the outcome. Wait for it!.
</p>

<h3>Stats</h3>

<p>
The remailers are listed in the drop lists with some stats. Those stats are as follows:
</p>
<ul class="description">
  <li><dfn>Name</dfn>: The name of the remailer.</li>
  <li><dfn>Latency</dfn>: Latency means how long the remailer will hold onto the message before delivering it to the next remailer in line.</li>
  <li><dfn>Uptime</dfn>: This is a percentage. Obviously you want to use remailers with high uptime. I would choose 95% or better.</li>
  <li><dfn>Middle</dfn>: If you see this word next to a remailer it means that this remailer only operates in middleman mode. That means you can only use it in the middle of a chain. If you use it at the end, your message will not be delivered.</li>
  <li><dfn>From</dfn>: This remailer may allow user-supplied from headers. See below for more information.</li>
</ul>

<h3><a name="from">From Lines</a></h3>

<p>
Not all remailers support from lines. If you wish 
to use a custom from line rather than one the remailer chooses for you, you must select 
a remailer that supports custom from lines as the last remailer in the chain! Put your 
from line in this format: <kbd>"John Smith" &lt;john@domain.com&gt;</kbd>
</p>

'''
    

def html_chain(stats):
    s = ''
    for i in range(0, conf.chain_max_length):
        s += '''      <select name="chain'''+str(i)+'''" >
        <option value="'''+NONE+'''" selected="selected"></option>
        <option value="'''+RANDOM+'''">Random</option>
'''
        for remailer in uptime_sort(stats):
            s += '        <option value="'+remailer+'">'+format_stats(remailer,stats[remailer]).replace(' ',"&nbsp;")+'</option>\n'
        s += '      </select><br/>'
    return s


def html_copies():
    s = '''      <select name="copies">
        <option value="1" selected="selected">1</option>
'''
    for i in range(1, conf.max_copies):
        s += '        <option value="'+str(i+1)+'" >'+str(i+1)+'</option>\n'
    s += '      </select>'
    return s


def html_back():
    return '''<p>
Press your browser's back button to come back to the mixmaster web interface.
</p>
'''

def html_success(msg):
    return '''<h2>Success!</h2>

<p>
'''+msg+'''
</p>
'''
