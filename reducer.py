#!/usr/bin/env python

import sys
import string
from operator import itemgetter

currword  = None
currcount = 0
word = None
doc = None
currdoc = None
occurences = []
stop_words = []

# Read the stop words
for arg in sys.argv:
	if arg == sys.argv[0]:
		continue
	stop_words.append(arg)
	

for line in sys.stdin.readlines():
        line = line.strip()
        
        try:
                word, doc, count, line, pos = line.split()
        except ValueError as e:
                print "ValueError: " + str(e)
                continue
	
	# Ignore stop words
	if word in stop_words:
		continue

        count = int(count)
        if word == currword:
                currcount += count
                occurences.append(str(doc) + "-" + str(line) + "-" + str(pos))
        else:
                if currword != None and currword != "":
			print "%s\t%s" % (currword, currcount),
                       	for occurence in occurences:
                               	print "\t%s" % (occurence),
                       	print ""
                currcount = count
                currword  = word
                occurences = []
                occurences.append(str(doc) + "-" + str(line) + "-" + str(pos))

if word == currword:
       	print "%s\t%s" % (currword, currcount),
       	for occurence in occurences:
               	print "\t%s" % (occurence),
	print "\n"
