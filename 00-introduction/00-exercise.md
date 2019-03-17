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

Although we won't be using it for just a few more weeks, please set up a new git repository, and add [JSTK](https://github.com/sikoried/jstk) as a submodule.

```bash
mkdir sl-examples
git init
git submodule add https://github.com/sikoried/jstk
```

Make sure to include `jstk` in your gradle build file.
We will also be using the Apache Commons [`lang3`](https://commons.apache.org/proper/commons-lang/), [`beanutils`](http://commons.apache.org/proper/commons-beanutils/) and [`configuration2`](https://commons.apache.org/proper/commons-configuration/userguide/upgradeto2_0.html) as well as `junit5`.
While IntelliJ does all the env magic for you, you may want to specify an `env` target that produces the correct `CLASSPATH` variable to be exported.
Here's a partial example:

```groovy
task env (dependsOn: configurations.runtime) {
    doLast {
        println "export CLASSPATH=${(configurations.runtime + sourceSets.main.runtimeClasspath).collect { File file -> file.absolutePath } join ':' }"
    }
}

dependencies {
    compile group: 'org.apache.commons', name: 'commons-lang3', version: '3.7'
    compile group: 'commons-beanutils', name: 'commons-beanutils', version: '1.9.3'
    compile group: 'org.apache.commons', name: 'commons-configuration2', version: '2.2'
    compile project(':jstk')  // comes with junit

    testCompile("org.junit.jupiter:junit-jupiter-api:${junit_jupiter_version}")
    testCompile("org.apache.logging.log4j:log4j-core:${log4j_version}")
    testCompile("org.apache.logging.log4j:log4j-jul:${log4j_version}")

    testRuntime("org.junit.jupiter:junit-jupiter-params:${junit_jupiter_version}")
    testRuntime("org.junit.jupiter:junit-jupiter-engine:${junit_jupiter_version}")
    testRuntime("org.junit.platform:junit-platform-launcher:${junit_platform_version}")
}
```

Note: The solutions to the Java exercises can be found in [sikoried/sl-examples](https://github.com/sikoried/sl-examples/), which has `jstk` as a submodule.


## Refresh Your Bash Skills

Throughout this class, we'll be using a lot of [bash](https://www.gnu.org/software/bash/).
In case you're not familiar, here's a [bash scripting tutorial](https://ryanstutorials.net/bash-scripting-tutorial/).


## Refresh Your Python Skills

We won't be using Python for a while, but if you have never worked with python, you should start looking into it.

