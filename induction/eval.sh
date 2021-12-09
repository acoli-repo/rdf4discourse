#!/bin/bash
# evaluation experiment

# get it from https://github.com/acoli-repo/acoli-dicts
DICTS=../../../acoli-dicts/trunk/stable/

# for real-world evaluation


	# ../tsv/LDM-v.1.3.tsv \
	
	# ../tsv/LICO-v.1.0.tsv \
	# ../tsv/czedlex0.6.tsv \
	# ../tsv/discodict.tsv \
	# ../tsv/lexconn.tsv \
	# ../tsv/DimLex.tsv \
	# ../tsv/pdtb2.tsv; do
				# ../tsv/LICO-v.1.0.tsv \
	
	# length 1

############
# BASELINE # (DiscMar)
############
# Table 1	
	
	# Apertium, DiscMar, ES -> EN, CA -> EN
	# python3 induce-dimlex.py \
			# --dimlex \
				# ../tsv/discmar.es.tsv \
				# ../tsv/discmar.en.tsv \
			# --dict \
				# $DICTS/apertium/apertium-rdf-2020-03-18/trans_EN-ES.tsv.gz	\
			# --tgt en \
			# --threshold 0.0 \
			# --max_senses 20\
			# --no_out;

	# python3 induce-dimlex.py \
			# --dimlex \
				# ../tsv/discmar.ca.tsv \
				# ../tsv/discmar.en.tsv \
			# --dict \
				# $DICTS/apertium/apertium-rdf-2020-03-18/trans_EN-CA.tsv.gz	\
			# --tgt en \
			# --max_senses 20\
			# --threshold 0.0 \
		# --no_out;

	# # FreeDict, DiscMar, ES -> EN
			
	# python3 induce-dimlex.py \
		# --dimlex \
				# ../tsv/discmar.es.tsv \
				# ../tsv/discmar.en.tsv \
			# --dict \
				# $DICTS/freedict/freedict-rdf-2019-02-05/en-es/*tsv.gz	\
				# $DICTS/freedict/freedict-rdf-2019-02-05/es-en/*tsv.gz	\
			# --tgt en \
			# --max_senses 20\
			# --threshold 0.0 \
		# --no_out;

	# # MUSE, DiscMar
	# python3 induce-dimlex.py \
			# --dimlex \
				# ../tsv/discmar.ca.tsv \
				# ../tsv/discmar.en.tsv \
			# --dict \
				# $DICTS/muse/muse-tsv-2020-06-12/en-ca.tsv	\
				# $DICTS/muse/muse-tsv-2020-06-12/ca-en.tsv	\
			# --tgt en \
			# --max_senses 20\
			# --threshold 0.0 \
		# --no_out;

	# python3 induce-dimlex.py \
			# --dimlex \
				# ../tsv/discmar.es.tsv \
				# ../tsv/discmar.en.tsv \
			# --dict \
				# $DICTS/muse/muse-tsv-2020-06-12/en-es.tsv	\
				# $DICTS/muse/muse-tsv-2020-06-12/es-en.tsv	\
			# --tgt en \
			# --max_senses 20\
			# --threshold 0.0 \
		# --no_out;

	# # all for EN-ES	(DiscMar)
		 # python3 induce-dimlex.py \
			# --dimlex \
				# ../tsv/discmar.es.tsv \
				# ../tsv/discmar.en.tsv \
			# --dict \
				# $DICTS/apertium/apertium-rdf-2020-03-18/trans_EN-ES.tsv.gz	\
				# $DICTS/freedict/freedict-rdf-2019-02-05/en-es/*tsv.gz	\
				# $DICTS/freedict/freedict-rdf-2019-02-05/es-en/*tsv.gz	\
				# $DICTS/muse/muse-tsv-2020-06-12/en-es.tsv	\
				# $DICTS/muse/muse-tsv-2020-06-12/es-en.tsv	\
			# --tgt en \
			# --threshold 0.0 \
			# --max_senses 20\
			# --no_out;

	# # all for CA-EN (DiscMar)
	# python3 induce-dimlex.py \
			# --dimlex \
				# ../tsv/discmar.ca.tsv \
				# ../tsv/discmar.en.tsv \
			# --dict \
				# $DICTS/apertium/apertium-rdf-2020-03-18/trans_EN-CA.tsv.gz	\
				# $DICTS/muse/muse-tsv-2020-06-12/en-ca.tsv	\
				# $DICTS/muse/muse-tsv-2020-06-12/ca-en.tsv	\
			# --tgt en \
			# --max_senses 20\
			# --threshold 0.0 \
		# --no_out;


