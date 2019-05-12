---
template: page
title: Recurrent Neural Networks
permalink: 07/rnns/
mathjax: true
---

# RNN-LM

Check out Andrej Karpathy's excellent blog post on the [Unreasonable Effectiveness of Recurrent Neural Networks](https://karpathy.github.io/2015/05/21/rnn-effectiveness/), and the corresponding basic (vanilla) [RNN implementation](https://gist.github.com/karpathy/d4dee566867f8291f086), that learns to [predict characters](https://karpathy.github.io/2015/05/21/rnn-effectiveness/#character-level-language-models) one at a time.
To generate new text, you can start with a random character, and then select randomly from the most likely next characters (to add some randomness to each generated text).

As you can see, it loads its input data from a plain text file ([line 8](https://gist.github.com/karpathy/d4dee566867f8291f086#file-min-char-rnn-py-L8)).
Choose from a variety of datasets to train different models and sample some text:

- [Goethe's Faust]({{site.baseurl}}/03-ngrams/faust.txt)
- [Schiller's Die Räuber]({{site.baseurl}}/03-ngrams/dieraeuber.txt)
- [Thesis Titles]({{site.baseurl}}/03-ngrams/hsro-theses.txt)
- [POTUS on Twitter]({{site.baseurl}}/07-rnns/putus.txt)
- ...or your `bash` history?


# Quick, draw! 

For a better task using LSTMs, we'll use the [quick, draw!](https://quickdraw.withgoogle.com/data) data.

The task is to classify a drawing of an object based on the pen strokes (ie. a sequence of drawing inputs).
For image processing tasks (and in fact, also for speech!), [convolutional neural networks]({{site.baseurl}}/07-rnns/sl-convnets.pdf) are a great choice to learn image structures.

You can work your way through the respective [TensorFlow Tutorial](https://www.tensorflow.org/tutorials/recurrent_quickdraw), or if you prefer to work on Colab, follow [this tutorial](https://medium.com/tensorflow/train-on-google-colab-and-run-on-the-browser-a-case-study-8a45f9b1474e)
