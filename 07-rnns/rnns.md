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
- [POTUS on Twitter]({{site.baseurl}}/07-rnns/potus.txt)
- ...or your `bash` history?


# RNN using pytorch

Here are a number of related tutorials:

- [Sentiment Analysis](https://medium.com/@dipikabaad/finding-the-hidden-sentiments-using-rnns-in-pytorch-f1e1e9638e9c)
- [Practical Pytorch's RNN Character Generation](https://github.com/spro/practical-pytorch/blob/master/char-rnn-generation/char-rnn-generation.ipynb)
- Ben Trevett's [basic](https://github.com/bentrevett/pytorch-sentiment-analysis/blob/master/1%20-%20Simple%20Sentiment%20Analysis.ipynb) and [advanced](https://github.com/bentrevett/pytorch-sentiment-analysis/blob/master/2%20-%20Upgraded%20Sentiment%20Analysis.ipynb) sentiment analysis
- Gabriel Loye's [LSTM Tutorial](https://github.com/gabrielloye/LSTM_Sentiment-Analysis/blob/master/LSTM_starter.ipynb)
