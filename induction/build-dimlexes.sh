#!/bin/bash
# evaluation experiment

# get it from https://github.com/acoli-repo/acoli-dicts
DICTS=pruned-dicts/apertium

SOURCES="en de cs fr pt it nl"
TARGETS=ca #"af an bg bn ca da el eo es eu fi ga gl he hr is ja kha kk ku la mk no oc pl ro ru sc sh sl sv tr uk zh"
dimlex=`ls tsv/*/*tsv | grep -v 'ted' | grep -v arabic | grep -v bangla | grep -v discmar`;
dicts=`find $DICTS | egrep tsv.gz | grep -i ca | grep -i en`

	echo project, incl. English, English PDTB, no DiscMar PDTB2/3 4 senses
	python3 induce-dimlex.py \
						--dimlex $dimlex				\
						--dict $dicts \
						--tgt $TARGETS \
						--threshold 0.45 \
						--max_senses 4 \
						--write_output \
						#--min_pivlangs 1 #5 
						# | \
						# perl -pe 's/\./,/g; s/ +/\t/g;'
				echo
