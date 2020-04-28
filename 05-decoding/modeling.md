---
template: page
title: Sequence Modeling with HMM
permalink: 05/decoding/
mathjax: true
---

> Note: Previous exercises revealed that it's hard to run these JSTK examples on Windows in lack of a proper shell (even using Linux on Windows) -- use a virtual machine with plenty of RAM and CPU and a linux distribution such as Ubuntu.


# Sequence Modeling with HMM

In this exercise, we'll build a very basic speech recognition system using the LDC [TIMIT](https://catalog.ldc.upenn.edu/LDC93S1) corpus:

>The TIMIT corpus of read speech is designed to provide speech data for acoustic-phonetic studies and for the development and evaluation of automatic speech recognition systems.
> TIMIT contains broadband recordings of 630 speakers of eight major dialects of American English, each reading ten phonetically rich sentences.
> The TIMIT corpus includes time-aligned orthographic, phonetic and word transcriptions as well as a 16-bit, 16kHz speech waveform file for each utterance.

We'll be _using_ JSTK from the commandline, putting things together using shell scripts/commands -- no "real" programming this week!


# LDC93S1

Start by downloading a copy of the dataset, located at `ml0.informatik.fh-nuernberg.de/~riedhammerko/ldc93s1.zip` (VPN!), unzip, and familiarize ( skim through `timit/readme.doc`).
We will be using all data (divided in training and test), as well as the audio and word-level transcriptions.


# Simple Digits

At the time of preparing this exercise, it made sense to use an actual speech data set.
However, compute times seem to be fairly long, so it might make sense to resort to the simple digits corpus of last week.
The steps to perform are the same, with the only difference being the alphabet and lexicon.

