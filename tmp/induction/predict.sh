#!/bin/bash
# production mode

# get it from https://github.com/acoli-repo/acoli-dicts
DICTS=../../../acoli-dicts/trunk/stable/

# reduce min_pivot from optimum to lower values
# if min_pivot==1, generate both with and without English

# run for levels 0, 1 and 2/3 separately, then merge

# after generation

# no English, incl. DiscMar, all dicts
	# for tgt in de cs fr pt it nl ca es; do
		# dimlex=`ls ../tsv/*tsv | grep -v 'ted' | grep -v arabic | grep -v bangla | grep -v discmar.en | grep -v pdtb`; 
		# for DICT in $DICTS; do
			# echo $tgt $DICT, no English, PDTB0 1 sense
			# dicts=`find $DICT | egrep tsv.gz`
				
					# python3 induce-dimlex.py \
						# --dimlex $dimlex				\
						# --dict $dicts \
						# --tgt $tgt \
						# --th_steps 20 \
						# --max_senses 1\
						# --test_pivlangs 7 \
						# --silent | \
						# perl -pe 's/\./,/g; s/ +/\t/g;'
				# echo
		# done
	# done

# #	for tgt in de cs fr pt it nl ca es; do
		# dimlex=`ls ../tsv/*tsv | grep -v 'ted' | grep -v arabic | grep -v bangla | grep -v discmar.en | grep -v pdtb`; 
		# for DICT in $DICTS; do
			# echo $tgt $DICT, no English, PDTB1 2 senses
			# dicts=`find $DICT | egrep tsv.gz`
				
					# #--tgt de cs fr pt it nl ca es
					# python3 induce-dimlex.py \
						# --dimlex $dimlex				\
						# --dict $dicts \
						# --tgt ca es \
						# --th_steps 20 \
						# --max_senses 2\
						# --test_pivlangs 7 \
						# --silent | \
						# perl -pe 's/\./,/g; s/ +/\t/g;'
				# echo
		# done
# #	done

DICTS=pruned-dicts/
#	for tgt in de cs fr pt it nl ; do
		dimlex=`ls ../tsv/*tsv | grep -v 'ted' | grep -v arabic | grep -v bangla | grep -v discmar | grep -v pdtb`; 
		for DICT in $DICTS; do
			echo $tgt $DICT, no English, no DiscMar PDTB2/3 4 sense 
			dicts=`find $DICT | egrep tsv.gz`
				
					python3 induce-dimlex.py \
						--dimlex $dimlex				\
						--dict $dicts \
						--tgt de cs fr pt it nl \
						--th_steps 20 \
						--max_senses 4\
						--test_pivlangs 5 \
						--silent | \
						perl -pe 's/\./,/g; s/ +/\t/g;'
				echo
		done
#	done


# w. English

# #	for tgt in en de cs fr pt it nl ca es; do
		# dimlex=`ls ../tsv/*tsv | grep -v 'ted' | grep -v arabic | grep -v bangla | grep -v discmar.en `; 
		# for DICT in $DICTS; do
			# echo $tgt $DICT, incl. English PDTB, PDTB0 1 sense
			# dicts=`find $DICT | egrep tsv.gz`
				
					# python3 induce-dimlex.py \
						# --dimlex $dimlex				\
						# --dict $dicts \
						# --tgt en de cs fr pt it nl ca es \
						# --th_steps 20 \
						# --max_senses 1\
						# --test_pivlangs 8 \
						# --silent | \
						# perl -pe 's/\./,/g; s/ +/\t/g;'
				# echo
		# done
# #	done

# #	for tgt in en de cs fr pt it nl ca es; do
		# dimlex=`ls ../tsv/*tsv | grep -v 'ted' | grep -v arabic | grep -v bangla | grep -v discmar.en `; 
		# for DICT in $DICTS; do
			# echo $tgt $DICT, incl. English PDTB, PDTB1 2 senses 
			# dicts=`find $DICT | egrep tsv.gz`
				
					# python3 induce-dimlex.py \
						# --dimlex $dimlex				\
						# --dict $dicts \
						# --tgt en de cs fr pt it nl ca es \
						# --th_steps 20 \
						# --max_senses 2\
						# --test_pivlangs 8 \
						# --silent | \
						# perl -pe 's/\./,/g; s/ +/\t/g;'
				# echo
		# done
# #	done

#	for tgt in en de cs fr pt it nl ; do
		dimlex=`ls ../tsv/*tsv | grep -v 'ted' | grep -v arabic | grep -v bangla | grep -v discmar`; 
		for DICT in $DICTS; do
			echo $tgt $DICT, incl. English PDTB, no DiscMar PDTB2/3 4 senses
			dicts=`find $DICT | egrep tsv.gz`
				
					python3 induce-dimlex.py \
						--dimlex $dimlex				\
						--dict $dicts \
						--tgt en de cs fr pt it nl \
						--th_steps 20 \
						--max_senses 4\
						--test_pivlangs 6 \
						--silent | \
						perl -pe 's/\./,/g; s/ +/\t/g;'
				echo
		done
#	done
