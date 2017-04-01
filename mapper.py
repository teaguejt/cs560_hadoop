#!/usr/bin/env python
import sys
import string
import os

linenum = 0
currfp   = None
currf    = None

for line in sys.stdin:
	# Since this is streaming, we need to get the input file from the environment
	try:
		if currfp == None or currfp != os.environ['mapreduce_map_input_file']:
			linenum = 0
			currfp = os.environ['mapreduce_map_input_file']
			currfpl = currfp.split('/')
			currf = currfpl[-1].split('.')[0]
			#currfps = currfpl[len(currfpl) - 1].split('.')
			#currf = currfps[0]
	except ValueError:
		if currfp == None or currfp != os.environ['map_input_file']:
			linenum = 0
			currf = os.environ['map_input_file']
			currfpl = currfp.split('/')
			currf = currfpl[-1].split('.')[0]
			#currfps = currfpl[len(currfpl) - 1].split('.')
			#currf = currfps[0]
		

       	linenum += 1
       	wordpos = 0
       	line = line.strip()
       	words = line.split()

       	for word in words:
               	wordpos += 1
               	# Ignore case and punctuation
               	word = word.lower()
               	word = word.translate(None, string.punctuation)

               	# Ignore blank words
               	if word == "" or word == None:
                       	continue
                
               	# Write to output file
               	print '%s\t%s\t%s\t%s\t%s' % (word, currf, 1, linenum, wordpos)
