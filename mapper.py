#!/usr/bin/env python
import sys
import string
import os

currfp   = None
currf    = None

for line in sys.stdin:
	# Since this is streaming, we need to get the input file from the environment
	try:
		if currfp == None or currfp != os.environ['mapreduce_map_input_file']:
			currfp = os.environ['mapreduce_map_input_file']
			currfpl = currfp.split('/')
			currf = currfpl[-1].split('.')[0]
			#currfps = currfpl[len(currfpl) - 1].split('.')
			#currf = currfps[0]
	except ValueError:
		if currfp == None or currfp != os.environ['map_input_file']:
			currf = os.environ['map_input_file']
			currfpl = currfp.split('/')
			currf = currfpl[-1].split('.')[0]
			#currfps = currfpl[len(currfpl) - 1].split('.')
			#currf = currfps[0]

       	wordpos = 0
       	line = line.strip()
       	words = line.split()

       	for word in words:
		if wordpos == 0:
			linenum = word
			wordpos += 1
			continue
		
               	# Ignore case and punctuation
               	word = word.lower()
               	word = word.translate(None, string.punctuation)

               	# Ignore blank words
               	if word == "" or word == None:
                       	continue
                
               	# Write to output file
               	print '%s\t%s\t%s\t%s\t%s' % (word, currf, 1, linenum, wordpos)
		wordpos += 1
