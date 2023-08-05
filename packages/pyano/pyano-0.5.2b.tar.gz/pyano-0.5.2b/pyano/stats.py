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
from config import conf

LATENT = 0
UPTIME = 1
MIDDLE = 2
FROM = 3


def get_stats():
    stats = {}
    try:
        _read_mlist(stats)
    except IOError: # could not read mlist2 file
        return None
    try:    
        _read_allow_from(stats)
    except IOError: # could not read from.html file
        pass
    return stats


def _read_mlist(stats):
    with open(conf.mlist2,'r') as f:
        n = 0
        in_stats_block = False
        in_remailer_block = False
        for line in f:
            n += 1
            if n == 5:
                in_stats_block = True
            if n >= 5 and in_stats_block:
                elems = line.split()
                if len(elems) == 0: # blank line, we are out of the stats block
                    in_stats_block = False
                else:
                    name = elems[0]
                    latent = elems[2]
                    uptime = float(elems[4].strip('%'))
                    stats[name] = [latent, uptime]

            else: # we are now looking for the remailer capabilities block 
                if '=' in line:
                    in_remailer_block = True
                if in_remailer_block:
                    name = line[11:].split('"',1)[0]
                    if "middle" in line:
                        stats[name].append(True)
                    else:
                        stats[name].append(False)


def _read_allow_from(stats):
    # by default no remailers accept from headers
    for name, s in stats.iteritems():
        stats[name].append(False)

    with open(conf.allow_from,'r') as f: # find out those that do accept from headers
        in_from_block = False
        m = re.compile("<td>(\w+)</td>")
        for line in f:
            if line.find("User Supplied From") >= 0:
                in_from_block = True
            if in_from_block:
                ok = m.search(line)
                if ok:
                    name = ok.group(1)
                    if name in stats:
                        stats[name][FROM] = True


def format_stats(name, stats):
    latent, uptime, middle, orig = stats
    s = name.ljust(12)+latent.rjust(5)+(str(uptime)+"%").rjust(7)
    if middle:
        s += " middle"
    if orig:
        s += " from"
    return s


def uptime_sort(stats):
    remailers = stats.keys()
    remailers.sort(cmp=lambda x,y: cmp(stats[y][UPTIME],stats[x][UPTIME]))
    return remailers
