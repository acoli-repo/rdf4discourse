all: retrieve.py data gazeteers
	@(langs="en de"; \
	for lang in $$langs; do \
		if [ ! -e data/$$lang.conll ]; then \
			echo data/$$lang.conll 1>&2; \
			python3 retrieve.py $$lang -f text -no_comments > data/$$lang.txt 2>/dev/null; \
			python3 retrieve.py $$lang -f conll -no_comments > data/$$lang.conll 2>/dev/null; \
		fi; \
	done; \
	for src in data/*txt; do \
		for tgt in data/*txt; do \
			l1=`basename $$src | sed s/'\.[^\.\/]*$$'//`; \
			l2=`basename $$tgt | sed s/'\.[^\.\/]*$$'//`; \
			if [ $$l1 != $$l2 ]; then \
				mrg=data/$$l1-$$l2.conll;\
				if [ ! -s $$mrg ]; then \
					echo $$mrg 1>&2; \
					(python3 align.py $$src $$tgt -low -tok -silent > $$mrg) 2>&1 | sed s/'^'/'  '/g 1>&2; \
				fi; \
			fi; \
		done; \
	done; \
	)


	# python3 similarity_align.py 20  data/$$lang.orig.conll=1 data/$$lang.norm.conll=1 | cut -f 1,2,4 > data/$$lang.conll; \
	# if [ -s data/$$lang.conll ]; then \
	# 	rm data/$$lang.*.conll;\
	# fi;\
	# egrep '^[0-9]' data/$$lang.conll | wc -l | sed s/'$$'/' tokens'/; \

olia:
	@echo 'Shall I clone OLiA [Y/n]?' 1>&2
	@(read x; if echo $$x | grep -i "n" ; then echo Please create the olia/ directory by hand, e.g., as a symlink to your OLiA repo 1>&2; exit 1 ;fi 1>/dev/null)
	git clone https://github.com/acoli-repo/olia

gazetteers: olia
	@# these gazeteers are automatically derived from ../../linked, but we filter out some low-coverage ones
	mkdir gazetteers
	(for ttl in ../../linked/*/*.ttl; do \
		if echo -n $$ttl | grep -v ted-mdb ; then \
			lang=`basename $$(dirname $$ttl)`;\
			if [ ! -e gazetteers/$$lang ]; then mkdir gazetteers/$$lang; fi;\
			tgt=gazetteers/$$lang/`basename $$ttl | sed s/'.ttl'//`.tsv; \
			if [ ! -s $$tgt ]; then \
				echo ' >' $$tgt;\
				arq --data $$ttl --namedgraph olia/owl/experimental/discourse/discourse.PDTB.owl --namedgraph olia/owl/experimental/discourse/discourse.PDTB-link.rdf --namedGraph olia/owl/experimental/discourse/olia_discourse.owl --namedGraph olia/owl/experimental/discourse/discourse.RST-link.rdf --namedGraph olia/owl/experimental/discourse/discourse.PDTB-CCR-link.rdf --namedGraph olia/owl/experimental/discourse/discourse.CCR.owl --query olia2gazetteer.sparql --results=TSV > $$tgt; \
			fi;\
		fi;\
	done;)

data:
	mkdir data

clear:
	rm retrieve.py
	rm -rf data

test: all
	@echo test retrieval 1>&2
	@( echo deu-CH | python3 retrieve.py 1>/dev/null ) 2>&1 | sed s/'^'/'  '/ 1>&2
	@echo 1>&2
	@echo 1>&2

	@echo test alignment 1>&2
	@python3 similarity_align.py 50



retrieve.py:
	@echo retrieve.py 1>&2
	@wget https://raw.githubusercontent.com/acoli-repo/acoli-corpora/master/biblical/api/retrieve.py 2>&1 | sed s/'^'/'  '/ 1>&2
