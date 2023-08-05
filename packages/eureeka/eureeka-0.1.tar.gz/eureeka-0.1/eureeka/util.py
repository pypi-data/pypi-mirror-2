"""
util.py - a library containing auxiliary definitions and functions for EUREEKA

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

import rdflib, sys, os, os.path, time, tarfile, cPickle, StringIO, MySQLdb, \
math, hashlib, gc
#from sets import Set
from copy import deepcopy
#from nltk.wordnet.stemmer import morphy
from nltk.corpus import wordnet as wn

# === constant definitions BEGIN ===

#global DEF_DIM, DEF_PARAM_PATH, DEF_LEX_SIM, DEF_LEX_DIROL, DEF_LEX_SUBOL, \
#RDFS_TO_EPR, DEF_CAND, DEF_OBODGR, DEF_PREF, DEF_T20, DEF_BSIZE, DEF_RPATH, \
#DEF_RULE_MATCH, DEF_MIN_SIM, DEF_TNORM, DEF_EPATH, DEF_DICT, HOME, MAX_TDEPTH,\
#DEF_MAX_INCLUSION, DEF_MIN_TRANS, DEF_RFACTOR, DEF_MERGE_SIM, DEF_EXTEND_SIM,\
#AMEAN, HMEAN, GMEAN
#DEF_GRID_FACTOR
#, DEF_DIFF_THRES

CTX_URLP = 'http://ontology.smile.deri.ie/aer/ctx/'

DOC_URLP = 'http://salt.semanticauthoring.org/'

STMT_PREF = 'http://ontologies.smile.deri.ie/aer/statement/'
PROV_PREF = 'http://ontologies.smile.deri.ie/aer/provenance/'
SALT_PREF = 'http://salt.semanticauthoring.org/publication/'

TERM_DIV = '_'

KBMASKF = '/usr/local/koraal/lib/resources/kb_mask.txt'

# positive "infinity"
INFTY = 1e10000

# arithmetic mean ID

AMEAN = 0

# geometric mean ID

HMEAN = 1

# harmonic mean ID

GMEAN = 2

# default threshold for analogical extension
DEF_EXTEND_SIM = 0.5

# default threshold for merging
DEF_MERGE_SIM = 0.75

# default restriction factor - the weight to be used when computing restriction
# values in grounded rule consequents

DEF_RFACTOR = 0.5

# minimaln value that needs to be crossed when computing transitivity

DEF_MIN_TRANS = 0.8

# maximal number of inclusion of one concept into the update queue in Focus

DEF_MAX_INCLUSION = 10

# maximum depth allowed for crappy transitive closure computation
# - ensures that it stops and doesn't run too far (even thouhg it makes
#   the result possibly incomplete)

MAX_TDEPTH = 20

# home directory for the EUREEKA installation

#HOME = "/home/novi/eureeka/"
#HOME = "/home/vitnov/devel/python/eureeka/"
HOME = '.'

# default dictionary location

DEF_DICT = HOME+"res/default.dct"

# default difference threshold for explicit rule type II application cycle
# stop condition

#DEF_DIFF_THRES = 0.1

# default minimal similarity threshold (to be used in stopping condition
# of matrix update or in rule type II application cycle)

DEF_MIN_SIM = 0.9

# default dimension of the conceptual representation matrices
# 50000 was too low for GO experiment...
DEF_DIM = 200000

# default dimension increase - to be used for extension when the dictionary 
# size has been exceeded

DEF_DIM_INCREASE = 100000

# default size of a bucket loaded into memory at one time, or stored on the
# disk (size in number of matrices)

DEF_BSIZE = 100000

# default number of matrix grid buckets used for pre-similarity hash bucket 
# computation

DEF_GRIDS = 400 # grids per row/column ~ 20

# default path to parameter file
DEF_PARAM_PATH = HOME+"res/self.params"

# default threshold for rule match - seems to be practical to set a threshold
# rather than just take it if there is any type degree; the threshold gives
# the maximal allowed absolute difference in the matrix and the rule
# antecedent property values (determining preliminary match, to be weighed by
# the actual similarity then, when applying the rule)

DEF_RULE_MATCH = 0.5

# default lexical similarity threshold (for the Levenshtein distance)

DEF_LEX_SIM = 0.75

# default lexical overlap threshold (for sets of terms - the ratio of
# terms that have to be similar in order to pronounce the whole set as 
# overlapping); two alternatives: 
#   (a) direct (only same or similar terms taken into account)
#   (b) subsumption overlap (same, similar or subsumed terms)

DEF_LEX_DIROL = 0.75
DEF_LEX_SUBOL = 0.75

# mappings from (some) RDF(S) constructs to EUREEKA primitives
# @TODO check the completeness of the mapping, sort out the namespaces if 
#       needed
RDFS_TO_EPR = {
  "Class"         : "-CLASS-",
  "Property"      : "-PROPERTY-",
  "type"          : "-TYPE-",
  "subClassOf"    : "-TYPE-",
  "subPropertyOf" : "-TYPE-",
  "domain"        : "-DOMAIN-",
  "range"         : "-RANGE-"
}

DEF_CFG = {
  'N3_IN'   : os.getcwd(),
  'N3_OUT'  : os.getcwd(),
  'TEXT'    : os.getcwd(),
  'DB_DUMP' : os.getcwd(),
  'RL_PATH' : os.path.join(os.getcwd(),'default.n3'),
  'DC_REL'  : os.path.join(os.getcwd(),'relevance.txt'),
  'DB_HOST' : 'localhost',
  'DB_USER' : 'eureeka',
  'DB_PASS' : 'eur33ka',
  'DB_NAME' : 'eureeka',
  'DEF_REL' : '0.2',
  'EXP_FORM': 'n3'
}

# list of elements that can hold a definition in RDF

DEF_CAND = ['definition', 'comment']

# dictionary of OBO synonym modifiers mapped to default degrees corresponding
# to them (to be set as built-in empirical synonymy relation degrees)

DEF_OBODGR = {
  "EXACT"   : 1.0,
  "BROAD"   : 0.5,
  "NARROW"  : 0.5,
  "RELATED" : 0.25
}

# default prefixes used in RDF(S), OWL

DEF_PREF = {
    "xmlns:owl"  : "http://www.w3.org/2002/07/owl#",
    "xmlns:owlx" : "http://www.w3.org/2003/05/owl-xml#",
    "xmlns:rdf"  : "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "xmlns:rdfs" : "http://www.w3.org/2000/01/rdf-schema#",
    "xmlns:a"    : "http://www.text2onto.org/ontology#"
}

# default Text2Onto tag-names (as parsed in cElementtree)

DEF_T2O = {
  "Rating"          : '{'+DEF_PREF["xmlns:a"]+'}'+"Rating",
  "Instance"        : '{'+DEF_PREF["xmlns:a"]+'}'+"Instance",
  "Relation"        : '{'+DEF_PREF["xmlns:a"]+'}'+"Relation",
  "Concept"         : '{'+DEF_PREF["xmlns:a"]+'}'+"Concept",
  "DisjointClasses" : '{'+DEF_PREF["xmlns:a"]+'}'+"DisjointClasses",
  "SubclassOf"      : '{'+DEF_PREF["xmlns:a"]+'}'+"SubclassOf",
  "InstanceOf"      : '{'+DEF_PREF["xmlns:a"]+'}'+"InstanceOf",
  "Domain"          : '{'+DEF_PREF["xmlns:a"]+'}'+"Domain",
  "Range"           : '{'+DEF_PREF["xmlns:a"]+'}'+"Range",
  "Label"           : '{'+DEF_PREF["xmlns:owlx"]+'}'+"Label"
}

# path to default rules persistent representation

DEF_RPATH = os.path.join(HOME,"resources","defrules.r")

# path to default essential property mappings persistent representation

DEF_EPATH = HOME+"res/default.ess"

# default t-norm to be used, list of ID mappings

MIMIMUM_TNORM = 0
PRODUCT_TNORM = 1
LUKASIEWICZ_TNORM = 2

DEF_TNORM = PRODUCT_TNORM

#def_cfg = {
#  'N3_IN' : '../testing/n3_in',
#  'N3_OUT': '../testing/n3_out',
#  'TEXT'  : '../testing/text',
#  'DB_DUMP' : '../testing/dumps',
#  'RL_PATH' : '../testing/rules/default.n3',
#  'DC_REL' : '../testing/n3_in/relevance.txt',
#  'DB_HOST' : 'localhost',
#  'DB_USER' : 'eureeka',
#  'DB_PASS' : 'eur33ka',
#  'DB_NAME' : 'eureeka',
#  'DEF_REL' : '0.2'
#}

DEFAULT_RULES = """
{?r :type :transitive. ?x ?r ?y. ?y ?r ?z} => {?x ?r ?z}.
{?r :type :antisymmetric. ?x ?r ?y. ?y ?r ?x} => {?x :equals ?y}. 
{?r :type :functional. ?x ?r ?y. ?x ?r ?z} => {?y :equals ?z}. 
{?r :type :inverseFunctional. ?y ?r ?x. ?z ?r ?x} => {?y :equals ?z}.
{?r :type :symmetric. ?x ?r ?y} => {?y ?r ?x}.
{?r :type ?s. ?x ?r ?y} => {?x ?s ?y}.
{?r :inverse ?s. ?x ?r ?y} => {?y ?s ?x}.
{?r :domain ?x. ?y ?r ?z} => {?y :type ?x}.
{?r :range ?x. ?y ?r ?z} => {?z :type ?x}.
"""

DEFAULT_RNAMES = ['generic relation', 'type of', 'same as', \
'different from', 'part of', 'has part', 'inverse of', 'reflexive relation', \
'symmetric relation', 'transitive relation', 'antisymmetric relation', \
'irreflexive relation', 'functional relation', 'inverse functional relation', \
'title', 'domain', 'range']

BASE_TERMS = {
  'type of' : ['type', 'is a', 'subClassOf'],
  'same as' : ['same', 'equals', 'equivalent', 'equivalent to', 'equals to'],
  'different from' : ['different'],
  'part of' : ['partOf'],
  'has part' : ['part', 'hasPart', 'have part'],
  'generic relation' : ['relation', 'property'],
  'generic entity' : ['class', 'entity', 'concept'],
  'generic individual' : ['instance', 'individual'],
  'domain' : ['has domain', 'hasDomain'],
  'range' : ['has range', 'hasRange'],
  'inverse of' : ['inverse', 'inverse relation'],
  'reflexive relation' : ['reflexive'],
  'symmetric relation' : ['symmetric'],
  'transitive relation' : ['transitive'],
  'antisymmetric relation' : ['antisymmetric'],
  'irreflexive relation' : ['irreflexive'],
  'functional relation' : ['functional'],
  'inverse functional relation' : ['inverse functional', 'inverseFunctional'],
  'generic link' : ['link', 'associated with', 'associated to', 'associated'],
  'generic variable' : ['variable', 'var'],
  'provenance' : ['prov', 'source'],
  'title' : ['has title', 'have title', 'hasTitle', 'hasProvenanceTitle', \
  'provenance title'],
  'default provenance' : ['baseProvenance', 'base provenance', \
  'defaultProvenance'], 
  'inferred provenance' : ['inferredProvenance', 'inferred']
}

MLIST = ['type of', 'same as', 'different from', 'part of', 'has part',\
'generic individual', 'domain', 'range', 'inverse of', 'reflexive relation',\
'symmetric relation', 'transitive relation', 'antisymmetric relation',\
'irreflexive relation', 'functional relation', 'inverse functional relation',\
'generic link', 'generic variable', 'provenance', 'title', \
'default provenance', 'inferred provenance']

RELATION_SUBTYPES = ['generic relation', 'type of', 'same as', \
'different from', 'part of', 'has part', 'inverse of', 'reflexive relation', \
'symmetric relation', 'transitive relation', 'antisymmetric relation', \
'irreflexive relation', 'functional relation', 'inverse functional relation', \
'title', 'domain', 'range', 'generic link']

KWORD_MAP = {
  'AND' : 'AND',
  'SEP' : ':',
  'NOT' : 'NOT',
  'CTX' : '@'
}

# === constant definitions END ===

# === function definitions BEGIN ===

def parseCFG(cfg_path):
    try:
        f, cfg = open(cfg_path,'r'), {}
        for line in f:
            hash_spl = line.split('#')[0].strip()
            tabl_spl = hash_spl.split('\t')
            if hash_spl and len(tabl_spl) >= 2:
                cfg[tabl_spl[0].upper().strip()] = tabl_spl[1].strip()
        f.close()
        return cfg
    except Exception:
        sys.stderr.write('Warning: problems with the provided config file!\n'+\
        '...using default instead...\n')
        return DEF_CFG

def lemmatise(term,tag='n'):
    words = unicode(`term`.lower()).split()
    try:
        words = unicode(term.lower()).split()
    except UnicodeDecodeError:
        # @TODO - uncomment this for later use
        #sys.stderr.write('\nWarning: unicode error in lemmatisation...\n')
        pass
    i, l = 0, []
    for word in words:
        lemma = None
        lemma = wn.morphy(word,tag)
        if not lemma and tag == 'n' and i < len(words):
            # try adjective lemma if lemmatising compound NP
            lemma = wn.morphy(word,'a')
        if not lemma:
            # leave as is if not conforming to anything
            lemma = word
        l.append(lemma)
    return reduce(lambda x,y: x+' '+y, l, '').strip()

def getRawURI(s):
    try:
        head, tail = os.path.split(s)
        return tail.split('.')[0]
    except IndexError:
        return None

def normTerm(t,chars=['<','>','[',']','{','}','&','^','AND','"',"'","`"]):
    ret = t.strip('-') # removing the '-' from the default names
    for c in chars:
        ret = ret.replace(c,'').strip()
    return ret

def mkRDFHeader(ctx_name,partial=False):

    # @TODO - tell Ioana about the change (partial added)

    s = "<?xml version='1.0' encoding='UTF-8'?><!DOCTYPE rdf:RDF [\n"
    s += '<!ENTITY rdfs "http://www.w3.org/2000/01/rdf-schema#">\n'
    s += '<!ENTITY rdf "http://www.w3.org/1999/02/22-rdf-syntax-ns#">\n'
    s += ']>\n'
    s += '<rdf:RDF\n'
    s += 'xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"\n'
    s += 'xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"\n'
    s += 'xmlns:aer="http://ontologies.smile.deri.ie/aer/aer#"\n'
    s += 'xml:base="'+ctx_name+'"\n'
    s += '>\n\n'
    partial_value = 'false'
    if partial:
        partial_value = 'true'
    s += '<rdf:Description rdf:about="#answer_description" aer:partial="'+\
    partial_value+'"/>\n\n'
    return s

def getLTStr():
    lt = time.localtime()
    return '['+`lt[0]`+'/'+`lt[1]`+'/'+`lt[2]`+'-'+`lt[3]`+':'+`lt[4]`+'.'+\
    `lt[5]`+']'

def isStr(s):
    if isinstance(s,str) or isinstance(s,unicode): return True
    else: return False

def tNorm(x,y,type=DEF_TNORM):
    if type == MIMIMUM_TNORM:
        return min(x,y)
    elif type == PRODUCT_TNORM:
        return x*y
    elif type == LUKASIEWICZ_TNORM:
        return max(0,x+y-1)
    else:
        return x*y

def stripLocalName(s):
    """
    To be used in RDF(S)-based parsers.
    Returns a local name stripped from either namespace prefixed or fully
    qualified name passed as an input. If no prefix or fully qualified 
    namespace URI is not detected, the input is returned.
    """

    name, stripped = s, None
    if isStr(s):
        stripped = "'"
    #elif `type(s)` == "<class 'rdflib.Literal.Literal'>":
    elif type(s) is rdflib.Literal:
        return s.n3()
    #elif `type(s)` == "<class 'rdflib.URIRef.URIRef'>":
    elif type(s) is rdflib.URIRef:
        name, stripped = name.n3(), "<>"
    else: 
        s = `s`

    # processing further if the type is generic string or any other not
    # processed above
    colon_split = name.strip().split(":") # for XMLNS prefix
    hash_split  = name.strip().split("#") # for URIref prefix
    scoln_split = name.strip().split(";") # for entity NS prefix
    if len(hash_split) > 1 and len(hash_split[-1]) != 0:
        return hash_split[-1].strip(stripped)
    if len(colon_split) > 1 and len(colon_split[-1]) != 0: 
        return colon_split[-1].strip(stripped)
    if len(scoln_split) > 1 and len(scoln_split[-1]) != 0: 
        return scoln_split[-1].strip(stripped)
    return s.strip(stripped)

def getVariations(groups,current=[]):
    """
    Computes variations of elements from the groups.

    Note: used in computation of "multiplied" rules with instantiated 
          properties instead of the variables. 
    """

    #print "DEBUG --- the groups: "+`groups`
    updated = []
    if len(groups) == 0:
        return current
    group = groups[-1]
    if current == []:
        for item in group:
            updated.append([item])
    else:
        for item in group:
            for sequence in current:
                #print "  DEBUG --- the current : "+`current`
                #print "  DEBUG --- the sequence: "+`sequence`
                #print "  DEBUG --- the group   : "+`group`
                #print "  DEBUG --- the item    : "+`item`

                # adding current item
                #if not item in sequence:
                #    sequence.append(item)
                # adding the updated sequence
                if not sequence in updated:
                    updated.append(sequence+[item])
        #print "DEBUG --- the updated: "+`updated`
    return getVariations(groups[:-1],updated)

def bin(x):
    d = \
    {0:'000', 1:'001', 2:'010', 3:'011', 4:'100', 5:'101', 6:'110', 7:'111'}
    return ''.join([d[int(dig)] for dig in oct(x)])


# === function definitions END ===

# === class definitions BEGIN ===

# === class definitions END ===

if __name__ == "__main__":
    #lops = LexOps()
    #print "Distance of <"+sys.argv[1]+"> and <"+sys.argv[2]+">: "+ \
    #`lops.levDist(sys.argv[1],sys.argv[2])`
    #sequence = [['a','b','c'],['d','e'],['f','g','h']]
    sequence = [['a']]
    combinations = getVariations(sequence)
    i = 0
    for item in combinations:
        i += 1
        item.reverse()
        print "Comb. "+`i`+": "+`item`

