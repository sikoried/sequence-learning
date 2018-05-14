#!/usr/bin/python

import re
import sys

phones = set()

# we're ignoring the stress markers (1, 2)

for l in sys.stdin:
	if l.startswith(';'):
		continue
	l = re.sub('[0-9/]', '', l.strip()).split()
	for p in l[1:]:
		phones.add(p)
	print "%s\t%s" % (l[0], " ".join(l[1:]))

for p in sorted(phones):
	print >>sys.stderr, "%s 3" % p
