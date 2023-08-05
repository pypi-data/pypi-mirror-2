"""
srvlib.py - library wrapping the essential EUREEKA functionalities into a
D-Bus server

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

import dbus, gobject
import dbus.service
import sys, cPickle, os.path, time
#from sets import Set
from rdflib.Graph import ConjunctiveGraph as Graph

#EUREEKA_HOME = '/home/eureeka/devel'
#sys.path.insert(0,os.path.join(EUREEKA_HOME,'lib'))
from eureeka.util import KWORD_MAP #, parseCFG, DEF_CFG
from eureeka.kb import KB

def isQuery(q):
    """
    A simple check whether the input could be a legal query or not.
    """

    isq = True
    for conjunct in q.split(KWORD_MAP['AND']):
        if len(conjunct.split(KWORD_MAP['SEP'])) != 3:
            isq = False
            break
    return isq

def relations2RDF(relations,format='xml'):
    gr = Graph()
    for r in relations:
        for triple in r.getTriples():
            gr.add(triple)
    return gr.serialize(format=format)

class EureekaServer(dbus.service.Object):

    def __init__(self, object_path, config):
        bus_name = \
        dbus.service.BusName('ie.deri.sw.smile.koraal.dbus.eureeka',\
        bus=dbus.SystemBus())
        dbus.service.Object.__init__(self, bus_name, object_path)
        self.cfg = config
        print '\n*** Initialising EureekaServer ***'
        self.kbase = KB(self.cfg)
        print '*** EureekaServer initialised ***'

    def __del__(self):
        # @TODO - check if this is OK
        loop = gobject.MainLoop()
        loop.quit()
        del self.kbase

    @dbus.service.method(dbus_interface=\
    "ie.deri.sw.smile.koraal.dbus.eureeka", in_signature="",out_signature="")
    def shutdown(self):
        self.__del__()

    @dbus.service.method(dbus_interface=\
    "ie.deri.sw.smile.koraal.dbus.eureeka",in_signature="s",out_signature="as")
    def askQuery(self,q):
        """
        Answers the query. 
        """

        sig, relations = None, []
        if not isQuery(q):
            sig = 'C'
            relations = \
            self.kbase.entities.getRelations([self.kbase.grounding.get(q)])
        else:
            sig = 'Q'
            relations = self.kbase.ask(q)
        return [sig,relations2RDF(relations)]

    @dbus.service.method(dbus_interface=\
    "ie.deri.sw.smile.koraal.dbus.eureeka",in_signature="s",out_signature="as")
    def extQuery(self,q):
        """
        Answers the query and extends the result according to the rules 
        associated with the knowledge base. 
        """

        sig, relations = None, []
        if not isQuery(q):
            sig = 'C'
            relations = \
            self.kbase.entities.getRelations([self.kbase.grounding.get(q)])
        else:
            sig = 'Q'
            relations = self.kbase.ask(q)
        ids = list(set(map(lambda x: \
        self.kbase.grounding.get(x.getSubject()),relations)))
        for r in self.kbase.extend(ids):
            relations.append(r)
        return [sig,relations2RDF(relations)]

    @dbus.service.method(dbus_interface=\
    "ie.deri.sw.smile.koraal.dbus.eureeka",in_signature="s",out_signature="as")
    def getPForS(self,subj):
        """
        Returns a list of possible property terms for the given subject term. 
        """

        s = self.kbase.grounding.get(subj)
        if not s:
            return []
        self.kbase.entities.cursor.execute("""SELECT DISTINCT predicate FROM
                                              entities WHERE subject=%s""",\
                                              (s,))
        return map(lambda x: self.kbase.grounding.get(x[0]), \
        self.kbase.entities.cursor.fetchall())

    @dbus.service.method(dbus_interface=\
    "ie.deri.sw.smile.koraal.dbus.eureeka",in_signature="s",out_signature="as")
    def getSForP(self,pred):
        """
        Returns a list of possible subject terms for the given predicate term. 
        """

        p = self.kbase.grounding.get(pred)
        if not p:
            return []
        self.kbase.entities.cursor.execute("""SELECT DISTINCT subject FROM
                                              entities WHERE predicate=%s""",\
                                              (p,))
        return map(lambda x: self.kbase.grounding.get(x[0]), \
        self.kbase.entities.cursor.fetchall())

    @dbus.service.method(dbus_interface=\
    "ie.deri.sw.smile.koraal.dbus.eureeka",in_signature="s",out_signature="as")
    def getOForP(self,pred):
        """
        Returns a list of possible object terms for the given predicate term. 
        """

        p = self.kbase.grounding.get(pred)
        if not p:
            return []
        self.kbase.entities.cursor.execute("""SELECT DISTINCT object FROM
                                              entities WHERE predicate=%s""",\
                                              (p,))
        return map(lambda x: self.kbase.grounding.get(x[0]), \
        self.kbase.entities.cursor.fetchall())

    @dbus.service.method(dbus_interface=\
    "ie.deri.sw.smile.koraal.dbus.eureeka",in_signature="ss",out_signature="as")
    def getOForSP(self,subj,pred):
        """
        Returns a list of possible object terms for the given subject and 
        predicate. 
        """

        s = self.kbase.grounding.get(subj), 
        p = self.kbase.grounding.get(pred,scope=self.kbase.grounding.REL_SCP)
        if not s or not p:
            return []
        self.kbase.entities.cursor.execute("""SELECT DISTINCT object FROM
                                              entities WHERE subject=%s AND 
                                              predicate=%s""",(s,p))
        return map(lambda x: self.kbase.grounding.get(x[0]), \
        self.kbase.entities.cursor.fetchall())

    @dbus.service.method(dbus_interface=\
    "ie.deri.sw.smile.koraal.dbus.eureeka",in_signature="s",out_signature="as")
    def getPForO(self,obj):
        """
        Returns a list of possible property terms for the given object term. 
        """

        o = self.kbase.grounding.get(obj)
        if not o:
            return []
        self.kbase.entities.cursor.execute("""SELECT DISTINCT predicate FROM
                                              entities WHERE object=%s""",(o,))
        return map(lambda x: self.kbase.grounding.get(x[0]), \
        self.kbase.entities.cursor.fetchall())

    @dbus.service.method(dbus_interface=\
    "ie.deri.sw.smile.koraal.dbus.eureeka",in_signature="ss",out_signature="as")
    def getSForOP(self,obj,pred):
        """
        Returns a list of possible subject terms for the given object and 
        predicate. 
        """

        o = self.kbase.grounding.get(obj)
        p = self.kbase.grounding.get(pred,scope=self.kbase.grounding.REL_SCP)
        if not o or not p:
            return []
        self.kbase.entities.cursor.execute("""SELECT DISTINCT subject FROM
                                              entities WHERE object=%s AND 
                                              predicate=%s""",(o,p))
        return map(lambda x: self.kbase.grounding.get(x[0]), \
        self.kbase.entities.cursor.fetchall())

    @dbus.service.method(dbus_interface=\
    "ie.deri.sw.smile.koraal.dbus.eureeka",in_signature="ss",out_signature="as")
    def getPForSO(self,subj,obj):
        """
        Returns a list of possible property terms for the given subject and
        object.
        """

        s, o = self.kbase.grounding.get(subj), self.kbase.grounding.get(obj)
        if not s or not o:
            return []
        self.kbase.entities.cursor.execute("""SELECT DISTINCT predicate FROM
                                              entities WHERE 
                                              subject=%s""",(s,))
        res1 = set(map(lambda x: x[0], self.kbase.entities.cursor.fetchall()))
        self.kbase.entities.cursor.execute("""SELECT DISTINCT predicate FROM
                                              entities WHERE 
                                              object=%s""",(o,))
        res2 = set(map(lambda x: x[0], self.kbase.entities.cursor.fetchall()))
        return map(lambda x: self.kbase.grounding.get(x), list(res1&res2))

    @dbus.service.method(dbus_interface=\
    "ie.deri.sw.smile.koraal.dbus.eureeka",in_signature="s",out_signature="as")
    def getSynonyms(self,t):
        """
        Returns synonyms of the input term. 
        """

        idx = self.kbase.grounding.get(t)
        if not idx:
            return []
        return filter(lambda x: x != None, map(lambda x: x[0], \
        self.kbase.grounding.getSynonyms(idx)))

