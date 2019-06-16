---
template: page
title: Age Estimation from Speech
permalink: 09/agerec/
mathjax: true
---

# Age Estimation from Speech

In this exercise, we will build a basic system that predicts the approximate age of a speaker.
We will use support vector regression (SVR) together with Gaussian mixture model (GMM) supervectors derived from spectral features.

This worksheet will guide you through the basic steps before you can start tuning the system.

## Prereqs

We will be using [jstk](https://github.com/sikoried/jstk) and [libsvm](https://github.com/cjlin1/libsvm); they should build on Windows, Mac and Linux.


## Data

We will use the LNDW2009 data set which consists of 307 speakers that were recorded at the "Lange Nacht der Wissenschaften 2009" where Tobias and I demonstrated a system similar to the one we'll be building today.

You can download the data from the course's Moodle page; see the `lndw.list` file for details.

```bash
unzip lndw2009.zip

# get a list of all files
/bin/ls wav/ > all.lst
```

## Features

Since we're dealing with speech, we will be using MFCC features again.
```bash
mkdir -p ft
cd wav

# feel free to change the feature configuration!
java com.github.sikoried.jstk.app.Mfcc -f t:wav/16 \
	-w hamm,25,10 -d 5:1 --turn-wise-mvn \
	--in-list ../all.lst ../ft/
```


## Speaker Model Training

We will first train a universal background model (UBM) and then use MAP adaptation to derive the speaker models.

```bash
mkdir -p mdl

# let's try with 512 Gaussians and do 10 EM iterations
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

# adapt the speaker models
awk '{printf "ft/%s mdl/%s\n", $1, $1}' all.lst > inout.lst
java com.github.sikoried.jstk.app.Map -i mdl/ubm${nd}.10 -L inout.lst

# write all the speaker models into one consecutive supervector file
# 'm' exports means only
(cd mdl; java com.github.sikoried.jstk.stat.Mixture s m ../all.lst ../all.sv)
```

## SVR Training

First, we need to convert our binary SV files to the svmlite ARFF format:

```
<label> <index1>:<value1> <index2>:<value2> ...
.
.
.
```

```bash
paste -d ' ' \
	<(awk '{print int(substr($1,5, 7))}' all.lst) \
	<(java com.github.sikoried.jstk.app.Convert frame ascii < all.sv | awk '{for (i=1;i<NF-1;i++) printf "%d:%s ", i, $i; printf "%d:%s\n", NF, $NF}') \
	> all.${nd}.arff
```

Now, we can train the SVR model; note that we need to scale the data using their tool.

```bash
LIBSVM=/Users/riedhammerko/git/libsvm
$LIBSVM/svm-scale -s scales.${nd} all.${nd}.arff > all-scaled.${nd}.arff
$LIBSVM/svm-train -s 3 -t 0 all-scaled.${nd}.arff eps-lin.${nd}.svm

# evaluating on train should work close-to-perfect...
$LIBSVM/svm-predict all-scaled.${nd}.arff eps-lin.${nd}.svm pred.${nd}.arff
paste -d ' ' \
	<(awk '{print int(substr($1,5, 7))}' all.lst) pred.${nd}.arff \
	| awk 'BEGIN{e=0; i=0} {i++; e+= sqrt(($1-$2)*($1-$2))} END{print i, e, e/i}'
```

You can use the `-v 10` argument to `svmtrain` to get cross-validated performance results.


## Test Using Real Data

Go ahead and try some real data!
Make sure you speak for 15-30 seconds, you could read [Nordwind und Sonne](https://de.wikipedia.org/wiki/Die_Sonne_und_der_Wind#Linguistische_Verwendung) (note: this should work independent of the text read!).

```bash
# eg. record using sox; make sure the format matches! 16khz, mono, pcm
rec -t wav -e signed-integer -b 16 -c 1 test.wav

fn=test
# extract features; make sure the config matches!
java com.github.sikoried.jstk.app.Mfcc -f t:wav/16 \
	-w hamm,25,10 -d 5:1 --turn-wise-mvn \
	-i ${fn}.wav -o ${fn}.ft
java com.github.sikoried.jstk.app.Map -i mdl/ubm${nd}.10 -f ${fn}.ft -o ${fn}.${nd}.mdl

# make SV file and convert to arff
java com.github.sikoried.jstk.stat.Mixture s m < ${fn}.${nd}.mdl > ${fn}.${nd}.sv
java com.github.sikoried.jstk.app.Convert frame ascii < ${fn}.${nd}.sv \
	| awk 'BEGIN{printf "0 "} {for (i=1;i<NF-1;i++) printf "%d:%s ", i, $i; printf "%d:%s\n", NF, $NF}'\
	> ${fn}.${nd}.arff

# scale and predict
$LIBSVM/svm-scale -r scales.${nd} ${fn}.${nd}.arff > ${fn}-scaled.${nd}.arff
$LIBSVM/svm-predict ${fn}-scaled.${nd}.arff eps-lin.${nd}.svm ${fn}-pred.${nd}.arff
```

Did it work for you?


## Extensions

The performance is probably pretty poor -- after all, it is a very simple system.
Here are things to optimize, try to evaluate those with the `-v 10` option on `svmtrain` to see their impact.
- Change the features; try different filterbanks, derivatives, etc.
- Change the GMM initialization
- Change the speaker model generation: try different `r` values, or use a single EM step instead.
- Advanced: Compute the kernel values after implementing a KL-based kernel.
