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

import ConfigParser

class Config:
    pass

conf = Config()

PYANO = 'Pyano'

class ConfigError(Exception):
    pass

def parse_config(config_file):
    config = ConfigParser.SafeConfigParser()
    config.add_section(PYANO)
    # fill defaults
    config.set(PYANO,'mixmaster','/usr/bin/mixmaster')
    config.set(PYANO,'mlist2','')
    config.set(PYANO,'allow_from','')
    config.set(PYANO,'hist_file','')
    config.set(PYANO,'hist_window','15')
    config.set(PYANO,'hist_max_uses','5')
    config.set(PYANO,'banned_file','')
    config.set(PYANO,'chain_max_length','5')
    config.set(PYANO,'max_copies','5')
    config.set(PYANO,'mail_header','')
    config.set(PYANO,'news_header','')
    config.set(PYANO,'footer','')
    config.set(PYANO,'mail2news','mail2news@dizum.com, mail2news@m2n.mixmin.net, mail2news@reece.net.au')
    # read config file
    try:
        config.read(config_file)
        conf.mixmaster = config.get(PYANO,'mixmaster')
        conf.mlist2 = config.get(PYANO,'mlist2')
        conf.allow_from = config.get(PYANO,'allow_from')
        conf.hist_file = config.get(PYANO,'hist_file')
        conf.hist_window = config.getint(PYANO,'hist_window')
        conf.hist_max_uses = config.getint(PYANO,'hist_max_uses')
        conf.banned_file = config.get(PYANO,'banned_file')
        conf.chain_max_length = config.getint(PYANO,'chain_max_length')
        conf.max_copies = config.getint(PYANO,'max_copies')
        conf.mail_header = config.get(PYANO,'mail_header')
        conf.news_header = config.get(PYANO,'news_header')
        conf.footer = config.get(PYANO,'footer')
        conf.mail2news = config.get(PYANO,'mail2news')
    except: # Something is wrong with the configuration file
        raise ConfigError('Error parsing configuration file.')
        

