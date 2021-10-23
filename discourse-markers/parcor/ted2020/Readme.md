# TED-2020

Parallel corpus from https://github.com/UKPLab/sentence-transformers/blob/master/docs/datasets/TED2020.md

Setup largely replicates [`../biblical`](../biblical), see there for explanations.

Retrieve source data, build `gazetteers/`, `data/` and `ensemble/` with

    $> make

## TODO

- Move gazetteer construction into main repo.
- Consolidate scripts with `biblical/`. The ones here are newer, but mostly unaltered.
- Change data files to *gz.
