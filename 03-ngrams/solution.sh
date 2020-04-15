#!/bin/bash


# Modelle schaetzen, Perplexität berechnen

# ein Beispiel
ngram-count -order 3 werther1.txt -lm werther1.arpa.gz
ngram -lm werther1.arpa.gz -ppl <(head -n3 werther1.txt)

# also try -debug 0, 1, 2

# file werther1.txt: 997 sentences, 17634 words, 0 OOVs
# 0 zeroprobs, logprob= -33140.61 ppl= 60.08814 ppl1= 75.74585
# file faust.txt: 3892 sentences, 32650 words, 10274 OOVs
# 0 zeroprobs, logprob= -64340.27 ppl= 281.4351 ppl1= 750.6099
# file werther2.txt: 1556 sentences, 21420 words, 3587 OOVs
# 0 zeroprobs, logprob= -48201.64 ppl= 306.2175 ppl1= 504.5985


# now do the approx same length in text!
ngram -lm werther1.arpa.gz -ppl <(head -c 10000 werther1.txt)
# file /dev/fd/11: 102 sentences, 1648 words, 1 OOVs
# 0 zeroprobs, logprob= -3094.877 ppl= 58.8183 ppl1= 75.70068

ngram -lm werther1.arpa.gz -ppl <(head -c 10000 faust.txt)
# file /dev/fd/11: 158 sentences, 1604 words, 430 OOVs
# 0 zeroprobs, logprob= -3430.357 ppl= 376.1342 ppl1= 835.4861

ngram -lm werther1.arpa.gz -ppl <(head -c 10000 werther2.txt)
# file /dev/fd/11: 108 sentences, 1673 words, 263 OOVs
# 0 zeroprobs, logprob= -3759.396 ppl= 299.6024 ppl1= 463.701


# explore...
for n in 1 2 3 4; do
  for f in werther1 werter2 faust; do
    ngram-count -text $i.txt -order $n -lm $i.arpa.gz
  done
done

ngram-count -text werther1.txt -lm werther1.arpa
ngram-count -order 3 -text <(cat hsro-theses.txt theses-ohm.txt) -lm theses.arpa.gz


# Modell auswerten:

for i in faust werther1; do ngram -lm $i.arpa.gz -ppl <(bash prep-2.sh sample.txt); done
# file /dev/fd/11: 4 sentences, 90 words, 1 OOVs
# 0 zeroprobs, logprob= -184.3947 ppl= 96.10334 ppl1= 117.9914
# file /dev/fd/11: 4 sentences, 90 words, 28 OOVs
# 0 zeroprobs, logprob= -165.8935 ppl= 326.2408 ppl1= 473.9167


# Modell samplen
ngram-count -order 3 -text theses.txt -lm theses.arpa.gz
ngram -lm theses.arpa.gz -gen 10



erlassen hab ich Feld und Auen, Die eine tiefe Nacht bedeckt, Mit ahnungsvollem, heil’gem Grauen In uns die beßre Seele weckt. Entschlafen sind nun wilde Triebe Mit jedem ungestümen Tun; Es reget sich die Menschenliebe, Die Liebe Gottes regt sich nun. Sei ruhig, Pudel! renne nicht hin und wider! An der Schwelle was schnoperst du hier? Lege dich hinter den Ofen nieder, Mein bestes Kissen geb ich dir. Wie du draußen auf dem bergigen Wege Durch Rennen und Springen ergetzt uns hast, So nimm nun auch von mir die Pflege,


cat testtext | tr A-Z a-z  



scp sl2018@tesla.inf.fh-rosenheim.de:/mnt/raid0/scratch/riko493/ngrams2/gemischt.arpa .
