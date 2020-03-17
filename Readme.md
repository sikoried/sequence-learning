# Sequence Learning

_Elective for [CS grad students](https://www.th-nuernberg.de/fakultaeten/in/studium/masterstudiengang-informatik/) at the [Technical University of Applied Sciences Nuremberg](https://www.th-nuernberg.de/)._



## Class Schedule and Credits

**Time and Location:** Thursdays at 8 (online)

**Announcements and Discussions:** Microsoft Teams: [Sequence Learning](https://teams.microsoft.com/l/team/19%3a4c844498dec6420ca6b0667b9ad02571%40thread.tacv2/conversations?groupId=9d0d8151-8b59-4160-a6ab-06afa1434d78&tenantId=2bb870ba-c8e4-4d13-b6c1-e78539138e20)

**Format:** 

Each week, we will discuss algorithms and their theory before implementing them to get a better hands-on understanding.
Java is suggested, pairprogramming encouraged, [_BYOD_](https://en.wikipedia.org/wiki/Bring_your_own_device) strongly recommended!

**Credits:**

We'll adopt a common research routine: identify a problem, research prior work, engineer a solution, write it up in a paper, review other papers, present your work.
Credits are earned through

- your [4 page paper](https://journals.ieeeauthorcenter.ieee.org/create-your-ieee-article/authoring-tools-and-templates/ieee-article-templates/templates-for-transactions/), prepared in teams of two, due **June 24** (60%)
- individually reviewing 3 other papers by **July 1** (20%)
- presenting your paper on **July 8** (tentative date). (20%)

_For more details see [these slides](99/credits-howto/)._

_Note: Materials will be in English, the lectures/tutorials will be taught in German; class project in language of choice._


## Recommended Textbooks

- Niemann, H: _Klassifikation von Mustern._ 2. Überarbeitete Auflage, 2003 ([available online](https://www5.cs.fau.de/fileadmin/Persons/NiemannHeinrich/klassifikation-von-mustern/m00-www.pdf))
- Huang, Acero, Hon: _Spoken Language Processing: A Guide to Theory, Algorithm and System Development._ (ISBN-13: 978-0130226167)
- Jurafsky, D and Martin, J: _Speech and Language Processing._ 2017 ([available online](http://web.stanford.edu/~jurafsky/slp3/))
- Manning, C, Raghavan P and Schütze, H: _Introduction to Information Retrieval_, Cambridge University Press. 2008. ([available online](https://nlp.stanford.edu/IR-book/))
- Goodfellow, I and Bengio,Y and Courville, A: _Deep Learning._ 2016 ([available online](http://www.deeplearningbook.org/))


## Syllabus

_All dates tentatively due to corona madness. ✆ indicates online Q&A._

- ✆ **March 19: Introduction.** ([slides](00/introduction/), [exercise](00/exercise/))

	We'll start with the general concepts of supervised vs. unsupervised learning and classification of independent observations vs. sequences of observations.
	To get you motivated, we'll look at a list of recent "AI products" that utilize sequence learning.

- ✆ **March 20: Auto-Correct.** ([slides](http://www.cs.jhu.edu/~langmea/resources/lecture_notes/dp_and_edit_dist.pdf) by [Ben Langmead](http://www.langmead-lab.org/), [exercise](01/autocorrect/))
	
	We'll start with a classic implementation of auto-correcting mispelled words to bring dynamic programming back to memory.
	We'll also look at scalability regarding computation and memory efforts.

- ✆ **April 2: States and Cost Functions.** ([slides](02/cost-and-states/slides/), [exercise](02/cost-and-states/))
	
	Understand how DP can be used on an abstraction of distances and states.
	We'll build a smarter, keyboard layout aware auto-correct and start looking into some applications in signal processing (isolated word and DTMF sequence classification).

- _April 9: Maundy Thursday (Gründonnerstag)_

- ✆ **April 16: Modeling Sequences.** ([slides](03-ngrams/sv-lm.pdf), [exercise](03/ngrams/))
	
	Learn about n-grams, a simple yet effective approach to learn contexts of distcrete symbols.
	We'll use n-grams to improve our auto-correct by incorporating context and suggesting following words.

- **April 23: Hidden Markov Models.** ([slides](04-hmms/hmm.pdf), [exercise](04/hmms/))
	
	We'll take a close look at hidden Markov models and how to (efficiently) evaluate and train them.
	The Viterbi decoding algorithm tells us the most likely sequence and the path that lead to it.
	We'll use them to build a proof-of-concept isolated word recognizer.

- **April 30: Higher-Level Sequence Modeling with HMM.** ([slides](05-decoding/decoding.pdf), [exercise](05/decoding/))
	
	Learn how to model complex sequences of arbitrary length that prohibit explicit modeling, such as speech recognition or choreographies in sports.
	Here we will combine what we've discussed so far: prefix trees, n-gram models and efficient search.

- **May 7: Feed-Forward Neural Networks.** (slides [perceptron](06-nnets/sl-perceptron.pdf) and [nnets](06-nnets/sl-mlp.pdf), [fizzbuzz.py](06-nnets/fizzbuzz.tf), [exercise](06/nnets/)).
	
	A brief introduction to neural networks: fundamentals, topologies and training.
	We'll skip implementing the details and use pytorch for the examples. Did you know that you could program _fizzbuzz_ as a neural network?
	_Please have Python with Numpy and PyTorch installed and operational on your machine!_

- **May 14: Recurrent Neural Networks.** (slides [cs231n: RNNs](07-rnns/cs231n_2018_lecture10_excerpts.pdf), [exercise](07/rnns/))
	
	Recurrent neural networks use feedback loops to introduce temporal context or "memory" into the network.
	We'll study them using two examples: language modeling and drawing classification.

- _May 21: Ascension Day (Christi Himmelfahrt)_

- **May 28: Project Proposals**

	No class; teams will meet individually with instructor to discuss their project proposals.
	Plan for 10-15 minutes discussion and bring 5 slides: Team, Task and a brief summary of 3 pieces of related work (textbook, paper, github).
	Book your time slot: <https://terminplaner4.dfn.de/SfHJAnhklDDhiWhB>

- **June 4: Sequence to Sequence Learning.** ([slides](08-seq2seq/seq2seq.pdf), [literature and exercise](08/seq2seq/))
	
	Previous algorithms explicitly modeled the sequence, either as a graph-like structure such as an HMM or by concatenating observations to a single data point.
	Encoder-decoder networks are a special kind of topology of recurrent neural networks that can be used to model sequence to sequence mappings, such as found in end-to-end speech recognition, machine translation or automatic summarization -- without explicitly modeling states!
	We'll also talk about the concept of attention, which allows the networks to learn an even better understanding of the context.

- _June 11: Corpus Christ (Fronleichnam)_

- **June 18: Project Check-In**

	No class; teams will meet individually with instructor to discuss their projects.
	Plan for 10-15 minutes to talk about your related work, implementation and performance of the chosen baseline, and a rough outline (bullet points) of the method and experiments sections.
	Book your time slot: <https://terminplaner4.dfn.de/coDapAxvNNILyKkg>

- **June 25: SVM, Sequence Kernels and Embeddings** ([slides](09-sequence-kernels/seq-kernels.pdf), [SVM slides](09-sequence-kernels/intro_svm_new.pdf), [seq. kernels](09-sequence-kernels/pr-seq-kernels.pdf), [assignment](09/agerec/))

	In many cases, classifying a sequence into a discrete class does not quite work with recurrent networks.
	We'll learn about support vector machines, sequence kernels and methods to map sequences into a single observation of a continuous space.
	Embeddings are learned feature representations that can incorporate large quantities of unlabeled data.

- **July 2: Papers due! [Peer Reviews](99/howto-peer-review/), [ML in Production](10/ml-in-production/)**

	We'll go through the process of reviewing and presenting a (scientific) paper.
	We'll then look at architectural challenges when training and deploying machine learning models for production.
	

- **July 1: Reviews due! Project Feedback and Presentation Check-In**
	
	No class; teams will meet individually with instructor to get feedback on their paper and discuss the outline of their presentations.
	Plan for 10-15 minutes total, and bring a rough outline of your presentation.
	Book your time slot: <https://terminplaner4.dfn.de/lvG45ebLuBSFG1u4>

- **July 8: Present your work!**


_Subscribe to [https://github.com/sikoried/sequence-learning/](https://github.com/sikoried/sequence-learning/) repository to follow updates._
