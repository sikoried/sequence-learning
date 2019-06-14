#!/usr/bin/python

import sys

tks = list()

with open('toolkits.txt') as f:
	tks = f.read().splitlines()

from numpy import random

for i in range(int(sys.argv[1])):
	print random.choice(tks, size=2, replace=False)

