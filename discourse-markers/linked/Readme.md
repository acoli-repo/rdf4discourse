# link converted OntoLex discourse marker inventories

for every converted OntoLex discourse marker inventory
- load the OLiA PDTB ontology (http://purl.org/olia/discourse/discourse.PDTB.owl) into the local graph
- match dimlex:sense against PDTB labels
- create ontolex:reference between OntoLex sense and PDTB concept
- return OntoLex propertys or classes, prune everything else
- manually added machine-readable license information 
- attribution information added

## known issues

add attribution information

## history

2010-05-26 PDTB.owl created
2012-02-10 PDTB.owl published as experimental model in the OLiA repository
2014-03-21 linked with olia_discourse.owl, renamed to discourse.PDTB.owl
2020-02-04 linking with discourse marker lexicons (via URIs)
2020-02-07 linking with discourse marker lexicons (via labels and altLabels)
2020-02-07 resolvable URIs via http://purl.org/acoli/dimlex

Christian Chiarcos