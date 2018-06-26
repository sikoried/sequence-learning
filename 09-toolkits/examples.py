#!/usr/bin/python

# usage: batches.py phones.txt 50 1 alis.txt

import sys

from operator import itemgetter

if len(sys.argv) != 4:
	print >>sys.stderr, "usage: %s <egs-size> <stride> <alis-txt>" % sys.argv[0]
	print >>sys.stderr, "  eg. %s 50 1 alis.txt" % sys.argv[0]
	sys.exit(1)

# number of output frames
nof = int(sys.argv[1])
stride = int(sys.argv[2])

# read labels, write to a list of (utt-key, [(phn, len), (phn, len) ...])
alis = list()
with open(sys.argv[3]) as f:
	for i, line in enumerate(f):
		# AAA_m159dxx0_000_AAA 1 4 ; 36 20 ; 29 5 ; 6 3  where tuples are (phn, len)
		utt, ali = line.strip().split(' ', 1)
		ali = map(int, ali.replace(' ;', '').split())  # remove ' ;', then split, then map to ints
		ali = zip(ali[::2], ali[1::2])  # [::2] is every other; [1::2] is every other starting at 1
		if len(ali) < nof:
			print >>sys.stderr, "Ignoring %d: %s since its too short (%d)" % (i, utt, len(ali))
			continue
		# looks good, make tuple (utt-key, [(phn, len), (phn, len) ...])
		alis.append((utt, ali))


# now make 'examples', ie. batches of output labels and corresponding
# frame indices of _input_ frames
egs = list()
for utt, ali in alis:
	i = 0
	offs = 0
	while i < len(ali) - nof:
		outs = ali[i:i+nof]
		labs = map(itemgetter(0), outs)
		egs_len = sum(map(itemgetter(1), outs))
		# utt-sub-key, [phn phn phn phn...], from-offset, to-offset
		egs.append((utt+'_'+format(i, '04d'), labs, offs, offs+egs_len))
		labels_to_skip = ali[i:i+stride]
		frames_to_skip = sum(map(itemgetter(1), labels_to_skip))
		offs += frames_to_skip
		i += stride

# print a list-like file
# utt-id from-mfcc to-mfcc labelseq
for utt, labs, fr, to in egs:
	print "%s %d %d %s" % (utt, fr, to, ' '.join(map(str, labs)))
