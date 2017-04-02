#!/usr/bin/env python
import sys
import string
import os

for line in sys.stdin:
       	line = line.strip()
       	words = line.split()
	wordpos = 0

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
               	print '%s\t%s' % (word, 1)
		wordpos += 1
