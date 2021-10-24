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
