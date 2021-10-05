#!/bin/bash
# iterate evaluation script over corpus

# evaluate against gold annotations from English (in default settings, this is best-performing)
# (echo "predicted dm	gold dm	tp	|	acc_dm	p_dm	r_dm	f_dm	|	acc_r	p_r	r_r	f_r"
# echo
# echo discourse 1
# python3 ensemble.py bibl.mrg.conll -w 1 -p 5 11 -e 17 -p 23 29 35 41 -silent -auto 2>&1 | \
# sed s/'.*\r'//g | grep -v predict  | perl -pe 's/(\])\s+/$1\t/g;'
# echo
# echo discourse 2
# python3 ensemble.py bibl.mrg.conll -w 1 -p 6 12 -e 18 -p 24 30 36 42 -silent -auto 2>&1 | \
# sed s/'.*\r'//g | grep -v predict  | perl -pe 's/(\])\s+/$1\t/g;'
# echo
# echo discourse 3
# python3 ensemble.py bibl.mrg.conll -w 1 -p 7 13 -e 19 -p 25 31 37 43 -silent -auto 2>&1 | \
# sed s/'.*\r'//g | grep -v predict  | perl -pe 's/(\])\s+/$1\t/g;'
# echo
# echo effect of -c, discourse 3 only
# echo "-c | predicted dm	gold dm	tp	|	acc_dm	p_dm	r_dm	f_dm	|	acc_r	p_r	r_r	f_r"
# for c in -1 0.0 0.01 0.05 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0; do
#   python3 ensemble.py bibl.mrg.conll -c $c -w 1 -p 7 13 -e 19 -p 25 31 37 43 -silent -iterate 2>&1 | \
#   sed s/'.*\r'//g | grep -v predict  | perl -pe 's/(\])\s+/$1\t/g;' | \
#   tail -n 1 | sed s/'^'/$c'\t'/g
# done
# echo
# echo effect of -th, discourse 3 only
# echo "-th | predicted dm	gold dm	tp	|	acc_dm	p_dm	r_dm	f_dm	|	acc_r	p_r	r_r	f_r"
# for th in -1 0.0 0.01 0.05 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0; do
#   python3 ensemble.py bibl.mrg.conll -th $th -w 1 -p 7 13 -e 19 -p 25 31 37 43 -silent -iterate 2>&1 | \
#   sed s/'.*\r'//g | grep -v predict  | perl -pe 's/(\])\s+/$1\t/g;' | \
#   tail -n 1 | sed s/'^'/$th'\t'/g
# done
echo
echo effect of -th vs. -c, discourse 3 only
echo "-th -c | predicted dm	gold dm	tp	|	acc_dm	p_dm	r_dm	f_dm	|	acc_r	p_r	r_r	f_r"
for th in -1 0.0 0.01 0.05 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0; do
  for c in -1 0.0 0.01 0.05 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0; do
    python3 ensemble.py bibl.mrg.conll -c $c -th $th -w 1 -p 7 13 -e 19 -p 25 31 37 43 -silent -iterate 2>&1 | \
    sed s/'.*\r'//g | grep -v predict  | perl -pe 's/(\])\s+/$1\t/g;' | \
    tail -n 1 | sed s/'^'/$th'\t'$c'\t'/g
  done
done
# ) | \
# tee eval.tsv


# eval using
# less eval.tsv | cut -f 1,3,7-8,11-13,16 | sed s/' '//g  | sort -k 8 | egrep '^\[19\]'
