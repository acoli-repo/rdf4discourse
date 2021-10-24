#!/bin/bash
# iterate evaluation script over corpus

MYHOME=`dirname $0`
SCRIPTS=$MYHOME/../../bibles/
ANNOS=$MYHOME/../ensemble

gazes="5 6 8 9 10 11 12"
#gazes=5

# different configurations for individual languages, note that we evaluate against PDTB
for gaz in $gazes; do

  # note: iterate produces both raw and then iterated score
  (echo "-e -p	predicted_dm	gold_dm	tp	|	acc_dm	p_dm	r_dm	f_dm	|	acc_r	p_r	r_r	f_r | conf" | sed s/'\s\s*'/'\t'/g;
    python3 $SCRIPTS/ensemble.py $ANNOS/ar.$gaz.conll -w 1 -e 4 -p 7    10 13 16 21 24 27 30 33 36    -silent -auto -iterate 2>&1 | egrep '0.*\|.*=';
    python3 $SCRIPTS/ensemble.py $ANNOS/bn.$gaz.conll -w 1 -p 4 -e 7 -p 10 13 16 21 24 27 30 33 36    -silent -auto -iterate 2>&1 | egrep '0.*\|.*=';
    python3 $SCRIPTS/ensemble.py $ANNOS/ca.$gaz.conll -w 1 -p 4 7 -e 10 -p 13 16 21 24 27 30 33 36    -silent -auto -iterate 2>&1 | egrep '0.*\|.*=';
    python3 $SCRIPTS/ensemble.py $ANNOS/cs.$gaz.conll -w 1 -p 4 7 10 -e 13 -p 16 21 24 27 30 33 36    -silent -auto -iterate 2>&1 | egrep '0.*\|.*=';
    python3 $SCRIPTS/ensemble.py $ANNOS/de.$gaz.conll -w 1 -p 4 7 10 13 -e 16 -p 21 24 27 30 33 36    -silent -auto -iterate 2>&1 | egrep '0.*\|.*=';
    python3 $SCRIPTS/ensemble.py $ANNOS/en.$gaz.conll -w 1 -p 4 7 10 13 16 -e 21 -p 24 27 30 33 36    -silent -auto -iterate 2>&1 | egrep '0.*\|.*=';
    python3 $SCRIPTS/ensemble.py $ANNOS/es.$gaz.conll -w 1 -p 4 7 10 13 16 21 -e 24 -p 27 30 33 36    -silent -auto -iterate 2>&1 | egrep '0.*\|.*=';
    python3 $SCRIPTS/ensemble.py $ANNOS/fr.$gaz.conll -w 1 -p 4 7 10 13 16 21 24 -e 27 -p 30 33 36    -silent -auto -iterate 2>&1 | egrep '0.*\|.*=';
    python3 $SCRIPTS/ensemble.py $ANNOS/it.$gaz.conll -w 1 -p 4 7 10 13 16 21 24 27 -e 30 -p 33 36    -silent -auto -iterate 2>&1 | egrep '0.*\|.*=';
    python3 $SCRIPTS/ensemble.py $ANNOS/nl.$gaz.conll -w 1 -p 4 7 10 13 16 21 24 27 30 -e 33 -p 36    -silent -auto -iterate 2>&1 | egrep '0.*\|.*=';
    python3 $SCRIPTS/ensemble.py $ANNOS/pt.$gaz.conll -w 1 -p 4 7 10 13 16 21 24 27 30 33    -e 36    -silent -auto -iterate 2>&1 | egrep '0.*\|.*=';
  echo) | tee $MYHOME/ensemble.$gaz.tsv &
done
