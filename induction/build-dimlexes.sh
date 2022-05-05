#!/bin/bash
# evaluation experiment

# get it from https://github.com/acoli-repo/acoli-dicts
DICTS=pruned-dicts/

SOURCES="en de cs fr pt it nl ca es"
TARGETS="af an bg bn da el eo eu fi ga gl he hr is ja kha kk ku la mk no oc pl ro ru sc sh sl sv tr uk zh"
dimlex=`ls tsv/*/*tsv | grep -v 'ted' | grep -v arabic | grep -v bangla` # | grep -v discmar`;
dicts=`find $DICTS | egrep tsv.gz` # | grep -i ca | grep -i en`

if [ ! -d stubs ]; then mkdir stubs; fi

	for min_l in 5 4 3 2 1; do

		echo project PDTB with min pivot languages $min_l, incl. English and DiscMar
		python3 induce-dimlex.py \
							--cols WORD LANG PDTB_INVERSE RST _ CCR_BASIC_OP CCR_ORDER CCR_POLARITY CCR_SOURCE CCR_TEMPORALITY \
							--dimlex $dimlex				\
							--dict $dicts \
							--tgt $TARGETS \
							--threshold 0.45 \
							--max_senses 4 \
							--write_output \
							--min_pivlangs $min_l > stubs/pdtb.$min_l.tsv

		echo project RST with min pivot languages $min_l, incl. English and DiscMar
		python3 induce-dimlex.py \
							--cols WORD LANG _ RST _ CCR_BASIC_OP CCR_ORDER CCR_POLARITY CCR_SOURCE CCR_TEMPORALITY \
							--dimlex $dimlex				\
							--dict $dicts \
							--tgt $TARGETS \
							--threshold 0.45 \
							--max_senses 4 \
							--write_output \
							--min_pivlangs $min_l > stubs/rst.$min_l.tsv

		echo project CCR with min pivot languages $min_l, incl. English and DiscMar
		python3 induce-dimlex.py \
							--cols WORD LANG _ _ _ CCR_BASIC_OP CCR_ORDER CCR_POLARITY CCR_SOURCE CCR_TEMPORALITY \
							--dimlex $dimlex				\
							--dict $dicts \
							--tgt $TARGETS \
							--threshold 0.45 \
							--max_senses 4 \
							--write_output \
							--min_pivlangs $min_l > stubs/ccr.$min_l.tsv
	done;