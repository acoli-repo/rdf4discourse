all: retrieve.py data
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
