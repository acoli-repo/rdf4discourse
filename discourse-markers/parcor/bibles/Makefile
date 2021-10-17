all: retrieve.py data
	@(for lang in en de; do \
		if [ ! -e data/$$lang.conll ]; then \
			echo -n data/$$lang.conll': ' 1>&2; \
			python3 retrieve.py $$lang -f conll -no_comments > data/$$lang.orig.conll 2>/dev/null; \
			python3 retrieve.py $$lang -f conll -no_comments -lower -no_punct > data/$$lang.norm.conll 2>/dev/null; \
			python3 similarity_align.py 20  data/$$lang.orig.conll=1 data/$$lang.norm.conll=1 | cut -f 1,2,4 > data/$$lang.conll; \
			if [ -s data/$$lang.conll ]; then \
				rm data/$$lang.*.conll;\
			fi;\
			egrep '^[0-9]' data/$$lang.conll | wc -l | sed s/'$$'/' tokens'/; \
		fi; \
	done)

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
