# Experiments

Use this directory to store and present experimental results.
[`eval.sh`](eval.sh) illustrates an exemplary evaluation loop, with results for different target annotations in `*tsv`.

Target annotations: encoded in file name
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

For basic evaluation and plots, run

    $> cat ensemble.5.tsv | grep  dimlex | cut -f 2,9,15  | python3 plot.py -min 0.2 -max 0.9 -t "Iterated prediction, PDTB" -o "dimlex.5.png"

(etc.)

# preliminary oservations

- relations can be predicted with an f-score close of up to 80% for PDTB, RST and most CCR dimensions
- this is with the exception of the CCR dimension order. The best prediction with full ensemble here is 26%. However, small-scale ensembles perform much better. Rather unclear why.
- `-iterate` helps relation prediction, but it hurts discourse marker prediction
- looking only at the best-performing configurations, we find that some languages can be more easily predicted from the ensemble than others. This does indicate at conceptual differences in their inventories

    direct prediction, best-performing configuration
    - en, tgt 12, ensemble size 7, f_pdtb=81.4%
    - pt, tgt 27, ensemble size 7, f_pdtb=67.6%
    - de, tgt 7, ensemble size 7, f_pdtb=67.1%
    - cs, tgt 4, ensemble size 6, f_pdtb=63.7% (adding 15 hurt)
    - it, tgt 21, ensemble size 7, f_pdtb=63.4%
    - fr, tgt 18, ensemble size 6, f_pdtb=55.6%
    - nl, tgt 24, ensemble size 7, f_pdtb=40.0%
    - es, tgt 15, ensemble size 4, f_pdtb=30.4% (ensemble: 7,12,21,27)

    The high score for English reflects the fact that English (and, within TextLink, German) served as a template for all other discourse marker inventories. The Portuguese model seems to follow both very closely, and can thus be grouped together. It is known that the Czech (and the following) models are based on resources that were converted to DimLex rather than natively created for it (with the possible exception of Dutch), their greater divergence from the model inventories (English, German; and, by closely following them, Portuguese) may reflect conceptual differences of the original source material from PDTB/DimLex conventions.
    This is particularly evident in the poor performance of Spanish (and the drop in the Czech prediction when adding it), as this goes back to a theory that only be very loosely aligned with PDTB (top-level alignment!), whereas all other inventories are modelled or infliuenced by PDTB. The relatively poor performance of French (originally SDRT rather than PDTB) may have similar reasons. The relatively poor performance of Dutch is unexplained, but may have reasons in the composition and/or coverage of the discourse marker inventory.

- With `-iterate`, a number of smaller inventories outperform larger inventories.
