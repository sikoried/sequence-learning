#!/bin/bash

export CLASSPATH=$(find /Users/riedhammerko/git/sikoried/jstk/build/libs -name '*.jar' | xargs echo | tr ' ' ':')

java com.github.sikoried.jstk.app.Version
