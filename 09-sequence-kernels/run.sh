#!/bin/bash

# run in LNDW2009
# exit 1

# pushd ~/git/sikoried
# $(gradle -q env)

# make list file
/bin/ls wav/ > all.lst

mkdir -p ft mdl
(cd wav; java com.github.sikoried.jstk.app.Mfcc -f t:wav/16 \
	-w hamm,25,10 -d 5:1,5:2 --turn-wise-mvn \
	--in-list ../all.lst ../ft/)

# train ubm
nd=512
java com.github.sikoried.jstk.app.Initializer \
	-n $nd -s random_50 \
	--list all.lst --dir ft \
	--gmm mdl/ubm${nd}.0
java com.github.sikoried.jstk.app.GaussEM \
	-i mdl/ubm${nd}.0 \
	-n 10 \
	-l all.lst -d ft \
	-o mdl/ubm${nd}.10

# adapt speaker models
awk '{printf "ft/%s mdl/%s\n", $1, $1}' all.lst > inout.lst
java com.github.sikoried.jstk.app.Map -i mdl/ubm${nd}.10 -L inout.lst

# make supervectors; here: use only means
(cd mdl; java com.github.sikoried.jstk.stat.Mixture s m ../all.lst ../all.sv)


# convert speaker mdls to svmlite format
# age 1:ft1 2:ft2 ...
paste -d ' ' \
	<(awk '{print int(substr($1,5, 7))}' all.lst) \
	<(java com.github.sikoried.jstk.app.Convert frame ascii < all.sv | awk '{for (i=1;i<NF-1;i++) printf "%d:%s ", i, $i; printf "%d:%s\n", NF, $NF}') \
	> all.${nd}.arff


# train
LIBSVM=/Users/riedhammerko/git/libsvm
$LIBSVM/svm-scale -s scales.${nd} all.${nd}.arff > all-scaled.${nd}.arff
$LIBSVM/svm-train -s 3 -t 0 all-scaled.${nd}.arff eps-lin.${nd}.svm
$LIBSVM/svm-predict all-scaled.${nd}.arff eps-lin.${nd}.svm pred.${nd}.arff

# evaluate
paste -d ' ' \
	<(awk '{print int(substr($1,5, 7))}' all.lst) pred.${nd}.arff \
	| awk 'BEGIN{e=0; i=0} {i++; e+= sqrt(($1-$2)*($1-$2))} END{print i, e, e/i}'

# test
# https://de.wikipedia.org/wiki/Die_Sonne_und_der_Wind#Linguistische_Verwendung
# rec -t wav -e signed-integer -b 16 -c 1 test.wav
#fn=f26
fn=m35
java com.github.sikoried.jstk.app.Mfcc -f t:wav/16 \
	-w hamm,25,10 -d 5:1,5:2 --turn-wise-mvn \
	-i ${fn}.wav -o ${fn}.ft
java com.github.sikoried.jstk.app.Map -i mdl/ubm${nd}.10 -f ${fn}.ft -o ${fn}.${nd}.mdl

java com.github.sikoried.jstk.stat.Mixture s m < ${fn}.${nd}.mdl > ${fn}.${nd}.sv
java com.github.sikoried.jstk.app.Convert frame ascii < ${fn}.${nd}.sv \
	| awk 'BEGIN{printf "35 "} {for (i=1;i<NF-1;i++) printf "%d:%s ", i, $i; printf "%d:%s\n", NF, $NF}'\
	> ${fn}.${nd}.arff

# scale and predict
$LIBSVM/svm-scale -r scales.${nd} ${fn}.${nd}.arff > ${fn}-scaled.${nd}.arff
$LIBSVM/svm-predict ${fn}-scaled.${nd}.arff eps-lin.${nd}.svm ${fn}-pred.${nd}.arff
