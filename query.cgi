#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import cgi
import sys

# enable debugging
import cgitb
cgitb.enable()

print "Content-Type: text/html"
print

form = cgi.FieldStorage()
d = form.getvalue('search')

print "<body><h1 style= 'color: green; line-height:2;'>Shakespeare Search:</h1></body>"

if not d:
  print "<h2 style= 'color: red;'>Please enter search terms.</h2>"
  print "<a href='http://web.eecs.utk.edu/~cjacks53/projectII/projectII.html'><h2>Search again?</h2></a>"
  exit()
ws = d.split()
for i in range(len(ws)):
  ws[i] = ws[i].lower()

if len(ws) == 1 and ws[0] in ["and","or","not"]:
  if ws[0] == "and":
    print "<h2 style= 'color: red;'>Cannot search for operational word 'and' in text.</h2>"
    print "<a href='http://web.eecs.utk.edu/~cjacks53/projectII/projectII.html'><h2>Search again?</h2></a>"
    exit()
  if ws[0] == "not":
    print "<h2 style= 'color: red;'>Cannot search for operational word 'not' in text.</h2>"
    print "<a href='http://web.eecs.utk.edu/~cjacks53/projectII/projectII.html'><h2>Search again?</h2></a>"
    exit() 
  if ws[0] == "or":
    print "<h2 style= 'color: red;'>Cannot search for operational word 'or' in text.</h2>"
    print "<a href='http://web.eecs.utk.edu/~cjacks53/projectII/projectII.html'><h2>Search again?</h2></a>"
    exit() 

if len(ws) == 2 and "and" in ws:
  print "<h2 style= 'color: red;'>Must supply at least 2 words to search for on same line.</h2>"
  print "<a href='http://web.eecs.utk.edu/~cjacks53/projectII/projectII.html'><h2>Search again?</h2></a>"
  exit()
  
if "not" in ws:
  if len(ws) > 3:  
    print "<h2 style= 'color: red;'>Not only supports binary operations.</h2>"
    print "<a href='http://web.eecs.utk.edu/~cjacks53/projectII/projectII.html'><h2>Search again?</h2></a>"
    exit()
  if len(ws) == 2:
    print "<h2 style= 'color: red;'>Cannot return every line",ws[1],"is not on.</h2>"
    print "<a href='http://web.eecs.utk.edu/~cjacks53/projectII/projectII.html'><h2>Search again?</h2></a>"
    exit()

f = open("../projectII/fullindex.txt",'r')
data = f.readlines()
f.close

word = {}

for i in range(len(data)):
    line = data[i].strip()
    words = line.split()
    w = words[0]
    if w not in word.keys():
      word[w] = {}
    for j in range(2,len(words)):
      p = words[j].split('-')
      if p[0] not in word[w].keys():
        word[w][p[0]] = [[],[]]
      word[w][p[0]][0].append(p[1])
      word[w][p[0]][1].append(p[2])

t=0
if "and" in ws:
  sd = []
  print '<h2>Results for "%s":</h2>' % (d)
  while "and" in ws:
    ws.remove("and")
  if ws[0] in word.keys():
    docs = word[ws[0]].keys()
    for doc in docs:
      c=0
      for i in range(1,len(ws)):
        if ws[i] not in word.keys():
          print "<h3 style= 'color: red;'>Word not in text:",ws[i],"</h3>"
          exit()
        if doc in word[ws[i]].keys():
          c+=1
      if c == len(ws)-1:
        sd.append(doc)
      else:
        print "<h3 style= 'color: red;'>Words not found in same text.</h3>"
    for z in sd:
      for l in word[ws[0]][z][0]:
        c=0
        for i in range(1,len(ws)):
          if l in word[ws[i]][doc][0]:
            c+=1
        if c == len(ws)-1:
          sl = l
          print "<h3>Document name:",doc,"</h3>"
          print "<h3>Line #:",l,"<h3>"
          print "<br>" 
          t = 1
      if not t:
        print "<h3 style= 'color: red;'>Words not found on same line in text.</h3>"
  else:
    print "<h3 style= 'color: red;'>Word not in text:",ws[0],"</h3>"
    print ""
  print "<a href='http://web.eecs.utk.edu/~cjacks53/projectII/projectII.html'><h2>Search again?</h2></a>"
elif "not" in ws:
  print '<h2>Results for "%s":</h2>' % (d)
  ws.remove("not")
  if ws[0] in word.keys() and ws[1] in word.keys():
    docs = word[ws[0]].keys()
    for doc in docs:
      for i in range(len(word[ws[0]][doc][0])):
        if word[ws[0]][doc][0][i] not in word[ws[1]][doc][0]:
          line = word[ws[0]][doc][0][i]
          pos = word[ws[0]][doc][1][i]
          t = 1
          print "<h3>Document name:",doc,"</h3>"
          print "<h3>Line #:",line,"</h3>"
          print "<br>"
    if not t:
      print "<h3 style= 'color: red;'>Words only found on same line in text.</h3>"
  elif ws[1] not in word.keys():
    print "<h3 style= 'color: red;'>Word not in text:",ws[1],"<h3>"
  else:  
    print "<h3 style= 'color: red;'>Word not in text:",ws[0],"<h3>"
    print ""
  print "<a href='http://web.eecs.utk.edu/~cjacks53/projectII/projectII.html'><h2>Search again?</h2></a>"
else:
  print '<h2>Results for "%s":</h2>' % (d)
  while "or" in ws:
    ws.remove("or")
  for s in ws:
    print "<hr>"
    print "<h2>%s:</h2>" % (s)
    print ""
    if s in word.keys():
      docs = word[s].keys()
      for doc in docs:
        for i in range(len(word[s][doc][0])):
          line = word[s][doc][0][i]
          pos = word[s][doc][1][i]
          print "<h3>Document name:",doc,"</h3>"
          print "<h3>Line #:",line,"</h3>"
          print "<br>"
    else:
      print "<h3 style= 'color: red;'>Word not in text:",s,"</h3>"
      print ""
  print "<a href='http://web.eecs.utk.edu/~cjacks53/projectII/projectII.html'><h2>Search again?</h2></a>"
