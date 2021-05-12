#!/bin/bash
# retrieve discourse markers
# encode as OntoLex

wget -nc https://raw.githubusercontent.com/synapse-developpement/Discovery/master/data/markers_list.txt

# convert and link with PDTB
python3 build.py > built.tsv

# invert dominant sense(s) in the distributional context of non-PDTB markers
python3 infer-senses.py > inferred.tsv

# convert enriched TSV file to OntoLex-Lemon
python3 tsv2lemon.py > discovery-en-enriched.ttl