#!/bin/bash
# iterate evaluation script over corpus

MYHOME=`dirname $0`
SCRIPTS=$MYHOME/../../../bibles/
ANNOS=$MYHOME/ensemble

langs=`ls $ANNOS | grep 'conll' | sed -e s/'.*\/'//g -e s/'\..*'// | sort -u`

# we evaluate against PDTB, so we have hierarchical structures, we split the original annotations in 3 layers
for lang in $langs; do
  src=$ANNOS/$lang.5.conll
  if [ -e $src ]; then
    cat $src | tee $ANNOS/$lang.5.3.conll | \
    perl -pe 's/([^\|\t\n]*\.)?([^\|\t\.\n]+\.[^\|\t\.]+)/$2/g' | tee $ANNOS/$lang.5.2.conll | \
    perl -pe 's/([\t\|\n])([^\|\t\n]+\.)/$1/g' > $ANNOS/$lang.5.1.conll
  fi;
done;

# different configurations for individual languages, note that we evaluate against PDTB
for depth in 1 2 3; do
  if [ ! -e $MYHOME/ensemble.depth-$depth.tsv ]; then
    (echo baseline: predict from target language gazeteer, direct prediction only
    python3 -u $SCRIPTS/ensemble.py $ANNOS/en.5.$depth.conll -w 1 -e 3 -p 21 -silent -iterate 2>&1 | egrep '0.*\|.*=' | sed s/'$'/'\ten<en'/g;
    python3 -u $SCRIPTS/ensemble.py $ANNOS/en.5.$depth.conll -w 1 -e 3 -p 22 -silent -iterate  2>&1 | egrep '0.*\|.*=' | sed s/'$'/'\ten<en'/g;
    python3 -u $SCRIPTS/ensemble.py $ANNOS/en.5.$depth.conll -w 1 -e 3 -p 23 -silent -iterate  2>&1 | egrep '0.*\|.*=' | sed s/'$'/'\ten<en'/g;
    python3 -u $SCRIPTS/ensemble.py $ANNOS/de.5.$depth.conll -w 1 -e 3 -p 17 -silent -iterate  2>&1 | egrep '0.*\|.*=' | sed s/'$'/'\tde<de'/g;
    python3 -u $SCRIPTS/ensemble.py $ANNOS/pt.5.$depth.conll -w 1 -e 3 -p 38 -silent -iterate  2>&1 | egrep '0.*\|.*=' | sed s/'$'/'\tpt<pt'/g;
    echo;
    echo ensemble: predict from full ensemble, direct prediction only
    python3 -u $SCRIPTS/ensemble.py $ANNOS/de.5.$depth.conll -w 1 -e 3 -p 5 8 11 14 23 26 29 32 35 38 -silent -auto -iterate 2>&1 | egrep '0.*\|.*=' | sed s/'$'/'\tde'/g;
    python3 -u $SCRIPTS/ensemble.py $ANNOS/en.5.$depth.conll -w 1 -e 3 -p 5 8 11 14 17 26 29 32 35 38 -silent -auto -iterate 2>&1 | egrep '0.*\|.*=' | sed s/'$'/'\ten'/g;
    python3 -u $SCRIPTS/ensemble.py $ANNOS/pt.5.$depth.conll -w 1 -e 3 -p 5 8 11 14 17 23 26 29 32 35 -silent -auto -iterate 2>&1 | egrep '0.*\|.*=' | sed s/'$'/'\tpt'/g;
    for lang in lt pl ru tr; do
      python3 -u $SCRIPTS/ensemble.py $ANNOS/$lang.5.$depth.conll -w 1 -e 3 -p 5 8 11 14 17 23 26 29 32 35 38 -silent -auto -iterate 2>&1 | egrep '0.*\|.*=' | sed s/'$'/'\t'$lang/g;
    done;
    echo
    echo ensemble, weighted
    python3 -u $SCRIPTS/ensemble.py $ANNOS/de.5.$depth.conll -w 1 -e 3 -p 5 8 11 14 23 26 29 32 35 38 -silent -auto -iterate -weighted 2>&1 | egrep '0.*\|.*='| sed s/'$'/'\tde'/g;
    python3 -u $SCRIPTS/ensemble.py $ANNOS/en.5.$depth.conll -w 1 -e 3 -p 5 8 11 14 17 26 29 32 35 38 -silent -auto -iterate -weighted  2>&1 | egrep '0.*\|.*='| sed s/'$'/'\ten'/g;
    python3 -u $SCRIPTS/ensemble.py $ANNOS/pt.5.$depth.conll -w 1 -e 3 -p 5 8 11 14 17 23 26 29 32 35 -silent -auto -iterate -weighted  2>&1 | egrep '0.*\|.*='| sed s/'$'/'\tpt'/g;
    for lang in lt pl ru tr; do
      python3 -u $SCRIPTS/ensemble.py $ANNOS/$lang.5.$depth.conll -w 1 -e 3 -p 5 8 11 14 17 23 26 29 32 35 38 -silent -auto -iterate -weighted  2>&1 | egrep '0.*\|.*='| sed s/'$'/'\t'$lang/g;
    done;
    echo) | tee $MYHOME/ensemble.depth-$depth.tsv
  fi &
done;
