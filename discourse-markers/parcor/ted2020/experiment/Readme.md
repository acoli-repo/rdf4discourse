# Experiments

Use this directory to store and present experimental results.
[`eval.sh`](eval.sh) illustrates an exemplary evaluation loop, with results for different target annotations in `*tsv`.

target annotations: encoded in file name
- `5`: PDTB2
- `6`: RST (inferred from PDTB2 via OLiA)
- `8`-`12`: CCR
  - `8`: causalilty
  - `9`: order (of causal relations)
  - `10`: polarity
  - `11`: subjectivity
  - `12`: temporality

flags:
- `-direct` predict via majority vote
- `-iterate`, `-dimlex` annotate as with `-direct` in first run, bootstrap a discourse marker inventory with frequency informaiton, if an ensemble predicts more than one option, predict the one with higher overall likelihood


## intermediate observations

- the alignment quality is poor, because we do document-level alignment rather than alignment over all language data
- `en` performance is roughly en par with that on `bibles/`
- `ar` underperforms massively. Possibly, the data is just too different, there are differences in orthography between text and lexicon (vowelization?) or there is some level of morphological variation that is not captured in the discourse markers (cliticism?). Requires feedback from a language expert.
