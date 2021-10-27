all:	ensemble eval

ensemble: data gazetteers
	@echo 'builds data/ and ensemble/, for eval/, call "make eval", for building all from scratch rather than archived versions, call "make clear" beforehand' 1>&2
	@(\
		langs="en de ar bn ca cs es fr it nl pt"; \
	  gazcols="5 6 8 9 10 11 12"; \
		# # debug config\
		# langs="en de";\
		# gazcols="5";\
		\
		all_langs_in () { \
			#echo $$0 $$1 1>&2;\
				for lang in $$langs; do \
					if [ ! -e $$1/$$lang.conll ]; then	\
						return 1; \
					fi;\
				done;\
				return 0;\
			};\
	\
	echo create initial conll files;\
	for doc in data/*/; do \
		# for doc in data/1/ data/2/; do \
		for lang in $$langs; do \
			if [ -e $$doc/$$lang.conll ]; then \
				for g in gazetteers/$$lang/*tsv; do \
					tgt=$$doc/$$lang.`basename $$g | sed s/'\.[^\.]*$$'//`.conll;\
					if [ -s $$tgt ]; then \
						echo keeping existing $$tgt 1>&2; \
					else \
						echo $$tgt 1>&2; \
						python3 gazetteer.py $$doc/$$lang.conll $$g > $$tgt; \
					fi;\
				done; # $$g \
			fi;\
		done; 		# $$lang \
		echo; \
		\
		# annotate every language for all gazeteers, split for layers 1>&2; \
		for col in $$gazcols; do \
			for lang in $$langs; do \
				src=$$doc/$$lang.conll;\
				tgt=$$doc/$$lang.conll.gaz.$$col; \
				if [ -e $$src ]; then \
					if [ -s $$tgt ]; then \
						echo keeping $$tgt 1>&2;\
					else \
						tmp=$$tgt.tmp;\
						(echo '# cols: ID WORD'; echo; cat $$doc/$$lang.conll) > $$tgt; \
						for gaz in $$doc/$$lang.*.conll; do \
							echo $$tgt': adding '$$gaz 1>&2; \
							cp $$tgt $$tmp; \
							gaz=`basename $$gaz | sed s/'^[^\.]*\.\(.*\)\.conll$$'/'\1'/`;\
							cut -f 2,$$col $$doc/$$lang.$$gaz.conll | \
							python3 similarity_align.py 25 $$tmp=1 - | \
							# drop misalignments\
							grep -v '^?' | \
							# restore incorrectly aligned sentence breaks\
							sed s/'^\s\s*\?.*'//g | \
							sed -e s/'^\(#[^\?]*\)[\? \t]*$$'/'\1'/g -e s/'^# cols: .*'/'& '$$lang.$$gaz/ > $$tgt; \
							cols=`egrep -m 1 '^1' $$tgt | perl -pe 's/\t/\n/g;' | wc -l`; \
							drop_col=`echo $$cols -1 | bc`;\
							cut --complement -f $$drop_col $$tgt > $$tmp; \
							mv $$tmp $$tgt; \
						done; #$$gaz \
					fi;\
				fi;\
			done; 			# $$lang \
			echo ; \
		done; 				# $$col \
		\
		echo alignments 1>&2;\
		if [ ! -e ensemble ]; then \
			mkdir ensemble; \
		fi;\
		if all_langs_in $$doc; then \
			for col in $$gazcols; do \
				for lang in $$langs; do \
					ensemble=ensemble/`basename $$doc`;\
					if [ ! -e $$ensemble ]; then \
						mkdir $$ensemble; \
						ls -l $$ensemble;\
					fi; \
						tgt=$$ensemble/$$lang.$$col.conll; \
						if [ -s $$tgt ]; then \
							echo $$tgt found 1>&2; \
						else \
							cp $$doc/$$lang.conll $$tgt; \
							for gaz in $$doc/*.gaz.$$col; do \
								tmp=$$tgt.tmp; \
								#echo python3 align_conll.py $$tgt=1 $$gaz=1 -low -noids -silent -nopunct;\
								echo $$tgt": adding "$$gaz 1>&2; \
								python3 align_conll.py $$tgt=1 $$gaz=1 -low -noids -silent -nopunct | \
								egrep -v '^[\?\*_]' > $$tmp; \
								mv $$tmp $$tgt; \
								# cp $$tgt $$tgt.`ls $$tgt* | wc -l`;\
								# debugging: \
								# cp $$tgt $$tgt.`ls $$tgt* | wc -l`;\
								# head -n 30 $$tgt;\
								echo; \
							done; # $$gaz \
						fi;\
				done;					# $$lang \
			done;						# $$col	\
		fi;\
	done;										# $$doc\
	for lang in $$langs; do \
		for gaz in $$gazcols; do \
			tgt=ensemble/$$lang.$$gaz.conll;\
			if [ -s $$tgt ]; then \
			echo $$tgt found 1>&2; \
			else \
				echo $$tgt 1>&2;\
				for doc in ensemble/*/; do \
					cat $$doc/$$lang.$$gaz.conll; \
					echo ;\
				done > $$tgt; # $$doc \
			fi; \
	done;							# $$gaz \
	done;								# $$lang \
	\
	gzip ensemble/*.conll; \
	echo done 1>&2; \
	)

data:	ted2020.tsv.gz
	@if [ ! -e data ]; then \
		mkdir data; \
		python3 split_ted.py ted2020.tsv.gz data/;\
	fi;

olia:
		@echo 'Shall I clone OLiA [Y/n]?' 1>&2
		@(read x; if echo $$x | grep -i "n" ; then echo Please create the olia/ directory by hand, e.g., as a symlink to your OLiA repo 1>&2; exit 1 ;fi 1>/dev/null)
		git clone https://github.com/acoli-repo/olia

ted2020.tsv.gz:
	if [ ! -e data ]; then \
		wget -nc https://public.ukp.informatik.tu-darmstadt.de/reimers/sentence-transformers/datasets/ted2020.tsv.gz; \
	fi;

gazetteers: olia
			@# these gazeteers are automatically derived from ../../linked, but we filter out some low-coverage ones
			@echo 'Shall I bootstrap Gazetteers from OLiA [Y/n]?' 1>&2
			@(read x; if echo $$x | grep -i "n" ; then echo Please create the gazetters/ directory by hand, e.g., as a symlink to another local folder, say ../biblical/gazetteers 1>&2; exit 1 ;fi 1>/dev/null)
			mkdir gazetteers
			(for ttl in ../../linked/*/*.ttl; do \
				if echo -n $$ttl | grep -v ted-mdb ; then \
					lang=`basename $$(dirname $$ttl)`;\
					if [ ! -e gazetteers/$$lang ]; then mkdir gazetteers/$$lang; fi;\
					tgt=gazetteers/$$lang/`basename $$ttl | sed s/'.ttl'//`.tsv; \
					if [ ! -s $$tgt ]; then \
						echo ' >' $$tgt;\
						arq --data $$ttl --namedgraph olia/owl/experimental/discourse/discourse.PDTB.owl --namedgraph olia/owl/experimental/discourse/discourse.PDTB-link.rdf --namedGraph olia/owl/experimental/discourse/olia_discourse.owl --namedGraph olia/owl/experimental/discourse/discourse.RST-link.rdf --namedGraph olia/owl/experimental/discourse/discourse.PDTB-CCR-link.rdf --namedGraph olia/owl/experimental/discourse/discourse.CCR.owl --query ../bibles/olia2gazetteer.sparql --results=TSV > $$tgt; \
					fi;\
				fi;\
			done;)

