"""
extraction.py - a library for simple quick'n'dirty relation extraction from 
natural language texts

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

# native module imports

import sys, os, random, rdflib, hashlib, xml.etree.cElementTree, socket, \
urllib, simplejson
#from sets import Set
from math import log, fabs #, sqrt
from collections import defaultdict
# NLTK module imports
import nltk
#from nltk.stem.porter import PorterStemmer
#from nltk.tokenize.punkt import PunktWordTokenizer
from nltk.tree import Tree
#from nltk.wordnet import V
#from nltk.wordnet.stemmer import morphy

# EUREEKA module imports

from eureeka.kb import Relation
from eureeka.util import lemmatise
#from kb import KB
#from util import getLTStr, INFTY, mkRDFHeader, CTX_URLP
#from lex import PRID, Lexicon

# === constants BEGIN ===

# English preposition list

GOOGLE_API = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s'

PREPS = set(['abaft', 'aboard', 'about', 'above', 'absent', 'across', 'after', 
         'against', 'along', 'alongside', 'amid', 'amidst', 'among', 'amongst',
         'around', 'as', 'aslant', 'astride', 'at', 'athwart', 'atop', 
         'barring', 'before', 'behind', 'below', 'beneath', 'beside', 
         'besides', 'between', 'beyond', 'but', 'by', 'concerning', 'despite', 
         'down', 'during', 'except', 'failing', 'following', 'for', 'from', 
         'in', 'inside', 'into', 'like', 'mid', 'minus', 'near', 'next', 
         'notwithstanding', 'of', 'off', 'on', 'onto', 'opposite', 'out', 
         'outside', 'over', 'past', 'per', 'plus', 'regarding', 'round', 
         'save', 'since', 'than', 'through', 'throughout', 'till', 'times', 
         'to', 'toward', 'towards', 'under', 'underneath', 'unlike', 'until', 
         'up', 'upon', 'via', 'with', 'within', 'without', 'worth'])

STOPWORDS = ['the', 'a', 'an'] # @TODO - extend these!

# namespace for EUREEKA presentation relations
NS_EUPRES = 'http://ontologies.smile.deri.ie/eureeka/presentation#'
# grammar for conjunctive NPs
GRM1 = """
NP: {<CD>?<JJ.*>*<NN.*>+((<IN>|<TO>)?<CD>?<JJ.*>*<NN.*>+)*((<CC>|,)<CD>?<JJ.*>*<NN.*>+((<IN>|<TO>)?<CD>?<JJ.*>*<NN.*>+)*)*}
"""
# grammar for single NPs
GRM2 = """
NP: {<CD>?<JJ.*>*<NN.*>+((<IN>|<TO>)?<CD>?<JJ.*>*<NN.*>+)*}
"""
# grammar for single raw NPs (no prepositions)
GRM3 = """
NP: {<CD>?<JJ.*>*<NN.*>+}
"""
chunker_npp = nltk.RegexpParser(GRM1)
chunker_nps = nltk.RegexpParser(GRM2)
chunker_npr = nltk.RegexpParser(GRM3)

# === constants END ===

# === functions BEGIN ===

def makesSense(t,use_google=False,sig_length=3):
    """
    Function determining whether the input term makes any sense (using Google 
    API and simple heuristic - no results -> no sense). Intended to be
    used for noun phrases.
    """

    if not t:
        return False
    # are all elements of the input string alphanumerical and of significant
    # length?
    makes_sense = all(x.isalnum() and len(x) >= sig_length for x in t.split())
    
    if use_google and makes_sense:
        query = urllib.urlencode({'q' : t})
        url = GOOGLE_API % (query)
        search_results = urllib.urlopen(url)
        json = simplejson.loads(search_results.read())
        makes_sense = len(json['responseData']['results'])
    
    return makes_sense

def procTerm(t,ctx=[],nps=[]):
    """
    Processes the input term in order to merge everything separated by the 'of'
    preposition and generate contexts from anything else than the left-most
    head noun term.
    """

    head, contexts, nouns = '', set(ctx), set(nps)
    np, cx = '', {'TYPE' : None, 'VALUE' : None}
    for word in t.split():
        if word in STOPWORDS:
            continue
        if word.lower() != 'of' and word.lower() in PREPS:
            # context type assignment
            if head and np and cx['TYPE']:
                cx['VALUE'] = np.strip()
                contexts.add((cx['TYPE'],cx['VALUE']))
            elif not head and np:
                head = np.strip()
            cx = {'TYPE' : word, 'VALUE' : None}
        elif word.lower() == 'of':
            # adding to the noun phrase
            np += ' ' + word
        else:
            # adding single noun terms to the list
            nouns.add(word)
            np += ' ' + word
    # adding possibly last context value
    if cx['TYPE'] and not cx['VALUE']:
        cx['VALUE'] = np.strip()
    if cx['TYPE'] and cx['VALUE']:
        contexts.add((cx['TYPE'],cx['VALUE']))
    # a single noun phrase with no 'of' and no contexts
    if not head:
        head = t
    # adding the compund noun phrases
    nouns.add(head)
    for ct, cv in contexts:
        nouns.add(cv)
    return head, contexts, nouns

def callExtRE(text,prov_tit,np2doc,address=('140.203.155.44',17175)):
    """
    Calls an external relation extraction module, otherwise similar to the 
    native extractRels() implementation (namely regarding the produced output).
    """

    np2freq, triples_raw = {}, ''
    try:
        prov_id = hashlib.sha1(prov_tit).hexdigest()
    except UnicodeEncodeError:
        sys.stderr.write('Unicode error occurred, not processing the file!\n')
        return {}, np2doc
    for sentence in nltk.sent_tokenize(text):
        # the body - binding and closing the socket for each sentence
        try:
            sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            sock.connect(address)
            sock.send(sentence.strip()+'\n')
            triples_raw += sock.recv(2*len(sentence))
            sock.close()
        except:
            sys.stderr.write('\nConnection refused on address: '+`address`+'\n')
            return {}, np2doc
    triples = map(lambda x: tuple(x.split('\t')[:3]), triples_raw.split('\n'))
    if not len(triples):
        sys.stderr.write('Empty relation set!\n')
        return {}, np2doc
    rels_raw = []
    for st, pt, ot in triples:
        s, ctx, nps = procTerm(st)
        p = lemmatise(pt.replace('_',' '),'v')
        o, ctx, nps = procTerm(ot,ctx,nps)
        if not makesSense(s) or not makesSense(o):
            # do not process nonsense
            continue
        # updating the indices
        for lemma in map(lemmatise,nps):
            if np2freq.has_key(lemma):
                np2freq[lemma] += 1
            else:
                np2freq[lemma] = 1
            if np2doc.has_key(lemma):
                np2doc[lemma].add(prov_id)
            else:
                np2doc[lemma] = set([prov_id])
        # updating the relations list
        rels_raw.append(s,p,o,ctx)
    # generating the relations
    sz = reduce(lambda x,y: x+y, np2freq.values())
    subjects, objects, relations = set(), set(), {}
    for s, p, o, ctx in rels_raw:
        subjects.add(s)
        objects.add(o)
        r = Relation(s,p,o,prov_tit, 1.0) # flags['CERTAINTY'])
        f1, f2 = 0.0, 0.0
        if np2freq.has_key(r.getSubject()):
            f1 = np2freq[r.getSubject()]
        else:
            f1 = np2freq[lemmatise(r.getSubject().split(' of ')[0].strip())]
        if np2freq.has_key(r.getObject()):
            f2 = np2freq[r.getObject()]
        else:
            f2 = np2freq[lemmatise(r.getObject().split(' of ')[0].strip())]
        r.setTF((f1+f2)/float(2*sz))
        for ctx_type, ctx_value in ctx:
            r.setContext(ctx_type,ctx_value)
        relations[r.getKey()] = r
    relations = getImpliedRelations(relations,subjects,prov_tit,np2freq,sz)
    relations = getImpliedRelations(relations,objects,prov_tit,np2freq,sz)
    return relations, np2doc

def extractRels(text,prov_tit,np2doc):
    """
    Extracts triples from a single document, updating the np2doc inverted 
    index (lemmatised noun phrases to sets of files containing them). Returns 
    a list of relation objects and the updated index. 
    """

    print 'EUREEKA/extraction.extract, document:', prov_tit
    print '...sentence and word tokenisation...'
    tokenised = [nltk.word_tokenize(x) for x in nltk.sent_tokenize(text)]
    print '...POS tagging...'
    tagged = [nltk.pos_tag(x) for x in tokenised]
    print '...NP chunking...'
    chunked = [chunker_npp.parse(x) for x in tagged]
    print 'DEBUG -- chunked sentences:'
    print chunked
    print '...building frequency index of raw single NPs...'
    
    try:
        prov_id = hashlib.sha1(prov_tit).hexdigest()
    except UnicodeEncodeError:
        sys.stderr.write('Unicode error occurred, not processing the file!')
        return {}, np2doc
    
    np2freq = defaultdict(int)
    np2doc_dfd = defaultdict(set)
    np2doc_dfd.update(np2doc)
    
    for t in [chunker_npr.parse(x) for x in tagged]:
        for np in [x for x in t[:] if isinstance(x,Tree)]:
            # updating indices for a compound NP
            np_lemma = lemmatise(' '.join(x[0] for x in np.leaves()).lower())            
            np2freq[np_lemma] += 1            
            np2doc_dfd[np_lemma].add(prov_id)
                
            for np_simple in [lemmatise(x[0].lower()) for x in np.leaves() if x[1][:2] == 'NN']:
                # updating indices for simple NPs
                np2freq[np_simple] += 1
                np2doc_dfd[np_simple].add(prov_id)
    
    np2doc.update(np2doc_dfd)
    np2freq = dict(np2freq)
                
    relations = {} # relation objects indexed by (s,p,o) to prevent duplicates
    print '...extracting relations from chunked sentences...'
    
    for t in chunked:
        processChunk(t,relations,prov_tit,np2freq)
    return relations, np2doc

def processChunk(t,relations,prov_tit,np2freq):
    """
    Given a chunked tree of a sentence, processes it into a list of relations.
    np2freq is used to determine the term frequencies of relations.
    """

    # init state and spo container
    state, spo = 0, {'S':None, 'P':None, 'O':None}
    # process the chunked sentence sequentially
    for elem in t[:]:
        if state == 0:
            # do nothing until a NP is reached
            if isinstance(elem,Tree):
                state, spo = 1, {'S':elem, 'P':None, 'O':None}
        else:
            if isinstance(elem,Tree):
                # finalise the triple and re-init
                if spo['P']:
                    spo['O'] = elem
                    relations = getRelations(spo,relations,prov_tit,np2freq)
                state, spo = 0, {'S':elem, 'P':None, 'O':None}    
            else:
                # collect the verb part, or re-init if non-verbs encountered
                if not elem[1][:2].upper() in ['MD','VB','CC','RB']:
                    state, spo = 0, {'S':elem, 'P':None, 'O':None}
                else:
                    if not spo['P']:
                        spo['P'] = [elem]
                    else:
                        spo['P'].append(elem)
    #relations = getRelations(spo,relations,prov_tit,np2freq)
    return relations

def getRelations(spo,relations,prov_tit,np2freq):
    """
    Given a (NP, verb-part list, NP) structure and np2freq, it updates
    the relations dictionary.
    """

    # getting the size of np2freq
    sz = reduce(lambda x,y: x+y, np2freq.values())
    # getting predicate verbs and flags
    predicates, flags = getPredicates(spo['P'])
    #print 'DEBUG -- predicates:', `predicates`
    if not predicates:
        # do not proceed if predicates are empty
        return relations
    # raw NPs (without prepositions) to form subjects
    subj_snp = filter(lambda x: isinstance(x,Tree),\
    chunker_npr.parse(spo['S'].leaves())[:])
    # raw NPs (with prepositions) to form objects
    obj_snp = filter(lambda x: isinstance(x,Tree),\
    chunker_nps.parse(spo['O'].leaves())[:])
    subjects, obj2ctx, pred_prep = [], {}, None
    for stree in subj_snp:
        subjects.append(reduce(lambda x,y: x+' '+y, \
        map(lambda x: x[0], stree.leaves())))
    #print 'DEBUG -- object candidates:', `obj_snp`
    for otree in obj_snp:
        # processing conjuncts
        sng_obj = chunker_npr.parse(otree.leaves())
        np, ctx, obj = '', None, None
        for item in sng_obj[:]:
            # processing particular non-preposition nouns
            if isinstance(item,Tree):
                np_local = reduce(lambda x,y: x+' '+y, \
                map(lambda x: x[0], item.leaves()))
                if len(np) > 2 and np[-2:].lower() == 'of':
                    # appending to an 'of' compound NP
                    np += ' ' + np_local
                else:
                    np = np_local
            elif item[0].lower() == 'of' and np:
                np += ' ' + item[0]
            else:
                #if not np:
                #    pred_prep = item[0].lower()
                #else:
                if not ctx:
                    obj2ctx[np], obj = {}, np
                else:
                    obj2ctx[obj][ctx] = np
                ctx = item[0].lower()
        if np:
            # flushing the last one
            if ctx:
                obj2ctx[obj][ctx] = np
            else:
                obj2ctx[np], obj = {}, np
    #print 'DEBUG -- subjects:', `subjects`
    # generate the directly extracted relations
    for subj in subjects:
        if not makesSense(subj):
            # do not process nonsense
            continue
        for pred in predicates:
            for obj in obj2ctx:
                if not makesSense(obj):
                    # do not process nonsense
                    continue
                r = Relation(subj,pred,obj,prov_tit,flags['CERTAINTY'])
                f1, f2 = 0.0, 0.0
                if np2freq.has_key(r.getSubject()):
                    f1 = np2freq[r.getSubject()]
                else:
                    f1 = \
                    np2freq[lemmatise(r.getSubject().split(' of ')[0].strip())]
                if np2freq.has_key(r.getObject()):
                    f2 = np2freq[r.getObject()]
                else:
                    f2 = \
                    np2freq[lemmatise(r.getObject().split(' of ')[0].strip())]
                r.setTF((f1+f2)/float(2*sz))
                for ctx in obj2ctx[obj]:
                    r.setContext(ctx,obj2ctx[obj][ctx])
                relations[r.getKey()] = r
    # generate relations implied among subjects/objects (is a and not is a)
    relations = getImpliedRelations(relations,subjects,prov_tit,np2freq,sz)
    relations = getImpliedRelations(relations,obj2ctx.keys(),prov_tit,\
    np2freq,sz)
    return relations

def getPredicates(wt):
    """
    Processes the input list of tagged words and produces a list of predicates
    together with a respective flag dictionary (indicating certainty and 
    activeness/passiveness).
    """
    
    predicates, flags, maybe_p = [], {'CERTAINTY':1.0, 'ACTIVE':True}, False
    predicate_prep = ''
    #if len(wt) and wt[-1][1].upper() in ['TO', 'IN']:
    #    predicate_prep = wt[-1][0].lower()
    for word, tag in wt:
        if tag.upper()[:2] not in ['VB','RB','MD','IN','CC']:
            return [], flags
        if tag.upper()[:2] == 'IN':
            predicate_prep = word.lower()
        if tag.upper()[:2] == 'MD':
            flags['CERTAINTY'] *= 0.9
        if tag.upper() == 'MD*' or word.lower() in ['not', "n't"]:
            flags['CERTAINTY'] *= -1.0
        if tag.upper()[:2] == 'VB' and word.lower() not in \
        ['be', 'is', 'are', 'was', 'were', "isn't", "aren't", "wasn't", \
        "weren't", 'has', 'have', 'had', "hasn't", "haven't", "hadn't", \
        'say', 'says', 'said', 'saying']:
            if not word in predicates:
                predicates.append(word)
        #if maybe_p and tag.upper() in ['VBN', 'VBD'] and word.lower() not in \
        #['be', 'is', 'are', 'was', 'were']:
        #    flags['ACTIVE'] = False
        #    predicates.append(word)
    if predicate_prep:
        predicates = map(lambda x: x + ' ' + predicate_prep, predicates)
    return predicates, flags

def getImpliedRelations(relations,nps,prov_tit,np2freq,sz):
    """
    Based on the input noun phrase list, generates the implied relations 
    (typeof stuff between <JJ.*>*<NN.*>+ elements, disjointness between each
    of the members).
    """

    for np1 in nps:
        # produce the <JJ.*>*<NN.*>+ subtyping
        f = 0.0
        if np2freq.has_key(lemmatise(np1)):
            f = np2freq[lemmatise(np1)]
        else:
            f = np2freq[lemmatise(lemmatise(np1).split(' of ')[0].strip())]
        tf = f/float(sz)
        #print 'DEBUG -- base noun phrase:', np1
        #print 'DEBUG -- base noun phrase lemma:', lemmatise(np1)
        #print 'DEBUG -- implied relation TF (pos. type):', `tf`
        spl = np1.split()
        if len(spl) > 1 and 'of' not in spl:
            while len(spl) > 1:
                s = reduce(lambda x,y: x+' '+y, spl)
                o = reduce(lambda x,y: x+' '+y, spl[1:])
                r = Relation(s,'type',o,prov_tit,1.0)
                r.setTF(tf)
                relations[r.getKey()] = r
                spl = spl[1:]
        for np2 in nps:
            if np1 == np2:
                continue
            # produce the disjoints
            r = Relation(np1,'type',np2,prov_tit,-1.0)
            f1, f2 = 0.0, 0.0
            if np2freq.has_key(r.getSubject()):
                f1 = np2freq[r.getSubject()]
            else:
                f1 = \
                np2freq[lemmatise(r.getSubject().split(' of ')[0].strip())]
            if np2freq.has_key(r.getObject()):
                f2 = np2freq[r.getObject()]
            else:
                f2 = \
                np2freq[lemmatise(r.getObject().split(' of ')[0].strip())]
            r.setTF((f1+f2)/float(2*sz))
            relations[r.getKey()] = r
    return relations

def trimRels(relations,np2doc,base=10,t1=0.005,t2=0.1,base_cert=0.7):
    """
    Given a list of relations and np2doc inverted index, trim insignificant 
    relations off.
    """

    # computing the number of documents according to the index
    corp_size = len(reduce(lambda x,y: x | y, np2doc.values(),set()))
    # getting the absolute TF-IDF values (logarithmed to make them shallower)
    abs_scores, p2freq = {}, {}
    rlen, i = len(relations), 0
    for key in relations:
        i += 1
        print 'Trimming the relations, ', `i`, '. out of ', `rlen`
        overlap_sz = 1
        if np2doc.has_key(key[0]) and np2doc.has_key(key[2]):
            overlap_sz = len(np2doc[key[0]] & np2doc[key[2]])
        idf = log(corp_size/(1.0+overlap_sz),base)
        abs_scores[key] = log(1.0+idf*relations[key].getTF(),base)
        if p2freq.has_key(key[1]):
            p2freq[key[1]] += 1
        else:
            p2freq[key[1]] = 1
    # producing normalised predicate frequency values (logarithming the stuff
    # first)
    for p in p2freq:
        p2freq[p] = log(1.0+p2freq[p],base)
    mx_pf = max(p2freq.values())
    for p in p2freq:
        p2freq[p] /= mx_pf
    mx_sc = max(abs_scores.values())
    trimmed = {}
    for key in abs_scores:
        sc = abs_scores[key]/mx_sc
        if sc < t1 or p2freq[key[1]] < t2:
            # discard relations with norm. score or pred. freq. < threshold
            continue
        k = 1.0
        if p2freq[key[1]] < 0.05:
            # predicate frequency-dependet quotient - lower it when the
            # relation is too infrequent (less than half of the max. frequent)
            k = 0.8
        trimmed[key] = relations[key]
        sign = 1.0
        if trimmed[key].getCertainty() < 0:
            sign = -1.0
        cert = sign*(base_cert + \
        fabs(trimmed[key].getCertainty())*sc*k*(1.0-base_cert))
        trimmed[key].setCertainty(cert)
    return trimmed

# === functions END ===

# === classes BEGIN ===

# === classes END ===

if __name__ == "__main__":
    pass

