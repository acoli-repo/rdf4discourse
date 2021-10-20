# discourse marker induction

## idea

- given massively parallel text (e.g., bibles) and multilingual discourse marker inventories
- pick your target language, here, Bavarian
- for all translations with discourse marker inventories, annotate all senses of the longest matching discourse marker
- by alignment, project these to target language (`build.sh` => `build.mrg.conll`)
- use these projections as an ensemble to predict the most likely discourse relation for the target language (here: the suggested relation(s) that are least frequently rejected, `ensembly.py`, called by `eval.sh`)
- as we don't have target language annotations, evaluate against another projection (`eval.sh`)

## building

requirements:
- Unix-style shell, tested on Ubuntu 20.4
- python3, Java (Apache Jena), Perl, make
- arq (Apache Jena, get it from https://jena.apache.org/download/index.cgi)

run

    $> make

This will create
- monolingual CoNLL files, without annotation (original spelling and use whitespace tokenization), e.g., `data/en.conll`:

    # b.GEN.1.2
    1	And
    2	the
    3	earth
    4	was
    5	waste

- bilingual CoNLL files, with translation as annotation (lowercase, using heuristic tokenization), e.g., `data/en-de.conll`:

    # text: and the earth was waste and empty , and darkness was on the face of the deep , and the spirit of god was hovering over the face of the waters .
    # translation: und die erde war wüst und leer , und es war finster auf der tiefe ; und der geist gottes schwebte auf dem wasser .
    1	and	1	und
    2	the	2	die
    3	earth	3	erde
    4	was	4	war
    5	waste	5	wüst

- monolingual CoNLL files with Gazetteer-based annotation (all *possible* senses, none of these is confirmed at this stage; original spelling and use whitespace tokenization), e.g., `data/en.pdtb2.conll`:

    # b.GEN.1.2
    1	And	And	en	Concession.COMPARISON|Condition.CONTIGENCY|Conjunction.EXPANSION|Contrast.COMPARISON|EXPANSION|Instantiation.EXPANSION|precedence.Asynchronous.TEMPORAL|result.Cause.CONTIGENCY|specification.Restatement.EXPANSION	Antithesis|Background|Circumstance|Concession|Condition|Conjunction|Contrast|Disjunction|Enablement|Evaluation|Interpretation|List|Means|MultiNuclearRestatement|NonVolitionalResult|Otherwise|Preparation|Purpose|Sequence|Summary|Unless|VolitionalResult	1|2|3	Additive|Causal|Conditional|NonConditionalCause	CauseConsequence|ConsequenceCause	Negative|Positive	Objective|Subjective	Antichronological|Chronological
    2	the	_	_	_	_	_	_	_	_	_	_
    3	earth	_	_	_	_	_	_	_	_	_	_
    4	was	_	_	_	_	_	_	_	_	_	_
    5	waste	_	_	_	_	_	_	_	_	_	_

### to be updated / not integrated yet

creates `build.mrg.conll`, with

    # b.GEN.1.2
    # Und d Erdn war oed und laer , finster war s über dyr Teuffn , und yn n Herrgot sein Geist gschwöbt über n Wasser .
    1	Und	1	und	?	?	?	?	1	und	de	COMPARISON|EXPANSION|TEMPORAL	COMPARISON:Contrast|EXPANSION:Conjunction|TEMPORAL:Asynchronous	COMPARISON:Contrast|EXPANSION:Conjunction|TEMPORAL:Asynchronous:Precedence	1	und	?	?	?	?	1	und	?	?	?	?	1	und	it	EXPANSION|TEMPORAL	EXPANSION:Conjunction|TEMPORAL:Asynchronous	EXPANSION:Conjunction|TEMPORAL:Asynchronous:Precedence	1	und	?	?	?	?	1	und	?	?	?	?	1	und	_	_	_	_
    2	d	2	d	_	_	_	_	2	d	_	_	_	_	2	d	_	_	_	_	2	d	_	_	_	_	2	d	_	_	_	_	2	d	_	_	_	_	2	d	_	_	_	_	2	d	_	_	_	_

Columns:

- 1 ID
- 2 WORD
- 3 TOK_ID
- 4 NORM
- 5 LANG
- 6 PDTB1_SENSE
- 7 PDTB2_SENSE
- 8 PDTB3_SENSE
(cols 3 to 8 iterate for all other alignment pairs)

- ID: original token id (whitespace tokenization)
- WORD: original token
- TOK_ID: token id of normalized text
- NORM: normalized token, may split several WORD tokens
- LANG: translation language that the last two and the following three columns refer to
- PDTBx_SENSE: discourse relation(s), PDTB hierarchy depth x with x from 1 to 3

For every aligned translation, the columns WORD TOK_ID, NORM, LANG and PDTB1..3 are repeated.
For the current setup, the aligned languages are

- Czech (cols 6-8)
- German (cols 12-14)
- English (cols 18-20)
- French (cols 24-26)
- Italian (cols 30-32)
- Dutch (cols 36-38)
- Portuguese (cols 42-44)
- Spanish (cols 48-50)

In the annotation columns, `_` means that alignment was successful but that no discourse information could be confirmed. `?` means that no target language alignment could be established.

For evaluation, run

    $> bash -e ./eval.sh

## notes

cf. http://www.semantic-web-journal.net/system/files/swj2898.pdf, also for related research

they demonstrate robustness of discourse annotations across (a certain sample) of languages

a difference is that we are completely annotation-free
