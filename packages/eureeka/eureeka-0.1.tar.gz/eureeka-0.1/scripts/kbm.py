#!/usr/bin/python

"""
kbm.py - script for creating dumps of entity/grounding database
tables and for initialisation of the databases with default values.

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

import MySQLdb, sys, os, getopt, time

EUREEKA_HOME = '/home/eureeka/devel'

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
    print 'dbm.py [-h | --help]   [-c | --config alternative config file]'
    print '[-m | --import]     [-i | --init]    [-d | --dump]'
    print '[-u | --update-scores] [-n | --input alternative import path]'
    print '  Initialisation, filling and backup of the EUREEKA  knowledge'
    print '  bases according to the  content in directories specified  in'
    print '  the configuration file.'
    print '  Default configuration file is       ../resources/eureeka.cfg'
    print '  An alternative configuration file can be specified using the'
    print '  -c or --config options.'
    print '  Other options:'
    print '  -m or --import             alternative path for loading data'
    print '  -n or --input              data loading directory'
    print '  -i or --init               init of the knowledge base'
    print '  -d or --dump               backup of the knowledge base'
    print '  -u or --update-scores      update the HITS-based scores'

def initModel(cfg):
    try:
        from eureeka.util import MLIST as mlist
        from eureeka.util import RELATION_SUBTYPES as relation_subtypes
        from eureeka.util import BASE_TERMS as base_terms
        from eureeka.storage import Grounding, Entities, initDB
    except ImportError:
        sys.path.insert(0,cfg['LIB'])
        from util import MLIST as mlist
        from util import RELATION_SUBTYPES as relation_subtypes
        from util import BASE_TERMS as base_terms
        from storage import Grounding, Entities, initDB
    db = MySQLdb.connect(host=cfg['DB_HOST'],user=cfg['DB_USER'],\
    passwd=cfg['DB_PASS'],db=cfg['DB_NAME'])
    cursor = db.cursor()
    initDB(cursor)
    # create backup
    dumpDB(cfg)
    cursor.execute("""DELETE FROM grounding""")
    cursor.execute("""DELETE FROM entities""")
    cursor.execute("""DELETE FROM scores""")
    # fill grounding and entitites with default values
    #db_param = {'host':cfg['DB_HOST'], 'user':cfg['DB_USER'],\
    #'passwd':cfg['DB_PASS'], 'db':cfg['DB_NAME']}
    g = Grounding(cfg)
    g.add('generic relation',scope=1)
    g.addSyn('relation','generic relation',scope=1)
    g.addSyn('property','generic relation',scope=1)
    g.add('generic entity',scope=2)
    g.addSyn('class','generic entity',scope=2)
    g.addSyn('entity','generic entity',scope=2)
    g.addSyn('concept','generic entity',scope=2)
    for master in mlist:
        sc = 1
        if master in relation_subtypes:
            sc = 1
        else:
            sc = 2
        g.add(master,scope=sc)
        for syn in base_terms[master]:
            g.addSyn(syn,master,scope=sc)
    e = Entities(cfg)
    for r in genBasicOntology(cfg):
        e.addRelation(r,g)

def genBasicOntology(cfg):
    l = []
    try:
        from eureeka.storage import Relation
    except ImportError:
        sys.path.insert(0,cfg['LIB'])
        from storage import Relation
    l.append(Relation('generic entity', 'type of', 'generic entity', \
    'default provenance'))
    l.append(Relation('default provenance', 'type of', 'generic entity', \
    'default provenance'))
    l.append(Relation('provenance', 'type of', 'generic entity', \
    'default provenance'))
    l.append(Relation('generic variable', 'type of', 'generic entity', \
    'default provenance'))
    l.append(Relation('generic relation', 'type of', 'generic entity', \
    'default provenance',subj_rel=True))
    l.append(Relation('generic relation', 'type of', 'generic relation', \
    'default provenance',subj_rel=True,obj_rel=True))
    l.append(Relation('generic individual', 'type of', 'generic entity', \
    'default provenance'))
    l.append(Relation('domain', 'type of', 'generic relation', \
    'default provenance',subj_rel=True,obj_rel=True))
    l.append(Relation('range', 'type of', 'generic relation', \
    'default provenance',subj_rel=True,obj_rel=True))
    l.append(Relation('domain', 'range', 'generic entity', \
    'default provenance',subj_rel=True))
    l.append(Relation('range', 'range', 'generic entity', \
    'default provenance',subj_rel=True))
    l.append(Relation('inverse of', 'type of', 'generic relation', \
    'default provenance',subj_rel=True,obj_rel=True))
    l.append(Relation('reflexive relation', 'type of', 'generic relation', \
    'default provenance',subj_rel=True,obj_rel=True))
    l.append(Relation('symmetric relation', 'type of', 'generic relation', \
    'default provenance',subj_rel=True,obj_rel=True))
    l.append(Relation('transitive relation', 'type of', 'generic relation', \
    'default provenance',subj_rel=True,obj_rel=True))
    l.append(Relation('antisymmetric relation', 'type of', 'generic relation',\
    'default provenance',subj_rel=True,obj_rel=True))
    l.append(Relation('irreflexive relation', 'type of', 'generic relation', \
    'default provenance',subj_rel=True,obj_rel=True))
    l.append(Relation('functional relation', 'type of', 'generic relation', \
    'default provenance',subj_rel=True,obj_rel=True))
    l.append(Relation('inverse functional relation', 'type of', \
    'generic relation', 'default provenance',subj_rel=True,obj_rel=True))
    l.append(Relation('generic link', 'type of', 'generic relation', \
    'default provenance',subj_rel=True,obj_rel=True))
    l.append(Relation('generic link', 'type of', 'transitive relation', \
    'default provenance',subj_rel=True,obj_rel=True))
    l.append(Relation('has title', 'type of', 'generic relation', \
    'default provenance',subj_rel=True,obj_rel=True))
    l.append(Relation('has part', 'type of', 'generic relation', \
    'default provenance',subj_rel=True,obj_rel=True))
    l.append(Relation('part of', 'type of', 'generic relation', \
    'default provenance',subj_rel=True,obj_rel=True))
    l.append(Relation('type of', 'type of', 'generic relation', \
    'default provenance',subj_rel=True,obj_rel=True))
    l.append(Relation('same as', 'type of', 'generic relation', \
    'default provenance',subj_rel=True,obj_rel=True))
    l.append(Relation('different from', 'type of', 'generic relation', \
    'default provenance',subj_rel=True,obj_rel=True))
    l.append(Relation('type of', 'type of', 'transitive relation', \
    'default provenance',subj_rel=True,obj_rel=True))
    l.append(Relation('type of', 'type of', 'antisymmetric relation', \
    'default provenance',subj_rel=True,obj_rel=True))
    l.append(Relation('has part', 'type of', 'transitive relation', \
    'default provenance',subj_rel=True,obj_rel=True))
    l.append(Relation('part of', 'type of', 'transitive relation', \
    'default provenance',subj_rel=True,obj_rel=True))
    l.append(Relation('has part', 'inverse of', 'part of', \
    'default provenance',subj_rel=True,obj_rel=True))
    l.append(Relation('part of', 'inverse of', 'has part', \
    'default provenance',subj_rel=True,obj_rel=True))
    l.append(Relation('same as', 'type of', 'transitive relation', \
    'default provenance',subj_rel=True,obj_rel=True))
    l.append(Relation('same as', 'type of', 'reflexive relation', \
    'default provenance',subj_rel=True,obj_rel=True))
    l.append(Relation('same as', 'type of', 'symmetric relation', \
    'default provenance',subj_rel=True,obj_rel=True))
    l.append(Relation('inferred provenance', 'type of', 'generic entity', \
    'default provenance'))
    return l

def dumpDB(cfg):
    # initialising common variables
    tstamp = reduce(lambda x,y: x+'-'+y, time.ctime().split()[1:])
    paths = {'grounding':'','entities':'','scores':''}
    paths['grounding'] = \
    os.path.join(cfg['DB_DUMP'],'grounding.'+tstamp+'.sql')
    paths['entities'] = \
    os.path.join(cfg['DB_DUMP'],'entities.'+tstamp+'.sql')
    paths['scores'] = \
    os.path.join(cfg['DB_DUMP'],'scores.'+tstamp+'.sql')
    user = ' --user='+cfg['DB_USER']
    pswd = ' --password='+cfg['DB_PASS']
    dbnm = cfg['DB_NAME']
    # dumping grounding
    outf = ' --result-file='+paths['grounding']
    tbnm = ' grounding'
    os.system('mysqldump'+user +pswd+' '+outf+' '+dbnm+' '+tbnm)
    # dumping entities
    outf = ' --result-file='+paths['entities']
    tbnm = ' entities'
    os.system('mysqldump'+user +pswd+' '+outf+' '+dbnm+' '+tbnm)
    # dumping scores
    outf = ' --result-file='+paths['scores']
    tbnm = ' scores'
    os.system('mysqldump'+user +pswd+' '+outf+' '+dbnm+' '+tbnm)
    # compressing the stuff
    os.system('gzip '+paths['grounding'])
    os.system('gzip '+paths['entities'])
    os.system('gzip '+paths['scores'])

if __name__ == "__main__":
    imp_path, noinp = os.getcwd(), True
    cfg_path, action = DEFAULT_CFGP, ''
    optlist, args = getopt.getopt(sys.argv[1:], 'c:mn:iduh', ['config=',\
    'import','input=','init','dump','update-scores','help'])
    for par, val in optlist:
        if par == '-c' or par == '--config':
            cfg_path = os.path.abspath(val)
        if par == '-m' or par == '--import':
            action = 'IMPORT'
        if par == '-n' or par == '--input':
            imp_path = os.path.abspath(val)
            noinp = False
        if par == '-i' or par == '--init':
            action = 'INIT'
        if par == '-d' or par == '--dump':
            action = 'DUMP'
        if par == '-u' or par == '--update-scores':
            action = 'UPDATE-SCORES'
        if par == '-h' or par == '--help':
            action = 'HELP'
    cfg = parseCFG(cfg_path)
    #print 'DEBUG -- CFG:\n', `cfg`
    #print 'DEBUG -- action:', action
    if cfg.has_key('N3_IN') and os.path.isdir(cfg['N3_IN']) and noinp:
        imp_path = cfg['N3_IN']
    if action == 'HELP':
        help()
    else:
        try:
            from eureeka.kb import KB
        except ImportError:
            sys.path.insert(0,cfg['LIB'])
            from kb import KB
        if action == 'INIT':
            print 'Initialising the ENTITY and GROUNDING databases...'
            initModel(cfg)
        elif action == 'DUMP':
            print 'Dumping the ENTITY, GROUNDING and SCORES databases...'
            dumpDB(cfg)
        elif action == 'IMPORT':
            #print 'DEBUG -- input path for the import:', imp_path
            kbase = KB(cfg)
            kbase.load(imp_path)
        elif action == 'UPDATE-SCORES':
            kbase = KB(cfg)
            kbase.updateScores(k=5,minf=3)

