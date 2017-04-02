#!/usr/bin/env python

import sys
import string
from operator import itemgetter

currword  = None
currcount = 0
word = None

for line in sys.stdin.readlines():
        line = line.strip()
        
        try:
		word, count = line.split()
        except ValueError as e:
                print "ValueError: " + str(e)
                continue

        count = int(count)
        if word == currword:
                currcount += count
        else:
                if currword != None and currword != "":
                        if currcount > 1800:
				print "%s\t%s" % (currword, currcount)
                currcount = count
                currword  = word

if word == currword:
	if currcount > 1800:
        	print "%s\t%s" % (currword, currcount)
