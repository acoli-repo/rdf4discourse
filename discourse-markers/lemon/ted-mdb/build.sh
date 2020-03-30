#!/bin/bash
# build TED-MDB dimlexes with default settings

# system settings		UPDATE!
##################

SAXON=saxon
# SAXON=java -classpath $SAXON_HOME/saxon9sa.jar net.sf.saxon.Transform

# converter settings	DO NOT CHANGE!
#####################

SRC_DIR=../../src/ted-mdb;

if [ ! -e PDTB2dimlex.class ]; then
	javac PDTB2dimlex.java;
fi;

# conversion			DO NOT CHANGE!
#############

if [ -e PDTB2dimlex.class ]; then
	if whereis $SAXON | grep ':.*/' >/dev/null; then # found
		for SRC in $SRC_DIR/*; do
			if [ -d $SRC ]; then
				if find $SRC | grep 'txt$' >& /dev/null; then
					ABox=ted-mdb-`echo $SRC | sed -e s/'\/*$'// -e s/'.*\/'// -e s/'.*'/'\L&'/`.ttl;
					DIMLEX=`echo $ABox | sed s/'\.ttl'//`.xml;
					echo -n build $ABox .. 1>&2
					if [ -e $ABox ]; then
						echo . found $ABox, reusing it 1>&2
					else
						RAW="";
						ANN="";
						cd $SRC/raw;
						for file in `find */ | grep 'txt$'`; do
							if [ -e ../ann/$file ] ; then
								RAW=$RAW" "$SRC/raw/$file;
								ANN=$ANN" "$SRC/ann/$file;
							fi;
						done;
						cd -;
						LANG=`find $SRC/ann | egrep -m 1 '\.txt$' | sed s/'.*[^a-z]\([a-z][a-z][a-zA-Z\-\_]*\)\.txt$'/'\1'/g;`
						java -Dfile.encoding=UTF-8 PDTB2dimlex $LANG $RAW -ann $ANN | \
						#tee $ABox.tmp | \
						xmllint --recover --format - > $DIMLEX;
						saxon \
							-s:$DIMLEX -xsl:dimlex2lemon.xsl \
							BASE=https://github.com/MurathanKurfali/Ted-MDB-Annotations/tree/master/`echo $SRC | sed -e s/'\/*$'// -e s/'.*\/'//`'/' \
							LANG=$LANG > $ABox;
						if [ -e $ABox ]; then echo . ok 1>&2; else echo ... failed 1>&2; fi;
					fi;
				fi;
			fi;
		done;
	else
		echo . 1>&2;
		echo did not find a Saxon executable, get it from http://saxon.sourceforge.net/#F9.8HE and configure the local "$"SAXON variable 1>&2;
	fi;
fi;


