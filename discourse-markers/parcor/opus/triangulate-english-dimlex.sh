#!/bin/bash
# triangulate german and italian dimlex annotations, to be integrated with build.sh
# reads conll from Europarl.en-de-it.dimlexed.conll, todo: column labels as arguments, to be propagated to CoNLLStreamExtractor, etc.
# current arguments only for CoNLLRDFFormatter
# TODO support MWEs

if [ ! -e Europarl.en-de-it.dimlexed.conll ]; then
	echo did not find Europarl.en-de-it.dimlexed.conll 1>&2;
else
	cat Europarl.en-de-it.dimlexed.conll | \
	# note that BELOW, ID is renamed as KEY, because conll:KEY (in the sparql updates) could also be applied to a conll:WORD
	CoNLLStreamExtractor http://example.org/irrelevant/ \
		KEY WORD DE_ID DE_WORD KEY__2 WORD__2 IT_ID__2 IT_WORD__2 DE_FORM DE_SENSE IT_FORM__2 IT_SENSE__2 \
		-u 	sparql/drop-unspec-nonWORD-nonKEY.sparql \
			sparql/split-invalid-alignments.sparql \
			sparql/drop-retoks.sparql{20} \
			sparql/merge-starred-lines.sparql{10} | \
	CoNLLRDFFormatter -conll KEY WORD DE_WORD DE_FORM DE_SENSE IT_WORD__2 IT_FORM__2 IT_SENSE__2 | \
	sed s/'^#.*'// | 				# strip comments, the following is to generate the correct column labels
	CoNLLStreamExtractor http://example.org/irrelevant/ \
		ID WORD DE DE_CUE SENSE1 IT IT_CUE SENSE2 \
		-u sparql/category-disambiguation.sparql \
	| \
	CoNLLRDFFormatter -conll ID WORD SENSE DE DE_CUE SENSE1 IT IT_CUE SENSE2
fi;	