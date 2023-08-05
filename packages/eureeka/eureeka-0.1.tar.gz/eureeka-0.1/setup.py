#!/usr/bin/python

from distutils.core import setup

setup(name='eureeka',
      version='0.1',
      description='EUREEKA knowledge store, inference engine and scripts',
      author='Vit Novacek',
      author_email='vit.novacek@deri.org',
      url='http://www.deri.org/',
      packages=['eureeka'],
      scripts=['scripts/kbm.py','scripts/eureekad.py','scripts/ext.py','scripts/pdf2txt.py','scripts/txt2xml.py','scripts/que.py'],
      requires=['nltk (>0.9.9)','rdflib','dbus (>=0.82.4)','MySQLdb','gobject','pdfminer']
     )
