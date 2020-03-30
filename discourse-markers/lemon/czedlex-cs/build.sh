#!/bin/bash
# build DimLex.ttl with default settings

# system settings		UPDATE!
##################

SAXON=saxon
# SAXON=java -classpath $SAXON_HOME/saxon9sa.jar net.sf.saxon.Transform

# converter settings	DO NOT CHANGE!
#####################

DIMLEX=../../src/czedlex0.6/
DICT=`find $DIMLEX | grep -m 1 'pml$'`
ABox=`echo $DICT | sed -e s/'.*\/'//g -e s/'\.pml$'//`.ttl

# conversion			DO NOT CHANGE!
#############

echo -n build $ABox .. 1>&2
if [ -e $ABox ]; then
	echo . found $ABox, reusing it 1>&2
else
	cp -n $DIMLEX/*index*html index.html;
	
	if whereis $SAXON | grep ':.*/' >/dev/null; then # found
		saxon -s:$DICT -xsl:pml2dimlex.xsl | \
		#tee tmp.xml | \
		saxon -s:- -xsl:dimlex2lemon.xsl > $ABox;
	else
		echo . 1>&2;
		echo did not find a Saxon executable, get it from http://saxon.sourceforge.net/#F9.8HE and configure the local "$"SAXON variable 1>&2;
	fi;
	if [ -e $ABox ]; then echo . ok 1>&2; else echo ... failed 1>&2; fi;
fi;

