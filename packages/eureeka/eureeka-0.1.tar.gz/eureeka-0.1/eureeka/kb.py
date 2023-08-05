"""
kb.py - a library containing the EUREEKA knowledge base implementation, 
together with respective basic querying and inference services

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

#from rules import *
from eureeka.rules import loadRules, Rule
from eureeka.util import getLTStr, normTerm, DEFAULT_RNAMES, BASE_TERMS, \
RELATION_SUBTYPES, DEFAULT_RULES
from eureeka.storage import Entity, Entities, Grounding, Relation
import random, sys, gc, os, re
from math import fabs, pow
#from sets import Set
from copy import deepcopy
from collections import deque
from rdflib.Graph import ConjunctiveGraph as Graph

# === classes BEGIN ===

def avgF(a):
    """
    A convenience function simulating the AVG OWA operator.
    """

    try:
        return (1.0/len(a))*reduce(lambda x,y:x+y,a)
    except Exception:
        raise Exception("Error: wrong arguments in an OWA operator!")

def aggregate(l,owa=avgF):
    aggs = {}
    owa = owa
    for m in l:
        if aggs.has_key(m.getID()):
            aggs[m.getID()].append(m)
        else:
            aggs[m.getID()] = [m]
    ret = []
    for i in aggs:
        po2d, c = {}, Entity(i)
        for m in aggs[i]:
            for p,o in m.getIndices():
                if not po2d.has_key((p,o)):
                    po2d[(p,o)] = [m.getDegree(p,o)]
                else:
                    po2d[(p,o)].append(m.getDegree(p,o))
        for p,o in po2d:
            c.setDegree(p,o,owa(po2d[(p,o)]))
        ret.append(c)
    return ret

class KB:
    """
    KB class - implements the inference and querying abstracting from
    the storage of the concepts. 
    """

    def __init__(self,cfg,trace=False):
        """
        Initialises the knowledge base. 
        """

        self.cfg = cfg
        #if not self.cfg:
        #    sys.stderr.write('Warning: using default EUREEKA config...\n')
        #    cfg = cfgParse(os.path.join('..','resources','eureeka.cfg'))
        # KB concept set, rule set and trace indicator
        self.grounding = Grounding(cfg)
        self.entities = Entities(cfg,trace)
        self.rules = {}
        self.loadRules()
        self.DEFAULT_IDS = []
        for name in BASE_TERMS:
            if name in RELATION_SUBTYPES:
                self.DEFAULT_IDS.append(self.grounding.get(name,\
                scope=self.grounding.REL_SCP))
            else:
                self.DEFAULT_IDS.append(self.grounding.get(name,\
                scope=self.grounding.DEF_SCP))
        self.trace = trace

    def loadRules(self,desc='default',path=None,format='n3'):
        """
        Loads rules with the description desc from the file specified by path.
        """

        if not path:
            if os.path.isfile(self.cfg['RL_PATH']):
                self.rules[desc] = loadRules(self.cfg['RL_PATH'],\
                self.grounding,format)
            else:
                # using default rules
                sys.stderr.write('\nWarning: using default rules!\n')
                try:
                    tmpfile = os.path.join(os.getcwd(),'default.tmp.n3')
                    f = open(tmpfile,'w')
                    f.write(DEFAULT_RULES)
                    f.close()
                    self.rules[desc] = loadRules(tmpfile,self.grounding,format)
                    os.remove(tmpfile)
                except IOError:
                    sys.stderr.write('\nWarning: permission problems, rules'+\
                    ' empty!\n')
                    self.rules[desc] = []
        else:
            self.rules[desc] = loadRules(path,self.grounding,format)

    def getRules(self,desc='default'):
        return self.rules[desc]

    def add(self,r):
        """
        Adding a relation.
        """

        self.entities.addRelation(r,self.grounding)

    def load(self,path):
        """
        Importing content from N3 files stored in the input path.
        """

        fcount, i, relations = 0, 0, []
        file_list = os.listdir(path)
        for fname in file_list:
            fcount += 1
            print 'Processing', `fcount`+'.', 'file out of', `len(file_list)`
            full_name = os.path.join(path,fname)
            if not os.path.isfile(full_name) or \
            full_name.split('.')[-1].lower() != 'n3':
                continue
            for r in self.__parseN3(full_name):
                relations.append(r)
                i += 1
                if i%100000 == 0:
                    print '  importing', `i/100000`+'-th', 'hundred thousand',\
                    'relation chunk...'
                    self.entities.addRelations(relations,self.grounding)
                    relations = []
        print 'Importing', `i/100000`+'-th', 'hundred thousand',\
        'relation chunk...'
        self.entities.addRelations(relations,self.grounding)

    def __parseN3(self,fname):
        """
        Parsing a N3 file into a list of Relation objects.
        """

        g, l = Graph(), []
        try:
            g.parse(fname,format='n3')
        except:
            sys.stderr.write('Warning: N3 file invalid, omitting...\n')
            return l
        id2relel = {} # relation elements
        # getting names of default relations and their synonyms
        rnames_extended = set(reduce(lambda x,y: x+y, \
        map(lambda x: map(lambda x: x[0], \
        self.grounding.getSynonyms(x,self.grounding.REL_SCP)),\
        DEFAULT_RNAMES),[]))
        relation_names = set()
        for t in g:
            rel_id = t[0].split('/')[-1]
            rel_pn = t[1].split('#')[-1]
            rel_on = t[2][:]
            if not id2relel.has_key(rel_id):
                id2relel[rel_id] = {}
            id2relel[rel_id][rel_pn] = rel_on
            if rel_pn == 'hasPredicate':
                # add every explicitly set relation name
                relation_names.add(rel_on)
        # add also subtype of default relations as relation names
        relation_names |= set(map(lambda x: x['hasSubject'], filter(lambda x:\
        x['hasObject'] in rnames_extended, id2relel.values())))
        for rel_id in id2relel:
            re = id2relel[rel_id]
            s, p, o = re['hasSubject'], re['hasPredicate'], re['hasObject']
            subj_rel = s in relation_names
            obj_rel = o in relation_names
            cert = float(re['hasCertainty'])
            r = Relation(s,p,o,cert=cert,subj_rel=subj_rel,obj_rel=obj_rel)
            if subj_rel:
                r.subjRelOn()
            if obj_rel:
                r.objRelOn()
            for pred in re:
                if pred in ['hasSubject', 'hasPredicate', 'hasObject', \
                'hasCertainty']:
                    continue
                elif pred == 'hasProvenance':
                    if len(re[pred].split(':')) > 1:
                        # re-composing the provenance title
                        title = reduce(lambda x,y: x+': '+y, \
                        re[pred].split(':')[1:])
                        r.setProvenance(title)
                    else:
                        r.setProvenance('default provenance')
                #elif pred == 'hasProvenanceTitle':
                #    # to support the old format of N3 serialisation
                #    r.setProvenance(re[pred])
                else:
                    r.setContext(pred,re[pred])
            l.append(r)
        return l

    def set(self,m):
        """
        Inserts an entity (possibly overwriting former content). 
        """

        self.entities[m.getID()] = m

    def get(self,x,scope=None,get_rels=False):
        """
        Attempts to retrieve a concept (specified either by an ID or by term).
        Note: if an ID is on the input, a single concept is retrieved, if
        a string is on the input, a list of possible concepts labelled by the
        term is returned.
        """

        if not scope:
            scope=self.grounding.DEF_SCP
        if isinstance(x,int):
            try:
                if not get_rels:
                    return self.entities[x]
                else:
                    return self.entities.getRelations(x,g=self.grounding)
            except KeyError:
                #raise KeyError("Error: no such concept in the knowledge base.")
                return None
        elif isinstance(x,str):
            try:
                i = self.grounding.get(x,scope=scope)
                if not get_rels:
                    return self.entities[i]
                else:
                    return self.entities.getRelations(i,g=self.grounding)
            except KeyError:
                #raise KeyError("Error: no such concept in the knowledge base.")
                return None
        return None

    def getAll(self):
        """
        Returns all concepts contained within a KB at the moment.
        """

        return self.entities.values()

    def __guessTerms(self,spo):
        sg, pg, og = spo
        if sg:
            sg = normTerm(sg)
        if pg:
            pg = normTerm(pg)
        if og:
            og = normTerm(og)
        if sg and sg[0] != self.grounding.VAR_SIG:
            t_id = self.grounding.get(sg.lower(),scope=self.grounding.DEF_SCP)
            if self.trace:
                print 'KB.__guessTerms() - subject ID:', `t_id`
            if not t_id:
                # get the stuff in original case if lower does not work
                t_id = self.grounding.get(sg,scope=self.grounding.DEF_SCP)
            if not t_id:
                # selecting only head verb or noun from the term if the 
                # term is not present in its whole
                head_only = sg.split()[-1]
                t_id = self.grounding.get(head_only.lower(),\
                scope=self.grounding.DEF_SCP)
                if not t_id:
                    # get the stuff in original case if lower does not work
                    t_id = self.grounding.get(head_only,\
                    scope=self.grounding.DEF_SCP)
            if t_id:
                sg = self.grounding.get(t_id)
                if self.trace:
                    print 'KB.__guessTerms() - subject guess:', `sg`
        if pg and pg[0] != self.grounding.VAR_SIG:
            t_id = self.grounding.get(pg.lower(),scope=self.grounding.REL_SCP)
            if self.trace:
                print 'KB.__guessTerms() - predicate ID:', `t_id`
            if not t_id:
                # get the stuff in original case if lower does not work
                t_id = self.grounding.get(pg,scope=self.grounding.REL_SCP)
            if not t_id:
                # selecting only head verb or noun from the term if the 
                # term is not present in its whole
                head_only = pg.split()[0]
                t_id = self.grounding.get(head_only.lower(),\
                scope=self.grounding.REL_SCP)
                if not t_id:
                    # get the stuff in original case if lower does not work
                    t_id = self.grounding.get(head_only,\
                    scope=self.grounding.REL_SCP)
            if t_id:
                pg = self.grounding.get(t_id,scope=self.grounding.REL_SCP)
                if self.trace:
                    print 'KB.__guessTerms() - predicate guess:', `pg`
        if og and og[0] != self.grounding.VAR_SIG:
            t_id = self.grounding.get(og.lower(),scope=self.grounding.DEF_SCP)
            if self.trace:
                print 'KB.__guessTerms() - object ID:', `t_id`
            if not t_id:
                # get the stuff in original case if lower does not work
                t_id = self.grounding.get(og,scope=self.grounding.DEF_SCP)
            if not t_id:
                # selecting only head verb or noun from the term if the 
                # term is not present in its whole
                head_only = og.split()[-1]
                t_id = self.grounding.get(head_only.lower(),\
                scope=self.grounding.DEF_SCP)
                if not t_id:
                    # get the stuff in original case if lower does not work
                    t_id = self.grounding.get(head_only,\
                    scope=self.grounding.DEF_SCP)
            if t_id:
                og = self.grounding.get(t_id)
                if self.trace:
                    print 'KB.__guessTerms() - object guess:', `og`
        return (sg,pg,og)

    def __parseQuery(self,q):
        """
        Parses a near-NL query into a rule object.
        """

        if not q:
            return None, {}
        ctx_string = ''
        query = q.split('@')[0].strip()
        if len(q.split('@')) >= 2:
            ctx_string = q.split('@')[1].strip()
        conjuncts = map(lambda x: x.strip(), query.split('AND'))
        statements, label, contexts = [], None, {}
        # constructing antecedent prefabricates
        for conjunct in conjuncts:
            tmp = conjunct.replace('NOT','')
            negative = False
            if conjunct.find('NOT') != -1:
                negative = True
            spo = map(lambda x: x.strip(), tmp.split(':'))
            #print 'DEBUG -- spo:', `spo`
            if len(spo) == 1 or (len(spo) > 1 and not reduce(lambda x,y: \
            x and y, map(len,spo))):
                # single label - set only the label and quit the cycle
                nempty = filter(lambda x: len(x) > 0, spo).pop()
                label = self.__guessTerms((nempty,None,None))[0]
                break
            elif len(spo) == 3:
                # regular statement
                d = 1.0
                if negative:
                    d *= -1
                guess = self.__guessTerms(spo)
                #if guess[1][0] != '?':
                    # don't append those with variables as predicates
                statements.append((guess[0],guess[1],guess[2],d))
        # constructing the rule itself
        if self.trace:
            print 'KB.__parseQuery() - statements:\n', `statements`
        qobj = Rule(0)
        if label:
            idx = self.grounding.get(label)
            if not idx:
                return None, contexts
            c = Entity(idx)
            qobj.setAntecedent(c)
        else:
            for stmt in filter(lambda x: x[0] and x[1] and x[2], statements):
                qobj.addStm(stmt,self.grounding)
            if not len(qobj.getAntecedents()):
                return None, contexts
        # generating the context dictionary
        if len(ctx_string):
            for pc in ctx_string.split('AND'):
                p, c = pc.split(':')[0].strip(), pc.split(':')[1].strip()
                p_id = self.grounding.get(p,scope=self.grounding.REL_SCP)
                if not p_id:
                    p_id = self.grounding.add(p,scope=self.grounding.REL_SCP)
                c_id = self.grounding.get(c,scope=self.grounding.DEF_SCP)
                if not c_id:
                    c_id = self.grounding.add(c,scope=self.grounding.DEF_SCP)
                contexts[p_id] = c_id
        return qobj, contexts

    def ask(self,q):
        """
        Evaluates the human-centric query q (after parsing it into internal 
        rule/query format) and returns the respective Relation objects.
        """

        qobj, contexts = self.__parseQuery(q)
        if not qobj or not len(qobj.getAntecedents()):
            if self.trace:
                print 'KB.ask() - parse failed, empty answer'
            return []
        if len(qobj.getAntecedents()) == 1 and \
        (not len(qobj.getAntecedents()[0]) or \
        (len(qobj.getAntecedents()[0]) == 1 and \
        self.grounding.isVar(qobj.getAntecedents()[0].getIndices()[0][0]))):
            # 1 antecedent statement with variable predicate or entity ID only
            if self.trace:
                print 'KB.ask() - doing simple query evaluation...'
            return self.__evalSimpleQ(qobj.getAntecedents(),\
            qobj.getConsequents(),contexts)
        if self.trace:
            print 'KB.ask() - doing regular query evaluation...'
        return self.execute(qobj,contexts=contexts)

    def updateScores(self,k=10,minf=25):
        self.entities.updateScores(k=k,minf=minf)

    def expandRules(self,rule_set):
        expanded, rule_id = [], 0
        type_id = self.grounding.get('type of',scope=self.grounding.REL_SCP)
        prop_id = self.grounding.get('generic relation',\
        scope=self.grounding.REL_SCP)
        #if self.trace:
        #    print 'DEBUG -- KB.expandRules() -- the default IDs:\n', \
        #    `self.DEFAULT_IDS`
        for rule in rule_set:
            if self.trace:
                print 'DEBUG -- KB.expandRules() -- expanding the rule:\n',\
                rule.getTxt(self.grounding)
            statements, var2inst = [], {}
            for ante in rule.getAntecedents():
                s = ante.getID()
                statements += map(lambda x: \
                (s,x[0],x[1],ante.getDegree(x[0],x[1])), ante.getIndices())
            pred_vars = set(map(lambda x: x[1], \
            filter(lambda x: self.grounding.isVar(x[1]), statements)))
            cond = filter(lambda x: x[0] in pred_vars, statements)
            if self.trace:
                print 'DEBUG -- KB.expandRules() -- pred_vars:\n',\
                `pred_vars`
            cs = (None, None, None, None)
            if len(cond):
                cs = cond[0]
            if len(cond) > 1:
                # at most one predicate variable condition-defining statement 
                continue
            if not len(pred_vars):
                # no variable predicates, just keep as is and move on
                rule.setID('exp-'+`rule_id`)
                expanded.append(rule)
                if self.trace:
                    print 'DEBUG -- KB.expandRules() -- rule added intact...'
                rule_id += 1
                continue
            elif len(pred_vars) == 1 and not self.grounding.isVar(cs[2]):
                # 1 variable in the condition, 1 for cycle
                self.entities.cursor.execute("""SELECT DISTINCT subject FROM 
                                                entities WHERE predicate=%s 
                                                AND object=%s 
                                                AND certainty*%s>0""", \
                                                (cs[1],cs[2],cs[3]))
                for inst, in self.entities.cursor.fetchall():
                    var2inst[cs[0]] = inst
                    exp_rule = \
                    self.__instRule(rule,'exp-'+`rule_id`,var2inst,cs[0])
                    if self.trace:
                        print 'DEBUG -- KB.expandRules() -- expanded:\n',\
                        exp_rule.getTxt(self.grounding)
                    expanded.append(exp_rule)
                    rule_id += 1
                    var2inst = {}
            elif len(pred_vars) == 1 and self.grounding.isVar(cs[2]):
                # 2 variables in the condition, 2 nested for cycles
                #subjects, objects = self.__getSOVarInstances(cs)
                #if self.trace:
                #    print 'DEBUG -- KB.expandRules() -- subjects, objects:\n',\
                #    `subjects`, '\n', `objects`
                for s, o in self.__getSOVarInstances(cs):
                    var2inst[cs[0]], var2inst[cs[2]] = s, o
                    exp_rule = \
                    self.__instRule(rule,'exp-'+`rule_id`,var2inst,cs[0])
                    if self.trace:
                        print 'DEBUG -- KB.expandRules() -- expanded:\n',\
                        exp_rule.getTxt(self.grounding)
                    expanded.append(exp_rule)
                    rule_id += 1
                    var2inst = {}
        return expanded

    def __getSOVarInstances(self,cond):
        type_id = self.grounding.get('type of',scope=self.grounding.REL_SCP)
        range_id = self.grounding.get('range',scope=self.grounding.REL_SCP)
        entity_id = self.grounding.get('generic entity')
        so = set()
        self.entities.cursor.execute("""SELECT DISTINCT t1.subject
                                        FROM entities t1, grounding t2
                                        WHERE t1.predicate=%s AND 
                                        t2.identifier=t1.subject AND 
                                        t2.scope=%s AND 
                                        t1.certainty*%s>0""", (cond[1],\
                                        self.grounding.REL_SCP,cond[3]))
        # excluding default identifiers for type predicate
        subjects = map(lambda x: x[0], self.entities.cursor.fetchall())
        if cond[1] == type_id:
            subjects = filter(lambda x: x not in self.DEFAULT_IDS, subjects)
        for s in subjects:
            comp_sign = '='
            if (range_id,entity_id) in self.entities[cond[1]].getIndices():
                # anything but relation for predicates with expl. entity range
                comp_sign = '!='
            self.entities.cursor.execute("""SELECT DISTINCT t1.object
                                            FROM entities t1, grounding t2
                                            WHERE t1.subject=%s AND 
                                            t1.predicate=%s AND 
                                            t2.identifier=t1.object AND 
                                            t2.scope"""+comp_sign+"""%s AND 
                                            t1.certainty*%s>0""", (s,cond[1],\
                                            self.grounding.REL_SCP,cond[3]))
            # excluding default identifiers for type predicate
            objects = filter(lambda x: x not in self.DEFAULT_IDS, \
            map(lambda x: x[0], self.entities.cursor.fetchall()))
            #if cond[1] == type_id:
            #    objects = filter(lambda x: x not in self.DEFAULT_IDS, objects)
            for o in objects:
                so.add((s,o))
        return so

    def __instRule(self,rule,rule_id,vid2iid,red):
        """
        Replaces the variables that are key in the vid2iid with the instances 
        given as the respective values. red gives the antecedent ID to be 
        reduced (i.e., expanded, therefore not included) in the resulting rule.
        """

        antecedents, consequents = {}, {}
        components = {'A': rule.getAntecedents(), 'C': rule.getConsequents()}
        for key in components:
            for m in components[key]:
                if m.getID() == red:
                    # don't include the predicate variable subjects
                    continue
                s = m.getID()
                if vid2iid.has_key(s):
                    s = vid2iid[s]
                nm = Entity(s)
                for p, o in m.getIndices():
                    np, no = p, o
                    if vid2iid.has_key(np):
                        np = vid2iid[np]
                    if vid2iid.has_key(no):
                        no = vid2iid[no]
                    nm.setDegree(np,no,m.getDegree(p,o))
                if key == 'A':
                    antecedents[nm.getID()] = nm
                elif key == 'C':
                    consequents[nm.getID()] = nm
        w, optim = rule.getWeight(), rule.isOptimisable()
        return Rule(rule_id,antecedents,consequents,w,optim)

    def getVInstances(self,v,gr,var2ins):
        # contructing the query condition list
        l = []
        cdct = {'subj_of':v.subj_of, 'obj_of':v.obj_of}
        for key in cdct:
            for x, y, d in cdct[key]:
                p, con_arg = None, None
                if key == 'subj_of':
                    p, con_arg = x, y
                else:
                    p, con_arg = y, x
                if con_arg in gr:
                    # variable
                    if var2ins.has_key(con_arg) and var2ins[con_arg]:
                        # has already an instance
                        con_arg = var2ins[con_arg]
                    else:
                        # no instance, only predicate-based query
                        con_arg = None
                if key == 'subj_of':
                    l.append((0,p,con_arg,d))
                else:
                    l.append((con_arg,p,0,d))
        if self.trace:
            print 'KB.getVInstances() - the conditions for DB query:\n', `l`
        # returning the respective instance candidates
        return self.entities.query(l,partial=False)

    def __initQueue(self,gr,var2ins,focus):
        root, root_inst_set = None, []
        if not focus:
            # pick a minimal root from the whole KB
            min_sz = sys.maxint
            for v in gr:
                inst_set = self.getVInstances(gr[v],gr,var2ins)
                sz = len(inst_set)
                if sz < min_sz:
                    root, min_sz, root_inst_set = gr[v].getID(), sz, inst_set
        else:
            # pick a "subject" root and assign focus as its instances
            subj_only = map(lambda x: x.getID(), \
            filter(lambda x: not x.obj_of,gr.values()))
            if self.trace:
                print 'KB.__initQueue() - DEBUG - the graph vertices:'
                for v in gr.values():
                    print `v.identifier`, ': subj_of=', `v.subj_of`, \
                    'obj_of=', `v.obj_of`
                print 'KB.__initQueue() - DEBUG - subj_only:\n', `subj_only`
            if len(subj_only):
                root = subj_only.pop() # pick one from the candidates
            else:
                root = random.choice(gr.keys()) # pick random (asume cycle)
            root_inst_set = focus
        # generating the initial to_visit set of (VAR,inst) pairs
        return deque(map(lambda x: (root,x), root_inst_set))

    def __genSucc(self,gr,var,inst,current,visvar,var2ins,max_res=1000):
        v, succ_tuples, match = gr[var], [], True
        for p, o, d in v.subj_of:
            if self.grounding.isVar(o):
                if o not in visvar:
                    succ_tuples += map(lambda x: (o,x[1]), filter(lambda x: \
                    x[0] == p and current.getDegree(x[0],x[1])*d>0, \
                    current.getIndices()))
                else:
                    if current.getDegree(p,var2ins[o])*d <= 0:
                        match = False
            else:
                if current.getDegree(p,o)*d <= 0:
                    match = False
        for s, p, d in v.obj_of:
            if self.grounding.isVar(s):
                if s not in visvar:
                    # @TODO - possibly make the subject>24 more generic
                    self.entities.cursor.execute("""SELECT DISTINCT t1.subject,
                                                    0.5*(t2.hub+t2.auth)
                                                    FROM entities t1, 
                                                    scores t2 WHERE 
                                                    t1.subject=t2.entity AND
                                                    t1.predicate=%s AND
                                                    t1.object=%s AND 
                                                    t1.subject>24 
                                                    AND t1.certainty*%s>0
                                                    ORDER BY 
                                                    0.5*(t2.hub+t2.auth)
                                                    desc""", \
                                                    (p,inst,d))
                    succ_tuples += map(lambda x: (s,x), \
                    map(lambda x: x[0],self.entities.cursor.fetchmany(max_res)))
                else:
                    if self.entities[var2ins[s]].getDegree(p,inst)*d <= 0:
                        match = False
            else:
                if self.entities[s].getDegree(p,inst)*d <= 0:
                    match = False
        #return (match, filter(lambda x: x not in visited, succ_tuples))
        return (match, succ_tuples)

    def execute(self,r,partial=True,e=0.4,max_res=1000,contexts={},focus=[],\
    itlim=1000):
        if self.trace:
            print '\nKB.execute() - the rule to be executed:\n', \
            r.getTxt(self.grounding)
        mater = []
        gr = r.getAnteGraph(self.grounding)
        if not len(gr):
            return mater
        var2ins = {}.fromkeys(gr.keys(),None)
        to_visit, visited = self.__initQueue(gr,var2ins,focus), set()
        if self.trace:
            print 'KB.execute() - to visit after initialisation:\n', `to_visit`
            print '             - the antecedent graph:\n', `gr`
        # traversing gr, materialising whenever all variables have instances;
        # safety block ensures only limited number of iterations
        i = 0
        while len(to_visit) and i < itlim:
            i += 1
            var, inst = to_visit.pop()
            if self.trace:
                print 'KB.execute() - current var/instance:', `var`,',',`inst`
            current = self.entities[inst]
            if (var, inst) not in visited:
                visited.add((var,inst))
                visvar = set(map(lambda x: x[0], list(visited)))
                # updating var2ins according to current instantiation
                var2ins[var] = inst
                for key in set(var2ins.keys()) - visvar:
                    var2ins[key] = None
                # generating the successor tuples
                match, succ_tuples = self.__genSucc(gr,var,inst,current,visvar,\
                var2ins,max_res=max_res)
                if self.trace:
                    print 'KB.execute() - match, queue, succ_tuples, var2ins:',\
                    '\n', `match`, ',' , `to_visit`, ',', `succ_tuples`, ',', \
                    `var2ins`
                if match:
                    to_visit.extend(succ_tuples)
                    if reduce(lambda x,y: x and y, var2ins.values(),True) and \
                    (not len(succ_tuples) or len(set(map(lambda x: x[0], \
                    succ_tuples)) & visvar)):
                        # nothing for extension or variable already processed, 
                        # fully instantiated -> try to materialise
                        if self.trace:
                            print 'KB.execute() - materialising'
                        agg_sim = self.getAggSim(r.getAntecedents(),var2ins)
                        mater += self.materialise(r.getAntecedents(),\
                        r.getConsequents(),r.getWeight(),var2ins,agg_sim,\
                        contexts)
                        visvar.remove(var)
                        visited.remove((var,inst))
        return mater

    def __evalSimpleQ(self,antes,conseqs=[],contexts=[]):
        """
        Processes simple query, i.e., query consisting of only one antecedent
        statement.
        """

        if not len(antes[0]):
            # returning enriched concept if there is only label
            idx = antes[0].getID()
            if self.grounding.contains(idx) and self.entities.has_key(idx):
                if not len(conseqs):
                    # query answering - return just a rich concept
                    #return [self.entities.getRichConcept(idx,disjoints=True)]
                    return self.entities.getRelations([idx],contexts=contexts)
            else:
                return []
        elif len(antes[0]) == 1 and \
        self.grounding.isVar(antes[0].getIndices()[0][0]):
            # by-passing the query evaluation for variable predicate
            s, o = antes[0].getID(), antes[0].getIndices()[0][1]
            d = antes[0].getDegree(antes[0].getIndices()[0][0],\
            antes[0].getIndices()[0][1])
            return self.entities.getRelations([s],contexts=contexts,\
            ftlr={s:(o,d)})

    def getAggSim(self,antes,var2inst,f=avgF):
        """
        Returns aggregate similarity of antecedents to the their instantiated 
        versions.
        """

        sims = []
        for a in antes:
            s = a.getID()
            if var2inst.has_key(s):
                s = var2inst[s]
            c = Entity(s)
            for p, o in a.getIndices():
                if var2inst.has_key(o):
                    o = var2inst[o]
                c.setDegree(p,o,a.getDegree(p,o))
            sims.append(c.sim(self.entities[s]))
        return f(sims)

    def materialise(self,antes,conseqs,w,var2inst,agg_sim,contexts={}):
        """
        Computes materialisation of a rule or query according to the given 
        variable-instance mapping. 
        """

        # @TODO - possibly add a limit on the size of retrieved instances

        u, v = 1-agg_sim, w
        if len(conseqs):
            # rule consequent materialisation
            l = []
            for con in conseqs:
                # concept from the knowledge base
                ns = con.getID()
                if var2inst.has_key(ns):
                    ns = var2inst[ns]
                con_k = None
                if ns in self.entities.keys():
                    con_k = self.entities[ns]
                # instantiated consequent
                con_inst = Entity(con.getID())
                if con.getID() in var2inst.keys():
                    con_inst = Entity(var2inst[con.getID()])
                for p, o in con.getIndices():
                    np, no, d = p, o, con.getDegree(p,o)
                    # if the p, o are variables, get the instances
                    if var2inst.has_key(np):
                        np = var2inst[np]
                    if var2inst.has_key(no):
                        no = var2inst[no]
                    con_inst.setDegree(np,no,d)
                aggregate = Entity(ns)
                if con_k:
                    for p, o in con_k.getIndices(True) | \
                    con_inst.getIndices(True):
                        if not con_k.getDegree(p,o):
                            aggregate.setDegree(p,o,con_inst.getDegree(p,o))
                        elif not con_inst.getDegree(p,o):
                            aggregate.setDegree(p,o,con_k.getDegree(p,o))
                        elif con_k.getDegree(p,o) != con_inst.getDegree(p,o):
                            # conflicting non-zero degrees
                            d = u*con_k.getDegree(p,o)+\
                            v*con_inst.getDegree(p,o)/(u+v)
                            aggregate.setDegree(p,o,d)
                else:
                    # adding an entirely new entity
                    aggregate = con_inst*v
                l.append(aggregate)
            return l
        else:
            # query answer materialisation
            if self.trace:
                print 'KB.materialise() - the instances and similarity:\n',\
                `var2inst.values()`, '\n', `agg_sim`
            #return map(lambda x: self.entities[x]*agg_sim, var2inst.values())
            # returning the Relation objects straightaway
            return self.entities.getRelations(var2inst.values(),sim=agg_sim,\
            contexts=contexts,g=self.grounding)

    def extend(self,to_extend,desc='default',partial=True,e=0.4,max_res=100,\
    contexts={},itlim=25):
        """
        Extends the input entities according to applicable rules.
        """

        # filtering to existing IDs only
        ids = filter(lambda x: self.entities.has_key(x), to_extend)
        # identify the rules applicable for extension
        expanded = self.expandRules(self.rules[desc])
        applicable = []
        for r in expanded:
            ante_subj = map(lambda x: x.getID(), r.getAntecedents())
            cons_subj = map(lambda x: x.getID(), r.getConsequents())
            if len(set(ante_subj) & set(cons_subj)):
                applicable.append(r)
        if self.trace:
            print 'KB.extend() - the IDs to be extended:\n', `ids`
        sz1 = reduce(lambda x,y: x+y, \
        map(lambda x:len(self.entities[x]), ids),0)
        # first iteration
        for r in applicable:
            for ent in self.execute(r,partial=partial,e=e,max_res=max_res,\
            contexts=contexts,focus=ids,itlim=itlim):
                self.entities.update(ent)
        sz2 = reduce(lambda x,y: x+y, \
        map(lambda x:len(self.entities[x]), ids),0)
        # cyclic extension until no new stuff is being added or until an
        # iteration limit is exceeded
        i = 0
        while not (sz1 == sz2 or i > itlim):
            i += 1
            sz1 = sz2
            for r in applicable:
                for ent in self.execute(r,partial=partial,e=e,max_res=max_res,\
                contexts=contexts,focus=ids,itlim=itlim):
                    self.entities.update(ent)
            sz2 = reduce(lambda x,y: x+y, \
            map(lambda x:len(self.entities[x]), ids),0)
        # returning only inferred relations
        return self.entities.getRelations(ids,contexts=contexts,\
        g=self.grounding,prov=0)

    def apply(self,rules,partial=True,e=0.4,max_res=1000,contexts={},\
    upd_only=False):
        results = set()
        if not rules:
            # pick appropriate from default rules
            expanded = self.expandRules(self.rules['default'])
            for r in expanded:
                ante_subj = map(lambda x: x.getID(), r.getAntecedents())
                cons_subj = map(lambda x: x.getID(), r.getConsequents())
                if not len(set(ante_subj) & set(cons_subj)):
                    rules.append(r)
        for r in rules:
            for ent in self.execute(r,partial=partial,e=e,max_res=max_res,\
            contexts=contexts):
                self.entities.update(ent)
                if not upd_only:
                    results.add(ent.getID())
        # returning only inferred relations
        if not upd_only:
            return self.entities.getRelations(list(results),contexts=contexts,\
            g=self.grounding,prov=0)
        else:
            # just update performed, thus no possibly "expensive" relations are
            # generated
            return []

    def __infSize(self):
        self.entities.cursor.execute("""SELECT subject, predicate, object
                                        FROM entities WHERE provenance=0""")
        return self.entities.cursor.rowcount

    def closure(self,desc='default',partial=True,e=0.4,max_res=1000,\
    contexts={}):
        """
        Runs the fix-point materialisation. 
        """

        expanded = self.expandRules(self.rules[desc])
        sz1 = self.__infSize()
        # first expansion of the whole KB
        for key in self.entities.keys():
            self.extend([key])
        self.apply([])
        sz2 = self.__infSize()
        # cyclic extension until no new stuff is being added
        while sz1 != sz2:
            sz1 = sz2
            for key in self.entities.keys():
                self.extend([key])
            self.apply([])
            sz2 = self.__infSize()

# === classes END ===

# testing-only functions

if __name__ == "__main__":
    pass
