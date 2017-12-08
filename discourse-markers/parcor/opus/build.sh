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

############################################
# merge German-English and English-Italian #
############################################
if [ ! -e $CORPUS.en-de-it.conll ]; then
	if [ ! -e $CORPUS.en-de.conll ]; then
		if [ ! -e $CORPUS.de-en.conll ]; then
			bash -e $HOME/opus2conll.sh $CORPUS de en | tee $CORPUS.de-en.conll
		else 
			cat $CORPUS.de-en.conll;
		fi | \
		$HOME/run.sh CoNLLSentenceReorder 2 0 | 												# restore English word order
		$HOME/run.sh CoNLLStreamExtractor http://example.org/irrelevant DE_ID DE EN_ID EN | 	# reorder columns
		$HOME/run.sh CoNLLRDFFormatter -conll EN_ID EN DE_ID DE > $CORPUS.en-de.conll;
	fi;

	if [ ! -e $CORPUS.en-it.conll ]; then
		bash -e $HOME/opus2conll.sh $CORPUS en it  > $CORPUS.en-it.conll
	fi;

	$HOME/run.sh org.acoli.conll.merge.CoNLLStreamMerger $CORPUS.en-de.conll $CORPUS.en-it.conll 1 1 -drop none -window=1000 | \
	# see eval/eval-CoNLLStreamMerger-window-2017-11-16.txt for motivating -window=1000, larger windows yield better results with lower runtime 
	\
	tee $CORPUS.en-de-it.conll;

	else cat $CORPUS.en-de-it.conll;
fi | \
# note that we write either the conversion results or the merged file into stdout
\
################################
# dimlex annotation for German #
################################
# input columns: EN_ID EN_WORD DE_ID DE_WORD EN_ID2 EN_WORD2 IT_ID IT_WORD
\
if [ ! -e $DIMLEX ]; then							# annotate German discourse markers
	echo skipping $DIMLEX annotation, not found 1>&2;
	cat;
else 
	$HOME/run.sh CoNLLSentenceReorder 2	|		# reorder for German to match multi-word expressions
	bash -e $HOME/dimlexCoNLL.sh $DIMLEX EN_ID EN_WORD DE_ID WORD EN_ID2 EN_WORD2 IT_ID IT_WORD;
fi | \
\
########################################
# dimlex (LiCo) annotation for Italian #
########################################
# input columns: EN_ID EN_WORD DE_ID DE_WORD EN_ID2 EN_WORD2 IT_ID IT_WORD DE_FORM DE_SENSE
if [ ! -e $LICO ]; then								# annotate Italian discourse markers
	echo skipping $LICO annotation, not found 1>&2;
	cat;
else
$HOME/run.sh CoNLLSentenceReorder 6 | 					# reorder for Italian to match multi-word expressions
	bash -e $HOME/dimlexCoNLL.sh $LICO EN_ID EN_WORD DE_ID DE_WORD EN_ID2 EN_WORD2 IT_ID WORD DE_FORM DE_SENSE
fi | \
\
##############################
# restore English word order #
##############################
# input columns: EN_ID EN_WORD DE_ID DE_WORD EN_ID2 EN_WORD2 IT_ID IT_WORD DE_FORM DE_SENSE IT_FORM IT_SENSE
$HOME/run.sh CoNLLSentenceReorder 0 4 2 6 | \
tee $CORPUS.en-de-it.dimlexed.conll | \
\
#######################################
# disambiguate projections to English #
#######################################
## todo: better support for English MWEs, we annotate the first word per alignment group, only
# note that BELOW, ID is renamed as KEY, because conll:KEY (in the sparql updates) could also be applied to a conll:WORD
$HOME/run.sh CoNLLStreamExtractor http://example.org/irrelevant/ \
		KEY WORD DE_ID DE_WORD KEY__2 WORD__2 IT_ID__2 IT_WORD__2 DE_FORM DE_SENSE__1 IT_FORM__2 IT_SENSE__2 \
		-u 	sparql/drop-unspec-nonWORD-nonKEY.sparql \
			sparql/split-invalid-alignments.sparql \
			sparql/drop-retoks.sparql{20} \
			sparql/merge-starred-lines.sparql{10} | \
$HOME/run.sh CoNLLRDFFormatter -conll KEY WORD DE_WORD DE_FORM DE_SENSE__1 IT_WORD__2 IT_FORM__2 IT_SENSE__2 | \
	sed s/'^#.*'// | 				# strip comments (= old headers), the following is also to generate the correct column labels
$HOME/run.sh CoNLLStreamExtractor http://example.org/irrelevant/ \
		ID WORD DE DE_CUE SENSE1 IT IT_CUE SENSE2 \
		-u sparql/category-disambiguation.sparql \
	| \
$HOME/run.sh CoNLLRDFFormatter -conll ID WORD SENSE DE DE_CUE SENSE1 IT IT_CUE SENSE2