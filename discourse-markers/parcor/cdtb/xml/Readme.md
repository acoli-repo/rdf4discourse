# discourse tree annotations extracted from CDTB discourse annotations

using the intermediate CoNLL format from `../conll`

Maintains only discourse annotations in an RST-like tree structure:
- A `node` element marks a dependent or SAT and its relation
- Its parent (`node/..`) is the (RST) span (composed of NUC and all its dependents)
- The textual content of the node (`node/text()`) is (roughly) equivalent to its PDTB ARG1 span.
- The textual content of the parent (`node/../text()`) is (roughly) equivalent to its PDTB ARG2 span.
