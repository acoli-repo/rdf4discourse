all: data gazetteers
	@(\
		langs="en de ar bn ca cs es fr it nl pt"; \
	  gazcols="5 6 8 9 10 11 12"; \
		# debug config\
		langs="en de";\
		gazcols="5";\
		\
		all_langs_in () { \
			echo $$0 $$1 1>&2;\
				for lang in $$langs; do \
					if [ ! -e $$1/$$lang.conll ]; then	\
						return 1; \
					fi;\
				done;\
				return 0;\
			};\
	\
	echo create initial conll files;\
	# for doc in data/*/; do \
	for doc in data/1/; do \
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
				done;\
			fi;\
		done; \
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
						done;\
					fi;\
				fi;\
			done;\
			echo ; \
			\
			if all_langs_in $$doc; then \
				echo alignments 1>&2;\
				ensemble=ensemble/`basename $$doc`;\
				if [ ! -e $$ensemble ]; then \
					mkdir -p $$ensemble; \
					ls -l $$ensemble;\
				fi; \
				for lang in $$langs; do \
					tgt=$$ensemble/$$lang.$$col.conll; \
					if [ -s $$tgt ]; then \
						echo $$tgt found 1>&2; \
					else \
						cp $$doc/$$lang.conll $$tgt; \
						for gaz in $$doc/*.gaz.$$col; do \
							tmp=$$tgt.tmp; \
							echo $$tgt": adding "$$gaz 1>&2; \
							python3 align_conll.py $$tgt=1 $$gaz=1 -low -noids -silent -nopunct | \
							egrep -v '^[\?\*_]' > $$tmp; \
							mv $$tmp $$tgt; \
							# cp $$tgt $$tgt.`ls $$tgt* | wc -l`;\
							# debugging: \
							# cp $$tgt $$tgt.`ls $$tgt* | wc -l`;\
							# head -n 30 $$tgt;\
							echo; \
						done; \
					fi;\
				done;\
			fi;\
		done;\
	done;\
	echo ; \
	)

data:	ted2020.tsv.gz
	@if [ ! -e data ]; then mkdir data; fi
	python3 split_ted.py ted2020.tsv.gz data/

olia:
		@echo 'Shall I clone OLiA [Y/n]?' 1>&2
		@(read x; if echo $$x | grep -i "n" ; then echo Please create the olia/ directory by hand, e.g., as a symlink to your OLiA repo 1>&2; exit 1 ;fi 1>/dev/null)
		git clone https://github.com/acoli-repo/olia

ted2020.tsv.gz:
	wget -nc https://public.ukp.informatik.tu-darmstadt.de/reimers/sentence-transformers/datasets/ted2020.tsv.gz

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
