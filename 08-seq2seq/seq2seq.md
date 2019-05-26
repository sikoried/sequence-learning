---
template: page
title: Sequence to Sequence Modeling
permalink: 08/seq2seq/
mathjax: true
---

# Literature

We'll cover three of the seminal papers in sequence to sequence learning:

- _Connectionist Temporal Classification: Labelling Unsegmented Sequence Data with Recurrent Neural Networks_ by Alex Graves et al. (<https://dl.acm.org/citation.cfm?id=1143891>, [author's copy](https://www.cs.toronto.edu/~graves/icml_2006.pdf)); check out this [very helpful visualization](https://distill.pub/2017/ctc/)
- _Sequence to Sequence Learning for Neural Networls_ by Sutskever et al. (<https://arxiv.org/abs/1409.3215>)
- _Neural Machine Translation by Jointly Learning to Align and Translate_ by Dzmitry Bahdanau et al. (<https://arxiv.org/abs/1409.0473>).
- _Listen, Attend and Spell_ by William Chan et al. (<https://arxiv.org/abs/1508.01211>)
- _Attention is all you need_ (<https://arxiv.org/abs/1706.03762>)



As well as [_Attention and Augmented Recurrent Neural Networks_](https://distill.pub/2016/augmented-rnns/#attentional-interfaces) by Chris Olah and Shan Carter.


# Exercise

There is way too much to cover in one exercise.
Here are a few options:

- [Transformer Implementation](https://github.com/lilianweng/transformer-tensorflow) in TensorFlow for Machine Translation. **Recommended exercise, using theses titles 2014-2018 (see Moodle)**
- Extensive TensorFlow tutorial on [machine translation using attention](https://github.com/tensorflow/nmt) ([Colab](https://github.com/tensorflow/tensorflow/blob/r1.13/tensorflow/contrib/eager/python/examples/nmt_with_attention/nmt_with_attention.ipynb)).
- Synthesis of handwriting using [rnnlib](https://github.com/szcom/rnnlib) and the Uni Bern [IAM On-Line Handwriting Database](http://www.fki.inf.unibe.ch/databases/iam-on-line-handwriting-database); see remarks below.


## Remarks

- You can either register for the dataset, or obtain a copy during class.
- If you run into trouble building openblas (as a submodule of rnnlib), you may need to specify the target CPU architecture (eg. Macbook Pro 2017: HASWELL, see [example diff file](08-seq2seq/patch-cmake.diff)).
- It's recommended to add the rnnlib directory to your path (eg. `export PATH=$(pwd):$PATH`).
- You will need the python packages `ScientificPython` and `scipy`
- On a mac, use `brew` to install the packages `netcdf`, `nco` and `ncview` (more on netcdf [here](https://www.unidata.ucar.edu/software/netcdf/docs/tutorial_8dox.html) or [here](http://pro.arcgis.com/en/pro-app/help/data/imagery/fundamentals-of-netcdf.htm))
- It seems that the current `master` branch is broken for recent netcfd/python2; use [this patch](08-seq2seq/patch-ncf4.diff) to fix the NCF generation.
- The recipe will take a few hours to compute -- it's best to let it run over night!
