#!/usr/bin/python

import sys

# if we have an argumeng, print it as fst
if len(sys.argv) > 1:
	for i, c in enumerate(sys.argv[1]):
		print("%d %d %s %s" % (i, i+1, c, c))
	print(len(sys.argv[1]))
	sys.exit(0)

# otherwise, make the edit transducer
alphabet = "abcdefghijklmnopqrstuvwxyz"

# write symbol table to stderr
sys.stderr.write('eps 0\n')
for i, c in enumerate(alphabet):
	sys.stderr.write("%s %d\n" % (c, i+1))

weight = {
    "d": 1.0,
    "i": 1.0,
    "s": 1.0
}

# no edit
for l in alphabet:
    print "0 0 %s %s %.3f" % (l, l, 0)

# deletes: input character, output epsilon
for l in alphabet:
    print "0 0 %s eps %.3f" % (l, weight["d"])

# insertions: input epsilon, output character
for l in alphabet:
    print "0 0 eps %s %.3f" % (l, weight["i"])

# substitutions: input one character, output another
for l in alphabet:
    for r in alphabet:
        if l is not r:
            print "0 0 %s %s %.3f" % (l, r, weight["s"])

# Final state
print 0
