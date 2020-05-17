#!/usr/bin/env python2.7

# Kindle Highlights/Notes Regex
# June 4 2017 
# Credit to https://stackoverflow.com/q/16947390 for a solid start

import re
import codecs
from datetime import datetime

import sys
# Need to do this so that you can redirect the output in bash
sys.stdout=codecs.getwriter('utf-8')(sys.stdout)


# Custom object for quotation
class Quote:
    def __init__(self,quote,location,timestring):
        self.quote = quote
        self.location = location
        self.timestring = timestring
    def __repr__(self):
        return repr((self.quote, self.location, self.timestring))
    def md_point(self):
        ''' Return markdown bullet point '''
        return '  * %s [%s, p. %d]'%(self.quote.strip(), self.timestring, self.location)

# Custom dictionary for storing quotes

class Knote(dict):
    def __init__(self, *args, **kwags):
        self['note'] = []
        self['location'] = []
        self['time'] = []

in_file = "clip.txt"

#read_file = open(in_file, 'r', encoding='utf8')

read_file = codecs.open(in_file, 'r', encoding = 'utf-8-sig')

file_lines = read_file.readlines()
read_file.close()
raw_note = "".join(file_lines)
raw_note = raw_note.split("==========")

# Save notes in dictionary by title
dnotes = {}

# Regex Pieces
title_author_regex = "(.+) \((.+)\)\r*\n"
location_regex = ".+?(?=Location|page)([A-z]+)\s([1-9-\-]+)"
date_regex = ".+?(?=Added\son)Added\son\s([a-zA-Z]+),\s([a-zA-Z]+)\s([0-9]+),\s([0-9]+)\s"
time_regex = "([0-9]+):([0-9]+):([0-9]+)\s(AM|PM)"
content_regex = "\r*\n\r\n(.*)"

# Compile Regex
regex_string =\
               title_author_regex +\
               location_regex +\
               date_regex +\
               time_regex +\
               content_regex 
regex = re.compile(regex_string)

verbose = True
verbose = False


for note in raw_note:
    rx = regex.findall(note)
    
    if len(rx)>0:
        #print rx
        # Citation is title+author
        rnote = rx[0]
        title = rnote[0].replace(u'\ufeff','')
        author = rnote[1]
        cite = '%s (%s)'%(title,author)
        if not (cite in dnotes.keys()):
            dnotes[cite] = []

        loc = rnote[3].split('-')
        loc = loc[0]
        tstr = "%s %s %s"%(rnote[5],rnote[6],rnote[7])
        dnotes[cite].append(Quote(rnote[12],int(loc),tstr))
    if verbose:
        print note
        print rx
        print "\n\n--------------------------\n\n"

# Sort by locatio
for k in dnotes.keys():
    dnotes[k] =sorted(dnotes[k], key=lambda quote: quote.location)

# Print Markdown

for k in dnotes.keys():
    print "\n# %s \n"%k
    for q in dnotes[k]:
        print q.md_point()
    
    
