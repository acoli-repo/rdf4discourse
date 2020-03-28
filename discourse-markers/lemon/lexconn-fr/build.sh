#!/bin/bash
# build lexconn.ttl with default settings

# system settings		UPDATE!
##################

SAXON=saxon
# SAXON=java -classpath $SAXON_HOME/saxon9sa.jar net.sf.saxon.Transform

# converter settings	DO NOT CHANGE!
#####################

SRC=https://raw.githubusercontent.com/discourse-lab/Connective-Lex.info/master/Original%20lexicons/LexConn/Lexconn.xml;
DIMLEX=lexconn.xml;
ABox=`echo $DIMLEX | sed -e s/'\.xml$'//g`.ttl

# conversion			DO NOT CHANGE!
#############

echo -n build $ABox .. 1>&2
if [ -e $ABox ]; then
	echo . found $ABox, reusing it 1>&2
else
	if [ ! -e $DIMLEX ]; then
		if whereis $SAXON | grep ':.*/' >/dev/null; then # found
			wget $SRC -O - | saxon -s:- -xsl:lexconn2dimlex.xsl  > $DIMLEX;
		else
			echo . 1>&2;
			echo did not find a Saxon executable, get it from http://saxon.sourceforge.net/#F9.8HE and configure the local "$"SAXON variable 1>&2;
		fi;
	fi;
	
	if [ -e $DIMLEX ]; then
		if whereis $SAXON | grep ':.*/' >/dev/null; then # found
			saxon -s:$DIMLEX -xsl:dimlex2lemon.xsl > $ABox;
		else
			echo . 1>&2;
			echo did not find a Saxon executable, get it from http://saxon.sourceforge.net/#F9.8HE and configure the local "$"SAXON variable 1>&2;
		fi;
	fi;
	if [ -e $ABox ]; then echo . ok 1>&2; else echo ... failed 1>&2; fi;
fi;