##################
# Baseline, PDTB #
##################
# Table 2

# for src in pt it nl fr cs de en; do
	# for tgt in de en; do
		# if [ $tgt != $src ]; then
			# echo $src "=>" $tgt
			# # python3 induce-dimlex.py \
				# # --dimlex \
					# # ../tsv/LDM-v.1.3.tsv \
					# # ../tsv/pdtb2.tsv \
					# # ../tsv/LICO-v.1.0.tsv \
					# # ../tsv/czedlex0.6.tsv \
					# # ../tsv/discodict.tsv \
					# # ../tsv/lexconn.tsv \
					# # ../tsv/DimLex.tsv \
					# # --dict \
						# # $DICTS/freedict/freedict-rdf-2019-02-05/$src-$tgt/*tsv.gz	\
						# # $DICTS/freedict/freedict-rdf-2019-02-05/$tgt-$src/*tsv.gz	\
					# # --tgt $tgt \
					# # --max_senses 20\
					# # --threshold 0.0 \
				# # --no_out;
			# # echo
			# # echo

			# python3 induce-dimlex.py \
				# --dimlex \
					# ../tsv/LDM-v.1.3.tsv \
					# ../tsv/pdtb2.tsv \
					# ../tsv/LICO-v.1.0.tsv \
					# ../tsv/czedlex0.6.tsv \
					# ../tsv/discodict.tsv \
					# ../tsv/lexconn.tsv \
					# ../tsv/DimLex.tsv \
					# --dict \
						# $DICTS/muse/muse-tsv-2020-06-12/$src-$tgt*tsv	\
						# $DICTS/muse/muse-tsv-2020-06-12/$tgt-$src*tsv	\
					# --tgt $tgt \
					# --max_senses 20\
					# --threshold 0.0 \
				# --no_out;
			# echo
			# echo

			# python3 induce-dimlex.py \
				# --dimlex \
					# ../tsv/LDM-v.1.3.tsv \
					# ../tsv/pdtb2.tsv \
					# ../tsv/LICO-v.1.0.tsv \
					# ../tsv/czedlex0.6.tsv \
					# ../tsv/discodict.tsv \
					# ../tsv/lexconn.tsv \
					# ../tsv/DimLex.tsv \
					# --dict \
						# $DICTS/freedict/freedict-rdf-2019-02-05/$src-$tgt/*tsv.gz	\
						# $DICTS/freedict/freedict-rdf-2019-02-05/$tgt-$src/*tsv.gz	\
						# $DICTS/muse/muse-tsv-2020-06-12/$src-$tgt*tsv	\
						# $DICTS/muse/muse-tsv-2020-06-12/$tgt-$src*tsv	\
					# --tgt $tgt \
					# --max_senses 20\
					# --threshold 0.0 \
				# --no_out;
			# echo
			# echo


		# fi;
	# done;
# done;

	


#####################
# indirect, DiscMar #
#####################
# Table 3

# # create pruned-dicts directory
# DICTS=pruned-dicts/
	
# for src in es ca; do

	# for tgt in en; do
		# dimlex=`ls ../tsv/discmar*tsv | egrep '\.('$tgt'|'$src')\.'`
	
		# for DICT in $DICTS/*/ $DICTS; do
			# echo $src $tgt $DICT
			# dicts=`find $DICT | egrep tsv.gz | egrep -i '[^a-z]('$tgt'|'$src')[^a-z]' | grep -i -v $tgt'-'$src | grep -i -v $src'-'$tgt`
			# echo $src $tgt $DICT
			
				# python3 induce-dimlex.py \
					# --dimlex $dimlex				\
					# --dict $dicts \
					# --tgt $tgt \
					# --threshold 0.0 \
					# --max_senses 20\
					# --no_out | \
					# perl -pe 's/\./,/g; s/ +/\t/g;'
			# echo
		# done
	# done
