#!/bin/bash
# iterate evaluation script over corpus

MYHOME=`dirname $0`
ANNOS=$MYHOME/../ensemble

#gazes="5 6 8 9 10 11 12"
gazes=5

# different configurations for individual languages, note that we evaluate against PDTB
for gaz in $gazes; do
  (echo "-e -p	predicted_dm	gold_dm	tp	|	acc_dm	p_dm	r_dm	f_dm	|	acc_r	p_r	r_r	f_r | conf" | sed s/'\s\s*'/'\t'/g;
  (
    python3 $MYHOME/../ensemble.py $ANNOS/cs.$gaz.conll -w 1 -e 4 -p 7 12 15 18 21 24 27    -silent -auto;
    python3 $MYHOME/../ensemble.py $ANNOS/de.$gaz.conll -w 1 -p 4 -e 7 -p 12 15 18 21 24 27 -silent -auto;
    python3 $MYHOME/../ensemble.py $ANNOS/en.$gaz.conll -w 1 -p 4 7 -e 12 -p 15 18 21 24 27 -silent -auto;
    python3 $MYHOME/../ensemble.py $ANNOS/es.$gaz.conll -w 1 -p 4 7 12 -e 15 -p 18 21 24 27 -silent -auto;
    python3 $MYHOME/../ensemble.py $ANNOS/fr.$gaz.conll -w 1 -p 4 7 12 15 -e 18 -p 21 24 27 -silent -auto;
    python3 $MYHOME/../ensemble.py $ANNOS/it.$gaz.conll -w 1 -p 4 7 12 15 18 -e 21 -p 24 27 -silent -auto;
    python3 $MYHOME/../ensemble.py $ANNOS/nl.$gaz.conll -w 1 -p 4 7 12 15 18 21 -e 24 -p 27 -silent -auto;
    python3 $MYHOME/../ensemble.py $ANNOS/pt.$gaz.conll -w 1 -p 4 7 12 15 18 21 24 -e 27    -silent -auto;
  ) 2>&1 | \
  egrep '0.*\|'
  echo) | tee $MYHOME/ensemble.$gaz.direct.tsv

  (echo "-e -p	predicted_dm	gold_dm	tp	|	acc_dm	p_dm	r_dm	f_dm	|	acc_r	p_r	r_r	f_r | conf" | sed s/'\s\s*'/'\t'/g;
  (
    python3 $MYHOME/../ensemble.py $ANNOS/cs.$gaz.conll -w 1 -e 4 -p 7 12 15 18 21 24 27    -silent -auto -iterate;
    python3 $MYHOME/../ensemble.py $ANNOS/de.$gaz.conll -w 1 -p 4 -e 7 -p 12 15 18 21 24 27 -silent -auto -iterate;
    python3 $MYHOME/../ensemble.py $ANNOS/en.$gaz.conll -w 1 -p 4 7 -e 12 -p 15 18 21 24 27 -silent -auto -iterate;
    python3 $MYHOME/../ensemble.py $ANNOS/es.$gaz.conll -w 1 -p 4 7 12 -e 15 -p 18 21 24 27 -silent -auto -iterate;
    python3 $MYHOME/../ensemble.py $ANNOS/fr.$gaz.conll -w 1 -p 4 7 12 15 -e 18 -p 21 24 27 -silent -auto -iterate;
    python3 $MYHOME/../ensemble.py $ANNOS/it.$gaz.conll -w 1 -p 4 7 12 15 18 -e 21 -p 24 27 -silent -auto -iterate;
    python3 $MYHOME/../ensemble.py $ANNOS/nl.$gaz.conll -w 1 -p 4 7 12 15 18 21 -e 24 -p 27 -silent -auto -iterate;
    python3 $MYHOME/../ensemble.py $ANNOS/pt.$gaz.conll -w 1 -p 4 7 12 15 18 21 24 -e 27    -silent -auto -iterate;
  ) 2>&1 | \
  egrep '0.*\|'
  echo) | tee $MYHOME/ensemble.$gaz.iterate.tsv

done


# todo: explore parameters for one specific constellation

# echo effect of -th, discourse 3 only
# echo "-th  | predicted dm	gold dm	tp	|	acc_dm	p_dm	r_dm	f_dm	|	acc_r	p_r	r_r	f_r"
# for th in -1 0.0 0.01 0.05 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0; do
#     python3 ensemble.py bibl.mrg.conll -th $th -w 1 -p 7 13 -e 19 -p 25 31 37 43 -silent 2>&1 | \
#     sed s/'.*\r'//g | grep -v predict  | perl -pe 's/(\])\s+/$1\t/g;' | \
#     tail -n 1 | sed s/'^'/$th'\t'/g
# done
# echo
# echo iterated, effect of -th vs. -c, discourse 3 only
# echo "-th -c | predicted dm	gold dm	tp	|	acc_dm	p_dm	r_dm	f_dm	|	acc_r	p_r	r_r	f_r"
# for th in -1 0.0 0.01 0.05 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0; do
#   for c in -1 0.0 0.01 0.05 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0; do
#     python3 ensemble.py bibl.mrg.conll -c $c -th $th -w 1 -p 7 13 -e 19 -p 25 31 37 43 -silent -iterate 2>&1 | \
#     sed s/'.*\r'//g | grep -v predict  | perl -pe 's/(\])\s+/$1\t/g;' | \
#     tail -n 1 | sed s/'^'/$th'\t'$c'\t'/g
#   done
# done
# ) | \
# tee eval.tsv


# eval using
# less eval.tsv | cut -f 1,3,7-8,11-13,16 | sed s/' '//g  | sort -k 8 | egrep '^\[19\]'
