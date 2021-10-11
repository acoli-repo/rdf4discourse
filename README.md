# Discourse parsing with RDF/LOD technology

Discourse parsing is concerned with understanding the hierarchical and relational structure of utterances in a text. Discourse semantics complement semantic parsing by capturing context dependencies and allowing to aggregate information over multiple sentences.

This involves several dimensions:

* discourse structure (hierarchical organization of the discourse)
* discourse relations (coherence relations between multiple discourse segments)
* discourse markers (explicit cues for discourse relations)
* frame semantics (implicit semantic roles)
* anaphora (coreference, bridging, event anaphora)
* etc.

So far, we've been focusing on

- **interoperability**: using RDF technology and ontologies to facilitate the interoperability between annotation schemas for discourse, coreference and information structure ([OLiA Discourse Extensions](http://www.acoli.informatik.uni-frankfurt.de/resources/discourse/), in the [OLiA repository](https://github.com/acoli-repo/olia/tree/master/owl/experimental/discourse)) (Chiarcos 2014)
- **implicit discourse relations**: discourse parsing of implicit relations (Rönnqvist, Schenk and Chiarcos 2017, [in separate repository](https://github.com/acoli-repo/shallow-discourse-parser))
- **interlinked discourse marker inventories**: using RDF technology and the OLiA Discourse Extensions for creating discourse marker inventories that are linked across languages and theoretical frameworks ([discourse marker inventories in OntoLex-Lemon](tree/master/discourse-markers/linked)) (Chiarcos and Ionov 2021)

Research on discourse semantics which do not directly depend on either RDF or LOD technology is being dealt with in separate ACoLi repositories.

## References

- Christian Chiarcos (2014), [Towards interoperable discourse annotation. Discourse features in the Ontologies of Linguistic Annotation](https://aclanthology.org/L14-1685/), In: Proceedings of the Ninth International Conference on Language Resources and Evaluation (LREC'14), May 2014, Reykjavik, Iceland, European Language Resources Association (ELRA)
- Samuel Rönnqvist, Niko Schenk, and Christian Chiarcos (2017), [A Recurrent Neural Model with Attention for the Recognition of Chinese Implicit Discourse Relations](https://aclanthology.org/P17-2040/), In: Proceedings of the 55th Annual Meeting of the Association for Computational Linguistics (ACL-2017), July 2017, Vancouver, Canada, Association for Computational Linguistics
- Christian Chiarcos and Maxim Ionov (2021), [Linking Discourse Marker Inventories](https://drops.dagstuhl.de/opus/volltexte/2021/14576/). In: Proceedings of the Third Conference on Language, Data and Knowledge (LDK 2021), Sep 2021, Zaragoza, Spain, Schloss Dagstuhl -- Leibniz-Zentrum für Informatik, Open Access Series in Informatics (OASIcs), vol. 93
