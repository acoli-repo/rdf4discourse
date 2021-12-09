#!/bin/bash

# dicts

# freedict
FD=../../../acoli-dicts/trunk/stable/freedict/freedict-rdf-2019-02-05/

# dimlexes, tsv
DL=../tsv/

# diven a string and one or multiple files
# return those that contain string surrounded by [^a-zA-Z0-9]
function filter {
	pattern=$1
	shift
	echo $* | sed s/' '/'\n'/g | egrep '^(.*[^a-zA-Z0-9])?'$pattern'([^a-zA-Z0-9].*)?$'
}

# return (first) language of dimlex
function lang {
	head $1 | egrep -v '#' | head -n 1 | cut -f 2
}

dimlexes=`ls $DL/*tsv`

for tgt in $dimlexes; do

	tgtlang=`lang $tgt`
	if echo $tgtlang | egrep "[a-z]" >& /dev/null; then

		for dimlex in `ls $DL/*tsv | grep -v $tgt`; do

			echo '##########################'
			echo '# '$dimlex' => DimLex.tsv'
			echo '##########################'

			lang=`lang $dimlex`
			
			if [ $lang != $tgtlang ]; then
			
				dicts=`filter $lang $(filter $tgtlang $FD/*/*.tsv.gz)`
				
				# single_language -> de direct
				python3 dimlex2tgt.py --symm \
					--dimlex $dimlex \
					--gold $DL/DimLex.tsv \
					--dicts $dicts

				echo;

				for dimlex2 in $dimlexes; do
					if [[ $dimlex < $dimlex2 ]]; then

						langs=`for dl in $dimlex $dimlex2; do lang $dl; done`
						
						if [ `echo $langs | sed s/' '/'\n'/g | sort -u | wc -l` = 2 ]; then

							dicts=`for lang in $langs; do filter $lang $FD/*de*/*.tsv.gz; done`
							
							echo '##########################'
							echo '# '$dimlex'+'$dimlex2' => DimLex.tsv'
							echo '##########################'
							
							# single_language -> de direct
							echo python3 dimlex2tgt.py --symm \
								--dimlex $dimlex \
								--gold $DL/DimLex.tsv \
								--dicts $dicts

							echo;
						fi
					fi
				fi
			done
		done;
		
	fi;

