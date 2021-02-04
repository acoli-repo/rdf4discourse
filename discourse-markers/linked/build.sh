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
	
	$UPDATE --data=$file --update=link.sparql --dump | \
	sort -u | \
	$RAPPER -i turtle -o turtle - file:$file \
	> $lang/`basename $file`
	
	if egrep -m 1 'ontolex.reference' $lang/`basename $file` >&/dev/null; then
		echo $lang $file ok 1>&2
	else
		echo $lang $file empty 1>&2
	fi
	
	echo 1>&2
done