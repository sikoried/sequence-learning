---
template: page
title: Cost and States
permalink: 02/cost-and-states/
mathjax: true
---

# Cost and States

In this assignment, we will explore different cost functions and ways to model state.


# Keyboard Aware Auto-Correct

In the previous assignment, we applied uniform cost to all substitutions.
This does not really make sense if you look at a keyboard: the QWERTY layout will favor certain substitutions (eg. _a_ and _s_), while others are fairly unlikely (eg. _a_ and _k_).

- Implement a distance metric that computes a weight for a given character substitution.
	Hint: Think of the keyboard as a checkerboard, where the keys are uniformly distributed; a simple heuristic is to map the keys to their offsets on the board, and compute the euclidean distance (compare eg. [here](https://github.com/wsong/Typo-Distance/blob/master/typodistance.py)).
- Integrate this distance to the basic edit distance from last week.


## Discuss your Implementation

- What could be better heuristics for cost of substitution than the one above?
- What about swipe-to-type?
- What about capitalization, punctiation and special characters?


# Isolated Word Recognition

Acutally, this is [really old](https://ieeexplore.ieee.org/document/1171695/), but worth the exercise :-)


## Getting Started with JSTK (again)

For the following two assignments, we will need the JSTK up and running, ideally with the libraries added to your classpath:

```
$ export CLASSPATH=$(find path/to/jstk/jstk/build/libs -name '*.jar' | xargs echo | tr ' ' ':')
$ java de.fau.cs.jstk.app.Version  # does this work?!
```


## Extracting Features

DP can be used to implemented isolated word recognition.
However, due to the relatively large sample number (e.g. 8kHz), performing [DTW](https://en.wikipedia.org/wiki/Dynamic_time_warping) (edit distance with uniform cost) on the raw audio signal is not advised (feel free to try!).
A better solution is to compute a set of features; here we will extract mel-frequency cepstral coefficients over windows of 25ms length, shifted by 10ms.

Here's an example to record audio from using the JSTK, convert it to WAV, and then compute a feature file (in `frame` format):

```
# query for audio mixers
$ java de.fau.cs.jstk.sampled.AudioCapture -L
Default Audio Device
Built-in Microphone

# reord 16khz/mono, convert to WAV
$ java de.fau.cs.jstk.sampled.AudioCapture -m "Built-in Microphone" | sox -t s16 -r 16000 - rec.wav

# compute MFCC features
$ java de.fau.cs.jstk.app.Mfcc -f t:wav/16 -w hamm,25,10 -i rec.wav -o rec.ft
```

These feature files can be read using the class `de.fau.cs.io.FrameInputStream`, for example

```java
FrameSource fs = new FrameInputStream(inFile);
int fd = fs.getFrameSize();

double[] buf = new double [fd];

while (fs.read(buf)) {
	// ...
}
```


## Implement Isolated Word Recognitio Using DP

1. Record the numbers from one to ten to form a training set; try to articulate clearly!
2. Record a few numbers to form a test set.
3. Implement isolated word recognition.
	a. Adapt your DTW implementation from the previous exercise, if necessary.
	b. For each test word, compute the (normalized) distance to the training words
	c. Select the closest word as classification result.


## Discuss your Implementation

- How can you extend this idea to continuous speech?
- How does this algorithm scale with a larger vocabulary, how can it be improved?
- What are inherent issues of this approach?


# DP and States: DTMF Decoding

You probably know about [Dual-tone multi-frequencey signaling](https://en.wikipedia.org/wiki/Dual-tone_multi-frequency_signaling) (DTMF), which is (was?) used to transmit numbers over the phone in a machine understandable way.


## Getting Familiar

Go to [audiocheck.net](https://www.audiocheck.net/audiocheck_dtmf.php) and create a few sequences.
An example DTMF sequence (_123A456B789C*0#D_) is provided here: [dtmf_123A_456B_789C_s0pD.wav]({{site.baseurl}}/02-cost-and-states/dtmf_123A_456B_789C_s0pD.wav).

Use a tool such as [Wavesurfer](https://sourceforge.net/projects/wavesurfer/files/wavesurfer/1.8.8p5/) or [Audacity](https://www.audacityteam.org/) to get an idea on how the spectrum looks like.


## Decoding DTMF Sequences

The idea is now to model DTMF sequences a small, fully corrected graph, that has 13 states:
0-9, A-D, \*, \# and _silence_.
The mapping from symbol to frequency pair is given as `[(1,697,1209), (2,697,1336), (3,697,1477), (A,697,1633), (4,770,1209), (5,770,1336), (6,770,1477), (B,770,1633), (7,852,1209), (8,852,1336), (9,852,1477), (C,852,1633), (*,941,1209), (0,941,1336), (#,941,1477), (D,941,1633)]` (see also [`de.fau.cs.jstk.framed.DTMF`](https://github.com/sikoried/jstk/blob/master/jstk/src/de/fau/cs/jstk/framed/DTMF.java)).

Use the [DTMF](https://github.com/sikoried/jstk/blob/master/jstk/src/de/fau/cs/jstk/framed/DTMF.java) program to extract DTMF features, either using it as a `FrameSource`, or using its `main` function:

```
$ java de.fau.cs.jstk.framed.DTMF dtmf_123A_456B_789C_s0pD.wav | head -n10
0 [main] INFO de.fau.cs.jstk.framed.DTMF  - FFT resolution (Hz/bin) = 15.625
1 [main] INFO de.fau.cs.jstk.framed.DTMF  - frequencies = [697, 770, 852, 941, 1209, 1336, 1477, 1633]
1 [main] INFO de.fau.cs.jstk.framed.DTMF  - corresponding FFT bins = [45, 49, 55, 60, 77, 86, 95, 105]
3687.88 0.50 0.01 0.00 0.00 0.50 0.00 0.00 0.00 1
4640.80 0.50 0.00 0.00 0.00 0.50 0.00 0.00 0.00 1
4638.79 0.50 0.00 0.00 0.00 0.50 0.00 0.00 0.00 1
4640.37 0.50 0.00 0.00 0.00 0.50 0.00 0.00 0.00 1
4641.66 0.50 0.00 0.00 0.00 0.50 0.00 0.00 0.00 1
4639.33 0.50 0.00 0.00 0.00 0.50 0.00 0.00 0.00 1
4636.45 0.50 0.00 0.00 0.00 0.50 0.00 0.00 0.00 1
...
# energy, 697Hz, 770Hz, ..., dialed key (energy + max-search)
```

As you can see, it's not really a hard problem, since a simple maximum search already finds the correct keys most of the time.
As a matter of fact, if you filter by a minimal energy (first column), and `uniq` the output, you get the punched keys:

```
$ java de.fau.cs.jstk.framed.DTMF dtmf_123A_456B_789C_s0pD.wav | awk '{if ($1 > 100) print $NF}' | uniq
1
2
3
A
4
5
6
B
7
8
9
C
*
0
#
D
```


## Implementing DP with States

We will now abstract edit distance in a way, that we compute the "distance" of an observation sequence to a series of state occupation (ie. key presses).

- For the decoding matrix, you will use the number of feature vectors in one dimension, and the number of states in the other.
- Define prototype vectors for each state; see DTMF table, use 0.5 for each of the active frequencies, or all 0 for silence.
- Remember: you can now "go backwards" on one axis, thus you need to compute the minimum for the complete row (or column, depending on your choice).
- Use uniform costs and the distance between the input vector and the state's prototype vector.
- Compute the backtrace and `uniq` the sequence to get the punched keys.


## Discuss your Implementation:

- How could it be improved in terms of computation and memory?
- Discuss limits of this modeling approach.
- Could you extend your isolated word recognition algorithm to this approach? Would it scale?

