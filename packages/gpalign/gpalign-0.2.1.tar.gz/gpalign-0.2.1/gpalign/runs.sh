#!/bin/bash

set -x

/usr/bin/time -o output/tfidf.time ./align.py output/tfidf.out
/usr/bin/time -o output/tfidf-nk.time ./align.py --no-kanjidic output/tfidf-nk.out

/usr/bin/time -o output/tf.time ./align.py --tf-only output/tf.out
/usr/bin/time -o output/tf-nk.time ./align.py --no-kanjidic --tf-only output/tfn-nk.out

/usr/bin/time -o output/idf.time ./align.py --idf-only output/idf.out
/usr/bin/time -o output/idf-nk.time ./align.py --no-kanjidic --idf-only output/idf-nk.out

/usr/bin/time -o output/random.time ./align.py --random output/random.out
/usr/bin/time -o output/random-nk.time ./align.py --no-kanjidic --random output/random-nk.out
