#!/usr/bin/python

# usage: batches.py phones.txt 50 1 alis.txt

# sikoried, 6/22/2018

# read kaldi-style phone alignments
#   eg. ali-to-phones --write-lengths=true final.mdl 'ark:gunzip -c /ali.*.gz|' ark,t:alis.txt
#
# AAA_m159dxx0_000_AAA 1 4 ; 36 20 ; 29 5 ; 6 3 ; 42 3 ; 9 3 ; 38 3 ; 42 6 ; 17 15 ; 32 6 ; 30 7 ; 34 5 ; 11 6 ; 14 6 ; 41 9 ; 42 3 ; 26 3 ; 21 3 ; 11 3 ; 30 9 ; 12 3 ; 11 7 ; 29 17 ; 20 5 ; 11 4 ; 42 16 ; 38 9 ; 11 25 ; 1 21 ; 36 12 ; 37 9 ; 14 4 ; 42 4 ; 43 3 ; 21 3 ; 37 8 ; 18 7 ; 39 4 ; 40 3 ; 12 3 ; 10 6 ; 9 3 ; 14 3 ; 10 3 ; 26 6 ; 12 3 ; 38 5 ; 24 5 ; 14 5 ; 42 6 ; 9 26 ; 1 8 ; 14 9 ; 10 6 ; 43 3 ; 21 5 ; 11 4 ; 26 3 ; 9 13 ; 1 16 ; 36 12 ; 37 39 ; 1 9 ; 29 9 ; 21 19 ; 7 21 ; 12 10 ; 11 12 ; 1 5 ; 42 8 ; 21 15 ; 12 8 ; 38 10 ; 1 3 ; 21 22 ; 12 13 ; 11 11 ; 29 5 ; 9 6 ; 18 7 ; 40 4 ; 34 16 ; 24 3 ; 9 3 ; 38 10 
# ...
#
# and map them to "egs", fixed-output-length training examples for seq2seq
# training
#   eg. <utt-sub-key> <start-mfcc> <end-mfcc> <label-seq...>
#
# AAA_m159dxx0_000_AAA_0000 0 334 1 36 29 6 42 9 38 42 17 32 30 34 11 14 41 42 26 21 11 30 12 11 29 20 11 42 38 11 1 36 37 14 42 43 21 37 18 39 40 12 10 9 14 10 26 12 38 24 14 42
# AAA_m159dxx0_000_AAA_0001 334 690 36 29 6 42 9 38 42 17 32 30 34 11 14 41 42 26 21 11 30 12 11 29 20 11 42 38 11 1 36 37 14 42 43 21 37 18 39 40 12 10 9 14 10 26 12 38 24 14 42 9
# ...
#
# Expects `phones.txt` to verify that the alignments are ok. Note that since
# the `<eps>` "phone" is always 0, the label ids should be decreased by 1,
# depending on the downstream seq2seq library (in case of CTC, labels should
# start at 0).

import sys

from operator import itemgetter


if len(sys.argv) != 5:
	print >>sys.stderr, "usage: %s <phone-map> <egs-size> <stride> <alis-txt>" % sys.argv[0]
	print >>sys.stderr, "  eg. %s phone.txt 50 1 alis.txt" % sys.argv[0]
	sys.exit(1)

# read phone map; used to check for potential alignment errors (invalid symbols)
int2sym = dict()
with open(sys.argv[1]) as f:
	for line in f:
		p, i = line.strip().split()
		if p == '<eps>':
			continue
		# ignore disambiguation symbols; those are at the end of phones.txt
		elif p.startswith('#'):
			break
		int2sym[int(i)] = p

# find minimum and maximum phone ids to detect ali errors
minp = min(int2sym.keys())
maxp = max(int2sym.keys())

# number of output frames
nof = int(sys.argv[2])
stride = int(sys.argv[3])

# read labels, write to a list of (utt-key, [(phn, len), (phn, len) ...])
alis = list()
with open(sys.argv[4]) as f:
	for i, line in enumerate(f):
		# AAA_m159dxx0_000_AAA 1 4 ; 36 20 ; 29 5 ; 6 3  where tuples are (phn, len)
		utt, ali = line.strip().split(' ', 1)
		ali = map(int, ali.replace(' ;', '').split())  # remove ' ;', then split, then map to ints
		ali = zip(ali[::2], ali[1::2])  # [::2] is every other; [1::2] is every other starting at 1
		if len(ali) < nof:
			print >>sys.stderr, "Ignoring %d: %s since its too short (%d)" % (i, utt, len(ali))
			continue
		# diagnostics: verify that every phone in this alignment is ok
		if min(map(itemgetter(0), ali)) < minp or max(map(itemgetter(0), ali)) > maxp:
			m1 = min(map(itemgetter(0), ali))
			m2 = max(map(itemgetter(0), ali))
			print >>sys.stderr, "Ignoring invalid alignment in line %d: minp=%d min=%d max=%d maxp=%d %s %s" % (i, minp, m1, m2, maxp, utt, ' '.join(map(str, map(itemgetter(0), ali))))
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
