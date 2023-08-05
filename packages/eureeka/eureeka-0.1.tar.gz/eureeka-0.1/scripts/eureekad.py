#!/usr/bin/python

"""
eureekad.py - script for running the EUREEKA D-Bus daemon

Copyright (C) 2009-2010  Vit Novacek (vit.novacek@deri.org)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import gobject, sys, os, getopt
from dbus.mainloop.glib import DBusGMainLoop

DEFAULT_CFGP = os.path.join(os.getcwd(), 'eureeka.cfg')

def parseCFG(cfg_path):
    try:
        f, cfg = open(cfg_path,'r'), {}
        for line in f:
            hash_spl = line.split('#')[0].strip()
            tabl_spl = hash_spl.split('\t')
            if hash_spl and len(tabl_spl) >= 2:
                key, value = tabl_spl[0].upper().strip(), tabl_spl[1].strip()
                try:
                    value = float(value)
                except ValueError:
                    pass # keep as a string if not convertible to a number
                cfg[key] = value
        f.close()
        # setting default values of expected parameters
        if not cfg.has_key('N3_IN'):
            cfg['N3_IN'] = os.getcwd()
        if not cfg.has_key('N3_OUT'):
            cfg['N3_OUT'] = os.getcwd()
        if not cfg.has_key('TEXT'):
            cfg['TEXT'] = os.getcwd()
        if not cfg.has_key('DB_DUMP'):
            cfg['DB_DUMP'] = os.getcwd()
        if not cfg.has_key('RL_PATH'):
            cfg['RL_PATH'] = os.path.join(os.getcwd(),'default.n3')
        if not cfg.has_key('DC_REL'):
            cfg['DC_REL'] = os.path.join(os.getcwd(),'relevance.txt')
        if not cfg.has_key('DEF_REL'):
            cfg['DEF_REL'] = 0.2
        return cfg
    except Exception:
        sys.exit('Terminating - problems with the provided config file!\n')

def help():
    print 'eureekad.py [-h | --help]   [-c | --config alternative config file]'
    print '  Launching the EUREEKA D-Bus server. Configuration defaults as per'
    print '  user manual, or can be specified in a respective alternate  file.'

if __name__=='__main__':
    optlist, args = getopt.getopt(sys.argv[1:], 'c:h',['config=','help'])
    cfg_path, help_only = DEFAULT_CFGP, False
    for par, val in optlist:
        # @TODO - possibly also reflect the termination of the server here
        if par == '-c' or par == '--config':
            cfg_path = os.path.abspath(val)
        if par == '-h' or par == '--help':
            help_only = True
    if help_only:
        help()
    else:
        # @TODO - possibly also reflect the termination of the server here
        cfg = parseCFG(cfg_path)
        try:
            from eureeka.srvlib import EureekaServer
        except ImportError:
            sys.path.insert(0,cfg['LIB'])
            from srvlib import EureekaServer
        DBusGMainLoop(set_as_default=True)
        EureekaServer("/ie/deri/sw/smile/koraal/dbus/eureeka",cfg)
        loop=gobject.MainLoop()
        loop.run()

