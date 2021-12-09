
# Copenhagen Dependency Treebank

(partial discourse annotation from https://github.com/mbkromann/copenhagen-dependency-treebank/tree/master/morten, a possibly more "official" discourse annotation is under https://github.com/mbkromann/copenhagen-dependency-treebank/tree/master/da, https://github.com/mbkromann/copenhagen-dependency-treebank/tree/master/en and https://github.com/mbkromann/copenhagen-dependency-treebank/tree/master/it. This data does not seem to have been included in any releases so far, but are available from the repository and fall under its licensing conditions)

## Licensing

LICENSE UPDATE 2020

The Copenhagen Dependency Treebanks are now licensed under the following open-source licenses:

* The MIT Opensource license: https://opensource.org/licenses/MIT
* The Creative Commons License (CC BY-SA 4.0): https://creativecommons.org/licenses/by-sa/4.0/
* The GNU PUblic License for libraries originally used for the treebanks

## Attribution

CDTB attribution:

Matthias Buch-Kromann <cdt@buch-kromann.dk>
Department of International Language Studies and Computational Linguistics
Copenhagen Business School

Also see https://github.com/mbkromann/copenhagen-dependency-treebank/blob/master/README.html

Discourse annotations:

The discourse annotations have been conducted by ‪Morten Gylling in 2010-2011, partial description under https://www.aclweb.org/anthology/W10-1817.pdf

## Documentation

I presume the most exhaustive description of the discourse annotations is in Morten Gylling's PhD thesis: https://www.econstor.eu/handle/10419/208872. He describes the relation inventory closely following Mann (2005), but the relations actually used in annotation are somewhat different. It is possible that at a later point in his work, he eventually used the RSTTool, but this data is not part of the CDTB.

|	Mann (2005); Gylling (2013, p. 188)	|	annotations with &3a;	|	with '+'	|	with ';'	|	"regular"	|	other variants	|
|	---	|	---	|	---	|	---	|	---	|	---	|
|	Antithesis	|		|		|		|		|		|
|		|	&3a;ATTRIBUTION	|		|		|	ATTRIBUTION	|	[ATTRIBUTION]	|
|	Background	|		|		|		|	BACKGROUND	|		|
|		|	&3a;CAUSE	|	+CAUSE	|	;CAUSE	|	CAUSE	|		|
|	Circumstance	|		|		|		|		|		|
|		|		|		|		|	COMMENT	|		|
|		|		|		|		|	COMPARISON	|		|
|	Concession	|		|		|		|		|		|
|	Condition	|		|		|		|	CONDITION	|		|
|	Conjunction	|		|		|		|		|		|
|	Contrast	|		|		|	;CONTRAST	|	CONTRAST	|	CONTR	|
|	Disjunction	|		|		|		|		|		|
|	Elaboration	|	&3a;ELABORATION	|	+ELABORATION	|	;ELABORATION	|	ELABORATION	|		|
|	Enablement	|		|		|		|	ENABLEMENT	|		|
|	Evaluation	|	&3a;EVALUATION	|	+EVALUATION	|		|	EVALUATION	|		|
|		|	&3a;EXPLANATION	|	+EXPLANATION	|	;EXPLANATION	|	EXPLANATION	|		|
|	Evidence	|		|		|		|		|		|
|	Interpretation	|		|		|		|		|		|
|	Joint	|		|	+JOINT	|	;JOINT	|	JOINT	|		|
|	Justify	|		|		|		|		|		|
|	List	|		|		|		|		|		|
|		|		|		|		|	MANNER	|		|
|	Means	|		|		|		|	MEANS	|		|
|	Motivation	|		|		|		|		|		|
|	Multinuclear Restatement	|		|		|		|		|		|
|	Nonvolitional Cause	|		|		|		|		|		|
|	Nonvolitional Result	|		|		|		|		|		|
|	Otherwise	|		|		|		|		|		|
|	Preparation	|		|		|		|		|		|
|	Purpose	|		|		|		|		|		|
|	Restatement	|		|		|		|		|		|
|	Sequence	|		|		|		|		|		|
|	Solutionhood	|		|		|		|		|		|
|	Summary	|		|		|		|	SUMMARY	|		|
|		|		|		|		|	TEMPORAL	|		|
|	Unconditional	|		|		|		|		|		|
|	Unless	|		|		|		|		|		|
|	Volitional Cause	|		|		|		|		|		|
|	Volitional Result	|		|		|		|		|		|
												
(outgoing) annotations from https://github.com/mbkromann/copenhagen-dependency-treebank/tree/master/morten											

I assume that the effective relation inventory uses exactly the following relations:

ATTRIBUTION
BACKGROUND
CAUSE
COMMENT
COMPARISON
CONDITION
CONTR
CONTRAST
ELABORATION
ENABLEMENT
EVALUATION
EXPLANATION
JOINT
MANNER
MEANS
SUMMARY
TEMPORAL

The marking of discourse markers is unclear, but could be `discmark` (Danish and Italian only, but *very rare*). In any case, they should be dependents of the satellite (cf. ARG2 in PDTB). The annotation is fused with syntax annotation, to the span is the word along with all its dependents.

## Conversion

Converted to an CoNLL format by CC

interpretation

- `@in` pointer from the (syntactic, etc.) dependent (current word) to the head (offset).
- `@out` pointer from head to dependents (if any)
- idea: create an incomplete conll format with XML markup (cf. Sketch Engine)
- note that it is tremendously hard to single out the syntactic annotation, as all annotations are conflated into `@in`. 

