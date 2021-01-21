# Sequence Learning

_Elective for [CS grad students](https://www.th-nuernberg.de/fakultaeten/in/studium/masterstudiengang-informatik/) at the [Technical University of Applied Sciences Nuremberg](https://www.th-nuernberg.de/)._



## Class Schedule and Credits

**Time and Location:** Mondays at 9.45 (online, Zoom link on Moodle)

**Announcements and Discussions:** [Moodle Course #5312](https://elearning.ohmportal.de/course/view.php?id=5312)

### Format

Each week, we will discuss algorithms and their theory before implementing them to get a better hands-on understanding.
The materials consist of a mix of required and recommended readings, slides as well as a set of programming assignments.
These assignments are mandatory and in `python3`.
Pairprogramming encouraged, [_BYOD_](https://en.wikipedia.org/wiki/Bring_your_own_device) strongly recommended!


### Credits

Credits are earned through two components:

1. All six assignments (dynamic programming, Markov chains, hidden Markov models, recurrent neural networks, attention, transformer) must be completed throughout the semester (pass/fail; pair programming encouraged).
2. Oral exam (20') covering theory and assignments (graded; individual exams).


_Note: Materials will be (mostly) in English, the lectures/tutorials will be taught in German unless English speaker present; oral exam in language of choice._


### Important Dates

_TBA_


## Recommended Textbooks

- Niemann, H: _Klassifikation von Mustern._ 2. Überarbeitete Auflage, 2003 ([available online](https://www5.cs.fau.de/fileadmin/Persons/NiemannHeinrich/klassifikation-von-mustern/m00-www.pdf))
- Huang, Acero, Hon: _Spoken Language Processing: A Guide to Theory, Algorithm and System Development._ (ISBN-13: 978-0130226167)
- Jurafsky, D and Martin, J: _Speech and Language Processing._ 2017 ([available online](http://web.stanford.edu/~jurafsky/slp3/))
- Manning, C, Raghavan P and Schütze, H: _Introduction to Information Retrieval_, Cambridge University Press. 2008. ([available online](https://nlp.stanford.edu/IR-book/))
- Goodfellow, I and Bengio,Y and Courville, A: _Deep Learning._ 2016 ([available online](http://www.deeplearningbook.org/))


## Syllabus

_Syllabus is currently undergoing updates... (as of Jan 21, 2021)_

- ✆ **March 19: Introduction.** ([slides](00/introduction/), [exercise](00/exercise/))

	We'll start with the general concepts of supervised vs. unsupervised learning and classification of independent observations vs. sequences of observations.
	To get you motivated, we'll look at a list of recent "AI products" that utilize sequence learning.

- ✆ **March 26: Auto-Correct.** ([slides](http://www.cs.jhu.edu/~langmea/resources/lecture_notes/dp_and_edit_dist.pdf) by [Ben Langmead](http://www.langmead-lab.org/), [exercise](01/autocorrect/))
	
	We'll start with a classic implementation of auto-correcting mispelled words to bring dynamic programming back to memory.
	We'll also look at scalability regarding computation and memory efforts.

- ✆ **April 2: States and Cost Functions.** ([slides](02/cost-and-states/slides/), [exercise](02/cost-and-states/))
	
	Understand how DP can be used on an abstraction of distances and states.
	We'll build a smarter, keyboard layout aware auto-correct and start looking into some applications in signal processing (isolated word and DTMF sequence classification).

> _April 9: Maundy Thursday (Gründonnerstag)_

- ✆ **April 16: Modeling Sequences.** ([slides](03-ngrams/sv-lm.pdf), [exercise](03/ngrams/))
	
	Learn about n-grams, a simple yet effective approach to learn contexts of distcrete symbols.
	We'll use n-grams to improve our auto-correct by incorporating context and suggesting following words.

- ✆ **April 23: Hidden Markov Models.** ([slides](04-hmms/hmm.pdf), [exercise](04/hmms/))
	
	We'll take a close look at hidden Markov models and how to (efficiently) evaluate and train them.
	The Viterbi decoding algorithm tells us the most likely sequence and the path that lead to it.
	We'll use them to build a proof-of-concept isolated word recognizer.

- ✆ **April 30: Higher-Level Sequence Modeling with HMM.** ([slides](05-decoding/decoding.pdf), [exercise](05/decoding/))
	
	Learn how to model complex sequences of arbitrary length that prohibit explicit modeling, such as speech recognition or choreographies in sports.
	Here we will combine what we've discussed so far: prefix trees, n-gram models and efficient search.

- ✆ **May 7: Feed-Forward Neural Networks.** (slides [perceptron](06-nnets/sl-perceptron.pdf) and [nnets](06-nnets/sl-mlp.pdf), [fizzbuzz.py](06-nnets/fizzbuzz.tf), [exercise](06/nnets/)).
	
	A brief introduction to neural networks: fundamentals, topologies and training.
	We'll skip implementing the details and use pytorch for the examples. Did you know that you could program _fizzbuzz_ as a neural network?
	_Please have Python with Numpy and PyTorch installed and operational on your machine!_

- ✆ **May 14: Recurrent Neural Networks.** (slides [cs231n: RNNs](07-rnns/cs231n_2018_lecture10_excerpts.pdf), [exercise](07/rnns/))
	
	Recurrent neural networks use feedback loops to introduce temporal context or "memory" into the network.
	Attention is a modeling concept which allows the networks to learn an even better understanding of the context.
	We'll study them using two examples: language modeling and sentiment analysis.

	**Also:** Introduction to the class project!

> _May 21: Ascension Day (Christi Himmelfahrt)_

> ⚠ **May 28: Project proposals due!** ⚠

- ✆ **May 28: Embeddings and Sequence-to-Sequence Learning ([embeddings](08-seq2seq/embeddings.pdf), [s2s](08-seq2seq/seq2seq.pdf), [literature and exercise](08/seq2seq/))** 

	Previous algorithms explicitly modeled the sequence, either as a graph-like structure such as an HMM or by concatenating observations to a single data point.
	Embeddings are learned feature representations that can incorporate large quantities of unlabeled data.
	Encoder-decoder networks are a special kind of topology of recurrent neural networks that can be used to model sequence to sequence mappings, such as found in end-to-end speech recognition, machine translation or automatic summarization -- without explicitly modeling states!
	We'll also look at transformers which can capture temporal structures without recurrence.

- ✆ **June 4: Project Check-In 1**

	No class; teams will meet individually with instructor to discuss their projects.
	Plan for 20 minutes discussion and bring 5 slides: rough outline of related work section (3 slides), baseline results (1) and experiments outline (1).

	Book your time slot: [DFN Terminplaner](https://terminplaner4.dfn.de/4nLli4nJKcKILKED)

> _June 11: Corpus Christ (Fronleichnam)_

- ✆ **June 18: Project Check-In 2**

	No class; teams will meet individually with instructor to discuss their projects.
	Plan for 20 minutes to talk about your implementation and experiments, and a rough outline (bullet points) of the method and experiments sections (slides as needed).

	Book your time slot: [DFN Terminplaner](https://terminplaner4.dfn.de/ZFlbjfoKuaIer7kH)

> ⚠ **June 25: Papers due!** ⚠

- ✆ **June 25: [How-To Peer Review](99/howto-peer-review/), Sequence Kernels ([slides](09-sequence-kernels/seq-kernels.pdf), [SVM slides](09-sequence-kernels/intro_svm_new.pdf), [seq. kernels](09-sequence-kernels/pr-seq-kernels.pdf), [assignment](09/agerec/))**
	
	In many cases, classifying a sequence into a discrete class does not quite work with recurrent networks.
	We'll learn about support vector machines, sequence kernels and methods to map sequences into a single observation of a continuous space.
	

>  ⚠ **July 2: Reviews due!** ⚠

- ✆ **July 2: Machine Learning in Production ([slides](10/ml-in-production))**
	
	We'll then look at architectural challenges when training and deploying machine learning models for production.

> ⚠ **July 9: Projects due!** ⚠

- ✆ **July 15-16: Project Colloquium**
	
	No class; teams will meet individually with instructor to present and discuss their paper and code.
	Plan for 20 minutes total to discuss: data usage, baseline, method, experiments and conclusions (slides to support the colloqium, not to present).

	Timeslots will be coordinated in Project Check-In #2.


_Subscribe to [https://github.com/sikoried/sequence-learning/](https://github.com/sikoried/sequence-learning/) to follow updates._
