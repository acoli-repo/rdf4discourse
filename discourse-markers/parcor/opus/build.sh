#!/bin/bash
# German, Italian and English Europarl v.7 sections from OPUS
# annotates against DimLex and LiCo
# note that we cannot disseminate them as the original Europarl license has not been clarified

# user configuration
CORPUS=Europarl

HOME=.
if echo $0 | egrep '\/' >&/dev/null; then HOME=`echo $0 | sed s/'\/[^\/]*$'//`; fi;

DICTS=$HOME/../../lemon;
DIMLEX=$DICTS/dimlex/DimLex.ttl;
LICO=`echo $DICTS/lico/LICO*.ttl | sed s/' '/'\n'/g |egrep -m 1 .`;

##################
# German-Italian #
##################
if [ -e $CORPUS.de-it.conll ] ; then				# read or generate CoNLL
	cat $CORPUS.de-it.conll;
else 
	bash -e $HOME/opus2conll.sh $CORPUS de it | \
	tee $CORPUS.de-it.conll;
fi | \
\
if [ ! -e $DIMLEX ]; then							# annotate German discourse markers
	echo skipping $DIMLEX annotation, not found 1>&2;
	cat;
else 
	bash -e $HOME/dimlexCoNLL.sh $DIMLEX DE_ID WORD IT_ID IT;
fi | \
\
java CoNLLSentenceReorder 2 0 | 					# restore Italian word order to match multi-word expressions
if [ ! -e $LICO ]; then								# annotate Italian discourse markers
	echo skipping $LICO annotation, not found 1>&2;
	cat;
else
	bash -e $HOME/dimlexCoNLL.sh $LICO DE_ID DE IT_ID WORD DE_CONN DE_SENSE;
fi | \
\
java CoNLLSentenceReorder 0 2;						# restore German word order for readability