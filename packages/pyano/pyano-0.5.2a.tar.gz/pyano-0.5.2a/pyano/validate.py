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

import re
import random

from stats import UPTIME, MIDDLE, FROM
from html import NONE, RANDOM
from config import conf


class InputError(Exception):
    pass

def val_email_local(local):
    ac = "[a-zA-Z0-9_!#\$%&'*+\-=?\^`{|}~]"
    m = re.compile( '^('+ac+'+\.)*'+ac+'+$')
    if not m.match(local):
        raise InputError()


def val_dot_seq(server):
    ac = '[a-zA-Z0-9+\-_]'
    m = re.compile( '^('+ac+'+\.)+'+ac+'+$')
    if not m.match(server):
        raise InputError()


def val_email(addr):
    m = re.compile( '^("?[\w ]*"? *<)?([^>]+)>?$' )
    ok =  m.match(addr)
    try:
        if not ok:
            raise InputError()
        email = ok.group(2)
        parts = email.split('@')
        if len(parts) != 2:
            raise InputError()
        val_email_local(parts[0])
        val_dot_seq(parts[1])
    except InputError:
        raise InputError(addr+' is not a valid email address.')


def val_newsgroups(newsgroups):
    groups = newsgroups.split(',')
    for group in groups:
        val_dot_seq(group)


def val_references(refs):
    m = re.compile( '^<(.*)>$' )
    try:
        for ref in refs.split(' '):
            ok = m.match(ref)
            if not ok:
                raise InputError()
            val_email( ok.group(1) )
    except:
        raise InputError(ref+' is not a valid reference.')


def val_mail2news(mail2news):
    for addr in mail2news.split(','):
        val_email(addr)


def val_hashcash(hc):
    m = re.compile('[a-zA-Z0-9_:+\-=; ]+')
    if not m.match(hc):
        raise InputError(hc+' is not a valid hashcash.')

def val_n_copies(n_copies):
    if n_copies <= 0 or n_copies > conf.max_copies:
        raise InputError('Invalid number of copies.')

# Explanation for the chain parsing:
#
# By default the mixmaster binary will accept messages with duplicate
# remailers (bad for privacy), or a middleman remailer as the final
# remailer (which will silently fail).
#
# On the other hand, when sending multi-part emails, it *requires*
# two random remailers in the chain.
#
# Here we make the following imperfect design choices:
#  - Translate a choice of RANDOM to '*' (the mixmaster random chain)
#    Except if a random remailer is chosen last, in which case this program
#    selects the final remailer and makes sure it is not a middleman.
#  - Check for duplicate remailers. However if the user selects a RANDOM remailer
#    mixmaster MAY select a duplicate remailer. (TODO: read the mixmaster code
#    to make sure...)
#
def parse_chain(fs,stats):
    chain = []
    for i in range(0, conf.chain_max_length):
        remailer = str(fs['chain'+str(i)])
        if remailer == NONE: # empty remailer, we stop the chain
            break
        elif remailer == RANDOM:
            chain.append('*')
        elif remailer in chain: # duplicate remailer!
            raise InputError('Cannot use the same remailer twice in the same chain.')
        elif remailer in stats:
            chain.append( remailer )
        else: # invalid remailer entry
            raise InputError(remailer+' is not a valid remailer.')

    if chain:
        last = chain[len(chain)-1]
        if last == '*': # make sure final remailer is neither a duplicate nor a middleman
            chain[len(chain)-1] = get_random_remailer(stats,isValid=lambda r : not( r in chain or stats[r][MIDDLE]) ) 
        elif stats[last][MIDDLE]: # make sure that final remailer is not a middleman
            raise InputError('Cannot select a "middle" remailer as your final remailer.')
    return chain


def get_random_remailer(stats,isValid=lambda r : True):
    # first select the subset of remailers that have 100% reliability
    reliable = set([])
    for remailer, s in stats.iteritems():
        if s[UPTIME] == 100.0 and isValid(remailer):
            reliable.add(remailer)
    if not reliable: # there are no 100% reliable remailers
        for remailer in stats.itervalues():
            if isValid(remailer):
                reliable.add(remailer)
    if not reliable: # no remailers matching criteria
        raise InputError('Could not select adequate random remailer.')
    # get a random remailer
    return random.choice(list(reliable))
