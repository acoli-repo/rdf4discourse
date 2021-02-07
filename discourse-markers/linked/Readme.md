# link converted OntoLex discourse marker inventories

for every converted OntoLex discourse marker inventory
- load the OLiA PDTB ontology (http://purl.org/olia/discourse/discourse.PDTB.owl) into the local graph
- match dimlex:sense against PDTB labels (uris)
- create ontolex:reference between OntoLex sense and PDTB concept
- return OntoLex propertys or classes, prune everything else

## known issues

The mapping runs against the local names in the PDTB ontology, not labels (the ontology provides none).
It performs heuristic camel case parsing and lower casing to facilitate matching, but apparently, a considerable number of required matches don't resolve yet.

## history

2010-05-26 PDTB.owl created
2012-02-10 PDTB.owl published as experimental model in the OLiA repository
2014-03-21 linked with olia_discourse.owl, renamed to discourse.PDTB.owl
2020-02-04 linking with discourse marker lexicons

Christian Chiarcos