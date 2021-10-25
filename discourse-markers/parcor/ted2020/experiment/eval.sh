#!/bin/bash
# iterate evaluation script over corpus

MYHOME=`dirname $0`
SCRIPTS=$MYHOME/../../bibles/
ANNOS=$MYHOME/../ensemble

gazes="5 6 8 9 10 11 12"
# gazes=5

# different configurations for individual languages, note that we evaluate against PDTB
for gaz in $gazes; do
  if [ ! -e $MYHOME/ensemble.$gaz.tsv ]; then
    # note: iterate produces both raw and then iterated score
    (echo "-e -p	predicted_dm	gold_dm	tp	|	acc_dm	p_dm	r_dm	f_dm	|	acc_r	p_r	r_r	f_r | conf" | sed s/'\s\s*'/'\t'/g;
      python3 -u $SCRIPTS/ensemble.py $ANNOS/ar.$gaz.conll.gz -w 1 -e 4 -p 7    10 13 16 21 24 27 30 33 36    -silent -auto -iterate 2>&1 | egrep '0.*\|.*=';
      python3 -u $SCRIPTS/ensemble.py $ANNOS/bn.$gaz.conll.gz -w 1 -p 4 -e 7 -p 10 13 16 21 24 27 30 33 36    -silent -auto -iterate 2>&1 | egrep '0.*\|.*=';
      python3 -u $SCRIPTS/ensemble.py $ANNOS/ca.$gaz.conll.gz -w 1 -p 4 7 -e 10 -p 13 16 21 24 27 30 33 36    -silent -auto -iterate 2>&1 | egrep '0.*\|.*=';
      python3 -u $SCRIPTS/ensemble.py $ANNOS/cs.$gaz.conll.gz -w 1 -p 4 7 10 -e 13 -p 16 21 24 27 30 33 36    -silent -auto -iterate 2>&1 | egrep '0.*\|.*=';
      python3 -u $SCRIPTS/ensemble.py $ANNOS/de.$gaz.conll.gz -w 1 -p 4 7 10 13 -e 16 -p 21 24 27 30 33 36    -silent -auto -iterate 2>&1 | egrep '0.*\|.*=';
      python3 -u $SCRIPTS/ensemble.py $ANNOS/en.$gaz.conll.gz -w 1 -p 4 7 10 13 16 -e 21 -p 24 27 30 33 36    -silent -auto -iterate 2>&1 | egrep '0.*\|.*=';
      python3 -u $SCRIPTS/ensemble.py $ANNOS/es.$gaz.conll.gz -w 1 -p 4 7 10 13 16 21 -e 24 -p 27 30 33 36    -silent -auto -iterate 2>&1 | egrep '0.*\|.*=';
      python3 -u $SCRIPTS/ensemble.py $ANNOS/fr.$gaz.conll.gz -w 1 -p 4 7 10 13 16 21 24 -e 27 -p 30 33 36    -silent -auto -iterate 2>&1 | egrep '0.*\|.*=';
      python3 -u $SCRIPTS/ensemble.py $ANNOS/it.$gaz.conll.gz -w 1 -p 4 7 10 13 16 21 24 27 -e 30 -p 33 36    -silent -auto -iterate 2>&1 | egrep '0.*\|.*=';
      python3 -u $SCRIPTS/ensemble.py $ANNOS/nl.$gaz.conll.gz -w 1 -p 4 7 10 13 16 21 24 27 30 -e 33 -p 36    -silent -auto -iterate 2>&1 | egrep '0.*\|.*=';
      python3 -u $SCRIPTS/ensemble.py $ANNOS/pt.$gaz.conll.gz -w 1 -p 4 7 10 13 16 21 24 27 30 33    -e 36    -silent -auto -iterate 2>&1 | egrep '0.*\|.*=';
    echo) | tee $MYHOME/ensemble.$gaz.tsv &
  fi
done

# plot distance between languages, direct predictions
echo
echo pair-wise direct projection
for gaz in $gazes; do
  echo -n $gaz;
  for tlang in `cut -f 1 $MYHOME/ensemble.$gaz.tsv | sort -n -u | egrep '^[0-9]*[0-9]$'`; do
    echo -n ' '$tlang;
  done;
  echo;
  for slang in `cut -f 1 $MYHOME/ensemble.$gaz.tsv | sort -n -u | egrep '^[0-9]*[0-9]$'`; do
    echo -n $slang
    for tlang in `cut -f 1 $MYHOME/ensemble.$gaz.tsv | sort -n -u | egrep '^[0-9]*[0-9]$'`; do
      if [ $slang = $tlang ]; then
        echo -n ' _'
      else
        echo -n ' ';
        egrep 'direct' $MYHOME/ensemble.$gaz.tsv | egrep '^'$tlang'\s' | egrep -m 1 '<= \['$slang'\]' | cut -f 15 | perl -pe 's/\s*//g;'
      fi;
    done;
    echo
  done;
  echo
done;
echo