# done


######################################
# indirect, DiscMark, with threshold #
######################################
# Table 4

# # create pruned-dicts directory
# DICTS=pruned-dicts/

# for src in es ca; do

	# for tgt in en; do
		# dimlex=`ls ../tsv/discmar*tsv | egrep '\.('$tgt'|'$src')\.'`
	
		# for DICT in $DICTS/*/ $DICTS; do
			# echo $src $tgt $DICT
			# dicts=`find $DICT | egrep tsv.gz | egrep -i '[^a-z]('$tgt'|'$src')[^a-z]' | grep -i -v $tgt'-'$src | grep -i -v $src'-'$tgt`
				# echo $src $tgt $DICT
				
					# python3 induce-dimlex.py \
						# --dimlex $dimlex				\
						# --dict $dicts \
						# --tgt $tgt \
						# --th_steps 20 \
						# --max_senses 50\
						# --silent | \
						# perl -pe 's/\./,/g; s/ +/\t/g;'
				# echo
		# done
	# done
# done

#########################################
# multi-source, DiscMar, with threshold #
#########################################

# create pruned-dicts directory
DICTS=pruned-dicts/

	# for tgt in en; do
		# dimlex=../tsv/discmar*tsv ;	
		# for DICT in $DICTS/*/ $DICTS; do
			# echo $tgt $DICT
			# dicts=`find $DICT | egrep tsv.gz`
				# echo ca es $DICT
				
					# python3 induce-dimlex.py \
						# --dimlex $dimlex				\
						# --dict $dicts \
						# --tgt $tgt \
						# --th_steps 20 \
						# --max_senses 50\
						# --silent | \
						# perl -pe 's/\./,/g; s/ +/\t/g;'
				# echo
		# done
	# done


# from all to DiscMar
	
	# for tgt in en; do
		# dimlex=`ls ../tsv/*tsv | grep -v 'ted' | grep -v 'pdtb' | grep -v arabic | grep -v bangla`; 
		# for DICT in $DICTS/*/ $DICTS; do
			# echo $tgt $DICT
			# dicts=`find $DICT | egrep tsv.gz`
				# echo ca es $DICT
				
					# python3 induce-dimlex.py \
						# --dimlex $dimlex				\
						# --dict $dicts \
						# --tgt $tgt \
						# --th_steps 20 \
						# --max_senses 50\
						# --silent | \
						# perl -pe 's/\./,/g; s/ +/\t/g;'
				# echo
		# done
	# done

# # from all to DiscMar, pruned
	# for tgt in en; do
		# dimlex=`ls ../tsv/*tsv | grep -v 'ted' | grep -v 'pdtb' | grep -v arabic | grep -v bangla`; 
		# for DICT in $DICTS/*/; do
			# echo $tgt discmar $DICT
			# dicts=`find $DICT | egrep tsv.gz`
				
					# python3 induce-dimlex.py \
						# --dimlex $dimlex				\
						# --dict $dicts \
						# --tgt $tgt \
						# --th_steps 20 \
						# --max_senses 50\
						# --test_pivots 10 \
						# --silent | \
						# perl -pe 's/\./,/g; s/ +/\t/g;'
				# echo
		# done
	# done

	

