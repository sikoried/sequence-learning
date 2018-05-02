#!/bin/bash

# Goethe Faust

tail -n +53 pg2229.txt |\
    sed -E 's:^ +::' |\
    sed -E 's/^[ A-Z]+://' |\
    perl -pe 's/,\R/ /g; $_=lc' |\
    tr 'ÄÖÜ' 'äöü' |\
    sed -E 's/[,.?!:;-()]//g' |\
    awk '{if (NF>1) print}' > faust.txt

# Goethe Werther 1+2
tail -n +300 pg2407.txt |\
    perl -pe 's/^(Am|Den) [0-9]+. [A-Za-z]+//' |\
    sed -E 's:--: :g' |\
    sed -E 's:["(),]: :g' |\
    perl -pe 's/\R/ /g; $_=lc' |\
    perl -ple 's/[.?!:;]/\n/g' |\
    perl -pe 's/^\s+//' |\
    perl -pe 's/\s\s+/ /g' > werther1.txt


tail -n +377 pg2408.txt |\
    perl -pe 's/^(Am|Den) [0-9]+. [A-Za-z]+//' |\
    sed -E 's:--: :g' |\
    sed -E 's:["(),]: :g' |\
    perl -pe 's/\R/ /g; $_=lc' |\
    perl -ple 's/[.?!:;]/\n/g' |\
    perl -pe 's/^\s+//' |\
    perl -pe 's/\s\s+/ /g' > werther2.txt


# Schiller Die Raeuber

tail -n +261 pg47804.txt |\
    perl -pe 's/^~[A-Za-z .]+~ //' |\
    perl -pe 's/([a-z,])\R/\1 /g; $_=lc' |
    perl -pe 's/\(_[A-Za-z .,]+_\)//g' |\
    perl -pe 's/~[A-Za-z .,]+~//g' |\
    sed -E 's:--: :g' |\
    sed -E 's:["(),»«_=]: :g' |\
    perl -pe 's/\./\n/g' |\
    perl -ple 's/[.?!:;]/ /g' |\
    perl -pe 's/^\s+//' |\
    perl -pe 's/\s\s+/ /g' > dieraeuber.txt
