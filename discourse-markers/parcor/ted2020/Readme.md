# TED-2020

Parallel corpus from https://github.com/UKPLab/sentence-transformers/blob/master/docs/datasets/TED2020.md

Setup largely replicates [`../bibles`](../bibles), see there for explanations.

Retrieve source data, build `gazetteers/`, `data/`, `ensemble/` and `eval/` with

    $> make

## Content

- [`ensemble/`](ensemble/): TED sub-corpus with *all* (50) talks that cover *all* DimLex languages with (projected) annotations from all gazeteers. Use `make all` to rebuild.
- `data/`: Full TED corpus with gazetteer annotations for all languages, use `make all` to build. This is the basis for the aggregate annotations in `ensemble/`. Dropped from the release for reasons of space.
- [`experiment/`](experiment/): internal evaluation (of `ensemble/` annotations against target language gazeteer)

- [`eval/`](eval/) data and code for external evaluation, currently featuring data from TED-MDB, only
- [`eval/ted-mdb`](eval/ted-mdb): CoNLL edition of TED-MDB, a manual, PDTB3-compliant, multilingual annotation of a small TED subcorpus (6 talks), use `make clear; make eval` to re-build fro original sources (if these get updated). Note that this has no overlap with `ensemble/`, so it cannot be used to evaluate `ensemble/` predictions, but has to work on a smaller ensembles.

## Format

`ensemble/`: TSV format with the following column structure

| TGT |  | cs |  |  | de |  |  | en |  |  |  |  | es |  |  | fr |  |  | it |  |  | nl |  |  | pt |  |  |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ID | WORD | ID | WORD | CzedLex | ID | WORD | CzedLex | ID | WORD | DiscMar | Discovery | PDTB | ID | WORD | DiscMar | ID | WORD | LexConn | ID | WORD | LICO | ID | WORD | DisCo | ID | WORD | LDM |
| 1 | Und | ? | ? | ? | 1 | Und | Conjunction.EXPANSION\|... | 1 | And | _ | Concession.COMPARISON\|...| Concession.COMPARISON\|... | 1 | Y | _ | ? | ? | ? | 1 | E | Conjunction.EXPANSION\|... | ? | ? | ? | 1 | A | _ |
| 2 | die | 2 | pak | Asynchronous.TEMPORAL\|... | 2 | die | _ | 2 | the | _ | _ | _ | 2 | la | _ | 1 | La | _ | 2 | la | _ | 1 | De | _ | 1 | A | _ |
| 3 | Erde | 1 | Země | _ | 3 | Erde | _ | 3 | earth | _ | _ | _ | 3 | tierra | _ | 2 | terre | _ | 3 | terra | _ | 2 | aarde | _ | 2 | terra | _ |
| 4 | war | 3 | byla | _ | 4 | war | _ | 4 | was | _ | _ | _ | 4 | estaba | _ | 3 | �tait | _ | 4 | era | _ | 3 | was | _ | 3 | era | _ |
| 5 | wüst | 4 | nesličná | _ | 5 | wüst | _ | 5 | waste | _ | _ | _ | 8 | Vac�a. | _ | 4 | informe | _ | 7 | deserta | _ | 4 | woest | _ | 4 | sem | Conjunction.EXPANSION\|... |
| 5 | wüst | 4 | nesličná | _ | 5 | wüst | _ | 5 | waste | _ | _ | _ | 8 | Vac�a. | _ | 4 | informe | _ | 7 | deserta | _ | 4 | woest | _ | 4 | sem | Conjunction.EXPANSION\|... |

- cols 1-2: target language
- cols 3-5: from Arabic
- cols 6-8: from Bangla
- cols 9-11: from Catalan
- cols 12-14: from Czech
- cols 15-17: from German
- cols 18-22: from English, col 20: DiscMar, col 21: distributional with PDTB2 interpretation, col 22: PDTB2
- cols 23-25: from Spanish
- cols 26-28: from French
- cols 29-31: from Italian
- cols 32-34: from Dutch
- cols 35-37: from Portuguese

Within each language, the first column holds the token ID, the second the WORD, the following the annotations. Note that we only preserve those words of the translation that have target language alignment. Also note that we preserve the first aligned word only for an n:m alignment. The original source format uses empty target language tokens to represent n:m alignment, but as we are not interested in the translation, but only in its annotation, this is omitted here.

## Evaluation

- internal evaluation: compare against target-language gazetteer as gold (`experiment/`)
- external evaluation: evaluate against TED-MDB annotations (`eval/`)
  - baseline: target-language gazeteer (3x `en`, `de`, `pt`)
  - ensemble predictions: all languages except for target language
  - we expect the ensemble to outperform the baseline because it provides some level of disambiguation

## TODO

- Move gazetteer construction into main repo.
- Consolidate scripts with `bibles/`. The ones here are newer, but mostly minor changes.
- Add support for Chinese. This requires either character-based tokenization or a more advanced tokenization script such as https://github.com/fxsjy/jieba