# from all to DiscMar, pruned

	
	# for tgt in en; do
		# dimlex=`ls ../tsv/*tsv | grep -v 'ted' | grep -v 'pdtb' | grep -v arabic | grep -v bangla`; 
		# for DICT in $DICTS/*/ $DICTS; do
			# echo $tgt discmar $DICT
			# dicts=`find $DICT | egrep tsv.gz`
				
					# python3 induce-dimlex.py \
						# --dimlex $dimlex				\
						# --dict $dicts \
						# --tgt $tgt \
						# --th_steps 20 \
						# --max_senses 50\
						# --min_pivots 1\
						# --test_pivlangs 9 \
						# --silent | \
						# perl -pe 's/\./,/g; s/ +/\t/g;'
				# echo
		# done
	# done

	# for tgt in en; do
		# dimlex=`ls ../tsv/*tsv | grep -v 'ted' | grep -v 'pdtb' | grep -v arabic | grep -v bangla`; 
		# for DICT in $DICTS; do	# sub-dicts we had before
			# echo $tgt discmar $DICT
			# dicts=`find $DICT | egrep tsv.gz`
				
					# python3 induce-dimlex.py \
						# --dimlex $dimlex				\
						# --dict $dicts \
						# --tgt $tgt \
						# --th_steps 20 \
						# --max_senses 50\
						# --test_pivots 10 \
						# --silent | \
						# perl -pe 's/\./,/g; s/ +/\t/g;'
				# echo
		# done
	# done
	
	# only for all-dicts

	# for tgt in en; do
		# dimlex=`ls ../tsv/*tsv | grep -v 'ted' | grep -v 'pdtb' | grep -v arabic | grep -v bangla`; 
		# for DICT in $DICTS; do
			# echo $tgt discmar $DICT
			# dicts=`find $DICT | egrep tsv.gz`
				
					# python3 induce-dimlex.py \
						# --dimlex $dimlex				\
						# --dict $dicts \
						# --tgt $tgt \
						# --th_steps 20 \
						# --max_senses 50\
						# --test_pivots 10 \
						# --test_pivlangs 9 \
						# --silent | \
						# perl -pe 's/\./,/g; s/ +/\t/g;'
				# echo
		# done
	# done

###############################################
# all-dict, all to DiscMar.en, with dict size #
###############################################

	# for tgt in en; do
		# dimlex=`ls ../tsv/*tsv | grep -v 'ted' | grep -v 'pdtb' | grep -v arabic | grep -v bangla`; 
		# for DICT in $DICTS; do
			# echo $tgt discmar $DICT
			# dicts=`find $DICT | egrep tsv.gz`
				
					# python3 induce-dimlex.py \
						# --dimlex $dimlex				\
						# --dict $dicts \
						# --tgt $tgt \
						# --th_steps 20 \
						# --max_senses 50\
						# --test_pivlangs 9 \
						# --dict_size 100000 70000 50000 30000 10000 7000 5000       \
						# --silent | \
						# perl -pe 's/\./,/g; s/ +/\t/g;'
				# echo
		# done
	# done

