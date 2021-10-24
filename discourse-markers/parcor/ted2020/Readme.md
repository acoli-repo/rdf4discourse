# TED-2020

Parallel corpus from https://github.com/UKPLab/sentence-transformers/blob/master/docs/datasets/TED2020.md

Setup largely replicates [`../biblical`](../biblical), see there for explanations.

Retrieve source data, build `gazetteers/`, `data/` and `ensemble/` with

    $> make

## Content

- [`ensemble/`](ensemble/): TED sub-corpus with *all* (50) talks that cover *all* DimLex languages with (projected) annotations from all gazeteers. Use `make all` to rebuild. Currently, this is
- `data/`: Full TED corpus with Gazeteer annotations for all languages, use `make all` to build.
- [`eval/ted-mdb`](eval/ted-mdb): CoNLL edition of TED-MDB, a manual, PDTB3-compliant, multilingual annotation of a small TED subcorpus (6 talks), use `make clear; make eval` to re-build. Note that this has no overlap with `ensemble/`, so it cannot be used for direct evaluation.

## TODO

- Move gazetteer construction into main repo.
- Consolidate scripts with `biblical/`. The ones here are newer, but mostly unaltered.
- Change data files to *gz.
