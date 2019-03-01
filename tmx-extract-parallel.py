#!/usr/bin/env python3

# Adapted from Apertium TMX tools
# http://wiki.apertium.org/wiki/Tools_for_TMX
#
# Extract parallel segments from tmx file using sax parser
# so we can stream very large files

from xml.sax import make_parser
from xml.sax.handler import ContentHandler
from optparse import OptionParser

import codecs
import sys
import re

version = "0.0.1"

class TMXHandler(ContentHandler):
        
        def __init__ (self, slang, tlang):
                self.pair = set([slang, tlang])
                self.inTag = ''
                self.note = ''
                self.tuid = ''
                self.type = ''
                self.cur_pair = set()	
                self.cur_lang = ''
                self.seg = {}
                self.seg[slang] = ''
                self.seg[tlang] = ''

        def startElement(self, name, attrs): 
                
                if name == 'tu':  
                        self.cur_pair = set()	
                        self.inTag = 'tu'
                        self.tuid = attrs.get('tuid','')
                        self.type = attrs.get('datatype','')
                elif name == 'note': 
                        self.inTag = 'note'
                        self.note = ""
                elif name == 'tuv': 
                        self.inTag = 'tuv'
                        self.cur_lang = attrs.get('xml:lang', '')
                        self.cur_pair.add(self.cur_lang)
                elif name == 'seg': 
                        self.inTag = 'seg'
                        if self.cur_lang in self.pair: 
                                self.seg[self.cur_lang] = ''

        def characters (self, c): 
                if self.inTag == 'note': 
                        self.note += c
                elif self.inTag == 'seg' and self.cur_lang in self.pair: 
                        self.seg[self.cur_lang] += c

        def endElement(self, name): 
                if name == 'tu' and self.pair == self.cur_pair: 

                        # hackish but whatever
                        for lang in self.cur_pair:
                                
                                # need to strip any newlines in segment?
                                if(options.lineclean):
                                        curseg = re.sub('\s+', ' ', self.seg[lang].strip().replace('\n', ' '))
                                else:
                                        curseg = self.seg[lang].strip()

                                if lang == options.srclang:
                                        srcout.write("%s\n" % curseg)
                                if lang == options.tgtlang:
                                        tgtout.write("%s\n" % curseg)
                        
if __name__ == '__main__':

    # Parse command line
    cl = OptionParser(version="%prog " + version)

    cl.add_option("-b", "--base", dest="base", help="base output filename")
    cl.add_option("-s", "--srclang", dest="srclang", help="source language")
    cl.add_option("-t", "--tgtlang", dest="tgtlang", help="target language")
    cl.add_option("-c", "--clean", dest="lineclean", help="clean newlines, spaces", action="store_true")

    (options, args) = cl.parse_args()

    parser = make_parser()

    # open output files
    srcout = codecs.open("%s.%s" % (options.base, options.srclang), 
                         "w", "utf-8")
    tgtout = codecs.open("%s.%s" % (options.base, options.tgtlang), 
                         "w", "utf-8")

    curHandler = TMXHandler(options.srclang, options.tgtlang)

    parser.setContentHandler(curHandler)

    parser.parse(sys.stdin)