clear:
	rm -rf data eval/ted-mdb

eval/ted-mdb:
	@# note that we include a static conversion of the corpus in CoNLL format, call make clear to rebuild
	@(svn checkout https://github.com/MurathanKurfali/Ted-MDB-Annotations.git/trunk/English eval/ted-mdb/en;\
		svn checkout https://github.com/MurathanKurfali/Ted-MDB-Annotations.git/trunk/Portuguese eval/ted-mdb/pt;\
		svn checkout https://github.com/MurathanKurfali/Ted-MDB-Annotations.git/trunk/German eval/ted-mdb/de;\
		svn checkout https://github.com/MurathanKurfali/Ted-MDB-Annotations.git/trunk/Polish eval/ted-mdb/pl;\
		svn checkout https://github.com/MurathanKurfali/Ted-MDB-Annotations.git/trunk/Russian eval/ted-mdb/ru;\
		svn checkout https://github.com/MurathanKurfali/Ted-MDB-Annotations.git/trunk/Turkish eval/ted-mdb/tr;\
		svn checkout https://github.com/MurathanKurfali/Ted-MDB-Annotations.git/trunk/Lithuanian eval/ted-mdb/lt;\
		\
		dirs=eval/ted-mdb/*/;\
		\
		mkdir eval/ted-mdb/conll;\
		wget https://raw.githubusercontent.com/MurathanKurfali/Ted-MDB-Annotations/master/README.md -O eval/ted-mdb/README.md;\
		\
		for dir in $$dirs; do \
			lang=`basename $$dir`; \
			echo $$lang $$dir $$dirs;\
			talkids=`ls $$dir/raw/*/talk*txt | sed -e s/'.*\/'//g -e s/'[^0-9]'//g | egrep '[0-9]' | sort -u`; \
			for talk in $$talkids; do \
				raw=$$dir/raw/01/talk_$${talk}_$$lang.txt;\
				ann=$$dir/ann/01/talk_$${talk}_$$lang.txt;\
				if [ ! -e $$raw ]; then	\
					for r in $$dir/raw/*/talk_$${talk}_$$lang*.txt; do \
						cp $$r $$raw;\
					done; # raw\
					for a in $$dir/ann/*/talk_$${talk}_$$lang*.txt; do \
						cat $$a >> $$ann;\
					done; # ann \
				fi;\
				if [ ! -e eval/ted-mdb/conll/$$talk ]; then \
					mkdir -p eval/ted-mdb/conll/$$talk;\
				fi; \
				python3 pdtb2conll.py $$raw $$ann > eval/ted-mdb/conll/$$talk/$$lang.conll; \
				done; # talk\
			done; # dir\
		)

