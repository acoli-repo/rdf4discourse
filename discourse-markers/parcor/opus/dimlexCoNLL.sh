#!/bin/bash
# given a dimlex lemon dictionary, annotate a CoNLL file with its sense

# (default) dictionary
DIMLEX=../../lemon/dimlex/DimLex.ttl

# help
echo "synopsis: "$0 "DICT.TTL COL1..COLn
	DICT.TTL dimlex/lemon file in ttl, by default "$DIMLEX"
	COLi     column labels for input file
read CoNLL file from stdin, annotate with the longest applicable dimlex concept, write to stdout" 1>&2

# dimlex
if [ -e $1 ] ; then 
	DIMLEX=$1;
	shift;
fi;

# columns
COLS=$@;

# java environment
HOME=`echo $0 | sed s/'[^\/]*$'//`./; 
CLASSPATH=$HOME":"`find $HOME/lib | perl -pe 's/\n/:/g;' | sed s/':$'//`;
if [ $OSTYPE = "cygwin" ]; then
	CLASSPATH=`echo $CLASSPATH | sed s/':'/';'/g;`;
fi;
JAVAS=$(
	for java in `find  $HOME | sed s/'^.\/'// | egrep 'java$'`; do
		class=`echo $java | sed s/'java$'/'class'/;`
		if [ ! -e $class ]; then
			echo $java;
		else if [ $java -nt $class ]; then
			echo $java;
			fi;
		fi;
	done;
	)
JAVA="java -Dfile.encoding=UTF8 -classpath "$CLASSPATH;
	
if	# compile local java files
	if echo $JAVAS | grep java >/dev/null; then
		javac -classpath $CLASSPATH $JAVAS;
	fi 2>&1;
then 
	# create CoNLL RDF
	$JAVA CoNLLStreamExtractor http://example.org/irrelevant/ $COLS | \
	# annotate CoNLL RDF
	# load dimlex dictionary into the ontolex graph
	# add columns LEX_ENTRY, LEX_FORM, LEX_SENSE, LEX_CONCEPT
	# concatenate alternative annotations of one word in a single string value
	$JAVA CoNLLRDFUpdater \
		-custom \
		-model $DIMLEX http://www.w3.org/ns/lemon/ontolex 	\
		-updates \
			sparql/annotate-lemon-concepts.sparql \
			sparql/make-surjective.sparql \
			sparql/conll2strings.sparql \
			sparql/uri2localname-in-strings.sparql | \
	$JAVA CoNLLRDFFormatter -conll $COLS LEX_FORM LEX_CONCEPT;
fi;


