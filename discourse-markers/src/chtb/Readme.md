# Chinese Discourse Treebank (CHDT)

Chinese Discourse Treebank was developed at Brandeis University as part of the Chinese Treebank Project and consists of approximately 73,000 words of Chinese newswire text annotated for discourse relations. It follows the lexically grounded approach of the Penn Discourse Treebank (PDTB) (LDC2008T05) with adaptations based on the linguistic and statistical characteristics of Chinese text. Discourse relations are lexically anchored by discourse connectives (e.g., because, but, therefore), which are viewed as predicates that take abstract objects such as propositions, events and states as their arguments. Along with PDTB-style schemes for English, Turkish, Hindi and Czech, Chinese Discourse Treebank provides an additional perspective on how the PDTB approach can be extended for cross-lingual annotation of discourse relations.

Several releases:
- original release (v.0.5): https://catalog.ldc.upenn.edu/LDC2014T21
- CoNLL-2016 edition: https://catalog.ldc.upenn.edu/LDC2016E50
- CoNLL-2016 post-release: re-release of CoNLL-2015+2016 data under https://catalog.ldc.upenn.edu/LDC2017T13

The discourse markers here are from the LDC2016E50 release (original CoNLL-2016 shared task data). We provide discourse marker statistics only, extracted from //Relations.json.
We consider aggregate statistics to not fall under LDC copyright, as no annotation nor primary data is exchanged.

To rebuild, run (set `chdt` to your corpus directory):

  $> python3 json2dimlex.py `find chdt | grep '/relations.json'` > chdt.xml
