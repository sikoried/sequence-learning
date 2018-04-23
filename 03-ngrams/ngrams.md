---
template: page
title: n-grams
permalink: 03/ngrams/
mathjax: true
---

# Working with n-grams

This week, we will use [SRILM](http://www.speech.sri.com/projects/srilm/) to estimate n-gram models, and then use them in our auto-correct, as auto-complete and to classify text genres.


## Data

We will work with some classic german literature:

- Goethe's [Faust 1](http://www.gutenberg.org/cache/epub/2229/pg2229.txt)
- Goethe's Die Leiden des jungen Werther [Teil 1](http://www.gutenberg.org/cache/epub/2407/pg2407.txt) and [Teil 2](http://www.gutenberg.org/cache/epub/2408/pg2408.txt)
- Schiller's [Die Räuber](http://www.gutenberg.org/cache/epub/47804/pg47804.txt)

Download the above data as a [zip file]({{site.baseurl}}/03-ngrams/gutenbergorg.zip); enclosed is a bash script `prep.sh` that strips the formatted text down to single UTF-8 lines.


## Get familiar with SRILM

You can find a recent build of [SRILM](http://www.speech.sri.com/projects/srilm/) on `tesla` at `/mnt/raid0/user/riko493/srilm`.
Add its `bin` and `sbin` to your path.

```bash
$ cd /mnt/raid0/user/riko493/srilm
$ export SRILM=$(pwd)
$ export PATH=$PATH:$SRILM/bin:$SRILM/bin/i686-m64:$SRILM/sbin
$ ngram-count -help  # verify srilm works!
```

## Estimate n-gram models

- estimate n-gram models with $n = 1, 2, 3, 4$ on the different text books, and one joint model
- for the trigram models, compute the perplexity of each model on each of the text books; can you interpret the score for the jointly trained model?
- take the German abstract of your bachelor thesis and normalize it for lowercase; what are the perplexities?


## Text classification

> Verlassen hab ich Feld und Auen,
  Die eine tiefe Nacht bedeckt,
  Mit ahnungsvollem, heil'gem Grauen
  In uns die beßre Seele weckt.
  Entschlafen sind nun wilde Triebe
  Mit jedem ungestümen Tun;
  Es reget sich die Menschenliebe,
  Die Liebe Gottes regt sich nun.  Sei ruhig, Pudel!  renne nicht hin und
  wider!
  An der Schwelle was schnoperst du hier?
  Lege dich hinter den Ofen nieder,
  Mein bestes Kissen geb ich dir.
  Wie du draußen auf dem bergigen Wege
  Durch Rennen und Springen ergetzt uns hast,
  So nimm nun auch von mir die Pflege,

- Normalize the text; feel free to learn from the `prep.sh` script.
- What's the perplexity of the above text?
- What model does it fit best?


# Auto-complete

- Write a routine to load n-gram models into memory
- Write a routine that displays the $m$ most likely words given the current history; for the first word, use the unigram probabilities.
- Write a command line (or gui) component that displays the the predicted words and allows the user to select one.
- Try it out with the different models.

# Auto-correct

- Extend the auto-correct algorithm by incorporating a history of previous words
