#!/bin/bash
# runs dimlex induction with default parameters

# get it from https://github.com/acoli-repo/acoli-dicts
DICTS=../../../acoli-dicts/trunk/stable/

python3 induce-dimlex.py \
	--dimlex \
		../tsv/discmar.*.tsv \
	--dict \
		$DICTS/apertium/apertium-rdf-2020-03-18/trans_EN-CA.tsv.gz	\
		$DICTS/apertium/apertium-rdf-2020-03-18/trans_EN-ES.tsv.gz	\
		$DICTS/apertium/apertium-rdf-2020-03-18/trans_ES-CA.tsv.gz	\
	--tgt en \
	--silent \
	--max_senses 20 \
	--th_steps 20 \
	--test_pivlangs 2 \
#	--dict_size 100000
#	--prune_senses
#	--test_pivots 5 \
#	--threshold 0.0 \


# python3 induce-dimlex.py \
	# --dimlex \
		# ../tsv/discmar.*.tsv \
	# --dict \
		# $DICTS/apertium/apertium-rdf-2020-03-18/trans_EN-CA.tsv.gz	\
		# $DICTS/apertium/apertium-rdf-2020-03-18/trans_EN-ES.tsv.gz	\
		# $DICTS/apertium/apertium-rdf-2020-03-18/trans_ES-CA.tsv.gz	\
	# --tgt en \
	# --silent \
	# --max_senses 20 \
	# --th_steps 20 \
	# --test_pivlangs 2 \
# #	--test_pivots 5 \
# #	--threshold 0.0 \

#		../tsv/pdtb2.tsv \

# python3 induce-dimlex.py \
	# --dimlex \
		# ../tsv/discmar.*.tsv \
	# --dict \
		# $DICTS/apertium/apertium-rdf-2020-03-18/trans_EN-CA.tsv.gz	\
		# $DICTS/apertium/apertium-rdf-2020-03-18/trans_EN-ES.tsv.gz	\
		# $DICTS/apertium/apertium-rdf-2020-03-18/trans_ES-CA.tsv.gz	\
	# --tgt en

# python3 induce-dimlex.py \
	# --dimlex \
		# ../tsv/discmar.*.tsv \
	# --dict \
		# $DICTS/apertium/apertium-rdf-2020-03-18/trans_*.tsv.gz	\
	# --tgt en


	
# NB: low precision indicates lack of coverage in the target vocabulary, to be manually evaluated