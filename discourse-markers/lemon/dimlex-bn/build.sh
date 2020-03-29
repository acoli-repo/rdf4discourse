#!/bin/bash
# build discodict.ttl with default settings

# system settings		UPDATE!
##################

SAXON=saxon
# SAXON=java -classpath $SAXON_HOME/saxon9sa.jar net.sf.saxon.Transform

# converter settings	DO NOT CHANGE!
#####################

DIMLEX=../../src/dimlex-bangla
ABox=dimlex-bangla.ttl

# conversion			DO NOT CHANGE!
#############

echo -n build $ABox .. 1>&2
if [ -e $ABox ]; then
	echo . found $ABox, reusing it 1>&2
else
	if [ -e $DIMLEX/README.md ]; then
		cp -n $DIMLEX/README.md README_orig.md;
	else
		echo did not find $DIMLEX/README.md, make sure to run $DIMLEX/build.sh 1>&2;
	fi;

	if whereis $SAXON | grep ':.*/' >/dev/null; then # found
		saxon -s:../../src/dimlex-bangla/bangla_dimlex.xml -xsl:dimlex2lemon.xsl > $ABox;
	else
		echo . 1>&2;
		echo did not find a Saxon executable, get it from http://saxon.sourceforge.net/#F9.8HE and configure the local "$"SAXON variable 1>&2;
	fi;
	if [ -e $ABox ]; then echo . ok 1>&2; else echo ... failed 1>&2; fi;
fi;

