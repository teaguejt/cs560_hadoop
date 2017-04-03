#!/usr/bin/env python

import sys

ws = []
if len(sys.argv) > 2:
  for line in sys.stdin:
    d = line
    ws.extend(str(d).strip().split())
else:
  d = raw_input('Enter query: ')
  ws = str(d).strip().split()

if not ws:
  print "Please enter search terms."
  exit()
for i in range(len(ws)):
  ws[i] = ws[i].lower()

f = open("index.txt",'r')
data = f.readlines()
f.close

word = {}
count = {}

for i in range(len(data)):
    line = data[i].strip()
    words = line.split()
    # A situation can arise in which a blank line is encountered.
    # Account for this
    if len(words) == 0:
        continue;
    w = words[0]
    if w not in word.keys():
      word[w] = {}
      count[w] = words[1]
    for j in range(2,len(words)):
      p = words[j].split('-')
      if p[0] not in word[w].keys():
        word[w][p[0]] = [[],[]]
      word[w][p[0]][0].append(p[1])
      word[w][p[0]][1].append(p[2])

if ws:
  print ""
  print 'Results.'
  while "or" in ws:
    ws.remove("or")
  for s in ws:
    print "-------------------------"
    if s in word.keys():
        print "%s: %s occurences" % (s, count[s])
    else:
        print "%s: 0 occurences" % (s)
    print ""
    if s in word.keys():
      docs = word[s].keys()
      for doc in docs:
        for i in range(len(word[s][doc][0])):
          line = word[s][doc][0][i]
          pos = word[s][doc][1][i]
          print "Document name:",doc
          print "Line #:",line
          print ""
    else:
      print "Word not in text:",s
      print ""
