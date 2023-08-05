"""
storage.py - a library containing the low-level storage implementations for
EUREEKA knowledge bases and groundings (i.e., lexicons)

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

import rdflib, sys, os, time, MySQLdb, hashlib, gc
from math import log, fabs, exp
from eureeka.util import parseCFG, lemmatise
#from sets import Set
#from nltk.wordnet.stemmer import morphy
from nltk.corpus import wordnet as wn

NS_EUPRES = 'http://ontologies.smile.deri.ie/eureeka/presentation#'

def initDB(cursor):
    cursor.execute("""CREATE TABLE IF NOT EXISTS grounding (
                        lemma       VARCHAR(500) NOT NULL,
                        identifier  INTEGER UNSIGNED NOT NULL,
                        scope       INTEGER UNSIGNED NOT NULL,
                        certainty   FLOAT NOT NULL,
                        INDEX ls    (lemma,scope),
                        INDEX ic    (identifier,certainty)
                      )""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS entities (
                        id          INTEGER UNSIGNED NOT NULL,
                        subject     INTEGER UNSIGNED NOT NULL,
                        predicate   INTEGER UNSIGNED NOT NULL,
                        object      INTEGER UNSIGNED NOT NULL,
                        provenance  INTEGER UNSIGNED,
                        certainty   FLOAT NOT NULL,
                        PRIMARY KEY (subject,predicate,object,provenance),
                        INDEX po    (predicate,object),
                        INDEX op    (object,predicate),
                        INDEX so    (subject,object),
                        INDEX prov  (provenance)
                      )""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS scores (
                        entity      INTEGER UNSIGNED NOT NULL,
                        hub         FLOAT NOT NULL,
                        auth        FLOAT NOT NULL,
                        lexical     FLOAT,
                        PRIMARY KEY (entity)
                      )""")

class Relation:
    """
    Container for extracted relations and their various features.
    """

    def __init__(self,s,p,o,prov_tit=None,cert=1.0,score=0.0,\
    subj_rel=False,obj_rel=False):
        self.subj_rel, self.obj_rel = subj_rel, obj_rel
        self.subject = lemmatise(s,'n')
        if subj_rel:
            # subject as relation
            self.subject = lemmatise(s,'v')
        self.predicate = lemmatise(p,'v')
        self.object = lemmatise(o,'n')
        if obj_rel:
            # object as relation
            self.object = lemmatise(o,'v')
        self.contexts = {} # meant for direct access
        self.certainty = cert
        self.score = score
        self.provenance = {}
        if prov_tit:
            self.provenance = {hashlib.sha1(`prov_tit`).hexdigest():prov_tit}
        self.tf = 0.0

    def getHashKey(self,g,prov_tit=None):
        if not prov_tit:
            prov_tit = self.getProvenanceTitle()
        s = `self.predicate`+'('+`self.subject`+','+`self.object`+')='+\
        `self.certainty`+'@'+`prov_tit`+'{'+`self.contexts.items()`+'}'
        hsh = hashlib.sha1(s).hexdigest()
        i = g.get(hsh,scope=g.DEF_SCP)
        if not i:
            i = g.add(hsh,scope=g.DEF_SCP)
        return i

    def isNegative(self):
        return self.certainty < 0

    def isSubjRel(self):
        return self.subj_rel

    def isObjRel(self):
        return self.obj_rel

    def subjRelOn(self):
        self.subj_rel = True

    def subjRelOff(self):
        self.subj_rel = False

    def objRelOn(self):
        self.obj_rel = True

    def objRelOff(self):
        self.obj_rel = False

    def getSubject(self):
        return self.subject

    def getPredicate(self):
        return self.predicate

    def getObject(self):
        return self.object

    def getSPO(self):
        return (self.subject,self.predicate,self.object)

    def getKey(self):
        return (self.subject,self.predicate,self.object,\
        self.provenance.keys()[0])

    def getContext(self,ctx_pred):
        try:
            return self.contexts[ctx_pred]
        except KeyError:
            return None

    def getContextTuples(self):
        return self.contexts.items()

    def getCertainty(self):
        return self.certainty

    def getScore(self):
        return self.score

    def getProvenanceTitle(self,key=None):
        if key:
            return self.provenance[key]
        return self.provenance[self.provenance.keys()[0]]

    def getProvenanceID(self,tit=None):
        if tit:
            return hashlib.sha1(tit).hexdigest()
        return self.provenance.keys()[0]

    def getTF(self):
        return self.tf

    def setSubject(self,s):
        self.subject = lemmatise(s,'n')

    def setPredicate(self,p):
        self.predicate = lemmatise(p,'v')

    def setObject(self,o):
        self.object = lemmatise(o,'n')

    def setSPO(self,spo):
        self.subject = lemmatise(spo[0],'n')
        self.predicate = lemmatise(spo[1],'v')
        self.object = lemmatise(spo[2],'n')

    def setContext(self,ctx_pred,ctx):
        self.contexts[ctx_pred] = lemmatise(ctx,'n')

    def setCertainty(self,c):
        self.certainty = c

    def setProvenance(self,prov_tit):
        self.provenance[hashlib.sha1(prov_tit).hexdigest()] = prov_tit

    def setScore(self,score):
        self.score = score

    def setTF(self,tf):
        self.tf = tf

    def getTriples(self,ns_pref='http://ontologies.smile.deri.ie/eureeka'):
        """
        Returns triple representation of itself in the form of RDFlib triples.
        """

        ns_suff = reduce(lambda x,y: x+'+'+y, self.provenance.keys(),'')
        ns = rdflib.Namespace(ns_pref+ns_suff+'/')
        nsp = rdflib.Namespace(NS_EUPRES)
        s_str = `self.predicate`+'('+`self.subject`+','+`self.object`+','+\
        `self.provenance.items`+')='+`self.certainty`
        rel_id = hashlib.sha1(s_str).hexdigest()
        triples = []
        triples.append((ns[rel_id],nsp['hasPredicate'],\
        rdflib.Literal(self.predicate)))
        triples.append((ns[rel_id],nsp['hasSubject'],\
        rdflib.Literal(self.subject)))
        triples.append((ns[rel_id],nsp['hasObject'],\
        rdflib.Literal(self.object)))
        triples.append((ns[rel_id],nsp['hasCertainty'],\
        rdflib.Literal(self.certainty)))
        triples.append((ns[rel_id],nsp['hasScore'],\
        rdflib.Literal(self.score)))
        for key in self.provenance:
            triples.append((ns[rel_id],nsp['hasProvenance'],\
            rdflib.Literal(key+' : '+self.provenance[key])))
        for key in self.contexts:
            #print 'DEBUG -- ctx triple being added:', `(ns[rel_id],nsp[key],\
            #rdflib.Literal(self.contexts[key]))`
            triples.append((ns[rel_id],nsp[key],\
            rdflib.Literal(self.contexts[key])))
        return triples

class Entity:
    """
    Simplified sparse identifier-tensor representation of entities. Essentially
    only read-only representation.
    """

    def __init__(self,i,statements=[]):
        """
        Initialised by (s,p,o,d) statements. Essentially read-only object.
        """

        self.identifier = i
        self.elements = {}
        for s, p, o, d in statements:
            if s != self.identifier:
                continue
            self.elements[(p,o)] = d

    def __mul__(self,x):
        """
        Multiplying the entity.
        """

        e = Entity(self.identifier)
        for p, o in self.elements:
            e.setDegree(p,o,self.elements[(p,o)]*x)
        return e

    def __add__(self,other):
        """
        Adding another entity. Implemented as extension by the currently zero
        degrees. In case of conflicts, the degree value with the biggest 
        absolute wins for same signum. For different signums, arithmetic mean
        is used in the result.
        """

        e = Entity(self.identifier)
        for p,o in self.getIndices():
            e.setDegree(p,o,self.getDegree(p,o))
        for p,o in other.getIndices():
            if not e.getDegree(p,o):
                e.setDegree(p,o,other.getDegree(p,o))
            else:
                d1, d2 = e.getDegree(p,o), other.getDegree(p,o)
                d = (d1+d2)/2 # default mean for different signums
                if d1*d2 > 0:
                    # set the biggest absolute value degree for same signums
                    d = d1
                    if fabs(d2) > fabs(d1):
                        d = d2
                e.setDegree(p,o,d)
        return e

    def __eq__(self,other):
        """
        Strong equality of entities.
        """

        if isinstance(other,Entity):
            return self.elements == other.elements
        return NotImplemented

    def __ne__(self,other):
        """
        Strong inequality of entities.
        """

        result = self.__eq__(other)
        if result is NotImplemented:
            return result
        return not result

    def __len__(self):
        return len(self.elements)

    def sim(self,other,fit_incl=True,penalty=2.0,even=False):
        """
        Similarity of this entity to the other, or their even comparison.
        """

        indices = set(self.elements.keys())
        if even:
            indices |= set(other.elements.keys())
        dist, misses = 0.0, 0
        for p, o in indices:
            d1, d2 = self.getDegree(p,o), other.getDegree(p,o)
            if not d1 or not d2: 
                misses += 1
            dist += fabs(d1-d2)
        dist /= float(len(indices)) # normalising distance
        k = 1.0
        if fit_incl:
            # taking fitness into account, too
            k = max(0,len(indices) - penalty*misses)/float(len(indices))
        return k*1.0/(1.0+dist)

    def isWeaklyEqualTo(self,e):
        """
        Checks whether self is weakly equal to the argument.
        """

        return self.identifier == e.getID()

    def getID(self):
        return self.identifier

    def getDegree(self,p,o):
        """
        Returns degree associated with property p and object o.
        """

        try:
            return self.elements[(p,o)]
        except KeyError:
            return 0.0

    def setDegree(self,p,o,d=1.0):
        """
        Sets the degree of respective element.
        """

        self.elements[(p,o)] = d

    def getProperties(self):
        """
        Returns all property indices.
        """

        return map(lambda x: x[0], self.elements.keys())

    def getIndices(self,get_set=False):
        """
        Returns (tuples of) indices of all non-zero entity elements.
        If get_set is True, a set is returned (instead of a list).
        """

        if get_set:
            return set(self.elements.keys())
        else:
            return self.elements.keys()

    def getTxt(self,dct):
        s, chunks = self.identifier, []
        for x in map(lambda x: (s,x[0][0],x[0][1],x[1]), \
        self.elements.items()):
            sw = dct.get(x[0],scope=dct.DEF_SCP)
            if not sw:
                sw = dct.get(x[0],scope=dct.VAR_SCP)
            pw = dct.get(x[1],scope=dct.REL_SCP)
            if not pw:
                pw = dct.get(x[1],scope=dct.VAR_SCP)
            ow = dct.get(x[2],scope=dct.DEF_SCP)
            if not ow:
                ow = dct.get(x[2],scope=dct.VAR_SCP)
            if not ow:
                ow = dct.get(x[2],scope=dct.REL_SCP)
            chunks.append('('+sw+' : '+pw+' : '+ow+')^'+`x[3]`)
        return reduce(lambda x,y: x+' AND '+y,chunks)

class Grounding:

    def __init__(self,cfg,stemmer=None,var_sig='?',trace=False):
        self.trace = trace
        self.stem_func = stemmer
        if not self.stem_func:
            self.stem_func = wn.morphy
        self.cfg = cfg
        #if not self.cfg:
        #    cfg = parseCFG(os.path.join('..','resources','eureeka.cfg'))
        # connecting to the specified database
        self.db = MySQLdb.connect(host=cfg['DB_HOST'],user=cfg['DB_USER'],\
        passwd=cfg['DB_PASS'],db=cfg['DB_NAME'])
        self.cursor = self.db.cursor()
        initDB(self.cursor)
        self.cursor.execute("""SELECT max(identifier) FROM grounding""")
        self.next_id = 1 # next ID to be used, at the same time, size
        tmp = self.cursor.fetchone()
        if tmp and tmp[0]:
            self.next_id = int(tmp[0]) + 1
        # hard-set the default context ID, assuming the ID of the abstract
        # context sense is the lowest one
        self.cursor.execute("""SELECT DISTINCT identifier FROM grounding WHERE 
                               lemma='generic entity' 
                               ORDER BY identifier asc""")
        self.DEF_SCP = self.cursor.fetchone()
        if self.DEF_SCP:
            self.DEF_SCP = self.DEF_SCP[0]
        else:
            self.DEF_SCP = 2
        self.cursor.execute("""SELECT DISTINCT identifier FROM grounding WHERE 
                               lemma='generic relation' ORDER BY identifier 
                               asc""")
        self.REL_SCP = self.cursor.fetchone()
        if self.REL_SCP:
            self.REL_SCP = self.REL_SCP[0]
        else:
            self.REL_SCP = 1
        self.cursor.execute("""SELECT DISTINCT identifier FROM grounding WHERE 
                               lemma='generic variable' ORDER BY identifier 
                               asc""")
        self.VAR_SCP = self.cursor.fetchone()
        if self.VAR_SCP:
            self.VAR_SCP = self.VAR_SCP[0]
        else:
            # @TODO - change to something that is fixed and corresponds to the
            #         default values after launching the debugged version!!!
            self.VAR_SCP = 20
        self.VAR_SIG = var_sig

    def __del__(self):
        # @TODO - possibly add some close-connnection routines, etc.
        pass

    def __len__(self):
        # size in unique concepts
        self.cursor.execute("""SELECT DISTINCT identifier FROM grounding""")
        return self.cursor.rowcount

    def size(self,in_terms=False):
        if not in_terms:
            # size in unique concepts
            return self.__len__()
        else:
            self.cursor.execute("""SELECT DISTINCT lemma FROM grounding""")
            return self.cursor.rowcount

    def __mapTag(self,tag):
        if not tag:
            tag = 'NN'
        tag_map = {'N':'n', 'J':'a', 'V':'v'}
        stem_tag = None
        # mapping Brown tags to the WordNet tags accepted by morphy
        if tag[0].upper() in tag_map.keys():
            stem_tag = tag_map[tag[0].upper()]
        return stem_tag

    def add(self,term,tag=None,force_id=None,scope=None):
        if not scope:
            scope = self.DEF_SCP
        if scope == self.REL_SCP:
            tag = 'VB'
        else:
            tag = 'NN'
        t = lemmatise(term,self.__mapTag(tag))
        if len(t) > 500:
            t = t[:500]
        identifier = force_id
        if identifier == None or \
        (identifier != 0 and identifier < self.next_id):
            #print 'DEBUG - Grounding.add() - generating new ID'
            is_new = False
            while not is_new:
                identifier = self.next_id
                self.next_id += 1
                self.cursor.execute("""SELECT * FROM grounding WHERE 
                                       identifier=%s""", (identifier,))
                if self.cursor.rowcount < 1:
                    is_new = True
        try:
            self.cursor.execute("""SELECT identifier, scope FROM grounding 
                                   WHERE lemma=%s AND certainty=1.0""", (t,))
        except UnicodeEncodeError:
            self.cursor.execute("""SELECT identifier, scope FROM grounding 
                                   WHERE lemma=%s AND certainty=1.0""", (`t`,))
        if self.cursor.rowcount < 1:
            # adding the new stuff if it is really new
            #print 'DEBUG - Grounding.add() - adding new'
            try:
                self.cursor.execute("""INSERT INTO grounding 
                                       (lemma,identifier,scope,certainty) VALUE 
                                       (%s,%s,%s,%s)""", \
                                       (t,identifier,scope,1.0))
            except UnicodeEncodeError:
                self.cursor.execute("""INSERT INTO grounding 
                                       (lemma,identifier,scope,certainty) VALUE 
                                       (%s,%s,%s,%s)""", \
                                       (`t`,identifier,scope,1.0))
        else:
            # assuming addition of another identifier to an existing term
            if scope not in map(lambda x: x[1], self.cursor.fetchall()):
                #print 'DEBUG - Grounding.add() - adding to existing'
                try:
                    self.cursor.execute("""INSERT INTO grounding 
                                           (lemma,identifier,scope,certainty) 
                                           VALUE (%s,%s,%s,%s)""",\
                                           (t,identifier,scope,1.0))
                except UnicodeEncodeError:
                    self.cursor.execute("""INSERT INTO grounding 
                                           (lemma,identifier,scope,certainty) 
                                           VALUE (%s,%s,%s,%s)""",\
                                           (`t`,identifier,scope,1.0))
        return identifier

    def addSyn(self,synonym,term,tag=None,d=0.75,scope=None):
        if not scope:
            scope = self.DEF_SCP
        if scope == self.REL_SCP:
            tag = 'VB'
        else:
            tag = 'NN'
        t = lemmatise(term,self.__mapTag(tag))
        s = lemmatise(synonym,self.__mapTag(tag))
        if len(t) > 500:
            t = t[:500]
        if len(s) > 500:
            s = s[:500]
        try:
            self.cursor.execute("""SELECT identifier FROM grounding WHERE 
                                   lemma=%s AND scope=%s AND certainty=1.0""",\
                                   (t,scope))
        except UnicodeEncodeError:
            self.cursor.execute("""SELECT identifier FROM grounding WHERE 
                                   lemma=%s AND scope=%s AND certainty=1.0""",\
                                   (`t`,scope))
        identifier = self.cursor.fetchone()
        if identifier:
            identifier = identifier[0]
            if d == 1.0:
                # ensuring that there is only one preferred term
                self.cursor.execute("""SELECT certainty FROM grounding WHERE 
                                       identifier=%s AND scope=%s 
                                       ORDER BY certainty desc""", \
                                       (identifier,scope))
                nd = 0.75
                if self.cursor.rowcount > 1:
                    degrees = map(lambda x: x[0], self.cursor.fetchmany(2))
                    nd = 0.5*(degrees[0]+degrees[1])
                self.cursor.execute("""DELETE FROM grounding WHERE
                                       identifier=%s AND scope=%s AND 
                                       certainty=1.0""", (identifier,scope))
                try:
                    self.cursor.execute("""INSERT INTO grounding 
                                           (lemma,identifier,scope,certainty) 
                                           VALUE (%s,%s,%s,%s)""", \
                                           (t,identifier,scope,nd))
                except UnicodeEncodeError:
                    self.cursor.execute("""INSERT INTO grounding 
                                           (lemma,identifier,scope,certainty) 
                                           VALUE (%s,%s,%s,%s)""", \
                                           (`t`,identifier,scope,nd))
            try:
                self.cursor.execute("""INSERT INTO grounding 
                                       (lemma,identifier,scope,certainty)
                                       VALUE (%s,%s,%s,%s)""", \
                                       (s,identifier,scope,d))
            except UnicodeEncodeError:
                self.cursor.execute("""INSERT INTO grounding 
                                       (lemma,identifier,scope,certainty)
                                       VALUE (%s,%s,%s,%s)""", \
                                       (`s`,identifier,scope,d))

    def __getitem__(self,key):
        # shortcut to the default context and tag key retrieval
        return self.get(key)

    def get(self,key,tag=None,scope=None):
        if not scope:
            scope = self.DEF_SCP
        if isinstance(key,int) or isinstance(key,long):
            self.cursor.execute("""SELECT lemma FROM grounding WHERE 
                                   identifier=%s AND scope=%s AND 
                                   certainty=1.0""", (key,scope))
            lemma = self.cursor.fetchone()
            if lemma:
                return lemma[0]
            else:
                #sys.stderr.write('Grounding - no entry found for: '+`key`+'\n')
                return None
                #raise KeyError('No lemma in the grounding for: '+`key`)
        elif isinstance(key,str) or isinstance(key,unicode):
            # automatically adjust the tag
            if scope == self.REL_SCP:
                tag = 'VB'
            else:
                tag = 'NN'
            t = lemmatise(key,self.__mapTag(tag))
            #print 'DEBUG -- the key term:', `t`
            try:
                self.cursor.execute("""SELECT DISTINCT identifier FROM 
                                       grounding WHERE lemma=%s AND 
                                       scope=%s""", (t,scope))
            except UnicodeEncodeError:
                self.cursor.execute("""SELECT DISTINCT identifier FROM 
                                       grounding WHERE lemma=%s AND 
                                       scope=%s""", (`t`,scope))
            if self.cursor.rowcount > 1:
                #raise KeyError('Ambiguous entries for: '+`(t,scope)`)
                # trying to retrieve the master one if there is a scope clash
                # @TODO - still, might be a possible source of problems!
                try:
                    self.cursor.execute("""SELECT DISTINCT identifier FROM 
                                           grounding WHERE lemma=%s AND 
                                           scope=%s AND certainty=1""", \
                                           (t,scope))
                except UnicodeEncodeError:
                    self.cursor.execute("""SELECT DISTINCT identifier FROM 
                                           grounding WHERE lemma=%s AND 
                                           scope=%s AND certainty=1""", \
                                           (`t`,scope))
            identifier = self.cursor.fetchone()
            if identifier:
                return identifier[0]
            else:
                #sys.stderr.write('Grounding - no entry found for: '+`key`+'\n')
                return None
                #raise KeyError('No identifier in the grounding for: '+`key`)
        else:
            sys.stderr.write('Grounding - no entry found for: '+`key`+'\n')
            return None
            #raise KeyError('No such item in the grounding: '+`key`)

    def __delitem__(self,key,tag=None):
        if isinstance(key,int):
            self.cursor.execute("""DELETE FROM grounding WHERE
                                   identifier=%s""", (key,))
        elif isinstance(key,str) or isinstance(key,unicode):
            t = lemmatise(key,self.__mapTag(tag))
            try:
                self.cursor.execute("""DELETE FROM grounding WHERE
                                       lemma=%s""", (t,))
            except UnicodeEncodeError:
                self.cursor.execute("""DELETE FROM grounding WHERE
                                       lemma=%s""", (`t`,))

    def contains(self,key,tag=None):
        if isinstance(key,int):
            self.cursor.execute("""SELECT DISTINCT lemma FROM grounding WHERE
                                   identifier=%s""", (key,))
        elif isinstance(key,str) or isinstance(key,unicode):
            t = lemmatise(key,self.__mapTag(tag))
            try:
                self.cursor.execute("""SELECT DISTINCT identifier FROM 
                                       grounding WHERE lemma=%s""", (t,))
            except UnicodeEncodeError:
                self.cursor.execute("""SELECT DISTINCT identifier FROM 
                                       grounding WHERE lemma=%s""", (`t`,))
        return self.cursor.rowcount > 0

    def has_key(self,key):
        if isinstance(key,int):
            return self.contains(key)
        return False

    def isVar(self,key):
        if not key:
            return False
        if isinstance(key,int) or isinstance(key,long) or \
        isinstance(key,str) or isinstance(key,unicode):
            term = key
            if isinstance(key,int) or isinstance(key,long):
                self.cursor.execute("""SELECT DISTINCT lemma FROM grounding 
                                       WHERE identifier=%s""", (key,))
                term = self.cursor.fetchone()
                if term:
                    term = term[0]
            return len(term.strip()) and term.strip()[0] == self.VAR_SIG
        return False

    def getSynonyms(self,key,scope=None):
        if not scope:
            scope = self.DEF_SCP
        if not (isinstance(key,int) or isinstance(key,long) or \
        isinstance(key,str) or isinstance(key,unicode)):
            return []
        identifier = key
        if isinstance(key,str) or isinstance(key,unicode):
            identifier = self.get(key,scope=scope)
        self.cursor.execute("""SELECT DISTINCT lemma, certainty FROM grounding 
                               WHERE identifier=%s ORDER BY certainty desc""", 
                               (identifier,))
        return self.cursor.fetchall()

    def getSenses(self,key):
        if not (isinstance(key,str) or isinstance(key,unicode)):
            return []
        l = []
        for tag in ['NN','JJ','VB']:
            # trying out all possible legal lemmatisations
            t = lemmatise(key,self.__mapTag(tag))
            try:
                self.cursor.execute("""SELECT DISTINCT identifier, scope FROM 
                                       grounding WHERE lemma=%s ORDER BY 
                                       scope desc""", (t,))
            except UnicodeEncodeError:
                self.cursor.execute("""SELECT DISTINCT identifier, scope FROM 
                                       grounding WHERE lemma=%s ORDER BY 
                                       scope desc""", (`t`,))
            l += self.cursor.fetchall()
        return l

class Entities:

    def __init__(self,cfg,trace=False):
        self.trace = trace
        self.cfg = cfg
        g = Grounding(self.cfg)
        #if not self.cfg:
        #    cfg = parseCFG(os.path.join('..','resources','eureeka.cfg'))
        # connecting to the specified database
        self.db = MySQLdb.connect(host=cfg['DB_HOST'],user=cfg['DB_USER'],\
        passwd=cfg['DB_PASS'],db=cfg['DB_NAME'])
        self.cursor = self.db.cursor()
        # generating the key set
        #self.cursor.execute("""SELECT DISTINCT subject FROM entities""")
        #self.key_set = Set(map(lambda x: x[0], self.cursor.fetchall()))
        # resource to relevance mapping
        self.res2rel, self.defrel = {}, float(cfg['DEF_REL'])
        if cfg.has_key('DC_REL') and os.path.isfile(cfg['DC_REL']):
            f = open(cfg['DC_REL'],'r')
            for line in f:
                ln = line.split('#')[0].strip()
                if ln and len(ln.split('\t')) >= 2:
                    prov_id = g.get(ln.split('\t')[0].strip())
                    if not prov_id:
                        prov_id = g.add(g.get(ln.split('\t')[0].strip()))
                    self.res2rel[prov_id] = float(ln.split('\t')[1].strip())
            f.close()

    def __del__(self):
        self.db.commit()

    def __len__(self):
        self.cursor.execute("""SELECT DISTINCT subject FROM entities""")
        return self.cursor.rowcount

    def __setitem__(self,key,value):
        """
        DEPRECATED - does not correctly handle relation identifiers!
        Use only addRelation() for correct maintenance!
        """

        sl = []
        if key == value.getID():
            s = key
            #self.key_set.add(s)
            # removing all potential statements corresponding to value
            self.cursor.execute("""SELECT id FROM entities 
                                   WHERE subject = %s""", (s,))
            for x in self.cursor.fetchall():
                self.cursor.execute("""DELETE * FROM entities 
                                       WHERE subject=%s""", (x[0],))
            self.cursor.execute("""DELETE * FROM entities WHERE subject=%s""",\
                                (s,))
            for p,o in value.getIndices():
                # @TODO - check whether Python None -> SQL NULL
                sl.append((s,p,o,None,value.getDegree(p,o)))
            self.cursor.executemany("""INSERT INTO entities (subject,predicate,
                                       object,provenance,certainty) VALUES 
                                       (%s,%s,%s,%s,%s)""",sl)

    def __delitem__(self,key):
        #self.key_set.discard(key)
        self.cursor.execute("""DELETE FROM entities WHERE subject=%s""",(key,))

    def __getitem__(self,s):
        #if not s in self.key_set:
        #    raise KeyError
        self.cursor.execute("""SELECT predicate, object, provenance, certainty 
                               FROM entities WHERE subject=%s""", (s,))
        po2pd = {}
        e = Entity(s)
        for p, o, prov, d in self.cursor.fetchall():
            if not po2pd.has_key((p,o)):
                po2pd[(p,o)] = []
            po2pd[(p,o)].append((prov,d))
        for p, o in po2pd:
            sum, defcount = 0.0, 0
            for prov, d in po2pd[(p,o)]:
                rel = self.defrel
                if self.res2rel.has_key(prov):
                    rel = self.res2rel[prov]
                else:
                    defcount += 1
                sum += rel*d
            k = reduce(lambda x,y: x+y, self.res2rel.values(), 0.0) + \
            defcount*self.defrel
            e.setDegree(int(p),int(o),sum/float(k))
        return e

    def get(self,s,prov=0):
        """
        Retrieves an entity with the given provenance only, resulting in
        plain __get__ if there are no respective statements.
        """

        #if not s in self.key_set:
        #    raise KeyError
        self.cursor.execute("""SELECT predicate, object, certainty 
                               FROM entities WHERE subject=%s AND
                               provenance=%s""", (s,prov))
        e = Entity(s)
        for p, o, d in self.cursor.fetchall():
            e.setDegree(p,o,d)
        if len(e):
            return e
        else:
            return self.__getitem__(s)

    def checkConnection(self):
        """
        Checks whether the connection is alive, refreshes it if not.
        """

        try:
            self.cursor.execute("""SELECT id FROM entities WHERE subj=1""")
            res = self.cursor.fetchone()
            self.cursor.nextset()
        except MySQLdb.OperationalError:
            del self.db
            del self.cursor
            #del self.key_set
            # run garbage collection - this way it is ensured it will be run
            # only once in 8 hours at most
            gc.collect()
            self.db = MySQLdb.connect(host=self.cfg['DB_HOST'],user=self.cfg['DB_USER'],\
            passwd=self.cfg['DB_PASS'],db=self.cfg['DB_NAME'])
            self.cursor = self.db.cursor()
            # generating the key set
            #self.cursor.execute("""SELECT DISTINCT subject FROM entities""")
            #self.key_set = Set(map(lambda x: x[0], self.cursor.fetchall()))

    def keys(self):
        self.cursor.execute("""SELECT DISTINCT subject FROM entities""")
        return map(lambda x: x[0], self.cursor.fetchall())

    def values(self):
        return map(lambda x: self.__getitem__(x), self.keys())

    def has_key(self,key):
        self.cursor.execute("""SELECT * FROM entities WHERE subject=%s""", \
        (key,))
        return self.cursor.rowcount > 0

    def update(self,ent):
        """
        Updates the storage with the input entity. If not defined otherwise, 
        provenance identifier is set to 0 in order to indicate inferred 
        statement (missing statements are assumed to be inferred by default).

        @TODO - reflect the 0 value for inferred provenance elsewhere!!!
        """

        s = ent.getID()
        #if s not in self.key_set:
        #    sys.stderr.write('Warning: trying to update a missing entity!')
        #else:
        stored, updates = self.__getitem__(s), []
        for p, o in ent.getIndices():
            if ent.getDegree(p,o) != stored.getDegree(p,o):
                updates.append((0,s,p,o,0,ent.getDegree(p,o)))
                # deleting the possibly conflicting stuff before
                self.cursor.execute("""DELETE FROM entities WHERE 
                subject=%s AND predicate=%s AND object=%s AND 
                provenance=0""", (s,p,o))
        # filtering to non-default types only
        # @TODO - possibly reconsider (some exceptions might be useful for
        #         relations...)
        updates = filter(lambda x: not (x[2] in [3,4] and x[3] <= 22),\
        updates)
        self.cursor.executemany("""INSERT INTO entities (id,subject,
                                   predicate,object,provenance,certainty) 
                                   VALUES (%s,%s,%s,%s,%s,%s)""", updates)

    def __cleanUp(self,tuples):
        dct = {}
        for t in tuples:
            if not dct.has_key((t[1],t[2],t[3],t[4])):
                dct[(t[1],t[2],t[3],t[4])] = {'id':t[0],'cert':[t[5]]}
            else:
                dct[(t[1],t[2],t[3],t[4])]['cert'].append(t[5])
        l = []
        for s, p, o, prov in dct:
            cert = (1.0/len(dct[(s,p,o,prov)]['cert']))*reduce(lambda x,y: x+y,\
            dct[(s,p,o,prov)]['cert'],0)
            self.cursor.execute("""SELECT id, certainty FROM entities WHERE
                                   subject=%s AND predicate=%s AND object=%s
                                   AND provenance=%s""", (s,p,o,prov))
            if self.cursor.rowcount < 1:
                # append only if not already present in the DB
                l.append((dct[(s,p,o,prov)]['id'],s,p,o,prov,cert))
        return l

    def addRelations(self,relations,g,limit=50000):
        """
        Adds a list of relations into the store, making use of SQL bulkinsert
        to optimise large batch additions
        """

        tuples = []
        for r in relations:
            tuples += self.addRelation(r,g,insert=False)
            if len(tuples) >= limit:
                self.cursor.executemany("""INSERT INTO entities 
                                           (id,subject,predicate,object,
                                           provenance,certainty) VALUES 
                                           (%s,%s, %s, %s, %s,%s)""", \
                                           self.__cleanUp(tuples))
                tuples = []
        self.cursor.executemany("""INSERT INTO entities 
                                   (id,subject,predicate,object,provenance,
                                    certainty) VALUES 
                                   (%s,%s, %s, %s, %s,%s)""", \
                                   self.__cleanUp(tuples))

    def addRelation(self,r,g,insert=True):
        """
        Adds a relation into the store. 
        """
        
        tuples = []
        def_dct = {} # default statements lexicon
        i = r.getHashKey(g)
        # getting the subject, predicate, object entity IDs
        subj_scope, obj_scope = g.DEF_SCP, g.DEF_SCP
        if r.isSubjRel():
            subj_scope = g.REL_SCP
        if r.isObjRel():
            obj_scope = g.REL_SCP
        s = g.get(r.getSubject(),scope=subj_scope)
        if not s and r.getSubject() == 'inferred provenance':
            s = 0
            g.add(r.getSubject(),force_id=0,scope=g.DEF_SCP)
        if s == None:
            # trying the relation sense
            s = g.get(r.getSubject(),scope=g.REL_SCP)
        if s == None:
            # adding new if not present
            s = g.add(r.getSubject(),scope=subj_scope)
        p = g.get(r.getPredicate(),scope=g.REL_SCP)
        if p == None:
            p = g.add(r.getPredicate(),scope=g.REL_SCP)
        o = g.get(r.getObject(),scope=obj_scope)
        if o == None:
            # trying the relation sense
            o = g.get(r.getObject(),scope=g.REL_SCP)
        if o == None:
            # adding new if not present
            o = g.add(r.getObject(),scope=obj_scope)
        def_dct[s] = g.DEF_SCP
        def_dct[p] = g.REL_SCP
        def_dct[o] = g.DEF_SCP
        # getting provenance title and identifier entity IDs
        #self.key_set |= Set([s,p,o])
        for prov_id in r.provenance:
            prov_tit = r.getProvenanceTitle(prov_id)
            prov = g.get(prov_id,scope=g.DEF_SCP)
            if not prov:
                prov = g.add(prov_id,scope=g.DEF_SCP)
            tit = g.get(prov_tit,scope=g.DEF_SCP)
            if not tit:
                tit = g.add(prov_tit,scope=g.DEF_SCP)
            d = r.getCertainty()
            i = r.getHashKey(g,prov_tit)
            try:
                if insert:
                    self.cursor.execute("""INSERT INTO entities 
                                       (id,subject,predicate,object,provenance,
                                       certainty) VALUES 
                                       (%s,%s,%s,%s,%s,%s)""",(i,s,p,o,prov,d))
                else:
                    tuples.append((i,s,p,o,prov,d))
                # inserting the default object statement with top-type, to
                # ensure it's present in the KB
                if not self.has_key(o):
                    # @TODO - consider doing this in a batch rather than for
                    #         each (consumes space and involves too many
                    #         possibly useless type of assertions)
                    if insert:
                        self.cursor.execute("""INSERT INTO entities 
                                               (id,subject,predicate,object,
                                               provenance,certainty) VALUES 
                                               (%s,%s,%s,%s,%s,%s)""",\
                                               (0,o,3,2,prov,1.0))
                    else:
                        tuples.append((0,o,3,2,prov,1.0))
                def_dct, tpl = \
                self.__insertContexts(r.getContextTuples(),i,prov,d,g,def_dct,\
                insert=insert)
                tuples += tpl
            except Exception:
                sys.stderr.write('Warning (Entities.addRelation()) duplicate:'+\
                                  '\n'+`(i,s,p,o,prov,d)`+'\n')
        tuples += self.__insertProvenance(r.provenance,g,insert=insert)
        tuples += self.__insertDefaults(def_dct,g,insert=insert)
        return tuples

    def __insertContexts(self,contexts,i,prov,d,g,def_dct,insert=True):
        l = []
        for pw, ow in contexts:
            p = g.get(pw,scope=g.REL_SCP)
            if not p:
                p = g.add(pw,scope=g.REL_SCP)
            o = g.get(ow,scope=g.DEF_SCP)
            if not o:
                o = g.add(ow,scope=g.DEF_SCP)
            l.append((0,i,p,o,prov,d))
            def_dct[p] = g.REL_SCP
            def_dct[o] = g.DEF_SCP
        # note - the identifier is set to 0 by default for contexts
        if insert:
            self.cursor.executemany("""INSERT INTO entities (id,subject,
                                       predicate,object,provenance,certainty) 
                                       VALUES (%s,%s,%s,%s,%s,%s)""", l)
        return def_dct, l

    def __insertProvenance(self,provenance,g,insert=True):
        tuples = []
        tp = g.get('type of',scope=g.REL_SCP)
        pr = g.get('provenance',scope=g.DEF_SCP)
        ht = g.get('title',scope=g.REL_SCP)
        dp = g.get(hashlib.sha1('default provenance').hexdigest(),\
        scope=g.DEF_SCP)
        if not dp:
            dp = g.add(hashlib.sha1('default provenance').hexdigest(),\
            scope=g.DEF_SCP)
        for prov_id in provenance:
            prov_tit = provenance[prov_id]
            prov = g.get(prov_id,scope=g.DEF_SCP)
            if not prov:
                prov = g.add(prov_id,scope=g.DEF_SCP)
            tit = g.get(prov_tit,scope=g.DEF_SCP)
            if not tit:
                tit = g.add(prov_tit,scope=g.DEF_SCP)
            if not self.has_key(prov):
                l = [(0,prov,tp,pr,dp,1.0), (0,prov,ht,tit,dp,1.0), \
                (0,tit,tp,g.DEF_SCP,dp,1.0)]
                # note - the identifier is set to 0 by default for provenance
                if insert:
                    self.cursor.executemany("""INSERT INTO entities 
                                               (id,subject,predicate,object,
                                               provenance,certainty) 
                                               VALUES (%s,%s,%s,%s,%s,%s)""",l)
                else:
                    tuples += l
                #self.key_set.add(prov)
                #self.key_set.add(tit)
        return tuples

    def __insertDefaults(self,def_dct,g,insert=True):
        tuples = []
        tp = g.get('type of',scope=g.REL_SCP)
        dp = g.get('default provenance',scope=g.DEF_SCP)
        for e in def_dct:
            if not self.has_key(e):
                super_type = def_dct[e]
                if insert:
                    self.cursor.execute("""INSERT INTO entities 
                                           (id,subject,predicate,object,
                                           provenance,certainty) VALUES 
                                           (0,%s, %s, %s, %s, 1.0)""", \
                                           (e,tp,super_type,dp))
                else:
                    tuples.append((0,e,tp,super_type,dp,1.0))
                #self.key_set.add(e)
        return tuples

    def getRelations(self,subj_ids,sim=1.0,mxsz=0,contexts={},g=None,ftlr={},\
    prov=-1):
        """
        Gets Relation objects corresponding to the particular index.

        ftlr is a dictionary supposed to restrict the relations only to 
        particular subject,object pairs (used when generating answers to 
        single-statement queries with variable predicate), supposed to be in
        the form of {s_1:(o_1,d_1), s_2:(o_2,d_2), ... , s_n:(o_n,d_n)}.
        """

        if not isinstance(g,Grounding):
            g = Grounding(self.cfg)
        results = []
        # sorting the subjects first
        if not len(subj_ids):
            return []
        cond = 'WHERE ' + reduce(lambda x,y: x+' OR '+y, \
        ['(entity=%s)']*len(subj_ids))
        #print 'DEBUG/getRelations() - getting sorted entity/score tuples...'
        self.cursor.execute('SELECT entity, 0.5*(hub+auth) FROM scores '+cond+\
        ' ORDER BY 0.5*(hub+auth) desc',subj_ids)
        esc = self.cursor.fetchall()
        # generating the most relevant statements from the most relevant
        # concepts first
        score2statements = {}
        ht = g.get('title',scope=g.REL_SCP)
        #ht = g.get('has title',scope=g.REL_SCP)
        #print 'DEBUG/getRelations() - generating score2statements...'
        for s, sc in esc:
            self.cursor.execute("""SELECT id, predicate, object, provenance, 
                                   certainty FROM entities 
                                   WHERE subject=%s""", (s,))
            ipopc = self.cursor.fetchall()
            if ftlr.has_key(s):
                # limiting only to certain objects
                ipopc = filter(lambda x: x[2] == ftlr[s][0] and \
                x[4]*ftlr[s][1] > 0, ipopc)
            if prov != -1:
                # limiting only to certain provenance
                ipopc = filter(lambda x: x[3] == prov, ipopc)
            for i, p, o, prov, d in ipopc:
                # getting the statement score
                self.cursor.execute("""SELECT MAX(0.5*(hub+auth)) FROM scores
                                       WHERE entity=%s OR entity=%s""", \
                                       (s,o))
                score = self.cursor.fetchone()
                if score:
                    score = score[0]
                else:
                    score = 0.0
                if not score2statements.has_key(score):
                    score2statements[score] = {}
                if not score2statements[score].has_key((i,s,p,o)):
                    score2statements[score][(i,s,p,o)] = []
                score2statements[score][(i,s,p,o)].append((prov,d))
        # processing the statements from the topmost score
        l = score2statements.keys()
        l.sort()
        l.reverse()
        statements = []
        #print 'DEBUG/getRelations() - computing aggregated certainties...'
        for score in l:
            for i, s, p, o in score2statements[score]:
                if len(contexts):
                    self.cursor.execute("""SELECT predicate, object FROM 
                                           entities WHERE subject=%s)""", (i,))
                    if not set(contexts.items())<=set(self.cursor.fetchall()):
                        continue # not matching contexts
                # computing the aggregated certainty
                sum, defcount = 0.0, 0
                for prov, d in score2statements[score][(i,s,p,o)]:
                    rel = self.defrel
                    if self.res2rel.has_key(prov):
                        rel = self.res2rel[prov]
                    else:
                        defcount += 1
                    sum += rel*d
                k = reduce(lambda x,y: x+y, self.res2rel.values(), 0.0) + \
                defcount*self.defrel
                statements.append({'SCORE':score,'ISPO':(i,s,p,o), \
                'CERTAINTY':sum/float(k), 'PROVENANCE':map(lambda x:x[0], \
                score2statements[score][(i,s,p,o)])})
        #print 'DEBUG/getRelations() - generating relations...'
        for stmt in statements:
            i, s, p, o = stmt['ISPO']
            s_term = g.get(s,scope=g.DEF_SCP)
            p_term = g.get(p,scope=g.REL_SCP)
            o_term = g.get(o,scope=g.DEF_SCP)
            if not s_term or not p_term or not o_term:
                continue
            r = Relation(s_term,p_term,o_term,cert=sim*stmt['CERTAINTY'])
            for prov in stmt['PROVENANCE']:
                #print 'DEBUG -- prov. identifier:', `prov`
                #print 'DEBUG -- prov. term      :', g.get(prov)
                self.cursor.execute("""SELECT object FROM entities WHERE 
                                       subject=%s AND predicate=%s""", \
                                       (prov,ht))
                prov_tit = self.cursor.fetchone()
                if prov_tit:
                    prov_tit = prov_tit[0]
                    r.setProvenance(g.get(prov_tit))
                else:
                    # @TODO - uncomment this for later use
                    #try:
                    #    sys.stderr.write('Warning: provenance title not found!\n')
                    #except IOError:
                    #    print 'IOError when trying to write to stderr...'
                    #    print '  the original message:', \
                    #    'Warning: provenance title not found!'
                    #    pass
                    continue
            self.cursor.execute("""SELECT predicate, object FROM entities 
                                   WHERE subject=%s""", (i,))
            for ctx_pred, ctx in self.cursor.fetchall():
                r.setContext(g.get(ctx_pred,scope=g.REL_SCP),g.get(ctx))
            # setting the score property (to be used later for ranking of the
            # statements)
            r.setScore(stmt['SCORE'])
            results.append(r)
            if mxsz and len(results) > mxsz:
                break
        return results

    def updateScores(self,k=10,minf=25,bulk_limit=100000):
        """
        Updates scores in the score table (first deletes everything from
        it, then fills it in again).
        """

        self.cursor.execute("""DELETE FROM scores""")
        p2f = {}
        self.cursor.execute("""SELECT DISTINCT predicate FROM entities""")
        for p in map(lambda x: x[0], self.cursor.fetchall()):
            self.cursor.execute("""SELECT subject, object FROM entities WHERE 
                                   predicate=%s""",(p,))
            p2f[p] = len(self.cursor.fetchall())
        auth, hub = {}, {}
        #self.cursor.execute("""SELECT DISTINCT object FROM entities""")
        #allc = self.key_set | Set(map(lambda x: x[0], self.cursor.fetchall()))
        allc = self.keys()
        for key in allc:
            auth[key], hub[key] = 1.0, 1.0
        for i in range(k):
            for c in allc:
                # generating the incoming neighbours
                self.cursor.execute("""SELECT DISTINCT subject, predicate, 
                                       certainty FROM entities WHERE 
                                       object=%s""", (c,))
                # updating auth[c] using the incoming neighbours
                for inc, p, d in self.cursor.fetchall():
                    if p2f.has_key(p) and p2f[p] >= minf:
                        # consider only predicates with certain freq. and weigh
                        # the hub measure by inversely proportional number
                        # @TODO - the degree values are taken from all possibly
                        #         non-aggregated statements - is this OK?!?
                        auth[c] += \
                        (1.0/log(exp(1)+p2f[p]-minf))*hub[inc]*fabs(d)
            for c in allc:
                # generating the outgoing neighbours
                self.cursor.execute("""SELECT DISTINCT object, predicate,
                                        certainty FROM entities WHERE 
                                        subject=%s""", (c,))
                # updating hub[c] using the outgoing neighbours
                for out, p, d in self.cursor.fetchall():
                    if p2f.has_key(p) and p2f[p] >= minf:
                        # consider only predicates with certain freq. and weigh
                        # the auth measure by inversely proportional number
                        # @TODO - the degree values are taken from all possibly
                        #         non-aggregated statements - is this OK?!?
                        hub[c] += \
                        (1.0/log(exp(1)+p2f[p]-minf))*auth[out]*fabs(d)
            # normalise the values by maximum
            auth_norm = max(auth.values())
            hub_norm = max(hub.values())
            for c in allc:
                auth[c] /= auth_norm
                hub[c] /= hub_norm
        # storing the score values
        l, sum = [], 0
        for c in allc:
            l.append((c,auth[c],hub[c]))
            if len(l) >= bulk_limit:
                sum += len(l)
                self.cursor.executemany("""INSERT INTO scores 
                                            (entity,hub,auth) 
                                            VALUES (%s, %s, %s)""", l)
                l = []
        self.cursor.executemany("""INSERT INTO scores 
                                    (entity,hub,auth) 
                                    VALUES (%s, %s, %s)""", l)

    def query(self,qs,contexts={},partial=True,idx_only=True,omit=[],mxid=0,\
    mxsz=0):
        """
        Evaluates generic query according to qs, which is a sequence of 
        (s,p,o,d) statements, where d is a degree used for degree-sign checks,
        and s,p,o is in the following acceptable forms (0,int,int), 
        (int,int,0), (0,int,None), (None,int,0), where 0 indicates what 
        one queries for and the int values represent the respective conditions.

        omit specifies a list of concept IDs that should not be included in 
        the result (i.e., the concept that served for the input conditions 
        construction)
        """

        qs2ans = {}
        for qc in qs:
            if qc[0] == 0:
                # asking for a subject
                if qc[2]:
                    # asking based on (predicate,object)
                    self.cursor.execute("""SELECT subject FROM entities WHERE 
                                           predicate=%s AND object=%s""", \
                                           (qc[1],qc[2]))
                    qs2ans[qc] = \
                    set(map(lambda x: x[0], self.cursor.fetchall()))
                else:
                    # asking based (predicate) only
                    self.cursor.execute("""SELECT subject FROM entities WHERE 
                                           predicate=%s""", (qc[1],))
                    qs2ans[qc] = \
                    set(map(lambda x: x[0], self.cursor.fetchall()))
            elif qc[2] == 0:
                # asking for an object
                if qc[0]:
                    # asking based on (subject,predicate)
                    self.cursor.execute("""SELECT object FROM entities WHERE 
                                           predicate=%s AND subject=%s""", \
                                           (qc[1],qc[0]))
                    qs2ans[qc] = \
                    set(map(lambda x: x[0], self.cursor.fetchall()))
                else:
                    # asking based (predicate) only
                    self.cursor.execute("""SELECT object FROM entities WHERE 
                                           predicate=%s""", (qc[1],))
                    qs2ans[qc] = \
                    set(map(lambda x: x[0], self.cursor.fetchall()))
        ans = []
        if reduce(lambda x, y: x and y, map(len,qs2ans.values())):
            ans = list(reduce(lambda x, y: x & y, qs2ans.values()))
        if partial and not len(ans):
            ans = list(reduce(lambda x, y: x | y, qs2ans.values()))
        if self.trace:
            print 'DEBUG -- storage.query() -- ans:', `ans`
        # sorting the answers accoeding to relevance
        rel2ans = {}
        for a in ans:
            self.cursor.execute("""SELECT 0.5*(hub+auth) FROM scores WHERE
                                   entity=%s""", (a,))
            rank = self.cursor.fetchone()
            if rank:
                rank = rank[0]
            else:
                rank = 0.0
            if rel2ans.has_key(rank):
                rel2ans[rank].append(a)
            else:
                rel2ans[rank] = [a]
        keys = rel2ans.keys()
        keys.sort()
        keys.reverse()
        res_ids = []
        for key in keys:
            res_ids += rel2ans[key]
        if mxid > 0:
            res_ids = res_ids[:mxid]
        # filtering the result according to contexts
        if len(contexts):
            items, tmp = contexts.items(), []
            for idx in res_ids:
                self.cursor.execute("""SELECT predicate, object FROM entities
                                       WHERE id = ANY (SELECT id FROM entities
                                       WHERE subject=%s)""", (idx,))
                if set(items) <= set(self.cursor.fetchall()):
                    tmp.append(idx)
            res_ids = tmp
        # returning the eventual result
        if idx_only:
            return res_ids
        else:
            return self.getRelations(res_ids,mxsz,contexts)

    def queryOld(self,qs,contexts={},partial=True,idx_only=True,omit=[],mxid=0,\
    mxsz=0):
        """
        Evaluates generic query according to qs, which is a sequence of 
        (s,p,o,d) statements, where d is a degree used for degree-sign checks,
        and s,p,o is in the following acceptable forms (0,int,int), 
        (int,int,0), (0,int,None), (None,int,0), where 0 indicates what 
        one queries for and the int values represent the respective conditions.

        omit specifies a list of concept IDs that should not be included in 
        the result (i.e., the concept that served for the input conditions 
        construction)

        @DEPRECATED - was not correctly implementing the entity retrieval 
                      (apart of being erroneous for certain multi-conditions)
                    - now replaced by new query() method with the same
                      interface and output
        """

        if not len(qs):
            return []
        # creating conjunctive conditions for getting subj and obj
        # - query subj/obj condition chunks and respective parameters
        sc_chunks, oc_chunks, sc_par, oc_par = [], [], [], []
        # process the condition tuples
        for s, p, o, d in qs:
            dstr = 't1.certainty>0'
            if d < 0.0:
                dstr = 't1.certainty<0'
            if s == 0:
                if o != None:
                    sc_chunks.append('(t1.predicate=%s AND t1.object=%s AND '+\
                    dstr+')')
                    sc_par += [p,o]
                else:
                    sc_chunks.append('(t1.predicate=%s AND '+dstr+')')
                    sc_par += [p]
            elif o == 0:
                if s != None:
                    oc_chunks.append('(t1.subject=%s AND t1.predicate=%s AND '+\
                    dstr+')')
                    oc_par += [s,p]
                else:
                    oc_chunks.append('(t1.predicate=%s AND '+dstr+')')
                    oc_par += [p]
        # asking the AND/OR queries according to the condition lists
        res_ids = []
        q1 = """SELECT DISTINCT t1.subject, 0.5*(t2.hub+t2.auth) FROM 
                entities t1, scores t2 WHERE t1.subject=t2.entity AND """
        q2 = """SELECT DISTINCT t1.object, 0.5*(t2.hub+t2.auth) FROM 
                entities t1, scores t2 WHERE t1.object=t2.entity AND """
        sf = ' ORDER BY 0.5*(t2.hub+t2.auth) desc'
        q3 = 'SELECT DISTINCT object FROM entities t1 WHERE '
        if len(sc_chunks) and len(oc_chunks):
            # nested query satisfying all subject and object conditions
            res_ids = self.__evalNestedQ(q1,q3,sf,sc_chunks,oc_chunks,mxid,\
            sc_par,oc_par,omit,partial)
        elif len(sc_chunks) and not len(oc_chunks):
            # query on subjects only
            res_ids = self.__evalSimpleQ(q1,sf,sc_chunks,mxid,sc_par,omit,\
            partial)
        elif not len(sc_chunks) and len(oc_chunks):
            # query on objects only
            res_ids = self.__evalSimpleQ(q2,sf,oc_chunks,mxid,oc_par,omit,\
            partial)
        # filtering the result according to contexts
        if len(contexts):
            items, tmp = contexts.items(), []
            for idx in res_ids:
                self.cursor.execute("""SELECT predicate, object FROM entities
                                       WHERE id = ANY (SELECT id FROM entities
                                       WHERE subject=%s)""", (idx,))
                if set(items) <= set(self.cursor.fetchall()):
                    tmp.append(idx)
            res_ids = tmp
        # returning the eventual result
        if idx_only:
            return res_ids
        else:
            return self.getRelations(res_ids,mxsz,contexts)

    def __evalNestedQ(self,q1,q3,sf,sc_chunks,oc_chunks,mxid,sc_par,oc_par,\
    omit,partial):
        res_ids = []
        cond1 = '('+reduce(lambda x,y: x+' AND '+y, sc_chunks)+')'
        cond2 = '('+reduce(lambda x,y: x+' AND '+y, oc_chunks)+')'
        self.cursor.execute(q1+cond1+' AND t1.subject = ANY ('+q3+cond2+')'+\
        sf, tuple(sc_par+oc_par))
        #print 'DEBUG - Entities.__evalNestedQ() - executed query:\n', \
        #q1+cond1+' AND t1.subject = ANY ('+q3+cond2+')'+sf
        #print 'DEBUG - Entities.__evalNestedQ() - query arguments:\n', \
        #`tuple(sc_par+oc_par)`
        if mxid > 0:
            res_ids = filter(lambda x: x not in omit,\
            map(lambda x: x[0], self.cursor.fetchmany(mxid)))
        else:
            res_ids = filter(lambda x: x not in omit,\
            map(lambda x: x[0], self.cursor.fetchall()))
        if not(len(res_ids)) and partial:
            cond1 = '('+reduce(lambda x,y: x+' OR '+y, sc_chunks)+')'
            cond2 = '('+reduce(lambda x,y: x+' OR '+y, oc_chunks)+')'
            self.cursor.execute(q1+cond1+' AND t1.subject = ANY ('+q3+cond2+\
            ')'+sf, tuple(sc_par+oc_par))
            if mxid > 0:
                res_ids = filter(lambda x: x not in omit,\
                map(lambda x: x[0], self.cursor.fetchmany(mxid)))
            else:
                res_ids = filter(lambda x: x not in omit,\
                map(lambda x: x[0], self.cursor.fetchall()))
        return res_ids

    def __evalSimpleQ(self,q,sf,chunks,mxid,par,omit,partial):
        res_ids = []
        cond = '('+reduce(lambda x,y: x+' AND '+y, chunks)+')'
        #print 'DEBUG - Entities.__evalNestedQ() - executed query:\n', \
        #q+cond+sf
        #print '  * parameters:', `tuple(par)`
        self.cursor.execute(q+cond+sf,tuple(par))
        if mxid > 0:
            res_ids = filter(lambda x: x not in omit,\
            map(lambda x: x[0], self.cursor.fetchmany(mxid)))
        else:
            res_ids = filter(lambda x: x not in omit,\
            map(lambda x: x[0], self.cursor.fetchall()))
        if not(len(res_ids)) and partial:
            cond = '('+reduce(lambda x,y: x+' OR '+y, chunks)+')'
            self.cursor.execute(q+cond+sf,tuple(par))
            if mxid > 0:
                res_ids = filter(lambda x: x not in omit,\
                map(lambda x: x[0], self.cursor.fetchmany(mxid)))
            else:
                res_ids = filter(lambda x: x not in omit,\
                map(lambda x: x[0], self.cursor.fetchall()))
        return res_ids

