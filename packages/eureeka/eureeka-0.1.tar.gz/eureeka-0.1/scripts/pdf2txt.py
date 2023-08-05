#!/usr/bin/python

"""
pdf2txt.py - a script for conversion of PDF documents to text

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

import sys, os
from pdfminer.pdfparser import PDFDocument, PDFParser
from pdfminer.pdfinterp import PDFResourceManager, process_pdf
from pdfminer.pdfdevice import PDFDevice
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams

if __name__ == "__main__":
    print '*** PDF to text converter ***'
    inpdir, outdir = sys.argv[1], sys.argv[2]
    # debug option
    debug = 0
    # input option
    password = ''
    pagenos = set()
    maxpages = 0
    # output option
    outfile = None
    outtype = None
    codec = 'utf-8'
    pageno = 1
    scale = 1
    laparams = LAParams()
    PDFResourceManager.debug = debug
    PDFDocument.debug = debug
    PDFParser.debug = debug
    PDFDevice.debug = debug
    outtype = 'text'
    files = filter(lambda x: os.path.isfile(x) and \
    x.split('.')[-1].lower() == 'pdf', \
    map(lambda x: os.path.join(inpdir,x), os.listdir(inpdir)))
    i = 0
    for fname in files:
        i += 1
        print 'Processing the file:', fname
        print '  (', `i`, 'out of', `len(files)`, ')'
        outfile = os.path.basename(fname).lower().rstrip('pdf') + 'txt'
        outfp = open(os.path.join(outdir,outfile), 'w')
        rsrc = PDFResourceManager()
        device = TextConverter(rsrc, outfp, codec=codec, laparams=laparams)
        fp = open(fname, 'rb')
        try:
            process_pdf(rsrc, device, fp, pagenos, maxpages=maxpages, \
            password=password)
        except:
            sys.stderr.write('\nWarning: an error in file: '+fname+'\n')
        device.close()
        outfp.close()
        fp.close()
