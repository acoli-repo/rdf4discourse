# Discourse marker induction from OPUS parallel corpora [DEPRECATED]

idea: annotate a parallel corpus (from OPUS, e.g., Europarl) against discourse marker inventories

## Deprecation

This branch is deprecated, but kept here for archiving purposes.

Reasons:
- OPUS-provided Europarl data is incomplete, in that it provides bi-lingual alignments and skips unaligned sentences. This is a massive source of alignment errors that CoNLL-Merge has been shown to compensate, but only to a limited extend. If longer sections are missing, two Europarl files get de-synchronized. This happens early on for Dutch, but can occur everywhere.
- Internal URI structure of OPUS changed (this can be easily updated, though)
- Java implementation superseded by Python re-implementation in [`../bibles`](../bibles) and [`../ted2020`](../ted2020)

However:
- Being directly built on CoNLL-RDF, the pipeline here provided a much more advanced way of integrating the output of the merging operations.
- As there are manual discourse annotations of Europarl available as part of the [CDT](https://github.com/mbkromann/copenhagen-dependency-treebank). If these can be converted to PDTB- or RST-compliant annotations, this can be an independent source of evaluation. However, these are small in scale and have been independently developed, so that this mapping is not easily done. In fact, they seem to be incomplete. At present (2021), *various* PDTB-compliant annotations for multilingual TED talks represent a better basis for evaluation.
- Nevertheless, there are (shallow) annotations over English Europarl that can serve as a basis for an independent evaluation: https://www.idiap.ch/dataset/Disco-Annotation (https://www.idiap.ch/webarchives/sites/www.idiap.ch/project/comtis/resources.html), also see [Ludivine Crible and Sandrine Zufferey (2015): Using a unified taxonomy to annotate discourse markers in speech and writing, In: Proceedings 11th Joint ACL - ISO Workshop on Interoperable Semantic Annotation, (isa-11), April 14, 2015, Queen Mary University of London, London, UK, p.14-22](https://d1wqtxts1xzle7.cloudfront.net/37043829/ISA-11_proceedings.pdf?1426843680=&response-content-disposition=attachment%3B+filename%3DUsing_a_unified_taxonomy_to_annotate_dis.pdf&Expires=1635854587&Signature=KXBPWo4MCrTtdmyR7qO7mqPfViUjHKMx2sNC0ZjVS2MQz75xJhFzpJsnm7mTyt1zPcnvU2e9Ck7ZruDvY~6g~pM1fvZCJ0QE3HrYdLTnwRPyZOtrCDVAHPqy5GpTT8R--joO2hjmn6tBKpYay0rLjkG9kA1~S~ClsjBYsbdmBTMhAXePWyfLGrxOYYzncoYk3-lRB5CIL4td8KBjujHfl2GTobvvSF-17zJYvuXnWr74FNGk-VQcrBuZOVgOJJpuHm0BNpB7igyG8jC80dHrZy4QjP6uCFF~J1mMaxx6Jz213NLCXwaAlzPkgXadWjfHp4PjRmM5CKGtADUFVcFHQQ__&Key-Pair-Id=APKAJLOHF5GGSLRBV4ZA)

## Approach

- monolingual annotation via lookup
- annotations in multiple languages can help disambiguating
- automatically disambiguated discourse markers can be projected to a third language, i.e., "sense triangulation"
- employs dimlex dictionaries (in lemon/rdf) for (PDTB3-)sense lookup, conll-rdf for annotation, and conll-merge for aggregation over multiple languages

CoNLL-Merge and CoNLL-RDF are available from https://github.com/acoli-repo/conll and https://github.com/acoli-repo/conll-rdf.

To build:

  $> bash -e ./build.sh

## History

- 2017-11-10 initial commit [CC]
- 2017-12-29 initial evaluation [CC]
- 2020-04-01 follow-up experiments [LG]
- 2021-10-24 deprecation notice [CC]

## Contributors

CC Christian Chiarcos, chiarcos@informatik.uni-frankfurt.de
LG Luis Glaser