eval/ted-mdb/data: data eval/ted-mdb
	@(\
	langs="en ru tr lt pl de pt ar bn ca cs es fr it nl"; \
	if [ ! -e eval/ted-mdb/data ] ; then mkdir eval/ted-mdb/data; fi;\
	for talk in eval/ted-mdb/conll/*/; do \
		talkid=`basename $$talk`; \
		mkdir eval/ted-mdb/data/$$talkid;\
		for lang in $$langs; do \
			if [ -e data/$$talkid/$$lang.conll ]; then \
				cp data/$$talkid/$$lang.conll eval/ted-mdb/data/$$talkid/$$lang.conll;\
			else \
				egrep '#.*sent_id' data/$$talkid/en.conll | \
				sed s/'$$'/'\n1\t?\n\n'/g > eval/ted-mdb/data/$$talkid/$$lang.conll;\
			fi;\
		done;\
	done;\
	)

eval/ted-mdb/mapping.sed: eval/ted-mdb/mapping.tsv
	#cat eval/ted-mdb/mapping.tsv | perl -pe 's/([^\t\n]+)\t([^\t\n]+)/s\/$1\/($$1=>$$2)\//g;' > eval/ted-mdb/mapping.sed	# DEBUG
	cat eval/ted-mdb/mapping.tsv | perl -pe 's/([^\t\n]+)\t([^\t\n]+)/s\/$$1\/$$2\//g;' > eval/ted-mdb/mapping.sed

eval/ted-mdb/ensemble: eval/ted-mdb eval/ted-mdb/data gazetteers eval/ted-mdb/mapping.sed
		tlangs="en ru tr lt pl de pt";\
		slangs="en de ar bn ca cs es fr it nl pt"; \
		langs=`echo $$tlangs $$slangs | sed s/'\s'/'\n'/g | sort -u`; \
	  gazcols="5"; \
		# # debug config\
		# langs="en de";\
		# gazcols="5";\
		\
	echo create initial conll files;\
	for doc in eval/ted-mdb/data/*/; do \
		# for doc in data/1/ data/2/; do \
		for lang in $$slangs; do \
			if [ -e $$doc/$$lang.conll ]; then \
				for g in gazetteers/$$lang/*tsv; do \
					tgt=$$doc/$$lang.`basename $$g | sed s/'\.[^\.]*$$'//`.conll;\
					if [ -s $$tgt ]; then \
						echo keeping existing $$tgt 1>&2; \
					else \
						echo $$tgt 1>&2; \
						python3 gazetteer.py $$doc/$$lang.conll $$g > $$tgt; \
					fi;\
				done; # $$g \
			fi;\
		done; 		# $$lang \
		echo; \
		\
		# annotate every language for all gazeteers, split for layers 1>&2; \
		for col in $$gazcols; do \
			for lang in $$slangs; do \
				src=$$doc/$$lang.conll;\
				tgt=$$doc/$$lang.conll.gaz.$$col; \
				if [ -e $$src ]; then \
					if [ -s $$tgt ]; then \
						echo keeping $$tgt 1>&2;\
					else \
						tmp=$$tgt.tmp;\
						(echo '# cols: ID WORD'; echo; cat $$doc/$$lang.conll) > $$tgt; \
						for gaz in $$doc/$$lang.*.conll; do \
							echo $$tgt': adding '$$gaz 1>&2; \
							cp $$tgt $$tmp; \
							gaz=`basename $$gaz | sed s/'^[^\.]*\.\(.*\)\.conll$$'/'\1'/`;\
							cut -f 2,$$col $$doc/$$lang.$$gaz.conll | \
							python3 similarity_align.py 25 $$tmp=1 - | \
							# drop misalignments\
							grep -v '^?' | \
							# restore incorrectly aligned sentence breaks\
							sed s/'^\s\s*\?.*'//g | \
							sed -e s/'^\(#[^\?]*\)[\? \t]*$$'/'\1'/g -e s/'^# cols: .*'/'& '$$lang.$$gaz/ > $$tgt; \
							cols=`egrep -m 1 '^1' $$tgt | perl -pe 's/\t/\n/g;' | wc -l`; \
							drop_col=`echo $$cols -1 | bc`;\
							cut --complement -f $$drop_col $$tgt > $$tmp; \
							mv $$tmp $$tgt; \
						done; #$$gaz \
					fi;\
				fi;\
			done; 			# $$lang \
			echo ; \
		done; 				# $$col \
		\
		echo alignments 1>&2;\
		if [ ! -e eval/ted-mdb/ensemble ]; then \
			mkdir eval/ted-mdb/ensemble; \
		fi;\
			for col in $$gazcols; do \
				for lang in $$tlangs; do \
					if [ -e data/`basename $$doc`/$$lang.conll ]; then \
						ensemble=eval/ted-mdb/ensemble/`basename $$doc`;\
						if [ ! -e $$ensemble ]; then \
							mkdir $$ensemble; \
							ls -l $$ensemble;\
						fi; \
							tgt=$$ensemble/$$lang.$$col.conll; \
							if [ -s $$tgt ]; then \
								echo $$tgt found 1>&2; \
							else \
								python3 similarity_align.py 20 $$doc/$$lang.conll=1 eval/ted-mdb/conll/`basename $$doc`/$$lang.conll=0 | \
								#tee $tgt.1 | \
								perl -pe 's/^\t[^\n]//g; s/^(#[^\t\n]*=[ \t]*[^\t \n]+)\t[^\n]*/$$1/g; s/^# sent_id/\n# sent_id/g;'  | grep -a -v '^[^0-9#]' | \
								iconv -f utf-8 -t utf-8 -c > $$tgt; \
								for gaz in $$doc/*.gaz.$$col; do \
									#cp $$tgt $$tgt.`ls $$tgt* | wc -l`; \
									tmp=$$tgt.tmp; \
									#echo python3 align_conll.py $$tgt=1 $$gaz=1 -low -noids -silent -nopunct;\
									echo $$tgt": adding "$$gaz 1>&2; \
									python3 align_conll.py $$tgt=1 $$gaz=1 -low -noids -silent -nopunct | \
									egrep -v '^[\?\*_]' > $$tmp; \
									mv $$tmp $$tgt; \
									# cp $$tgt $$tgt.`ls $$tgt* | wc -l`;\
									# debugging: \
									# cp $$tgt $$tgt.`ls $$tgt* | wc -l`;\
									# head -n 30 $$tgt;\
									echo; \
								done; # $$gaz \
							fi;\
						fi;\
				done;					# $$lang \
			done;						# $$col	\
	done;										# $$doc\
	for lang in $$tlangs; do \
		for gaz in $$gazcols; do \
			tgt=eval/ted-mdb/ensemble/$$lang.$$gaz.conll;\
			if [ -s $$tgt ]; then \
			echo $$tgt found 1>&2; \
			else \
				echo $$tgt 1>&2;\
				for doc in eval/ted-mdb/ensemble/*/; do \
					if [ -e $$doc/$$lang.$$gaz.conll ]; then \
						cat $$doc/$$lang.$$gaz.conll; \
						echo ;\
					fi;\
				done | \
				sed -f eval/ted-mdb/mapping.sed > $$tgt; # $$doc \
			fi; \
	done;							# $$gaz \
	done;								# $$lang \

eval: eval/ted-mdb eval/ted-mdb/ensemble
