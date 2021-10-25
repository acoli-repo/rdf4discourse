#!/bin/bash
# retrieve all converted ttl files
# use sense labels to link to PDTB2 (!) ontology

########
# CONF #
########

UNLINKED=../lemon/

# apache jena
UPDATE=update

# Raptor
RAPPER=rapper

#######
# AUX #
#######

# escape paths to feed into sed
function escape {
	echo $1 | sed s/'\/'/'\\\/'/g;
}

#######
# RUN #
#######

for file in `find $UNLINKED | egrep 'ttl$'`; do

	lang=`egrep '@' $file | \
		sed s/'\s'/'\n'/g | \
		egrep '@' | \
		sed -e s/'.*[A-Za-z].*@'//g -e s/'[^a-z]'//g | \
		egrep '^...?$' | uniq -c | sort -rn | head -n 1 | sed s/'[^a-z]'//g`
	mkdir -p $lang

	echo $lang $file 1>&2

	if [ -e $lang/`basename $file` ]; then
		echo found $lang/`basename $file`, skipping $file 1>&2;
	else

		SRC=`rapper -i turtle $file '#' | \
			egrep ontolex.LexicalEntry | \
			head -n 100 | \
			sed s/'\s.*'//g | grep -v LexicalEntry | head -n 1 | \
			sed -e s/'[<>]'//g -e s/'[#\/][^#\/]*$'//`

		TGT='http://purl.org/acoli/dimlex/'$lang'/'`basename $file`

		#echo src: $SRC tgt: $TGT 1>&2

		(\
		# 0. PREFIX declarations\
		echo "PREFIX dimlex: <https://github.com/discourse-lab/dimlex/blob/master/DimLex.dtd#>";\
		echo "PREFIX ontolex: <http://www.w3.org/ns/lemon/ontolex#>";\
		echo "PREFIX pdtb: <http://purl.org/olia/discourse/discourse.PDTB.owl#>";\
		echo "PREFIX cdtb: <http://purl.org/olia/discourse/discourse.CDTB.owl#>";\
		echo "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>";\
		echo "PREFIX skos: <http://www.w3.org/2004/02/skos/core#>";\
		echo "PREFIX : <"$TGT"#>";\
		echo;\
		\
		# by default, we link to PDTB
		linker=link.sparql;\
		\
		# unless there is a separate model defined	\
		if echo $file | grep cdtb >&/dev/null; then	\
			linker=link-cdtb.sparql; \
		fi; \
		\
		# 1. link to PDTB or domain ontology and prune \
		$UPDATE --data=$file --update=$linker --dump | \
		rapper -i turtle -o ntriples - $SRC | \
		#sort -u | \
		\
		# 2. update to resolvable URLs \
		sed s/`escape $SRC`/`escape $TGT`/g; \
		\
		# 3. link back to source data \
		rapper -i turtle $file | \
		sed s/'\s'/'\n'/g | grep $SRC | sort -u | \
		sed s/'\(.*\)'`escape $SRC`'\(.*\)$'/'\1'`escape $TGT`'\2 rdfs:isDefinedBy \1'`escape $SRC`'\2 .'/g; \
		) | \
		rapper -i turtle -o turtle - $SRC > $lang/`basename $file`

		if egrep -m 1 'ontolex.reference' $lang/`basename $file` >&/dev/null; then
			echo $lang $file ok 1>&2
		else
			echo $lang/`basename $file` empty 1>&2
		fi
	fi;

	echo 1>&2
done
