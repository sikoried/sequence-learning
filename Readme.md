# Sequence Learning


_Elective for [CS grad students](https://www.fh-rosenheim.de/technik/informatik-mathematik/informatik-master/) at the [University of Applied Sciences Rosenheim](https://www.fh-rosenheim.de)._


## Class Schedule and Credits

**Time and Location:** Tuesdays at 11.45, B0.08a

**Comunication** via [Mattermost](https://inf-mattermost.fh-rosenheim.de/sl-2018/channels/town-square) ([register](https://inf-mattermost.fh-rosenheim.de/signup_user_complete/?id=c9txudhce7bdxni5uxfrzxqm5r)).

**Format:** Each week, we will discuss algorithms and their theory before implementing them to get a better hands-on understanding.
Java is suggested, pairprogramming encouraged, [_BYOD_](https://en.wikipedia.org/wiki/Bring_your_own_device) strongly recommended!

**Credits:** oral exam (15') at the end of the semester, tentative date: July 10 (last day of classes).

_Note: Materials will be in English, the lectures/tutorials will be taught in German; the oral exam in the language of your choice._


## Recommended Textbooks

- Niemann, H: _Klassifikation von Mustern._ 2. Überarbeitete Auflage, 2003 ([available online](https://www5.cs.fau.de/fileadmin/Persons/NiemannHeinrich/klassifikation-von-mustern/m00-www.pdf))
- Huang, Acero, Hon: _Spoken Language Processing: A Guide to Theory, Algorithm and System Development._ (ISBN-13: 978-0130226167)
- Goodfellow, I and Bengio,Y and Courville, A: _Deep Learning._ 2016 ([available online](http://www.deeplearningbook.org/))
- Jurafsky, D and Martin, J: _Speech and Language Processing._ 2017 ([available online](http://web.stanford.edu/~jurafsky/slp3/))
- Manning, C, Raghavan P and Schütze, H: _Introduction to Information Retrieval_, Cambridge University Press. 2008. ([available online](https://nlp.stanford.edu/IR-book/))



## Syllabus

- **March 20: Introduction.** ([slides](00/introduction/), [exercise](00/exercise/))
	
	We'll start with the general concepts of supervised vs. unsupervised learning and classification of independent observations vs. sequences of observations.
	To get you motivated, we'll look at a list of recent "AI products" that utilize sequence learning.

- **March 27: Auto-Correct.** ([slides](http://www.cs.jhu.edu/~langmea/resources/lecture_notes/dp_and_edit_dist.pdf) by [Ben Langmead](http://www.langmead-lab.org/), [exercise](01/autocorrect/))
	
	We'll start with a classic implementation of auto-correcting mispelled words to bring dynamic programming back to memory.
	We'll also look at scalability regarding computation and memory efforts.

- _April 3: Easter holidays_

- _April 10: no class_

- **April 17: States and Cost Functions.** ([slides](02/cost-and-states/slides/), [exercise](02/cost-and-states/))
	
	Understand how DP can be used on an abstraction of distances and states.
	We'll build a smarter, keyboard layout aware auto-correct and start looking into some applications in signal processing (isolated word and DTMF sequence classification).

- **April 24: Modeling Sequences.**
	
	Learn about n-grams, a simple yet effective approach to learn contexts of distcrete symbols.
	We'll use n-grams to improve our auto-correct by incorporating context and suggesting following words.

- _May 1: Labor Day_

- **Maz 8: Hidden Markov Models.**
	
	We'll take a close look at hidden Markov models and how to (efficiently) evaluate them.
	The Viterbi decoding algorithm tells us the most likely sequence and the path that lead to it.

- **May 15: Training of HMM.**
	
	We'll look into the difficulties of training HMMs and how the Viterbi algorithm can be used for a much more efficient training.
	Build your own isolated word recognizer to understand how training and decoding works in practice.

- _May 22: Pentecost_

- **May 29: Higher-Level Sequence Modeling with HMM.**
	
	Learn how to model complex sequences of arbitrary length that prohibit explicit modeling, such as in large vocabulary speech recognition or choreographies in sports.
	Here we will combine what we've discussed so far: prefix trees, n-gram models and efficient search.

- **June 6: Sequence Kernels for Classification.**
	
	We'll take a little detour into how to leverage basic classification algorithms for sequence classification, and demonstrate its use for speaker identification.

- **June 12: Neural Networks.**
	
	A brief introduction to neural networks: fundamentals, topographies, training and embeddings.
	We'll skip implementing the details and use tensorflow for the examples. Did you know that you could program _fizzbuzz_ as a neural network?

- **June 19: Case Study: LVCSR.**
	
	Large vocabular continuous speech recognition (LVCSR) is a flagship application of sequence learning: The state of the art is to combine weighted finite state transducers (as HMM) with deep neural networks (as emission probability surrogate).
	Follow a basic recipe (US/English) to understand which steps and what data is necessary to train a system.

- **June 26: Sequence to Sequence Learning.**
	
	Previous algorithms explicitly modeled the sequence, either via the kernel or via a graph-like structure such as an HMM.
	Encoder-decoder networks are a special kind topology of recurrent neural networks that can be used to model sequence to sequence mappings, such as found in end-to-end speech recognition, machine translation or automatic summarization -- without explicitly modeling states!

- **July 3: Deep Learning: Practical Considerations.**
	
	We'll compare different deep learning toolkits and their requirements or potential to get a grip on what's necessary to apply them to a new problem.

- **NN: Review, Q&A and Exam Prep**
	
	We'll recap the topics we've covered and work through a set of example questions to prepare for the oral exam.
	Please come prepared to get the most out of this class!

- **July 10: oral exams**


_Subscribe to [https://github.com/sikoried/sequence-learning/](https://github.com/sikoried/sequence-learning/) repository to follow updates._
