# Discourse markers from Discovery : Mining Discourse Markers for Unsupervised Sentence Representation Learning

Original data under https://github.com/synapse-developpement/Discovery, no license given.

Attribution:
Authors: Damien Sileo, Tim Van de Cruys, Camille Pradel and Philippe Muller
"Mining Discourse Markers for Unsupervised Sentence Representation Learning"
NAACL 2019, https://www.aclweb.org/anthology/N19-1351/

Note that the authors do not provide PDTB senses but only a plain list of discourse markers. The original data is thus enriched by a match with the PDTB inventory. For unknown discourse markers, the dominant PDTB3 sense of their distributional context is inferred in the following way:

- if a discourse marker is listed at PDTB, return this analysis, set confidence score to 1.0 and break
- rank all Discovery discourse markers with respect to their distributional similarity*
- we initialize the pool of senses with those of the highest-scored discourse marker, initially, these scores are 1 / number of senses
- if there is a single sense with maximum score, return it and the set of discourse markers consulted so far as "supporters"
- if there are multiple senses that entertain maximum score, iterate the procedure, add scores for every marker
- remove all supporters that do not feature the top-ranked sense
- the resulting score is the cosine distance from the highest-ranking supporter

As a result, every "novel" discourse marker receives a single tentative PDTB3 sense assignment (PDTB1-2 senses are extrapolated on this basis) along with a confidence score < 1.0.

* We calculate distributional similarity as cosine similarity over the GloVe 6B 50d embeddings. Aggregate embeddings for phrasal expressions are determined by average. Lookup is performed with flexible degrees of normalization:

	- Direct lookup; if it fails, then
	- Direct lookup of lower case form; then
	- dropping [^a-zA-Z0-9 ]; then
	- -"- with lowercase; 
	- then failure
	
For running the entire pipeline, see `build.sh`.
	
Note that because of the simple structure of the input data, the enrichment is performed in a TSV format and subsequently converted to OntoLex, only.

Also note that two additional columns are added to the TSV format, confidence and the list of "supporters".
Note that we have to make up `dimlex:confidence` because there is no OntoLex property to encode confidence scores.