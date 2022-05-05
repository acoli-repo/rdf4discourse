# Inducing Discourse Marker Inventories from Lexical Knowledge Graphs

Using [linked discourse marker inventories](../discourse-markers/linked) from nine European languages, and three collections of [machine-readable bi-dictionaries](https://github.com/acoli-repo/acoli-dicts) (Apertium, FreeDict, MUSE), we induce discourse marker inventories for novel languages.

Note that the methodology is restricted to lexical discourse markers (i.e., those typically provided in a dictionary), but the generated discourse marker inventory stubs can serve as a nucleus for the development of discourse marker inventories for novel languages. In particular, they can be manually pruned and then used for developing language-specific substitution tests to instruct annotators to chose one discourse relation or another.

For details, see (and refer to)

- Christian Chiarcos (2022/accepted), Inducing Discourse Marker Inventories from Lexical Knowledge Graphs. Accepted at LREC-2022, Marseille, France, June 2022.

## Generated stubs

We provide automatically generated discourse marker stubs for Bulgarian, Greek, Esperanto, Finnish, Japanese, Norwegian, Polish, Russian, Swedish and Turkish in a simple TSV format:

- [`stubs/pdtb.5.tsv`](stubs/pdtb.5.tsv) PDTB inventories, 5 pivot languages
- [`stubs/pdtb.4.tsv`](stubs/pdtb.4.tsv) PDTB inventories, 4 pivot languages
- [`stubs/rst.5.tsv`](stubs/rst.5.tsv) RST inventories, 5 pivot languages
- [`stubs/rst.4.tsv`](stubs/rst.4.tsv) RST inventories, 4 pivot languages
- [`stubs/ccr.5.tsv`](stubs/ccr.5.tsv) CCR inventories, 5 pivot languages
- [`stubs/ccr.4.tsv`](stubs/ccr.4.tsv) CCR inventories, 4 pivot languages

Note that these have been constructed using the same alorithm, but independently from each other for different schemas, PDTB v.2, Rhetorical Structure Theory (extrapolated from PDTB) and CCR features (extrapolated from PDTB). For each language, the predicted discourse markers are ranked according to their Level 0 score (discourse marker likelihood), and discourse relations are ranked according to their respective score. PDTB Levels 1-3 have been induced independently, but are merged here for presentational reasons. (This is because Level 1 relations can also occur in Level 2 and 3 annotations, etc., as a means of underspecification.)

Note that we list *all* discourse marker candidates, including those with marginal scores, but these should be removed in subsequent manual curation (or automated filtering). Discourse marker candidates with Level 0 score lower than 0.2 can be considered unlikely, but are nevertheless given for the sake of completeness. Considering Russian (PDTB, 4 pivot languages) as an example, we find the non-discourse marker *пять* ("five") right between the (potential) discourse markers *конечно* ("of course") and *последний* ("next") with Level 0 scores around 0.035. 

## Data processing

prep with

    $> make

eval with

    $> ./eval.sh

create stub discourse marker lexicons (in `stub/`) with

    $> ./build-dimlexes.sh

