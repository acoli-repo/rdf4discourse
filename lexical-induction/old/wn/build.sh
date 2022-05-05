#!/bin/bash

####################
# (1) retrieve WNs #
####################

wget -nc http://wordnet-rdf.princeton.edu/wn31.nt.gz

# omw, all using the same concept URIs
wget -nc http://compling.hss.ntu.edu.sg/omw/wns/fra.zip
wget -nc http://compling.hss.ntu.edu.sg/omw/wns/spa.zip # = cat.zip, same index
wget -nc http://compling.hss.ntu.edu.sg/omw/wns/por.zip
wget -nc http://compling.hss.ntu.edu.sg/omw/wns/eng.zip
wget -nc http://compling.hss.ntu.edu.sg/omw/wns/ita.zip
# wget -nc http://compling.hss.ntu.edu.sg/omw/wns/ron.zip # buggy

#################
# (2) tab files #
#################

# echo -n wn31.tsv 1>&2
# if [ -e wn31.tsv ] ; then
	# echo ' 'found  1>&2
# else	
	# if javac WN31Reader.java; then java WN31Reader wn31.nt.gz ; fi | sed s/'^[^\t]*\/\([0-9][^\/>]*\)>\t'/'\1\t'/ > wn31.tsv
	# echo ' 'retrieved  1>&2
# fi;

echo -n por.tsv 1>&2;
if [ -e por.tsv ] ; then
	echo ' 'found  1>&2
else
	unzip -c por.zip por/wn-data-por.tab | sed s/'^\([0-9][0-9]*\-\([a-z]\t\)\)lemma\t\(.*\)$'/'\1\2"\3"@pt'/ \
	| egrep -a '^[0-9]'  \
	> por.tsv
	echo ' 'retrieved 1>&2;
fi;

echo -n spa.tsv 1>&2;
if [ -e spa.tsv ] ; then
	echo ' 'found  1>&2
else
	unzip -c spa.zip mcr/wn-data-spa.tab | sed s/'^\([0-9][0-9]*\-\([a-z]\t\)\)lemma\t\(.*\)$'/'\1\2"\3"@es'/ \
	| egrep -a '^[0-9]'  \
	> spa.tsv
	echo ' 'retrieved 1>&2;
fi;

echo -n cat.tsv 1>&2;
if [ -e cat.tsv ] ; then
	echo ' 'found  1>&2
else
	unzip -c spa.zip mcr/wn-data-cat.tab | sed s/'^\([0-9][0-9]*\-\([a-z]\t\)\)lemma\t\(.*\)$'/'\1\2"\3"@ca'/ \
	| egrep -a '^[0-9]'  \
	> cat.tsv
	echo ' 'retrieved 1>&2;
fi;

echo -n glg.tsv 1>&2;
if [ -e glg.tsv ] ; then
	echo ' 'found  1>&2
else
	unzip -c spa.zip mcr/wn-data-glg.tab | sed s/'^\([0-9][0-9]*\-\([a-z]\t\)\)lemma\t\(.*\)$'/'\1\2"\3"@gl'/ \
	| egrep -a '^[0-9]'  \
	> glg.tsv
	echo ' 'retrieved 1>&2;
fi;

echo -n eus.tsv 1>&2;
if [ -e eus.tsv ] ; then
	echo ' 'found  1>&2
else
	unzip -c spa.zip mcr/wn-data-eus.tab | sed s/'^\([0-9][0-9]*\-\([a-z]\t\)\)lemma\t\(.*\)$'/'\1\2"\3"@eu'/ \
	| egrep -a '^[0-9]'  \
	> eus.tsv
	echo ' 'retrieved 1>&2;
fi;

echo -n eng.tsv 1>&2;
if [ -e eng.tsv ] ; then
	echo ' 'found  1>&2
else
	unzip -c eng.zip eng/wn-data-eng.tab | sed s/'^\([0-9][0-9]*\-\([a-z]\t\)\)lemma\t\(.*\)$'/'\1\2"\3"@en'/ \
	| egrep -a '^[0-9]'  \
	> eng.tsv
	echo ' 'retrieved 1>&2;
fi;

echo -n fra.tsv 1>&2;
if [ -e fra.tsv ] ; then
	echo ' 'found  1>&2
else
	unzip -c fra.zip fra/wn-data-fra.tab | sed s/'^\([0-9][0-9]*\-\([a-z]\t\)\)[a-z:][a-z:]*\t\(.*\)$'/'\1\2"\3"@fr'/ \
	| egrep -a '^[0-9]'  \
	> fra.tsv
	echo ' 'retrieved 1>&2;
fi;

# echo -n ron.tsv 1>&2;
# if [ -e ron.tsv ] ; then
	# echo ' 'found  1>&2
# else
	# unzip -c ron.zip ron/wn-data-ron.tab | sed s/'^\([0-9][0-9]*\-\([a-z]\t\)\)[a-z:][a-z:]*\t\(.*\)$'/'\1\2"\3"@ro'/ \
	# | egrep -a '^[0-9]'  \
	# > ron.tsv
	# echo ' 'retrieved 1>&2;
# fi;

echo -n ita.tsv 1>&2;
if [ -e ita.tsv ] ; then
	echo ' 'found  1>&2
else
	unzip -c ita.zip ita/wn-data-ita.tab | sed s/'^\([0-9][0-9]*\-\([a-z]\t\)\)[a-z:][a-z:]*\t\(.*\)$'/'\1\2"\3"@it'/ \
	| egrep -a '^[0-9]'  \
	> ita.tsv
	echo ' 'retrieved 1>&2;
fi;

#########################
# (3) concept induction #
#########################