done

	# for i in dimlex in $dimlexes; do
		# for dimlex2 in $dimlexes; do
			# if 
		

		# echo '##########################'
		# echo '# '$dimlex' => DimLex.tsv'
		# echo '##########################'

		# lang=`lang $dimlex`
		# dicts=`filter $lang $FD/*de*/*.tsv.gz`
		
		# # single_language -> de direct
		# python3 dimlex2tgt.py --symm \
			# --dimlex $dimlex \
			# --gold $DL/DimLex.tsv \
			# --dicts $dicts

		# echo;
	# done;



		
	# for dimlex in `ls $DL/*tsv | grep -v DimLex`; do
		# for dimlex2 in `ls $DL/*tsv | grep -v DimLex | grep -v $dimlex`; do

			# echo '####################################'
			# echo '# '$dimlex'+'$dimlex2' => DimLex.tsv'
			# echo '####################################'

			# # single_language -> de direct
			# python3 dimlex2tgt.py --symm \
				# --dimlex $dimlex $dimlex2 \
				# --gold $DL/DimLex.tsv \
				# --dicts $FD/*de*/*.tsv.gz

			# echo;
		# done
	# done
		
	# for dimlex in `ls $DL/*tsv | grep -v DimLex`; do
		# for dimlex2 in `ls $DL/*tsv | grep -v DimLex | grep -v $dimlex`; do
			# for dimlex3 in `ls $DL/*tsv | grep -v DimLex | grep -v $dimlex | grep -v $dimlex2`; do

				# echo '###############################################'
				# echo '# '$dimlex'+'$dimlex2'+'$dimlex3' => DimLex.tsv'
				# echo '###############################################'

				# # single_language -> de direct
				# python3 dimlex2tgt.py --symm \
					# --dimlex $dimlex $dimlex2 $dimlex3 \
					# --gold $DL/DimLex.tsv \
					# --dicts $FD/*de*/*.tsv.gz

				# echo;
			# done
		# done
	# done

	# for dimlex in `ls $DL/*tsv | grep -v DimLex`; do
		# for dimlex2 in `ls $DL/*tsv | grep -v DimLex | grep -v $dimlex`; do
			# for dimlex3 in `ls $DL/*tsv | grep -v DimLex | grep -v $dimlex | grep -v $dimlex2`; do
				# for dimlex4 in `ls $DL/*tsv | grep -v DimLex | grep -v $dimlex | grep -v $dimlex2 | grep -v $dimlex3`; do

					# echo '##########################################################'
					# echo '# '$dimlex'+'$dimlex2'+'$dimlex3'+'$dimlex4' => DimLex.tsv'
					# echo '##########################################################'

					# # single_language -> de direct
					# python3 dimlex2tgt.py --symm \
						# --dimlex $dimlex $dimlex2 $dimlex3 $dimlex4 \
						# --gold $DL/DimLex.tsv \
						# --dicts $FD/*de*/*.tsv.gz

					# echo;
				# done;
			# done
		# done
	# done


	# echo '###################'
	# echo '# all => DimLex.tsv'
	# echo '###################'

	# # all -> de, direct path
	# python3 dimlex2tgt.py --symm --mwe \
		# --dimlex `ls $DL/*tsv | grep -v DimLex` \
		# --gold $DL/DimLex.tsv \
		# --dicts $FD/*de*/*.tsv.gz 

	# echo

	# echo '##########################'
	# echo '# it -> X -> => DimLex.tsv'
	# echo '##########################'

	# # it -> X -> de 
	# python3 dimlex2tgt.py --symm \
		# --lang it \
		# --dimlex $DL/LICO-v.1.0.tsv \
		# --gold $DL/DimLex.tsv \
		# --dicts $FD/de-en/*.tsv.gz \
				# $FD/de-fr/*.tsv.gz \
				# $FD/de-nl/*.tsv.gz \
				# $FD/de-pl/*.tsv.gz \
				# $FD/de-sv/*.tsv.gz \
				# $FD/en-it/*.tsv.gz \
				# $FD/fr-it/*.tsv.gz \
				# $FD/nl-it/*.tsv.gz \
				# $FD/pl-it/*.tsv.gz \
				# $FD/sv-it/*.tsv.gz

	# python3 dimlex2tgt.py --symm \
		# --dimlex $DL/LICO-v.1.0.tsv \
		# --gold $DL/DimLex.tsv $DL/lexconn.tsv \
		# --dicts $FD/de-it/*.tsv.gz \
				# $FD/de-it/*.tsv.gz \
				# $FD/fr-it/*.tsv.gz 
		
	# # it -> all, direct path
	# python3 dimlex2tgt.py --symm --mwe \
		# --dimlex $DL/LICO-v.1.0.tsv \
		# --gold $DL/*tsv \
		# --dicts $FD/*it*/*.tsv.gz 

	# # all -> de, direct path
	# python3 dimlex2tgt.py --symm --mwe \
		# --dimlex `ls $DL/*tsv | grep -v DimLex` \
		# --gold $DL/DimLex.tsv \
		# --dicts $FD/*de*/*.tsv.gz 
		
	# # it -> X -> de 
	# python3 dimlex2tgt.py --symm \
		# --dimlex $DL/LICO-v.1.0.tsv \
		# --gold $DL/DimLex.tsv \
		# --dicts $FD/de-en/*.tsv.gz \
				# $FD/de-fr/*.tsv.gz \
				# $FD/de-nl/*.tsv.gz \
				# $FD/de-pl/*.tsv.gz \
				# $FD/de-sv/*.tsv.gz \
				# $FD/en-it/*.tsv.gz \
				# $FD/fr-it/*.tsv.gz \
				# $FD/nl-it/*.tsv.gz \
				# $FD/pl-it/*.tsv.gz \
				# $FD/sv-it/*.tsv.gz

	# # de -> it direct
	# python3 dimlex2tgt.py --symm \
		# --lang it \
		# --gold $DL/LICO-v.1.0.tsv \
		# --dimlex $DL/DimLex.tsv \
		# --dicts $FD/de-it/*.tsv.gz 


	# # fr -> de direct
	# python3 dimlex2tgt.py --symm \
		# --lang de \
		# --dimlex $DL/lexconn.tsv \
		# --gold $DL/DimLex.tsv \
		# --dicts $FD/fr-de/*.tsv.gz \
				# $FD/de-fr/*.tsv.gz 
				
	# # en -> de direct
	# python3 dimlex2tgt.py --symm \
		# --lang de \
		# --dimlex $DL/pdtb2.tsv \
		# --gold $DL/DimLex.tsv \
		# --dicts $FD/en-de/*.tsv.gz \
				# $FD/de-en/*.tsv.gz 
				
	# # pt -> de direct
	# python3 dimlex2tgt.py --symm \
		# --lang de \
		# --dimlex $DL/pdtb2.tsv \
		# --gold $DL/DimLex.tsv \
		# --dicts $FD/en-de/*.tsv.gz \
				# $FD/de-en/*.tsv.gz 
				

				
	# # python3 dimlex2tgt.py --symm \
		# # --lang es \
		# # --rel 2 \
		# # --gold ../tsv/discmar.es.tsv	\
		# # --dimlex $DL/DimLex.tsv \
		# # --dicts $FD/de-es/*.tsv.gz
