---
template: page
title: Auto-Correct
permalink: 01/autocorrect/
mathjax: true
---

# 1. Distances

Compute the Hamming and Levenshtein (edit) distances between these word pairs, first _by hand_ and then using a Java (or Javascript) implementation:

![kühler schrank, schüler krank]({{site.baseurl}}/01-autocorrect-dp/97090.jpg)
{: .figcenter}

![nicht ausgeloggt, licht ausgenockt]({{site.baseurl}}/01-autocorrect-dp/97222.jpg)
{: .figcenter}

![gurken schaben, schurkengaben]({{site.baseurl}}/01-autocorrect-dp/97669.jpg)
{: .figcenter}


# 2. Spelling Correction

For spelling correction, we will use prior knowledge, to put some *learning* into our system.

The underlying idea is the _Noisy Channel Model_, that is: The user _intends_ to write a word `w`, but through some noise in the process, happens to type the word `x`.

The correct word $\hat{w}$ is that word, that is a valid candidate and has the highest probability:

$$
\begin{eqnarray}
\DeclareMathOperator*{\argmax}{argmax}
\hat{w} & = & \argmax_{w \in V} P(w | x) \\
        & = & \argmax_{w \in V} \frac{P(x|w) P(w)}{P(x)} \\
        & = & \argmax_{w \in V} P(x|w) P(w)
\end{eqnarray}
$$

1. The candidates $V$ can be obtained from a _vocabulary_.
2. The probability $P(w)$ of a word $w$ can be _learned (counted) from data_.
3. The probability $P(x\|w)$ is more complicated... It could be learned from data, but we could also use a _heuristic_ that relates to the edit distance, e.g. rank by distance.

You can find word statistics and training data at: <http://norvig.com/ngrams/>


### Literature for Noisy Channel (1960s)

- **IBM:** 
	Mays, Eric, Fred J. Damerau and Robert L. Mercer. 1991. Context based spelling correction. _Information Processing and Management_, 23(5), 517–522.
- **AT&T Bell Labs:** 
	Kernighan, Mark D., Kenneth W. Church, and William A. Gale. 1990. A spelling correction program based on a noisy channel model. _Proceedings of COLING_ 1990, 205-210.



# 3. Efficient Implementation

Start working on this in class, finish at home.

How can you implement a spell correction so that it works fast even for large lexica? For now, restrict to isolated words.

Food for thought:

1. How could you optimize the distance computation for words that share a prefix?
2. What about unknown words?

