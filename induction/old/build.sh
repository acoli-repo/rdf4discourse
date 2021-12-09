#!/bin/bash
# create TSV files from DimLex-lemon dictionaries for sense induction experiments using general lexical data

# (c) 2020-03-23 Christian Chiarcos, christian.chiarcos@web.de
# Apache License 2.0, see https://www.apache.org/licenses/LICENSE-2.0

##########
# CONFIG #
##########

# set carefully to languages with reasonable dimlex coverage
langs="it fr pt nl en cs de ca es"

# set to your own TIAD TSV dicts
# here: selected dictionaries from https://github.com/acoli-repo/acoli-dicts/tree/master/stable
dicts="";
for lang1 in $langs; do
	for lang2 in $langs; do
		dicts=$dicts" "`ls ../../../acoli-dicts/trunk/stable/apertium/apertium-rdf-2020-03-18/*tsv.gz ../../../acoli-dicts/trunk/stable/freedict/*/*/*tsv.gz | \
		egrep -i '[^a-zA-Z0-9]'$lang1'[^a-zA-Z0-9\/][^a-zA-Z0-9\/]*'$lang2'([^a-zA-Z0-9\/][^\/]*)?\.tsv(\.[^\/]*)?$'
		`;
	done;
done;
	
# word nets im OMW TSV format (we require language tags!), see wn/build.sh to produce these files
WNs=wn/*tsv
	
# SPARQL 1.1 engine, replace by your own
# Apache Jena's arq can be obtained from https://jena.apache.org/download/
ARQ=arq;
# development system:
# Jena:       VERSION: 3.9.0
# Jena:       BUILD_DATE: 2018-09-28T17:15:32+0000
# ARQ:        VERSION: 3.9.0
# ARQ:        BUILD_DATE: 2018-09-28T17:15:32+0000
# RIOT:       VERSION: 3.9.0
# RIOT:       BUILD_DATE: 2018-09-28T17:15:32+0000

# discourse marker lexicons in OntoLex-lemon (same repo, hence local paths); we require ttl input
# note that we rely on the language codes at writtenRep objects to determine the language
# we expect a single language per dimlex
dimlexes=../tsv/*tsv

########################################################################
# (1) mkdir TIAD TSV files from wordnet, dimlex and other dictionaries #
########################################################################

mkdir tsv >&/dev/null;
for lang in $langs; do
	for depth in 1 2 3; do
		tgt=tsv/$lang-dimlex-$depth.tsv;
		if [ -e $tgt ]; then
			echo found $tgt, skipping 1>&2;
		else
			echo build $tgt 1>&2;
			mydicts=`ls $dicts | egrep -i '[^a-zA-Z0-9]'$lang'([^a-zA-Z0-9\/][^\/]*)?\.tsv(\.[^\/]*)?$'`;
			echo java CompileConcepts $lang $depth -dimlex $dimlexes -dict $mydicts -wn $WNs 1>&2;
			java -Dfile.encoding=UTF-8 CompileConcepts $lang $depth -dimlex $dimlexes > `echo $tgt | sed s/'\.tsv$'//`-dimlex.tsv;
			java -Dfile.encoding=UTF-8 CompileConcepts $lang $depth -dimlex $dimlexes -wn $WNs > `echo $tgt | sed s/'\.tsv$'//`-nodict.tsv;
			java -Dfile.encoding=UTF-8 CompileConcepts $lang $depth -dimlex $dimlexes -dict $mydicts -wn $WNs > $tgt;
			echo 1>&2;
		fi;
	done;
done;

############################
# (2) first gen projection #
############################

if [ -e ConstrainedTranslationProjector.class ]; then
	if [ ConstrainedTranslationProjector.class -nt ConstrainedTranslationProjector.java ]; then
		rm ConstrainedTranslationProjector.class
	fi;
fi;

if [ ! -e ConstrainedTranslationProjector.class ]; then
	javac ConstrainedTranslationProjector.java;
fi;

if [ -e ConstrainedTranslationProjector.class ]; then
	cat java ConstrainedTranslationProjector
fi;