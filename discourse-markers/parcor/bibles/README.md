
# Weakly Supervised Discourse Marker Induction

## Idea

- given massively parallel text (e.g., Bibles) and multilingual discourse marker inventories
- pick your target language, say, Bavarian (or any other language you have parallel text for), here using the Python API of the [ACoLi Bible Corpus](https://github.com/acoli-repo/acoli-corpora/tree/master/biblical)
- for all translations with discourse marker inventories, annotate all senses of the longest matching discourse marker (=> [`data/*.conll`](data))
- by alignment, project these to target language ([`ensemble/`](ensemble))
- use these projections as an ensemble to predict the most likely discourse relation for the target language (here: the suggested relation(s) that are least frequently rejected, `ensembly.py`)

  * [Building raw annotations](#building-raw-annotations)
  * [Experimental setup](#experimental-setup)
  * [Experiments](#experiments)
  * [Related research](#related-research)

## Building raw annotations

After running the `make` script, raw annotations (gazeteer-based, no disambiguation) will be deposited under `ensemble/`.

requirements:
- Unix-style shell, tested on Ubuntu 20.4
- python3, Java (Apache Jena), Perl, make
- arq (Apache Jena, get it from https://jena.apache.org/download/index.cgi)

To build

    $> make

This will create
- monolingual CoNLL files, without annotation (original spelling and use whitespace tokenization), e.g., `data/en.conll`:

      # b.GEN.1.2
      1	And
      2	the
      3	earth
      4	was
      5	waste

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

## Experimental setup

Run

    $> python3 ensemble.py ensemble/de.5.conll -e 4 -p 7 8 9

if `ensemble/de.5.conll` holds direct annotations in column 5 and predictor annotations in columns 8-10. This will append six columns:
- predicted discourse marker probability (ratio of predictors from `-p` columns that predict a discourse relation)
- top-ranked discourse relation(s) (having maximum score)
- score of top discourse relations
- the same types of columns for evaluation data (`-e` column[s], without an `-e` flag, these will be empty)


      1	Und	1	Und	Conjunction.EXPANSION|Contrast.COMPARISON|precedence.Asynchronous.TEMPORAL	1	And	_	Concession.COMPARISON|Condition.CONTIGENCY|Conjunction.EXPANSION|Contrast.COMPARISON|EXPANSION|Instantiation.EXPANSION|precedence.Asynchronous.TEMPORAL|result.Cause.CONTIGENCY|specification.Restatement.EXPANSION	Concession.COMPARISON|Condition.CONTIGENCY|Conjunction.EXPANSION|Contrast.COMPARISON|EXPANSION|Instantiation.EXPANSION|precedence.Asynchronous.TEMPORAL|result.Cause.CONTIGENCY|specification.Restatement.EXPANSION	0.6666666666666666	Concession.COMPARISON|Condition.CONTIGENCY|Conjunction.EXPANSION|Contrast.COMPARISON|EXPANSION|Instantiation.EXPANSION|precedence.Asynchronous.TEMPORAL|result.Cause.CONTIGENCY|specification.Restatement.EXPANSION	1.0	1.0	Conjunction.EXPANSION|Contrast.COMPARISON|precedence.Asynchronous.TEMPORAL	1.0
      2	die	2	die	_	2	the	_	_	_	0.0	_	0.0	0.0	_	0.0
      3	Erde	3	Erde	_	3	earth	_	_	_	0.0	_	0.0	0.0	_	0.0
      4	war	4	war	_	4	was	_	_	_	0.0	_	0.0	0.0	_	0.0
      5	wüst	5	wüst	_	5	waste	_	_	_	0.0	_	0.0	0.0	_	0.0

Also produces evaluation scores: accuracy, prec, recall, f (for discourse marker detection and discourse relation disambiguation). From these, accuracy is not a meaningful measurement because discourse markers are overall underrepresented and the majority class (no prediction) beats almost any meaningful prediction (e.g., for Czech, not to predict any discourse marker gives you 92.4% accuracy, many combinations of predictors beat that, but they don't have a large margin to improve upon, so accuracy just doesn't you insight about the significance of these improvements). Focus on precision and recall instead.

Other options:
- `-silent` return evaluation results only, no data. without `-e` flag, this returns nothing
- `-dimlex` bootstrap discourse marker inventory instead of/in addition to doing annotation
- `-iterate` after a first run of annotation, bootstrap a discourse marker inventory and use it for pruning raw predictions
- `-auto` test all subsets of predictors, if no `-e` is given, run against every individual predictor as evaluation basis
- `-weighted` self-supervision: weigh predictors wrt. agreement with predictor majority, if used in combination with `-dimlex` or `-iterate`, these are performed after initial weighting. Note that this operates on predicted *relations*. Its scoring function maximizes true_positive/(true_positive + false_positive + false_negative), with true_positive defined as partial overlap.

      usage: ensemble.py [-h] [-p PREDICTOR [PREDICTOR ...]]
                         [-e [EVALUATOR [EVALUATOR ...]]] [-weighted] [-dimlex]
                         [-iterate] [-w WORDS_COL] [-th PRED_THRESHOLD]
                         [-c MIN_CONFIDENCE] [-eth EVAL_THRESHOLD] [-slim] [-silent]
                         [-auto]
                         input

      if a text has been annotated by multiple tools according to the same schema,
      run a number of bootstrapping experiments

      positional arguments:
        input                 CoNLL file to read from, if omitted, read from stdin

      optional arguments:
        -h, --help            show this help message and exit
        -p PREDICTOR [PREDICTOR ...], --predictor PREDICTOR [PREDICTOR ...]
                              columns that contain the invidual input predictions
        -e [EVALUATOR [EVALUATOR ...]], --evaluator [EVALUATOR [EVALUATOR ...]]
                              columns that constitute an ensemble that the predictor
                              is evaluated against
        -weighted, --self_weighted
                              use the first run to weigh different predictors for
                              their agreement with the majority
        -dimlex, --dimlex_mode
                              instead of doing annotation, bootstrap a discourse
                              marker inventory, note that this requires input to be
                              a file
        -iterate, --self_supervision
                              bootstrap a discourse marker inventory, then use it to
                              re-annotate the input, note that this requires input
                              to be a file
        -w WORDS_COL, --words_col WORDS_COL
                              WORDS/FORM column, needed for
                              -iterate/--self_supervision
        -th PRED_THRESHOLD, --pred_threshold PRED_THRESHOLD
                              threshold for predictions: predict only if probability
                              for a discourse marker is at least at this value, 0.4
                              is a good guess
        -c MIN_CONFIDENCE, --min_confidence MIN_CONFIDENCE
                              threshold for predictions: predict only if dimlex
                              confidence >= min_confidence, in iterative mode, only
        -eth EVAL_THRESHOLD, --eval_threshold EVAL_THRESHOLD
                              threshold for evaluation, if evaluated against a
                              single target annotation, defaults to --pred_threshold
        -slim, --slim_output  return only --words_col, --predictor and --evaluator
                              columns, as well as their predictions
        -silent, --no_output  return only scores, no annotations
        -auto, --test_all_combinations
                              if set, explore all possible combinations, overrides
                              all other arguments except for input, -p, -e, -w


## Experiments

Individual experiments and their results under [`experiment/`](experiment), based on current configuration of `Makefile`, e.g., for `ensemble/de.5.conll`:

| TGT |  | cs |  |  | de |  |  | en |  |  |  |  | es |  |  | fr |  |  | it |  |  | nl |  |  | pt |  |  |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ID | WORD | ID | WORD | CzedLex | ID | WORD | DimLex | ID | WORD | DiscMar | Discovery | PDTB | ID | WORD | DiscMar | ID | WORD | LexConn | ID | WORD | LICO | ID | WORD | DisCo | ID | WORD | LDM |
| 1 | Und | ? | ? | ? | 1 | Und | Conjunction.EXPANSION\|... | 1 | And | _ | Concession.COMPARISON\|... | Concession.COMPARISON\|... | 1 | Y | _ | ? | ? | ? | 1 | E | Conjunction.EXPANSION\|... | ? | ? | ? | 1 | A | _ |
| 2 | die | 2 | pak | Asynchronous.TEMPORAL\|... | 2 | die | _ | 2 | the | _ | _ | _ | 2 | la | _ | 1 | La | _ | 2 | la | _ | 1 | De | _ | 1 | A | _ |
| 3 | Erde | 1 | Země | _ | 3 | Erde | _ | 3 | earth | _ | _ | _ | 3 | tierra | _ | 2 | terre | _ | 3 | terra | _ | 2 | aarde | _ | 2 | terra | _ |
| 4 | war | 3 | byla | _ | 4 | war | _ | 4 | was | _ | _ | _ | 4 | estaba | _ | 3 | �tait | _ | 4 | era | _ | 3 | was | _ | 3 | era | _ |
| 5 | wüst | 4 | nesličná | _ | 5 | wüst | _ | 5 | waste | _ | _ | _ | 8 | Vac�a. | _ | 4 | informe | _ | 7 | deserta | _ | 4 | woest | _ | 4 | sem | Conjunction.EXPANSION\|... |

In the current setup, the column structure is

- target language (cols 1-2)
- Czech (cols 3-5)
- German (cols 6-8)
- English (cols 9-13)
- Spanish (cols 14-16)
- French (cols 17-19)
- Italian (cols 20-22)
- Dutch (cols 23-25)  
- Portuguese (cols 26-28)

For each column group, the first two columns are ID and WORD, the third and following represent different gazetteers.

- TODO: update evaluation loop from `experiment/eval.sh`

Evaluation strategies:
- against annotation with target language gazeteer (as currently implemented in `ensemble.py`)
- evaluation of bootstrapped DimLex against target language DimLex

## Related Research

- [Özer et al., subm.](http://www.semantic-web-journal.net/system/files/swj2898.pdf) previously demonstrated robustness of discourse annotations across (a certain sample) of languages.
A difference is that this experiment is completely annotation-free.
