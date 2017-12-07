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
		$HOME/run.sh CoNLLStreamExtractor ttp://example.org/irrelevant DE_ID DE EN_ID EN | 	# reorder columns
		$HOME/run.sh CoNLLRDFFormatter -conll EN_ID EN DE_ID DE > $CORPUS.en-de.conll;
	fi;

	if [ ! -e $CORPUS.en-it.conll ]; then
		bash -e $HOME/opus2conll.sh $CORPUS en it  > $CORPUS.en-it.conll
	fi;

	$HOME/run.sh org.acoli.conll.merge.CoNLLStreamMerger $CORPUS.en-de.conll $CORPUS.en-it.conll 1 1 -drop none -window=15000 | \
	tee $CORPUS.en-de-it.conll;
	#
	# tested window sizes: 
	# window	time	lines
	#	100	34,982s	346914
	#	300	18,598s	376618
	#	350	20,389s	524243
	#	375	28,423s	
	#	400	23,188s	663300
	#	450	17,931s	438928
	#	500	15,867s	407171
	#	750	17,072s	370364
	#	1000	19,935s	383882
	#	2000	22,853s	351464
	#	5000	35,370s	360878
	#	7500	42,754s	541638
	#	9000	1m25,621s	943816
	#	9500	52,418s	679902
	#	10000	36,984s	328985
	#	10000	36,213s	328985
	#	10000	33,976s	351460
	#	10000	36,753s	328985
	#	10000	38,847s	328985
	#	10000	35,290s	328985
	#	12500	1m4,133s	554001
	#	14000	39,215s	358210
	#	15000	41,848s	346895
	#	15000	10,334s	50830
	#	15000	53,000s	414108
	#	15000	1m5,684s	519974
	#	15000	48,249s	380471	#
	#	15500	40,650s	336540
	#	15750	41,450s	364880
	#	15750	56,457s	564886
	#	16000	49,789s	501511
	#	16250	40,616s	412593
	#	16500	56,828s	417671
	#	16500	49,224s	398689
	#	16500	45,609s	324240
	#	16500	53,980s	417671
	#	17000	37,995s	370893
	#	17250	1m10,938s	562875
	#	17250	44,502s	358289
	#	17250	43,359s	358289
	#	17500	34,699s	322445
	#	17750	56,629s	572847
	#	18000	34,697s	270298
	#	20000	46,842s	330866
	#	50000	3m36,343s	579127
	#	75000	1m50,317s	173480

	# iterations	sec	lines	lines without break comments	lines/sec
	# 100	35	346914	343445	9813
	# 300	19	376618	375363	19756
	# 350	20	524243	522745	26137
	# 375	28	818246	816064	29145
	# 400	23	663300	661642	28767
	# 450	18	438928	437953	24331
	# 500	16	407171	406357	25397
	# 750	17	370364	369870	21757
	# 1000	20	383882	383498	19175
	# 2000	23	351464	351288	15273
	# 5000	35	360878	360806	10309
	# 10000	36,33333333	332730,8333	332698	9157
	# 50000	216	579127	579115	2681
	
	# however, small windows also mean a quality drop => we go with 1000, i.e., 2/3 speed

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