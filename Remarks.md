# Remarks for 2018

## Syllabis Brainstorm

- Intro:
	+ Supervised and unsupervised learning
	+ Classification vs. sequence classification
	+ Applications of Sequence Learning
	+ Exercises: set up your environment:
		* SSH key to tesla (--> SL container?)
		* Mosh/Tmux Tutorial
		* jstk
		* Languages? Java, Python
- 1/A basic auto-correct algorithm using DP
	We'll implement a basic auto-correct algorithm based on string edit distance (aka Levenshtein distance) and a word list
	+ Measuring differences in sequences: Levenshtein
	+ Baseline implementation (DP)
	+ Practical considerations: max-edit, partial results?
	+ Improved implementation: prefix trees, rx
- 2/Understanding states and cost functions.
	Understand how DP can abstract on states and cost functions, and how this can drive sequence classification for various applications
	+ auto-correct for different languages or keyboard layouts
	+ isolated word recognition
	+ DTMF sequence recognition
	+ phone sequence recognition (using mean values)
- 3/Modeling sequences: n-gram Models
	N-grams are a simple yet effective way to model sequences of discrete symbols.
	+ Estimating n-gram models
	+ Factored language model weights for improved auto-correct
	+ Predicting symbols based on n-gram models
	+ http://norvig.com/ngrams/
	+ http://norvig.com/spell-correct.html
- 4/Hidden Markov Models
	Learn how DTW is a (very) special case of an HMM and how it can be used to model sequences.
	+ Basic HMM evaluation (no training just yet)
	+ Alignment and Viterbi Algorithm
	+ EM/Baum-Welch training
	+ Viterbi training
	+ Isolated word recognition
- 5/Higher-level models and efficient decoding
	+ jump sequence detection
	+ basic word recognition
	+ TIMIT/word sequences?
- 6/Sequence kernels and classification
	+ Isolated word recognition
	+ Speaker identification
- 7/Neural Networks: Basics, Training and Topographies
- 8/Sequence to Sequence Learning
- 9/Case Study: large vocabylary speech recognition with kaldi
- 10/Deep Learning Toolkits

