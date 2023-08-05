"""
rules.py - a library containing implementation of EUREEKA rule objects and 
associated auxiliary functions

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

from eureeka.storage import Entity
from re import match
#from rdflib.Graph import ConjunctiveGraph as Graph
import rdflib, hashlib

# === constants BEGIN ===

# === constants END ===

# === exceptions BEGIN ===

class RuleParseError(Exception):
    def __init__(self,value="Syntax error in the rule persistence file."):
        self.parameter=value

    def __str__(self):
        return repr(self.parameter)

class RuleElementError(Exception):
    def __init__(self,value="Invalid rule element encountered."):
        self.parameter=value

    def __str__(self):
        return repr(self.parameter)

# === exceptions END ===

# === functions BEGIN ===

def loadRules(f,g,format='n3'):
    if format == 'n3':
        return loadRulesN3(f,g)
    elif format == 'text':
        return loadRulesTxt(f,g)
    else:
        return []

def triple2stmt(triple):
    s, p, o, d = None, None, None, 1.0
    if isinstance(triple[0],rdflib.URIRef):
        # definite statement element
        s = triple[0].split('#')[-1]
    elif isinstance(triple[0],unicode):
        # variable statement element
        s = '?' + triple[0]
    if isinstance(triple[1],rdflib.URIRef):
        # definite statement element
        p = triple[1].split('#')[-1]
    elif isinstance(triple[1],unicode):
        # variable statement element
        p = '?' + triple[1]
    if isinstance(triple[2],rdflib.URIRef):
        # definite statement element
        o = triple[2].split('#')[-1]
    elif isinstance(triple[2],unicode):
        # variable statement element
        o = '?' + triple[2]
    return (s,p,o,d)

def loadRulesN3(f,g):
    """
    Loads rules in the N3 format. Variables are expected to be encoded as 
    ?str, where str is any string. Definite entities are expected to be 
    encoded in the local namespace, i.e., as :entityName. 
    """

    impl_res = rdflib.URIRef('http://www.w3.org/2000/10/swap/log#implies')
    equiv_res = rdflib.URIRef('http://www.w3.org/2002/07/owl#sameAs')
    w, rls = 1.0, []
    grph = rdflib.ConjunctiveGraph()
    grph.parse(f, format="n3")
    for s, p, o in grph:
        if p == equiv_res and s.split('#') == 'relevance':
            w = float(o.toPython())
        elif p == impl_res:
            statements = {'A':[], 'C':[]}
            for ante in s:
                statements['A'].append(triple2stmt(ante))
            for conseq in o:
                statements['C'].append(triple2stmt(conseq))
            # textual representation of the rule
            q = reduce(lambda x,y: `x`+' AND '+`y`, statements['A'], '') + \
            '=>' + reduce(lambda x,y: `x`+' AND '+`y`, statements['C'], '')
            # generating the list of predicate variables
            rel_vars = filter(lambda x: x[0] == '?', map(lambda x: x[1], \
            statements['A']))
            # generating the rule ID
            i = hashlib.sha1(q).hexdigest()
            r = Rule(i)
            for ac in statements:
                for statement in statements[ac]:
                    if ac == 'A' and statement[0] in rel_vars:
                        r.addStm(statement,g,ac,var_rel=True)
                    else:
                        r.addStm(statement,g,ac,var_rel=False)
            rls.append(r)
    # setting the relevance weight for all rules
    for r in rls:
        r.setWeight(w)
    return rls
    
def loadRulesTxt(f,g,str_inp=False):
    """
    Loads rules from the file fn, supposed to be in the text format. 
    Uses the dictionary d to resolve and update IDs/terms.
    """

    rls, ff = [], None
    try:
        if not isinstance(f,str):
            return rls
        if str_inp:
            ff = [f]
        else:
            ff = open(f,'r')
    except IOError:
        return rls
    for line in ff:
        l = line.split('#')[0].strip()
        if not len(l):
            continue
        lspl = l.split('::')
        rule_id = lspl[0].strip()
        rsplit = lspl[-1].split('=>')
        if len(rsplit) != 3 or not \
        match('(?u)^[0-9\.]+$',rsplit[1].strip()):
            continue
        rule = Rule(rule_id)
        parts = {'A' : rsplit[0], 'C' : rsplit[2]}
        rule.setWeight(eval(rsplit[1].strip()))
        statements = {}
        for key in parts:
            part = parts[key]
            for stmt in part.split('AND'):
                # processing the statements
                spl = stmt.split(':')
                if len(spl) != 3 or \
                not reduce(lambda x,y: x and y,\
                map(lambda x: len(x.strip()),spl),True):
                    continue
                d = '1.0'
                tail = spl[2].split('>^')
                if len(tail) > 1 and \
                match('(?u)^[0-9\.]+$',tail[-1].strip()):
                    d = spl[2].split('>^')[-1].strip()
                p, o = spl[1].strip(), tail[0].strip()
                head = spl[0].split('<')
                pref, s = head[0].strip(), head[1].strip()
                if pref == 'NOT':
                    d = '-'+d
                if not statements.has_key(key):
                    statements[key] = []
                statements[key].append((s,p,o,eval(d)))
        for key in statements:
            rel_vars = filter(lambda x: x[0] == '?', map(lambda x: x[1], \
            statements[key]))
            for s, p, o, d in statements[key]:
                if s in rel_vars:
                    # adding a statement with subject supposed to be a relation
                    rule.addStm((s,p,o,d),g,key,var_rel=True)
                else:
                    # `normal' statement
                    rule.addStm((s,p,o,d),g,key,var_rel=False)
        rls.append(rule)
    #print "DEBUG/io.loadRules: rule: ", rule.getTxt(dct)
    if not str_inp and isinstance(ff,file):
        ff.close()
    return rls

# === functions END ===

# === classes BEGIN ===

class Vertex:
    def __init__(self,i):
        self.identifier = i
        # lists serving for the construction of SQL query conditions
        self.subj_of = [] # list of (p,o,d) values
        self.obj_of = []  # list of (s,p,d) values

    def getID(self):
        return self.identifier

    def getSuccessors(self,gr=[]):
        sl = map(lambda x: x[1], self.subj_of) + \
        map(lambda x: x[0], self.obj_of)
        if gr:
            return filter(lambda x: x in gr, sl)
        return sl

    def subjectOf(self,p,o,d):
        self.subj_of.append((p,o,d))

    def objectOf(self,s,p,d):
        self.obj_of.append((s,p,d))

class Rule:

    def __init__(self,i,ante=None,conseq=None,weight=1.0,optim=True):
        self.ruleid, self.weight, self.optim = i, weight, optim
        self.ante, self.conseq = ante, conseq
        if not self.ante: self.ante = {}
        if not self.conseq: self.conseq = {}

    def __cmpl(self,l1,l2):
        if len(l1) != len(l2):
            return False
        for x in l1:
            if not x in l2:
                return False
        for x in l2:
            if not x in l1:
                return False
        return True

    def __eq__(self,other):
        if isinstance(other,Rule):
            if self.weight != other.weight or \
            not self.__cmpl(self.ante,other.ante) or \
            not self.__cmpl(self.conseq,other.conseq):
                return False
            return True
        return NotImplemented
        
    def __ne__(self,other):
        result = self.__eq__(other)
        if result is NotImplemented:
            return result
        return not result

    def setID(self,i):
        self.ruleid = i

    def getID(self):
        return self.ruleid

    def setWeight(self,w):
        self.weight = w

    def getWeight(self):
        return self.weight

    def getAnteGraph(self,ground):
        """
        Returns graph corresponding to the antecedent and supporting the
        variable instantiation according to the graph traversal. 
        """

        g = {}
        for e in self.ante.values():
            s, v = e.getID(), None
            if ground.isVar(s):
                if not g.has_key(s):
                    v = Vertex(s)
                else:
                    v = g[s]
            for p, o in e.getIndices():
                if v:
                    v.subjectOf(p,o,e.getDegree(p,o))
                if ground.isVar(o):
                    if not g.has_key(o):
                        g[o] = Vertex(o)
                    g[o].objectOf(s,p,e.getDegree(p,o))
            if v and not g.has_key(s):
                g[s] = v
        return g

    def getConnection(self,v1,v2,direction='so'):
        """
        Attempts to return connection between two antecedent variables - the
        property and its degree. Default direction is so (from subject to 
        object), but the reverse os option is also possible. Returns empty
        tuple if no connection exists.
        """

        if direction == 'so':
            if not self.ante.has_key(v1):
                return ()
            for p,o in self.ante[v1].getIndices():
                if o == v2:
                    return (p,self.ante[v1].getDegree(p,o))
            return ()
        elif direction == 'os':
            if not self.ante.has_key(v2):
                return ()
            for p,o in self.ante[v2].getIndices():
                if o == v1:
                    return (p,self.ante[v2].getDegree(p,o))
            return ()
        else:
            return ()

    def setOptimisable(self,o):
        """
        Sets the optimisability flag. Essentially, this is true iff all
        antecedents contain a variable only in the subject position. 
        Variables in the optimisable rules can be unified with a knowledge 
        base content just by means of query answering (no need for antecedent
        graph traversal).
        """

        self.optim = o

    def isOptimisable(self):
        return self.optim

    def isPlain(self,lx):
        """
        Has no variable predicates? If a rule is not plain, it has to be 
        expanded before the actual evaluation.
        """

        if not len(filter(lx.isVar,reduce(lambda x,y: \
        x.getProperties()+y.getProperties(),self.ante.values()))):
            return True
        return False

    def addAntecedent(self,m):
        #m.setDegree(PRID['-TYPE-'],PRID['-CONCEPT-'])
        if m.getID() in self.ante:
            self.ante[m.getID()].change(m) 
        else:
            self.ante[m.getID()] = m

    def setAntecedent(self,m):
        if isinstance(m,Entity): 
            self.ante[m.getID()] = m

    def getAntecedents(self):
        return self.ante.values()
    
    def getAntecedent(self,i=None):
        try:
            if not i:
                return self.ante[self.ante.keys()[0]]
            else:
                return self.ante[i]
        except KeyError:
            return None

    def remAntecedent(self,i):
        try:
            del self.ante[i]
        except KeyError:
            pass

    def addConsequent(self,m):
        #m.setDegree(PRID['-TYPE-'],PRID['-CONCEPT-'])
        if m.getID() in self.conseq:
            self.conseq[m.getID()].change(m)
        else:
            self.conseq[m.getID()] = m

    def setConsequent(self,m):
        if isinstance(m,Entity): 
            self.conseq[m.getID()] = m

    def getConsequents(self):
        return self.conseq.values()

    def getConsequent(self,i=None):
        try:
            if not i: 
                return self.conseq[self.conseq.keys()[0]]
            else:
                return self.conseq[i]
        except KeyError:
            return None

    def remConsequent(self,i):
        try:
            del self.conseq[i]
        except KeyError:
            pass

    def getDet(self,i,lx):
        """
        Returns determiners, i.e., definite p, o tuples for antecedent i.
        """

        if not self.ante.has_key(i):
            return []
        dets = []
        for p, o in self.ante[i].getIndices():
            if not lx.isVar(o):
                dets.append((p,o))
        return dets

    def getNextPO(self,i,lx):
        """
        Return a tuple - a property leading to the object variable and the 
        respective variable ID.
        """

        if not self.ante.has_key(i):
            return None
        for p, o in self.ante[i].getIndices():
            if lx.isVar(o):
                return (p, o)
        return None

    def addStm(self,stm,g,ac='A',var_rel=False):
        print 'DEBUG - Rule.addStm() - statement:', `stm`
        s, p, o, d = stm[0], stm[1], stm[2], float(stm[3])
        id_s, id_p, id_o = None, None, None
        if isinstance(s,int) and isinstance(p,int) and \
        isinstance(o,int) and g.contains(s) and \
        g.contains(p) and g.contains(o):
            print 'DEBUG - Rule.addStm() - integer statement...'
            # just taking over if integer
            id_s, id_p, id_o = s, p, o
            if g.isVar(s) and g.isVar(o):
                self.setOptimisable(False)
        elif (isinstance(s,str) or isinstance(s,unicode)) and \
        (isinstance(p,str) or isinstance(o,unicode)) and \
        (isinstance(p,str) or isinstance(o,unicode)):
            print 'DEBUG - Rule.addStm() - string statement...'
            # adding to the grounding if string
            s_ctx, p_ctx, o_ctx = g.DEF_SCP, g.DEF_SCP, g.DEF_SCP
            if var_rel:
                o_ctx = g.REL_SCP
            if s[0] == '?':
                s_ctx = g.VAR_SCP
            if p[0] == '?':
                p_ctx = g.VAR_SCP
            else:
                p_ctx = g.REL_SCP
            if o[0] == '?':
                o_ctx = g.VAR_SCP
            id_s = g.get(s,scope=s_ctx)
            id_p = g.get(p,scope=p_ctx)
            id_o = g.get(o,scope=o_ctx)
            print 'DEBUG - Rule.addStm() - statement IDs (before add):',\
            `(id_s, id_p, id_o)`
            if not id_s:
                id_s = g.add(s,scope=s_ctx)
            if not id_p:
                id_p = g.add(p,scope=p_ctx)
            if not id_o:
                id_o = g.add(o,scope=o_ctx)
            if g.isVar(s) and g.isVar(o):
                self.setOptimisable(False)
        print 'DEBUG - Rule.addStm() - statement IDs:', `(id_s, id_p, id_o)`
        if ac == 'A':
            if not self.ante.has_key(id_s):
                self.ante[id_s] = Entity(id_s)
            self.ante[id_s].setDegree(id_p,id_o,d)
        elif ac == 'C':
            if not self.conseq.has_key(id_s):
                self.conseq[id_s] = Entity(id_s)
            self.conseq[id_s].setDegree(id_p,id_o,d)

    def getTxt(self,dct,prec=3):
        """
        Returns the textual representation (in the presentation syntax)
        of the rule.
        """

        ante_txt = []
        for c in self.ante.values():
            ante_txt.append(c.getTxt(dct))
        if len(ante_txt):
            ante_txt = reduce(lambda x,y:x+' AND '+y,ante_txt)
        else:
            ante_txt = ''
        conseq_txt = []
        for c in self.conseq.values():
            conseq_txt.append(c.getTxt(dct))
        if len(conseq_txt):
            conseq_txt = reduce(lambda x,y:x+' AND '+y,conseq_txt)
        else:
            conseq_txt = ''
        return `self.ruleid`+' :: '+ante_txt+' => '+\
        `round(self.weight,prec)`[:prec+2]+' => '+conseq_txt

# === classes END ===

