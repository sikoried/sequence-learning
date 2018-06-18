---
template: page
title: Sequence to Sequence Modeling
permalink: 08/seq2seq/
mathjax: true
---

# Literature

We'll cover three of the seminal papers in sequence to sequence learning:

- _Connectionist Temporal Classification: Labelling Unsegmented Sequence Data with Recurrent Neural Networks_ by Alex Graves et al. (<https://dl.acm.org/citation.cfm?id=1143891>, [author's copy](https://www.cs.toronto.edu/~graves/icml_2006.pdf))
- _Listen, Attend and Spell_ by William Chan et al. (<https://ieeexplore.ieee.org/document/7472621/> (<https://arxiv.org/abs/1508.01211>))
- _Neural Machine Translation by Jointly Learning to Align and Translate_ by Dzmitry Bahdanau et al. (<https://arxiv.org/abs/1409.0473>).

As well as [_Attention and Augmented Recurrent Neural Networks_](https://distill.pub/2016/augmented-rnns/) by Chris Olah and Shan Carter.


# Exercise

There is a basic [TensorFlow tutorial on seq2seq](https://www.tensorflow.org/tutorials/seq2seq).

For this week, let's get a smaller example going: synthesis of handwriting using [rnnlib](https://github.com/szcom/rnnlib) and the Uni Bern [IAM On-Line Handwriting Database](http://www.fki.inf.unibe.ch/databases/iam-on-line-handwriting-database).

## Remarks

- You can either register for the dataset, or obtain a copy during class.
- If you run into trouble building openblas (as a submodule of rnnlib), you may need to specify the target CPU architecture (eg. Macbook Pro 2017: HASWELL).
- It's recommended to add the rnnlib directory to your path (eg. `export PATH=$(pwd):$PATH`).
- You will need the python packages `ScientificPython` and `scipy`
- On a mac, use `brew` to install the packages `netcdf`, `nco` and `ncview` (more on netcdf [here](https://www.unidata.ucar.edu/software/netcdf/docs/tutorial_8dox.html) or [here](http://pro.arcgis.com/en/pro-app/help/data/imagery/fundamentals-of-netcdf.htm))
