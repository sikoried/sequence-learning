#!/usr/bin/python

import string
import sys

prompts = {}
with open(sys.argv[1]) as pf:
	for line in pf:
		if line.startswith(';'):
			continue
		# string.punctation = !"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~
		w = line.lower().translate(string.maketrans("",""), "!#$%&\"()*+,/:;<=>?@[\\]^`{|}").split()
		if w[-2].endswith('.'):
			w[-2] = w[-2][:-1]
		utt, txt = w[-1], " ".join(w[:-1])
		# print >>sys.stderr, "%s %s" % (utt, txt)
		prompts[utt] = txt

for line in sys.stdin:
	# test-dr4-mlll0-sx283.wav
	a = line[:-5].split('-')
	print "%s %s" % (line.strip(), prompts[a[-1]])
