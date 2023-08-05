#!/usr/bin/python

"""
que.py - script for evaluating EUREEKA queries

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

import sys, getopt, os, hashlib
#from sets import Set
from rdflib.Graph import ConjunctiveGraph as Graph

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
    print 'que.py [-h | --help]   [-c | --config alternative config file]'
    print '[-q | --query query] [-x | --extend]  [-g | --get entity name]'
    print '  Knowledge base querying, entity retrieval. Output stored  to'
    print '  the path specified  in the configuration file.'
    print '  Default configuration file is       ../resources/eureeka.cfg'
    print '  An alternative configuration file can be specified using the'
    print '  -c or --config options.'
    print '  Other options:'
    print '  -q or --query              ask a query'
    print '  -g or --get                get an entity representation'
    print '  -x or --extend             generate extension of the answers'

if __name__ == "__main__":
    cfg_path, action = DEFAULT_CFGP, '' #'QUERY'
    optlist, args = getopt.getopt(sys.argv[1:], 'c:q:g:xalr:',['config=',\
    'query=', 'get=', 'extend', 'apply', 'closure', 'rules='])
    extension, closure, apply = False, False, False
    q, t, rule_desc = '', '', 'default'
    for par, val in optlist:
        if par == '-c' or par == '--config':
            cfg_path = os.path.abspath(val)
        if par == '-q' or par == '--query':
            q, action = val, 'QUERY'
        if par == '-g' or par == '--get':
            t, action = val, 'GET'
        if par == '-x' or par == '--extend':
            extension = True
        if par == '-l' or par == '--closure':
            closure = True
        if par == '-a' or par == '--apply':
            apply = True
        if par == '-r' or par == '--rules':
            rule_desc = val
        if par == '-h' or par == '--help':
            action = 'HELP'
    if action == 'HELP':
        help()
    else:
        cfg = parseCFG(cfg_path)
        #print 'DEBUG -- CFG:\n', `cfg`
        try:
            from eureeka.kb import KB
        except ImportError:
            sys.path.insert(0,cfg['LIB'])
            from kb import KB
        kbase = KB(cfg,trace=True)
        relations, dest = [], cfg['N3_OUT']
        if action == 'QUERY':
            dest = os.path.join(dest,hashlib.sha1(q).hexdigest()+'.n3')
            relations = kbase.ask(q)
        elif action == 'GET':
            dest = os.path.join(dest,hashlib.sha1(t).hexdigest()+'.n3')
            relations = kbase.entities.getRelations([kbase.grounding.get(t)])
        g = kbase.grounding
        if extension:
            # append the extension relations
            # @TODO - perhaps generalise, now onlt DEF_SCP subjects reflected
            ids = list(set(map(lambda x: g.get(x.getSubject()),relations)))
            for r in kbase.extend(ids):
                relations.append(r)
        if closure and not q and not t:
            dest = os.path.join(dest,hashlib.sha1('closure').hexdigest()+'.n3')
            kbase.closure()
            ids = kbase.entities.keys()
            relations = \
            kbase.entities.getRelations(ids,g=kbase.grounding,prov=0)
        if apply and not q and not t:
            dest = os.path.join(dest,hashlib.sha1('apply').hexdigest()+'.n3')
            relations = kbase.apply([])
        gr = Graph()
        for r in relations:
            for triple in r.getTriples():
                #print 'DEBUG -- triple:', `triple`
                gr.add(triple)
        print 'Serialising the results to:', dest
        gr.serialize(dest,'n3')
