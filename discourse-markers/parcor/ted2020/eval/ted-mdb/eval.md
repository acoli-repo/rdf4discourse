# Evaluation against TED-MDB

## content

- [`conll/`](conll) original TED-MDB data, converted to CoNLL, labels only, no relations nor features
- `data/` data repository that copies `../../data/*conll` files for gazetteer und TED-MDB languages, along with gazeteer annotations (where applicable). For missing languages, it contains placeholder sentences with correct sentence IDs (from English). This directory contains intermediate data only, but can be built using

    $> cd ../..
    $> rm -rf eval/ted-mdb/data
    $> make eval/ted-mdb/data

- [`ensemble/*conll`](ensemble) for every TED-MDB language, these files contain the the following annotations

  - target language data (from `data/`, cols 1-2): `ID`, `WORD`
  - target language annotation (from `conll/`, cols 3-4): `WORD`, `SENSE`. The files under `ensemble/*/*conll` contain the original annotations, the files under `ensemble/*conll` are normalized to PDTB2 annotations using [`mapping.tsv`](mapping.tsv)
  - Arabic (from `data`, as the following, cols 4-6): `TID` `TRANSLATION`, `SENSE`
  - Bangla (cols 7-9): `TID` `TRANSLATION`, `SENSE` (currently empty)
  - Catalan (cols 10-12): `TID` `TRANSLATION`, `SENSE`
  - Czech (cols 13-15): `TID` `TRANSLATION`, `SENSE`
  - German (cols 16-18): `TID` `TRANSLATION`, `SENSE`
  - English (cols 19-23): `TID` `TRANSLATION` `SENSE_DiscMar SENSE_Discovery SENSE_PDTB2`
  - Spanish (cols 24-26): `TID` `TRANSLATION`, `SENSE`
  - French (cols 27-30): `TID` `TRANSLATION`, `SENSE`
  - Italian (cols 31-33): `TID` `TRANSLATION`, `SENSE`
  - Dutch (cols 34-36): `TID` `TRANSLATION`, `SENSE`
  - Portuguese (cols 37-39): `TID` `TRANSLATION`, `SENSE`

- `eval.sh` evaluation script

  run

      $> bash -e ./eval.sh

- evaluation against TED-MDB doesn't yield impressive results, but ensemble improves over direct gazetteer annotation, mostly because it provides disambiguation. The picture doesn't change drastically if only higher levels of the PDTB hierarchy are concerned, but -dimlex has a positive effect.
