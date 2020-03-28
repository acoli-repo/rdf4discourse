#!/bin/bash
# create lemon discourse marker dictionary from discmar tsv

# system settings		UPDATE!
##################

CONLL_RDF=~/conll-rdf
# set to your local CoNLL-RDF installation

# converter settings	DO NOT CHANGE!
#####################

SRC=../../src/discmar
TSV=$SRC/discmar.tsv
DESC=$SRC/description.html

# conversion			DO NOT CHANGE!
#############

for lang in en es ca; do

	ABox=`echo $TSV | sed -e s/'.*\/'//g -e s/'\.tsv$'//g`.$lang.ttl

	echo -n build $ABox .. 1>&2

	if [ -e $ABox ]; then
		echo . found $ABox, reusing it 1>&2
	else
		if ls $CONLL_RDF/run.sh | egrep '.' >&/dev/null; then # found
			egrep '^[0-9][0-9]*\s'$lang'\s' $TSV | \
			$CONLL_RDF/run.sh CoNLLStreamExtractor \
				https://cs.famaf.unc.edu.ar/~laura/shallowdisc4summ/discmar/ \
				ID LANG WORD ENGLISH STRUCT SEM POS COMMENT EXAMPLE \
				-u tsv2lemon.sparql > $ABox
		else
			echo . 1>&2;
			echo did not find CoNLL-RDF, get it from https://github.com/acoli-repo/conll-rdf and configure the local "$"CONLL_RDF variable 1>&2;
		fi;
		if [ -e $ABox ]; then echo . ok 1>&2; else echo ... failed 1>&2; fi;
	fi;

done;