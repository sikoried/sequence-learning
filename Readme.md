# Sequence Learning

_Elective for [CS grad students](https://www.th-nuernberg.de/fakultaeten/in/studium/masterstudiengang-informatik/) at the [Technical University of Applied Sciences Nuremberg](https://www.th-nuernberg.de/)._


## Class Schedule and Credits

**Time and Location:** Mondays at 9.45, HQ.104

**Announcements and Discussions:** [Moodle course 5312](https://elearning.ohmportal.de/course/view.php?id=5312).

**Format:** 

Each week, we will discuss algorithms and their theory before implementing them to get a better hands-on understanding.
Java is suggested, pairprogramming encouraged, [_BYOD_](https://en.wikipedia.org/wiki/Bring_your_own_device) strongly recommended!

**Credits:**

We'll adopt a common research routine: identify a problem, research prior work, engineer a solution, write it up in a paper, review other papers, present your work.
Credits are earned through

- your [6 page paper](https://journals.ieeeauthorcenter.ieee.org/create-your-ieee-article/authoring-tools-and-templates/ieee-article-templates/templates-for-transactions/) submitted by June 24 (60%)
- revieweing 3 other papers by July 1 (20%)
- presenting your work on July 8 (tentative date). (20%)

_Note: Materials will be in English, the lectures/tutorials will be taught in German; class project in language of choice._


## Recommended Textbooks

- Niemann, H: _Klassifikation von Mustern._ 2. Überarbeitete Auflage, 2003 ([available online](https://www5.cs.fau.de/fileadmin/Persons/NiemannHeinrich/klassifikation-von-mustern/m00-www.pdf))
- Huang, Acero, Hon: _Spoken Language Processing: A Guide to Theory, Algorithm and System Development._ (ISBN-13: 978-0130226167)
- Jurafsky, D and Martin, J: _Speech and Language Processing._ 2017 ([available online](http://web.stanford.edu/~jurafsky/slp3/))
- Manning, C, Raghavan P and Schütze, H: _Introduction to Information Retrieval_, Cambridge University Press. 2008. ([available online](https://nlp.stanford.edu/IR-book/))
- Goodfellow, I and Bengio,Y and Courville, A: _Deep Learning._ 2016 ([available online](http://www.deeplearningbook.org/))


## Syllabus

- **March 18: Introduction.** ([slides](00/introduction/), [exercise](00/exercise/))

	We'll start with the general concepts of supervised vs. unsupervised learning and classification of independent observations vs. sequences of observations.
	To get you motivated, we'll look at a list of recent "AI products" that utilize sequence learning.

_The remaining syllabus is still subject to change!_

- **March 25: Auto-Correct.** ([slides](http://www.cs.jhu.edu/~langmea/resources/lecture_notes/dp_and_edit_dist.pdf) by [Ben Langmead](http://www.langmead-lab.org/), [exercise](01/autocorrect/))
	
	We'll start with a classic implementation of auto-correcting mispelled words to bring dynamic programming back to memory.
	We'll also look at scalability regarding computation and memory efforts.

- **April 1: States and Cost Functions.** ([slides](02/cost-and-states/slides/), [exercise](02/cost-and-states/))
	
	Understand how DP can be used on an abstraction of distances and states.
	We'll build a smarter, keyboard layout aware auto-correct and start looking into some applications in signal processing (isolated word and DTMF sequence classification).

- **April 8: Modeling Sequences.** ([slides](03-ngrams/sv-lm.pdf), [exercise](03/ngrams/))
	
	Learn about n-grams, a simple yet effective approach to learn contexts of distcrete symbols.
	We'll use n-grams to improve our auto-correct by incorporating context and suggesting following words.

- **April 15: Hidden Markov Models.** ([slides](04-hmms/hmm.pdf), [exercise](04/hmms/))
	
	We'll take a close look at hidden Markov models and how to (efficiently) evaluate and train them.
	The Viterbi decoding algorithm tells us the most likely sequence and the path that lead to it.
	We'll use them to build a proof-of-concept isolated word recognizer.

- _April 22: no class (Easter)_

- **April 29: Higher-Level Sequence Modeling with HMM.** ([slides](05-decoding/decoding.pdf), [exercise](05/decoding/))
	
	Learn how to model complex sequences of arbitrary length that prohibit explicit modeling, such as speech recognition or choreographies in sports.
	Here we will combine what we've discussed so far: prefix trees, n-gram models and efficient search.

- **May 8: Feed-Forward Neural Networks.** (slides [perceptron](06-nnets/sl-perceptron.pdf) and [nnets](06-nnets/sl-mlp.pdf), [fizzbuzz.py](06-nnets/fizzbuzz.tf), [exercise](06/nnets/)).
	
	A brief introduction to neural networks: fundamentals, topologies and training.
	We'll skip implementing the details and use tensorflow for the examples. Did you know that you could program _fizzbuzz_ as a neural network?
	_Please have Python with Numpy and TensorFlow installed and operational on your machine!_

- **May 15: Recurrent Neural Networks.** (slides [cs231n: RNNs](07-rnns/cs231n_2018_lecture10_excerpts.pdf), [exercise](07/rnns/))
	
	Recurrent neural networks use feedback loops to introduce temporal context or "memory" into the network.
	We'll study them using two examples: language modeling and drawing classification.

- **May 20: Sequence Kernels and Embeddings for Instance Classification**

	In many cases, classifying a sequence into a discrete class does not quite work with recurrent networks.
	We'll learn about sequence kernels and embeddings that map sequences into a single observation of a continuous space, that can then be used by conventional classifiers.

- **May 27: Sequence to Sequence Learning.** ([literature and exercise](08/seq2seq/), [attention slides](08-seq2seq/sl-augmented.pdf), [CCL'17 tutorial slides](http://www.cips-cl.org/static/CCL2017/slides/T1_part2.pdf))
	
	Previous algorithms explicitly modeled the sequence, either as a graph-like structure such as an HMM or by concatenating observations to a single data point.
	Encoder-decoder networks are a special kind of topology of recurrent neural networks that can be used to model sequence to sequence mappings, such as found in end-to-end speech recognition, machine translation or automatic summarization -- without explicitly modeling states!

- **June 3: Project Kickoff**

- _June 10: no class (Whit Monday)_

- **June 17: Project Check-In**

- **June 24: Deep Learning: Practical Considerations.** (slides: [toolkits](09/toolkits/slides/), [practical considerations](09/toolkits/practical-considerations/), [deployment](09/toolkits/deployment/), [exercise](09/toolkits/))

	Papers due!
	
	We'll compare different deep learning toolkits and their requirements or potential to get a grip on what's necessary to apply them to a new problem.
	

- **July 1: tbd**
	Reviews due.

- **July 8 _(tentative date)_**
	Present your work.


_Subscribe to [https://github.com/sikoried/sequence-learning/](https://github.com/sikoried/sequence-learning/) repository to follow updates._
