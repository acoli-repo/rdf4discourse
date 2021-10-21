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

- monolingual CoNLL files with that aggregate over all gazeteers for that language, but split for different columns (annotations) of the gazetteers, e.g., `data/en.conll.gaz.5` (PDTB annotation from all gazeteers):

      # cols: ID WORD	 en.discmar.en	 en.discovery-en-enriched	 en.pdtb2
      # b.GEN.1.2
      1	And	_	Concession.COMPARISON|Condition.CONTIGENCY|Conjunction.EXPANSION|Contrast.COMPARISON|EXPANSION|Instantiation.EXPANSION|precedence.Asynchronous.TEMPORAL|result.Cause.CONTIGENCY|specification.Restatement.EXPANSION	Concession.COMPARISON|Condition.CONTIGENCY|Conjunction.EXPANSION|Contrast.COMPARISON|EXPANSION|Instantiation.EXPANSION|precedence.Asynchronous.TEMPORAL|result.Cause.CONTIGENCY|specification.Restatement.EXPANSION
      2	the	_	_	_
      3	earth	_	_	_
      4	was	_	_	_
      5	waste	_	_	_

  Analoguously, `*.6` represents RST annotations, `*.8` .. `*.12` represent CCR annotations.

- multilingual CoNLL files that aggregate over all multilingual gazeteers, including the source language (ordered by $LANGUAGE_ID.$GAZETTEER, split into separate files for every annotation layers, e.g., `ensemble/en.5.conll` (PDTB annotations from all gazeteers):

      # sent_id = b.GEN.1.2
      1	And	1	Und	Conjunction.EXPANSION|Contrast.COMPARISON|precedence.Asynchronous.TEMPORAL	1	And	_	Concession.COMPARISON|Condition.CONTIGENCY|Conjunction.EXPANSION|Contrast.COMPARISON|EXPANSION|Instantiation.EXPANSION|precedence.Asynchronous.TEMPORAL|result.Cause.CONTIGENCY|specification.Restatement.EXPANSION	Concession.COMPARISON|Condition.CONTIGENCY|Conjunction.EXPANSION|Contrast.COMPARISON|EXPANSION|Instantiation.EXPANSION|precedence.Asynchronous.TEMPORAL|result.Cause.CONTIGENCY|specification.Restatement.EXPANSION
      2	the	2	die	_	2	the	_	_	_
      3	earth	3	Erde	_	3	earth	_	_	_
      4	was	4	war	_	4	was	_	_	_
      5	waste	5	wüst	_	5	waste	_	_	_

  Annotations are ordered by language, then by name of gazeteer (as in data files). Here, the first annotation (columns 2-4) is German (col 2: ID, col3: WORD, col4: DimLex gazeteer), then English (columns 5-9; col 5: ID, col 6: WORD, col 7: DiscMar, col 8: Discovery, col 9: PDTB).

### to be updated

update and describe combination

For the current setup, the aligned languages are

- Czech (cols 6-8)
- German (cols 12-14)
- English (cols 18-20)
- French (cols 24-26)
- Italian (cols 30-32)
- Dutch (cols 36-38)
- Portuguese (cols 42-44)
- Spanish (cols 48-50)

### to be integrated

In the annotation columns, `_` means that alignment was successful but that no discourse information could be confirmed. `?` means that no target language alignment could be established.

For evaluation, run

    $> bash -e ./eval.sh

## notes

cf. http://www.semantic-web-journal.net/system/files/swj2898.pdf, also for related research

they demonstrate robustness of discourse annotations across (a certain sample) of languages

a difference is that we are completely annotation-free
