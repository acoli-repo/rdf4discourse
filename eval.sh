#!/bin/bash
# iterate evaluation script over corpus

# evaluate against gold annotations from English (in default settings, this is best-performing)
(echo "predicted dm	gold dm	tp	|	acc_dm	p_dm	r_dm	f_dm	|	acc_r	p_r	r_r	f_r"
echo
echo discourse 1
python3 ensemble.py bibl.mrg.conll -w 1 -p 5 11 -e 17 -p 23 29 35 41 -silent -auto 2>&1 | \
sed s/'.*\r'//g | grep -v predict  | perl -pe 's/(\])\s+/$1\t/g;'
echo
echo discourse 2
python3 ensemble.py bibl.mrg.conll -w 1 -p 6 12 -e 18 -p 24 30 36 42 -silent -auto 2>&1 | \
sed s/'.*\r'//g | grep -v predict  | perl -pe 's/(\])\s+/$1\t/g;'
echo
echo discourse 3
python3 ensemble.py bibl.mrg.conll -w 1 -p 7 13 -e 19 -p 25 31 37 43 -silent -auto 2>&1 | \
sed s/'.*\r'//g | grep -v predict  | perl -pe 's/(\])\s+/$1\t/g;'
) | \
tee eval.tsv

# eval using
# less eval.tsv | cut -f 1,3,7-8,11-13,16 | sed s/' '//g  | sort -k 8 | egrep '^\[19\]'