You can refer to [cmudict](https://github.com/cmusphinx/cmudict/blob/master/cmudict.dict) to get pronunciations (and thus alphabet) for the numbers.


# Setup

We will need to process a couple of files before we begin:

- Audio format adjustment (sphere to wav)
- List files for downstream processing
- Alphabet and lexicon
- Feature computation
- Language model estimation


## Adjust Audio Format

Unfortunately, the audio data is in [NIST sphere](https://www.ldc.upenn.edu/language-resources/tools/sphere-conversion-tools) format, which is hard to read.
Let's use `sox` to turn it into something useful, and while we're at it, rename them to something handy:

```bash
mkdir wav
for i in `find LDC93S1 -name "*.wav"`; do
	n=$(echo $i | perl -F/ -nlae 'print join "-", @F[2..$#F]')
	sox $i wav/$n
done
```


## Lists and Transcription

Let's assemble some file lists, and get the transcripts:

```bash
# file lists
(cd wav; /bin/ls > ../list.all)
grep ^train list.all > list.train
grep ^test list.all > list.test

# transcripts
cat list.all | ../gettext.py <(cat LDC93S1/timit/doc/prompts.txt | sed -e 's:~vpres:~v_pres:g' | sed -e 's:~vpast:~v_past:g') > list.all.trl
grep ^train list.all.trl > list.train.trl
grep ^test list.all.trl > list.test.trl
```


## Alphabet and Lexicon

A sequence decoding system is typically built in a hierarchical way:

- The _alphabet_ is a set of the smallest units.
	These _symbols_ are typically each modeled as an individual HMM; for speech, these are typically phonemes.
- The _lexicon_ describes the decodable units, which will be composed of _symbols_; for speech, these are typically words.

We'll use three states for each phone, and prepend a _silence_ word to the dictionary.

```bash
# prepend a silence word to the dictionary; 
# parse dict, write stdout to lex and stderr to alphabet
cat <(echo 'sil sil') <(echo '-- sil') LDC93S1/timit/doc/timitdic.txt | ../parsedict.py > timit.l 2> timit.a

# verify files...
head timit.[a,l]
```

```
==> timit.a <==
aa 3
ae 3
ah 3
ao 3
aw 3
ax 3
axr 3
ay 3
b 3
ch 3

==> timit.l <==
sil	sil
-- sil
bourgeoisie	b uh r zh w aa z iy
lined	l ay n d
simmered	s ih m axr d
teeny	t iy n iy
'em	ax m
-knacks	n ae k s
-upmanship	ah p m ax n sh ih p
-ups	ah p s
```

## Compute Features

Just like in the prior examples, we'll use our basic MFCC features.

```bash
mkdir ft
java com.github.sikoried.jstk.app.Mfcc --in-list list.all ft/ --dir wav/ -f t:wav/16 -w hamm,25,10 -b 188,6071,-1,.5 -d "5:1" --turn-wise-mvn
```

## Language Model Estimation

Use srilm to estimate a bi-gram model:

```bash
ngram-count -order 2 -text <(cut -d' ' -f 2- list.train.trl) -lm timit.bg.arpa -no-sos -no-eos

# alternatively: unigram
ngram-count -order 1 -text <(cut -d' ' -f 2- list.train.trl) -lm timit.ug.arpa -no-sos -no-eos
```


# Architecture

The figure below shows the general architecture for the JSTK packages.

![architecture overview](https://github.com/sikoried/jstk/raw/master/docs/architecture.png)

For sequence decoding, we need to compile the alphabet and lexicon into a configuration (basically the model files).
We'll allocate three Gaussians per state, and limit ourselves to monophones (phones without context).

```bash
# train a codebook, if semi-cont desired (see below)
num_gauss=256
num_gauss_iter=10
nj_gauss=0
java com.github.sikoried.jstk.app.Initializer --gmm cb.init -f -n $num_gauss -s sequential_50 --list list.train --dir ft/
java com.github.sikoried.jstk.app.GaussEM -i cb.init -o cb.em -l list.train -d ft/ -n $num_gauss_iter -p $nj_gauss

# monophone configuration, with shared codebook
java com.github.sikoried.jstk.arch.Configuration \
	--compile timit.a timit.l 0 \
	--semi cb.em \
	--write conf.xml conf.cb.0

# alt 1: 3 gaussians per state
java com.github.sikoried.jstk.arch.Configuration \
	--compile timit.a timit.l 0 \
	--cont0 24 3 \
	--write conf.xml conf.cb.0

# alternatively, use tri-phones that show up at least 200 times
java com.github.sikoried.jstk.arch.Configuration \
	--compile timit.a timit.l 3 \
	--cont0 24 2 \
	--prune 200 <(cut -d' ' -f 2- list.train.trl) \
	--write conf.xml conf.cb.0
```


# Training

Just like last week, we'll start with a forced-linear alignment, and then alternate alignment and Viterbi training.

```bash
nj=0

# initial forced-linear alignment
java com.github.sikoried.jstk.app.Trainer conf.xml conf.cb.0 conf.cb.1 list.train.trl ft/ -a linear -t vt -p $nj

# iterate...
mkdir ali logs
num_iters=40
realign_iters="2 3 4 5 6 7 8 9 10 12 14 16 18 20 23 26 29 32 35 38"
for i in `seq 2 $num_iters`; do
	echo "Iteration $i"

	if echo $realign_iters | grep -w $i >/dev/null; then
		echo "Aligning data"
		java com.github.sikoried.jstk.app.Aligner conf.xml conf.cb.$[$i-1] -l list.train.trl ft/ ali/ -p $nj -b "sil" > logs/align.$i.log
	fi

    java com.github.sikoried.jstk.app.Trainer conf.xml conf.cb.$[$i-1] conf.cb.$i list.train.trl ft/ -a forced -t vt -p $nj > logs/train.$i.log
done
```


# Decoding

For decoding, you can try a number of different parameters, and see what happens...

```bash
cb_test=conf.cb.40
lm=timit.ug.arpa
beam_size=300
lm_weight=1
insertion_penalty=1e-2
mode=word  # use 'ma' (meta-alignment) with wavesurfer, or 'compact'
java com.github.sikoried.jstk.app.Decoder \
	conf.xml $cb_test $lm \
	-f ft/test-dr1-faks0-sa1.wav \
	-bs $beam_size -n 1 \
	-w $lm_weight -i $insertion_penalty \
	-m $mode -o outfile
```

```
# convert alignment to Wavesurfer label (transcription) format
awk -v s=0 -v f=160 '{print s, s+($2*f), $1; s+=($2*f)}' test-dr1-faks0-sa1.ali > test-dr1-faks0-sa1.lab
```
