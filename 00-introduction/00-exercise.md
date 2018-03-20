---
layout: page
title: Preliminary Exercise
permalink: /00/exercise/
---

# Preliminary Exercise

In this exercise, you will set up your environment and verify your access to the GPU compute server (which we will use for deep learning with TF later this summer).


## Access to Tesla

We have 4 Tesla V100, one P100 and one K40 cards in `tesla.inf.fh-rosenheim.de`.
To get access, send `@riko493` your public SSH key and (official) username.
You need to be inside the `fhintern` WiFi or VPN to read this server.


1. Generate a new password protected SSH key pair (`ssh-keygen`), and send it to `@riko493`, along with your (official) username.
2. `tesla` supports direct SSH login, but since the VPN is a pain, I recommend to use tmux and mosh.
	- <https://github.com/tmux/tmux/wiki>
	- <https://mosh.org/>
	- Here's a great howto: <https://blog.filippo.io/my-remote-shell-session-setup/>
	- ...and a cheat sheet: <http://atkinsam.com/documents/tmux.pdf>
	- I have an alias to `mosh --ssh ssh riko493@tesla.inf.fh-rosenheim.de -- sh -c "ssh-agent tmux a && exit"` which I use to reconnect to my sessions.
3. Get familiar with the terminal; here are a few commands you should know
	- `who` shows you who is currently logged in
	- `htop` shows you current load (processors and memory)
	- `nvidia-smi` shows you the current GPU load
	- You should be able to `import` the `tensorflow` and `numpy` packages in python

> Note: Although we'll do most programming in Java, you will have to get familiar with the terminal if you want to leverage other toolkits and the compute power!


## JSTK

Although we won't be using it for just a few more weeks, please clone and build the [JSTK](https://github.com/sikoried/jstk).

You should set the class path so that you can conveniently run its applications:

```bash
$ export CLASSPATH=$(find path/to/jstk/jstk/build/libs -name '*.jar' | xargs e
cho | tr ' ' ':')
$ java de.fau.cs.jstk.Version
```

## Refresh Your Java Knowledge

We'll be starting with Java programming next week.
Make sure you're up to date on how to parse and write basic text files, and how to work with the standard containers.

Things we'll be needing:

- basics ([gradle](https://gradle.org/), [junit](https://junit.org/junit5/), [log4j](https://logging.apache.org/log4j/2.x/))
- string matching with [regular expressions](https://docs.oracle.com/javase/9/docs/api/java/util/regex/Pattern.html)
- file I/O with `BufferedReader`, `Scanner`, etc.
