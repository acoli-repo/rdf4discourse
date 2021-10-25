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
- `en` has f_pdtb<=74.9% (iterated <= 82.6%)
- `it` has f_pdtb <= 67.4 (iterated <= 76.4)
- `ca` has f_pdtb<=64.5% (direct, iterated<=72.0%), but this is not an ensemble projection, but from a single source, 24 (es). In the current sample, these are the only DiscMar-based inventories (in place of the English DiscMar, we used PDTB2)
- `es` has f_pdtb<=64.9% (iterated <= 72.4%), single source: Catalan
- `pt` has f_pdtb <= 60.5 (iterated <= 69.0)
- `de` has f_pdtb<=55.4% (direct, iterated <= 62.4%)
- `bn` performs better, with f_pdtb<=51.3\% as best performing direct projection (and 63.6% as best-performing iterated projection)
- `cs` has f_pdtb<=49.8% (direct, iterated <= 57.8%)
- `nl` has f_pdtb <= 48.4 (iterated <= 55.1)
- `fr` has f_pdtb <= 43.1 (iterated <= 51.5%)
- `ar` underperforms massively, with f_pdtb=21.0% as best-performing direct projection. Possibly, the data is just too different, there are differences in orthography between text and lexicon (vowelization?) or there is some level of morphological variation that is not captured in the discourse markers (cliticism?). Requires feedback from a language expert.
