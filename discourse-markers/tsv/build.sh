#!/bin/bash
# iterate over all mapping files, use CoNLL-RDF to create TSV files with written representations of discourse markers and their PDTB relation

# system settings		UPDATE!
##################

CONLL_RDF=~/conll-rdf
# set to your local CoNLL-RDF installation

# conversion			DO NOT CHANGE!
#############
if ls $CONLL_RDF/run.sh | egrep '.' >&/dev/null; then # found

	for dimlex in ../lemon/*/; do
		if [ -e $dimlex/mapping.tsv ] ; then
			for dict in $dimlex/*ttl; do
				tgt=`echo $dict | sed -e s/'.*\/'// -e s/'\.ttl$'//`.tsv;
				if [ -s $tgt ]; then
					echo keeping $tgt 1>&2;
				else
					cat $dimlex/mapping.tsv | \
					$CONLL_RDF/run.sh CoNLLStreamExtractor \
						https://ignore.me/ \
						SENSE PDTB3 | \
						tee tmp.ttl | \
					$CONLL_RDF/run.sh CoNLLRDFUpdater \
						-custom -model $dict http://dimlex-lemon.org \
						-updates mapping2tsv.sparql | \
						tee tmp2.ttl | \
					$CONLL_RDF/run.sh CoNLLRDFFormatter -sparqltsv return-table.sparql > $tgt
				fi;
			done;
		fi;
	done;
else
	echo . 1>&2;
	echo did not find CoNLL-RDF, get it from https://github.com/acoli-repo/conll-rdf and configure the local "$"CONLL_RDF variable 1>&2;
fi;
