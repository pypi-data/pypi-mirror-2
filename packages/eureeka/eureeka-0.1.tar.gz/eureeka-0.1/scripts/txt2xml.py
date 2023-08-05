#!/usr/bin/python

"""
txt2xml.py - script for conversion of raw text into XML (annotated by the 
title of the respective text)

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

import sys, os, getopt

def help():
    print 'txt2xml.py [-h | --help]           [-m | --map filename2title]'
    print '           [-d | --dir input directory]'
    print '  Converts text to XML with title annotations according to the'
    print '  provided filename2title  map (rows of the respective  tuples'
    print '  divided by tabulators). By default, the filename is selected'
    print '  for the title. The input directory  is supposed to   contain'
    print '  the text files to be converted (in the same location).'

FILE2NAME = {}
HEADER = """<?xml version="1.0" encoding="UTF-8"?>
<xml>
"""
FOOTER = """</doc>
</xml>
"""

def valchar(c):
    """
    Is the input character valid for XML?
    """

    OK = ['(',')','{','}','/','"',"'",'`',',','.',';',':','?','!','*','+','-']
    if (c.isalnum() or c.isspace() or c in OK) and ord(c) != 12:
        return True
    return False

def xmlval(text):
    """
    Make a XML-valid text out of the input.
    """
    valid = ''
    for c in text:
        if valchar(c):
            if ord(c) < 256:
                valid += c
            else:
                valid += `c`
    return valid

if __name__ == "__main__":
    optlist, args = getopt.getopt(sys.argv[1:], 'hm:d:', ['help','map=','dir='])
    action, dir = '', os.getcwd()
    for par, val in optlist:
        if par == '-m' or par == '--map':
            f = open(os.path.abspath(val),'r')
            for line in os.path.abspath(val):
                tabsep = line.split('#')[0].split('\t')
                if len(tabsep) >= 2:
                    FILE2NAME[tabsep[0].strip()] = tabsep[1].strip()
            f.close()
        if par == '-h' or par == '--help':
            action = 'HELP'
        if par == '-d' or par == '--dir':
            dir = os.path.abspath(val)
    if action == 'HELP':
        help()
    else:
        for fname in os.listdir(dir):
            path = os.path.join(dir,fname)
            if not (os.path.isfile(path) and path.endswith('.txt')):
                continue
            title = fname
            if FILE2NAME.has_key(fname):
                title = FILE2NAME[fname]
            text = open(path,'r').read()
            f = open(path+'.xml','w')
            f.write(HEADER+'\n')
            f.write('<doc title="'+title+'">\n')
            f.write(xmlval(text))
            f.write(FOOTER)
            f.close()
