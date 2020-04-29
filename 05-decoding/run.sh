#!/bin/bash

# location on ml0
export LDC93S1=/mnt/md0/data/ldc/LDC93S1


# convert and rename data
mkdir wav
for i in `find $LDC93S1 -name "*.wav"`; do
  n=$(echo $i | perl -F/ -nlae 'print join "-", @F[2..$#F]')
  sox $i wav/$n
done


# create file lists (partitions)
(cd wav; /bin/ls > ../list.all)
grep train list.all > list.train
grep test list.all > list.test


# extract transcripts
cat list.all | ../gettext.py <(cat $LDC93S1/timit/doc/prompts.txt | sed -e 's:~vpres:~v_pres:g' | sed -e 's:~vpast:~v_past:g') > list.all.trl
grep train list.all.trl > list.train.trl
grep test list.all.trl > list.test.trl


# create lexicon and alphabet
cat <(echo 'sil sil') <(echo '-- sil') $LDC93S1/timit/doc/timitdic.txt | ../parsedict.py > timit.l 2> timit.a

# verify files...
head timit.[a,l]


# compute features
mkdir ft
java com.github.sikoried.jstk.app.Mfcc --in-list list.all ft/ --dir wav/ \
  -f t:wav/16 -w hamm,25,10 -b 188,6071,-1,.5 -d "5:1" --turn-wise-mvn


# estimate language model

# srilm on ml0
export PATH=/mnt/md0/tools/srilm/bin{,/i686-m64}:$PATH

ngram-count -order 2 -text <(cut -d' ' -f 2- list.train.trl) -lm timit.bg.arpa -no-sos -no-eos

# alternatively: unigram
ngram-count -order 1 -text <(cut -d' ' -f 2- list.train.trl) -lm timit.ug.arpa -no-sos -no-eos


# train models
num_gauss=256
num_gauss_iter=10
nj_gauss=0

# monophone configuration, with shared codebook
java com.github.sikoried.jstk.app.Initializer --gmm cb.init -f \
  -n $num_gauss -s sequential_50 --list list.train --dir ft/
java com.github.sikoried.jstk.app.GaussEM -i cb.init -o cb.em \
  -l list.train -d ft/ -n $num_gauss_iter -p $nj_gauss

java com.github.sikoried.jstk.arch.Configuration \
  --compile timit.a timit.l 0 \
  --semi cb.em \
  --write conf.xml conf.cb.0

# alternatively, use continuous densities (5 per state)
num_gauss_cont=5
java com.github.sikoried.jstk.arch.Configuration \
  --compile timit.a timit.l 0 \
  --cont0 24 $num_gauss_cont \
  --write conf.xml conf.cb.0

# alternatively, use tri-phones that show up at least 120 times
java com.github.sikoried.jstk.arch.Configuration \
  --compile timit.a timit.l 3 \
  --cont0 24 $num_gauss_cont \
  --prune 120 <(cut -d' ' -f 2- list.train.trl) \
  --write conf.xml conf.cb.0


# train the hmms
nj=48

# initial forced-linear alignment
java com.github.sikoried.jstk.app.Trainer conf.xml conf.cb.0 conf.cb.1 list.train.trl ft/ -a linear -t vt -p $nj

# iterate...
mkdir ali logs
num_iters=40
JAVA_OPTS="-Xmx32G -Xms4G"
realign_iters="2 3 4 5 6 7 8 9 10 12 14 16 18 20 23 26 29 32 35 38"
for i in `seq 2 $num_iters`; do
  echo "Iteration $i"

  if echo $realign_iters | grep -w $i >/dev/null; then
    echo "Aligning data"
    java com.github.sikoried.jstk.app.Aligner conf.xml conf.cb.$[$i-1] -l list.train.trl ft/ ali/ -p $nj -b "sil" > logs/align.$i.log
  fi

  java com.github.sikoried.jstk.app.Trainer conf.xml conf.cb.$[$i-1] conf.cb.$i list.train.trl ft/ -a forced -t vt -p $nj > logs/train.$i.log
done


# decoding

# get 10 test samples
egrep 'si[0-9]+' list.test | head -n10 > list.test.short
egrep 'si[0-9]+' list.test.trl | head -n10 > list.test.short.trl

# parameters
cb_test=conf.cb.40
lm=timit.ug.arpa
beam_size=300
lm_weight=1
insertion_penalty=1e-2
mode=word  # use 'ma' (meta-alignment) with wavesurfer, or 'compact'

java com.github.sikoried.jstk.app.Decoder conf.xml $cb_test $lm \
  -f ft/test-dr1-faks0-sa1.wav \
  -bs $beam_size -n 1 \
  -w $lm_weight -i $insertion_penalty \
  -m $mode -o outfile3

# evaluate; lines need to be "blah blah (utterence_id)"
export PATH=/mnt/md0/tools/kaldi/tools/sctk/bin:$PATH

fn_ref=list.test.short.trl
paste -d' ' \
  <(cut -d' ' -f 2- $fn_ref) \
  <(awk '{print $1}' $fn_ref | sed 's/.wav//' | awk -F- '{printf("(%s_%s)\n", $(NF-1), $NF)}') > ref

fn_hyp=outfile3
paste -d' ' \
  <(cut -d' ' -f 2- $fn_hyp) \
  <(awk '{print $1}' $fn_ref | sed 's/.wav//' | awk -F- '{printf("(%s_%s)\n", $(NF-1), $NF)}') > hyp

# score using sclite
sclite -h hyp trn -r ref trn -i wsj -o snt stdout


