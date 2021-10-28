#!/bin/bash
# iterate evaluation script over corpus

MYHOME=`dirname $0`
SCRIPTS=$MYHOME/../../../bibles/
ANNOS=$MYHOME/ensemble

# different configurations for individual languages, note that we evaluate against PDTB
  if [ ! -e $MYHOME/ensemble.tsv ]; then
    (echo baseline: predict from target language gazeteer, direct prediction only
    python3 -u $SCRIPTS/ensemble.py $ANNOS/en.5.conll -w 1 -e 3 -p 20 -silent -iterate 2>&1 | egrep '0.*\|.*=' | sed s/'$'/'\ten<en'/g;
    python3 -u $SCRIPTS/ensemble.py $ANNOS/en.5.conll -w 1 -e 3 -p 21 -silent -iterate  2>&1 | egrep '0.*\|.*=' | sed s/'$'/'\ten<en'/g;
    python3 -u $SCRIPTS/ensemble.py $ANNOS/en.5.conll -w 1 -e 3 -p 22 -silent -iterate  2>&1 | egrep '0.*\|.*=' | sed s/'$'/'\ten<en'/g;
    python3 -u $SCRIPTS/ensemble.py $ANNOS/de.5.conll -w 1 -e 3 -p 17 -silent -iterate  2>&1 | egrep '0.*\|.*=' | sed s/'$'/'\tde<de'/g;
    python3 -u $SCRIPTS/ensemble.py $ANNOS/pt.5.conll -w 1 -e 3 -p 38 -silent -iterate  2>&1 | egrep '0.*\|.*=' | sed s/'$'/'\tpt<pt'/g;
    echo;
    echo ensemble: predict from full ensemble, direct prediction only
    python3 -u $SCRIPTS/ensemble.py $ANNOS/de.5.conll -w 1 -e 3 -p 5 8 11 14 22 25 29 32 35 38 -silent -auto -iterate 2>&1 | egrep '0.*\|.*=' | sed s/'$'/'\tde'/g;
    python3 -u $SCRIPTS/ensemble.py $ANNOS/en.5.conll -w 1 -e 3 -p 5 8 11 14 17 25 29 32 35 38 -silent -auto -iterate 2>&1 | egrep '0.*\|.*=' | sed s/'$'/'\ten'/g;
    python3 -u $SCRIPTS/ensemble.py $ANNOS/pt.5.conll -w 1 -e 3 -p 5 8 11 14 17 22 25 29 32 35 -silent -auto -iterate 2>&1 | egrep '0.*\|.*=' | sed s/'$'/'\tpt'/g;
    for lang in lt pl ru tr; do
      python3 -u $SCRIPTS/ensemble.py $ANNOS/$lang.5.conll -w 1 -e 3 -p 5 8 11 14 17 22 25 29 32 35 38 -silent -auto -iterate 2>&1 | egrep '0.*\|.*=' | sed s/'$'/'\t'$lang/g;
    done;
    echo
    echo ensemble, weighted
    python3 -u $SCRIPTS/ensemble.py $ANNOS/de.5.conll -w 1 -e 3 -p 5 8 11 14 22 25 29 32 35 38 -silent -auto -iterate -weighted 2>&1 | egrep '0.*\|.*='| sed s/'$'/'\tde'/g;
    python3 -u $SCRIPTS/ensemble.py $ANNOS/en.5.conll -w 1 -e 3 -p 5 8 11 14 17 25 29 32 35 38 -silent -auto -iterate -weighted  2>&1 | egrep '0.*\|.*='| sed s/'$'/'\ten'/g;
    python3 -u $SCRIPTS/ensemble.py $ANNOS/pt.5.conll -w 1 -e 3 -p 5 8 11 14 17 22 25 29 32 35 -silent -auto -iterate -weighted  2>&1 | egrep '0.*\|.*='| sed s/'$'/'\tpt'/g;
    for lang in lt pl ru tr; do
      python3 -u $SCRIPTS/ensemble.py $ANNOS/$lang.5.conll -w 1 -e 3 -p 5 8 11 14 17 22 25 29 32 35 38 -silent -auto -iterate -weighted  2>&1 | egrep '0.*\|.*='| sed s/'$'/'\t'$lang/g;
    done;
    echo) | tee $MYHOME/ensemble.tsv
fi;
