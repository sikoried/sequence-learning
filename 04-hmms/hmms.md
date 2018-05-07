---
template: page
title: Hidden Markov Models
permalink: 04/hmms/
mathjax: true
---

# Hidden Markov Models

In this exercise, we'll build an isolated word recognizer using Hidden Markov Models.
We will use the following classes of the package `com.github.sikoried.jstk.stat`:

- `Mixture`: This will serve as the implementation for the emission densitites.
	There is a constructor that takes an `InputStream`, as well as a `write` method to save models to file.
- `hmm.HMM`: As the basic implementation of hidden Markov models.
	There is a constructor that takes an `InputStream`, as well as a `write` method to save models to file.
- `hmm.SCState` and `hmm.CState` as implementations of states with semi- and continuous emission probabilities.
- `hmm.Alignment` to compute and store HMM state alignments.


### Preliminaries

We'll be using JSTK as well as our own code, so make sure to set up your `CLASSPATH`:

```bash
cd path/to/sl-examples
$(gradle -q env)  # will exec export CLASSPATH=...
```


# Data Prep

- Clone the [Free Spoken Digit Dataset](https://github.com/Jakobovski/free-spoken-digit-dataset).
- Create file lists for training and test; we'll use `jackson` as training speaker, and `theo` for test.
- Compute MFCC features, using first derivatives and per-file normalization.
- Train a Gaussian mixture model (128 diagonal densities), which we will be using as codebook later

```bash
# clone data set
git clone https://github.com/Jakobovski/free-spoken-digit-dataset.git
cd free-spoken-digit-dataset/recordings

# make lists
/bin/ls [0-9]_jackson_*.wav > list.train
/bin/ls [0-9]_theo_*.wav > list.test
cat list.{train,test} > list.all

# compute features
mkdir ft
java com.github.sikoried.jstk.app.Mfcc \
	-f t:wav/8 -w hamm,25,10 \
	-b 0,4000,-1,24 -d 5:1 \
	--turn-wise-mvn \
	--in-list list.all ft

# init and train GMM
N=128
mkdir mdl
java com.github.sikoried.jstk.app.Initializer \
	--list list.train --dir ft \
	--gmm mdl/init${N}.mdl -n $N -s g-ev
java com.github.sikoried.jstk.app.GaussEM \
	-i mdl/init${N}.mdl \
	-o mdl/em${N}.mdl \
	-l list.train -d ft
```


# Training

To keep things simple, we'll make a few assumptions:

- The classes (words) are the numbers 0 through 9.
- Filenames always follow the scheme `{class}_{speaker}_{rec-id}.wav`, ie. the first part is the class label.
- Feature files and models are stored in `ft/` and `mdl/`, respectively (hard-code path names).

The overall training routine will be:

1. Align all examples using a linear alignment
2. Accumulate the statistics and re-estimate
3. Force-align the training data
4. Accumulate the statistics and re-estimate; optionally repeat this step
5. Repeat at 3.

Complete the binary `iw.Trainer`, that accepts property file, to be read via [Commons Configuration](https://commons.apache.org/proper/commons-configuration/userguide/quick_start.html), containing the following variables (defaults in parentheses):

- list that contains the training files
- number of states per class/HMM (`4`)
- classes (`0, 1, 2, 3, 4, 5, 6, 7, 8, 9`; retrieve with `getStringArray`); models will be stored as `<name>.mdl[.<iter>]`
- directory where to store the model files (`mdl/`)
- directory where to find the feature files (`ft/`)
- number of overall iterations (`10`)
- iterations when to re-align (`1, 2, 5, 8`; retrieve with `getIntArray`)
- `CState`: number of densities (1)
- `SCState`: codebook to use (`null`; **note:** copy will be written to model directory)

An example properties file could look like

```
iw.list = list.train
iw.states = 4
iw.classes = 0, 1, 2, 3, 4, 5, 6, 7, 8, 9
iw.mdldir = mdl-batch1
iw.ftdir = ft
iw.iterations = 10
iw.realign = 1, 2, 5, 8
iw.codebook = mdl/em10-128.mdl
```

### Implement the Training Routine

0. for each class, allocate a HMM; use SCState if codebook is specified, CState otherwise
1. compute an initial estimate, by creating linear alignments for each file and class; save the initial estimates as `<name>.mdl.0`
2. reset the accumulators
3. if (cur_iter in realign): compute the forced alignment
4. accumulate according to alignments (eg. `accumulateVT`)
5. re-estimate the parameters (`.reestimate()`), save current estimate
6. if (cur\_iter < num\_iters): goto 2


# Classification

Complete the binary `iw.Classifier`, which accepts a properties file with the following settings:

- file list containing the test data
- list of classes to load
- directory where to store the model files (`mdl/`)
- directory where to find the feature files (`ft/`)
- if required, the codebook (relative to model directory)

```
iw.list = list.test
iw.classes = 0, 1, 2, 3, 4, 5, 6, 7, 8, 9
iw.mdldir = mdl-batch1
iw.ftdir = ft
iw.codebook = em10-128.mdl
```

### Implement the Classification Routine

0. Load the model files (and codebook)
1. For each feature file, align each of the models
2. Normalize the scores to a soft-max (to get probabilities for each class)
3. Output lines of `<file> <best-class> <class-scores ...>`


### Evaluation

- How does your classifier perform?
- Run experiments with different settings (iterations, states, classes)
- Can you see patterns of classes that get mixed up?


# Adjust for Silence

- Change your trainer and classifier, so that it allows for leading and trailing silence
- Use 3 states for silence; make sure that all recordings contribute to a single silence model
- How does modeling silence affect performance?


# Outlook: Decoding

- The current classifier allows only single word decisions.
- How would you handle word *sequences*?
- Recall the DTMF tone decoder. How would you transfer the idea to isolated word recognition?
- Outline an algorithm that allows you to decode arbitrary sequences of digits.