# ############################################
# # all-dict, to German and PDTB2, piv_langs #
# ############################################
	
	# all-dict
	
	# for tgt in en de; do
		# dimlex=`ls ../tsv/*tsv | grep -v 'ted' | grep -v 'discmar' | grep -v arabic | grep -v bangla`; 
		# for DICT in $DICTS; do
			# echo $tgt $DICT
			# dicts=`find $DICT | egrep tsv.gz`
				
					# python3 induce-dimlex.py \
						# --dimlex $dimlex				\
						# --dict $dicts \
						# --tgt $tgt \
						# --th_steps 20 \
						# --max_senses 500\
						# --test_pivlangs 9 \
						# --silent | \
						# perl -pe 's/\./,/g; s/ +/\t/g;'
				# echo
		# done
	# done

	# indiv dicts 
	
	# for tgt in en de; do
		# dimlex=`ls ../tsv/*tsv | grep -v 'ted' | grep -v 'discmar' | grep -v arabic | grep -v bangla`; 
		# for DICT in $DICTS/*/; do
			# echo $tgt $DICT
			# dicts=`find $DICT | egrep tsv.gz`
				
					# python3 induce-dimlex.py \
						# --dimlex $dimlex				\
						# --dict $dicts \
						# --tgt $tgt \
						# --th_steps 20 \
						# --max_senses 500\
						# --test_pivlangs 9 \
						# --silent | \
						# perl -pe 's/\./,/g; s/ +/\t/g;'
				# echo
		# done
	# done

	# for tgt in de en; do
		# dimlex=`ls ../tsv/*tsv | grep -v 'ted' | grep -v 'discmar' | grep -v arabic | grep -v bangla`; 
		# for DICT in $DICTS ; do
			# echo $tgt $DICT filter senses
			# dicts=`find $DICT | egrep tsv.gz`
				
					# python3 induce-dimlex.py \
						# --dimlex $dimlex				\
						# --dict $dicts \
						# --tgt $tgt \
						# --th_steps 20 \
						# --test_pivlangs 9 \
						# --silent | \
						# perl -pe 's/\./,/g; s/ +/\t/g;'
				# echo
		# done
	# done

	# for tgt in de en; do
		# dimlex=`ls ../tsv/*tsv | grep -v 'ted' | grep -v 'discmar' | grep -v arabic | grep -v bangla`; 
		# for DICT in $DICTS ; do
			# echo $tgt $DICT prune senses
			# dicts=`find $DICT | egrep tsv.gz`
				
					# python3 induce-dimlex.py \
						# --dimlex $dimlex				\
						# --dict $dicts \
						# --tgt $tgt \
						# --th_steps 20 \
						# --max_senses 500\
						# --test_pivlangs 9 \
						# --prune_senses \
						# --silent | \
						# perl -pe 's/\./,/g; s/ +/\t/g;'
				# echo
		# done
	# done
	
	# for tgt in de en; do
		# dimlex=`ls ../tsv/*tsv | grep -v 'ted' | grep -v 'discmar' | grep -v arabic | grep -v bangla`; 
		# for DICT in $DICTS ; do
			# echo $tgt $DICT prune senses, fix senses
			# dicts=`find $DICT | egrep tsv.gz`
				
					# python3 induce-dimlex.py \
						# --dimlex $dimlex				\
						# --dict $dicts \
						# --tgt $tgt \
						# --th_steps 20 \
						# --test_pivlangs 9 \
						# --prune_senses \
						# --silent | \
						# perl -pe 's/\./,/g; s/ +/\t/g;'
				# echo
		# done
	# done


	# # test max_sense prediction
	# for tgt in en; do
		# dimlex=`ls ../tsv/*tsv | grep -v 'ted' | grep -v 'discmar' | grep -v arabic | grep -v bangla`; 
		# for DICT in $DICTS; do
			# echo $tgt $DICT explore max_senses, th=0, non-pruning
			# dicts=`find $DICT | egrep tsv.gz`
				
					# python3 induce-dimlex.py \
						# --dimlex $dimlex				\
						# --dict $dicts \
						# --tgt $tgt \
						# --threshold 0 \
						# --test_pivlangs 6 \
						# --silent | \
						# perl -pe 's/\./,/g; s/ +/\t/g;'
				# echo


			# echo $tgt $DICT explore max_senses, th=0, pruning
			# dicts=`find $DICT | egrep tsv.gz`
				
					# python3 induce-dimlex.py \
						# --dimlex $dimlex				\
						# --dict $dicts \
						# --tgt $tgt \
						# --threshold 0 \
						# --test_pivlangs 6 \
						# --prune_senses \
						# --silent | \
						# perl -pe 's/\./,/g; s/ +/\t/g;'
				# echo
			# done
	# done

	
	
# # other langs (todo)	
	# for tgt in de cs fr pt it nl; do
		# dimlex=`ls ../tsv/*tsv | grep -v 'ted' | grep -v 'discmar' | grep -v arabic | grep -v bangla`; 
		# for DICT in $DICTS; do
			# echo $tgt $DICT
			# dicts=`find $DICT | egrep tsv.gz`
				
					# python3 induce-dimlex.py \
						# --dimlex $dimlex				\
						# --dict $dicts \
						# --tgt $tgt \
						# --th_steps 20 \
						# --max_senses 500\
						# --test_pivlangs 9 \
						# --silent | \
						# perl -pe 's/\./,/g; s/ +/\t/g;'
				# echo
		# done
	# done

###########################
# multi-target projection #
###########################

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
