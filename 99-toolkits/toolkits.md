---
template: page
title: "Deep Learning: Practical Considerations"
permalink: 09/toolkits/
mathjax: true
---

# Part 1: Comparing Toolkits

Here's a list of currently "hot" machine learning toolkits:

- [Theano](http://www.deeplearning.net/software/theano/)
- [TensorFlow](https://www.tensorflow.org)
- [Microsoft Cognitive Toolkit](https://docs.microsoft.com/en-us/cognitive-toolkit/)
- [Torch](http://torch.ch/)
- [MXNet](http://mxnet.incubator.apache.org/)
- [Caffe](http://caffe.berkeleyvision.org/)
- [Keras](https://keras.io)
- [deeplearning4j](https://deeplearning4j.org/)
- [Core ML](https://developer.apple.com/machine-learning/)

## Exercise

Pick two toolkits.

- What are pros and cons?
- Which one would you choose, and why?
- Work out a basic example that gets you started: [admission.asc]({{site.baseurl}}/09-toolkits/admission.asc) is a tiny classification task, the last column is the label

For your reference, Wikipedia maintains a [comparison of deep learning software](https://en.wikipedia.org/wiki/Comparison_of_deep_learning_software), and there's a recent arxiv article that [compares numerous toolkits](https://arxiv.org/pdf/1803.04818.pdf).


# Part 2: Practical Considerations

See the [slide deck]({{site.baseurl}}/09/toolkits/practical-considerations/).

## Exercise

For sequence to sequence learning, it is common practice to use training examples that have a fixed number of _output frames_, with variable-but-similar number of _input frames_.
For an example problem, you've been provided the following [alignments]({{site.baseurl}}/09-toolkits/alignments.txt) to be used to partition your data:

```
# <file-id> [<symbol> <length> (; <symbol> <length>)*]
AAA_m159dxx0_010_AAA 1 5 ; 23 13 ; 35 5 ; 9 4 ; 41 7 ; 32 6 ; 35 6 ; 17 10 ; 40 11 ; 1 3 
```

Where `symbol` is an integer ID of the output symbol, and `length` is the number of input samples corresponding to this segment.

- Write a function that reads in the [alignments file]({{site.baseurl}}/09-toolkits/alignments.txt) and outputs a list of examples, similar to the lines below
- Files with less output symbols than the desired length should be ignored

```
# <example-id> <start-input-index> <end-input-index> <output labels...>
AAA_m159dxx0_018_AAA_0042 368 422 40 12 10 9 14 10 24 14 42 9
```

```python
def make_examples(file, num_outputs=8, stride=1):
	"""
	Given per-file alignments, compute output labels and corresponding
	input frame indices for the given parameters:
	  file:        file pointer to read alignments from
	  num_outputs: how many output labels per example
	  stride:      how many output frames should the window be advanced
	  returns:     list of tuples (egs-id, input-start, input-end, [labels...])
	"""
	# ...
```


Solution: [examples.py]({{site.baseurl}}/09-toolkits/examples.py)

# Part 3: Deploying Machine Learning Models

See the [slide deck]({{site.baseurl}}/09/toolkits/deployment/).
