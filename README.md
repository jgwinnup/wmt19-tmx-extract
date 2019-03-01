# wmt19-tmx-extract

Extraction script for Paracrawl tmx files for use in WMT19

Adapted from Apertium TMX tools
http://wiki.apertium.org/wiki/Tools_for_TMX

use:

gzcat tmx.gz | ./tmx-extract-parallel.py -b <base filename> -s <src lang> -t <tgt lang> -c (optional - removes crlf in <seg>)


