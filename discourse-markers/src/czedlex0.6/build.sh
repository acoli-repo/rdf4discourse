#!/bin/bash
if [ ! -e czedlex0.6.pml ]; then
	if [ ! -e czedlex0.6.zip ]; then
		curl --remote-name-all https://lindat.mff.cuni.cz/repository/xmlui/bitstream/handle/11234/1-3074{/czedlex0.6.zip,/czedlex0.6_index_lindat.html};
	fi;
	unzip -c -nc czedlex0.6.zip czedlex0.6/PML/*.pml > czedlex0.6.pml
fi;