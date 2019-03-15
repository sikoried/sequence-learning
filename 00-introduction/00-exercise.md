---
layout: page
title: Prelims
permalink: /00/exercise/
---

# Preliminaries

In the first week, you should set up your environment with the necessary tools.
We'll be using Java ([openjdk 11](https://jdk.java.net/11/) recommended), [JSTK](https://github.com/sikoried/jstk) and bash in the first half, Python with Keras and Tensorflow in the second.

If you're using a PC, I stronly recommend to use linux (eg. Ubuntu), ideally as your native OS.
If you have a CUDA-ready graphics card in your machine, make sure to install the `cudatk`.


## Refresh Your Java Skills

We'll be starting with Java programming next week.
I suggest using [IntelliJ](https://www.jetbrains.com/idea/), the community edition is free.
Make sure you're up to date on how to parse and write basic text files, and how to work with the standard containers.

Things you should be familar with:

- basics ([gradle](https://gradle.org/), [junit](https://junit.org/junit5/), [log4j](https://logging.apache.org/log4j/2.x/))
- string matching with [regular expressions](https://docs.oracle.com/javase/11/docs/api/java/util/regex/Pattern.html)
- file I/O with `BufferedReader`, `Scanner`, etc.


## JSTK

Although we won't be using it for just a few more weeks, please clone and build the [JSTK](https://github.com/sikoried/jstk).

You should set the class path so that you can conveniently run its applications:

```bash
$ export CLASSPATH=$(find path/to/jstk/jstk/build/libs -name '*.jar' | xargs echo | tr ' ' ':')
$ java de.fau.cs.jstk.app.Version
```


## Refresh Your Bash Skills

Throughout this class, we'll be using a lot of [bash](https://www.gnu.org/software/bash/).
In case you're not familiar, here's a [bash scripting tutorial](https://ryanstutorials.net/bash-scripting-tutorial/).

