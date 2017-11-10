annotate a parallel corpus (from OPUS, e.g., Europarl) against discourse marker inventories

- monolingual annotation via lookup
- annotations in multiple languages can help disambiguating
- automatically disambiguated discourse markers can be projected to a third language, i.e., "sense triangulation"
- employs dimlex dictionaries (in lemon/rdf) for (PDTB3-)sense lookup, conll-rdf for annotation, and conll-merge for aggregation over multiple languages

CoNLL-Merge and CoNLL-RDF are available from https://github.com/acoli-repo/conll and https://github.com/acoli-repo/conll-rdf. Proper Maven integration in preparation.

Run build.sh

Sample output (no disambiguation yet, de+it only) in Europarl.de-it.annotated-sample.conll