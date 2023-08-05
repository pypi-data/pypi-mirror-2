#!/usr/bin/python

"""
ext.py - script for extraction of relations from textual files 
and storing them in N3 format

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

import sys, os, getopt, time
from xml.etree import cElementTree
from rdflib.Graph import ConjunctiveGraph as Graph
#from sets import Set

DEFAULT_CFGP = os.path.join(os.getcwd(), 'eureeka.cfg')

def ppTime(tm):
    h = int(tm/3600)
    m = int((tm - 3600*h)/60)
    s = tm - 3600*h - 60*m
    return `h`+'h:'+`m`+'m:'+`s`+'s'

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
    print 'ext.py  [-h | --help]  [-c | --config alternative config file]'
    print '        [-i | --input alternative input path]   [-o | --output'
    print '         alternative output path]'
    print '  Extracts  knowledge from textual resources in the  directory'
    print '  specified in the configuration file.'
    print '  Default configuration file is       ../resources/eureeka.cfg'
    print '  An alternative configuration file can be specified using the'
    print '  -c or --config options.'
    print '  Also, one can specify alternative folders with  input (text)'
    print '  files and for output (N3) files, using the resp. options.'

if __name__ == "__main__":
    cfg_path = DEFAULT_CFGP
    optlist, args = getopt.getopt(sys.argv[1:], 'hc:i:o:n', \
    ['help','config=','input=','output=','noext'])
    action, noext = 'EXTRACT', False
    inpdir, outdir = '', ''
    for par, val in optlist:
        if par == '-c' or par == '--config':
            cfg_path = os.path.abspath(val)
        if par == '-h' or par == '--help':
            action = 'HELP'
        if par == '-i' or par == '--input':
            inpdir = os.path.abspath(val)
        if par == '-o' or par == '--output':
            outdir = os.path.abspath(val)
        if par == '-n' or par == '--noext':
            noext = True
    if action == 'HELP':
        help()
    else:
        cfg = parseCFG(cfg_path)
        try:
            from eureeka.extraction import extractRels, callExtRE, trimRels
        except ImportError:
            sys.path.insert(0,cfg['LIB'])
            from extraction import extractRels, callExtRE, trimRels
        if not inpdir:
            inpdir = cfg['TEXT']
        if not outdir:
            outdir = cfg['N3_IN']
        #print 'DEBUG -- CFG:\n', `cfg`
        np2doc, relations = {}, {}
        for inf in os.listdir(inpdir):
            if not os.path.isfile(os.path.join(inpdir,inf)) or not \
            inf.split('.')[-1] == 'xml':
                continue
            print 'Processing file:', inf
            try:
                xml = cElementTree.parse(os.path.join(inpdir,inf))
            except SyntaxError:
                sys.stderr.write('Warning - syntax error in the file!\n')
                continue
            root = xml.getroot()
            for elem in root:
                if elem.tag != 'doc':
                    continue
                title = elem.attrib['title']
                text = elem.text
                # calling the native relation extraction
                tm1 = time.time()
                print '  - calling native relation extraction...'
                relations_local, np2doc = extractRels(text,title,np2doc)
                for key in relations_local:
                    relations[key] = relations_local[key]
                tm2 = time.time()
                print '  * duration:', ppTime(tm2-tm1)
                tm1 = tm2
                # calling the external tool
                if not noext:
                    print '  - calling external relation extraction...'
                    relations_local, np2doc = callExtRE(text,title,np2doc)
                    for key in relations_local:
                        relations[key] = relations_local[key]
                    tm2 = time.time()
                    print '  * duration:', ppTime(tm2-tm1)
        l_b = len(relations)
        relations = trimRels(relations,np2doc) #,t1=0.0,t2=0.0)
        l_a = len(relations)
        print 'No. of extracted relations:', `l_b`
        print 'No. of trimmed relations  :', `l_a`
        # creating the relation graphs
        prov2graph = {}
        for key in relations:
            if not prov2graph.has_key(key[3]):
                prov2graph[key[3]] = Graph()
            for triple in relations[key].getTriples():
                prov2graph[key[3]].add(triple)
        # dumping the relation graphs
        for prov in prov2graph:
            dest = os.path.join(outdir,prov+'.n3')
            prov2graph[prov].serialize(dest,'n3')

