#!/bin/bash
# build LICO-v.1.0.ttl with default settings

# system settings		UPDATE!
##################

SAXON=saxon
# SAXON=java -classpath $SAXON_HOME/saxon9sa.jar net.sf.saxon.Transform

# converter settings	DO NOT CHANGE!
#####################

LICO=../../src/lico/
SRC=`find $LICO | grep -m 1 'xml$'`;
ABox=`echo $SRC | sed -e s/'.*\/'//g -e s/'.xml$'//`.ttl

# conversion			DO NOT CHANGE!
#############

echo -n build $ABox .. 1>&2
if [ -e $ABox ]; then
	echo . found $ABox, reusing it 1>&2
else
	cp -n $LICO/readme* $LICO/README* 2>/dev/null;

	if whereis $SAXON | grep ':.*/' >/dev/null; then # found
		saxon -s:$SRC -xsl:lico2lemon.xsl > $ABox;
	else
		echo . 1>&2;
		echo did not find a Saxon executable, get it from http://saxon.sourceforge.net/#F9.8HE and configure the local "$"SAXON variable 1>&2;
	fi;
	if [ -e $ABox ]; then echo . ok 1>&2; else echo ... failed 1>&2; fi;
fi;
