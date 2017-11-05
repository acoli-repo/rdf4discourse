************** LICO, Lexicon for Italian COnnectives (version 1.0) **************

By downloading or using this data, you accept the terms and conditions of the Creative Commons Attribution 4.0 (CC BY 4.0) license agreement (https://creativecommons.org/licenses/by/4.0/).

© 2016, Fondazione Bruno Kessler and University di Pavia 

Contacts: Feltracco Anna: feltracco@fbk.eu; Magnini Bernardo: magnini@fbk.eu; Jezek Elisabetta: jezek@unipv.it
Website: https://hlt.fbk.eu/technologies/lico-lexicon-italian-connectives

Publications or presentations containing research results obtained through the use of LICO should cite the following reference: 
Feltracco Anna, Jezek Elisabetta, Magnini Bernardo, Stede Manfred. LICO: A Lexicon of Italian Connectives In: Proceedings of the Third Italian Conference on Computational Linguistics (CLiC-it 2016), Napoli, December 5-7, 2016.

=== Acknowledgments ==============================================

We acknowledge Denise Pangrazzi, for her contribution in identifying the Italian equivalents of the German connectives, and propose an Italian version of the German examples.
We acknowledge Felix Dombek, for his contribution in aligning LICO entries with DimLex entries (Stede, 2002)
We acknowledge Manfred Stede, for having stimulated our work on LICO.
=======================================================================

In this folder you will find:
- 1 xml files with the list of connectives and their attributes
- this readme file

=== Resource Description ==============================================

LICO includes 173 discourse connectives used in Italian, together with:
- orthographic variants, 
- part of speech(es), 
- semantic relation(s) according to the Penn Discourse Treebank 3.0 schema of relations (Webber et al., 2016; Rehbein et al., 2016) as proposed in the DimLex resource (Scheffler and Stede, 2016) which is our main reference resource, 
- a number of usage examples.


=== Entry description =================================================
Currently, for each entry LICO specifies:

- an identification number (tag = <entry id>)

- whether the connective is composed by correlating part and eventually the specification of the two correlating parts
		tag = entry id, nested_tag = <orth>, attribut = type, attribute_value = discont 
	or not:
		tag = entry id, nested_tag = <orth>, attribut = type, attribute_value = cont
		
- whether the connective is composed by a single token
		tag = entry id, nested_tag = <orth>, nested_tag = <part>, attribut = type, attribute_value = single
	or by more than one token 
		tag = entry id, nested_tag = <orth>, nested_tag = <part>, attribut = type, attribute_value = phrasal
		
- the connective
		tag = entry id, nested_tag = <orth>, nested_tag = <part>, text = THE_CONNECTIVE
		
- possible orthographic variants
		tag = entry id, nested_tag = <orth>, nested_tag = <part>, attribut = var, attribute_value = orth
	or lexical variants:
		tag = entry id, nested_tag = <orth>, nested_tag = <part>, attribut = var, attribute_value = lex. 
	In case of variants another tag <orth> is listed under the same entry id;
	
- pos category: adverbs, preposition, subordinating or coordinating conjunctions 
		tag = entry id, nested_tag = syn, attribut = type, attribute_value = adverbial,
		tag = entry id, nested_tag = syn, attribut = type, attribute_value = prepositional,
		tag = entry id, nested_tag = syn, attribut = type, attribute_value = subordinating, 
		tag = entry id, nested_tag = syn, attribut = type, attribute_value = coordinating;
			
- the semantic relation(s) that the connective indicates, according to the PDTB 3.0 schema (in Webber et al., 2016; Rehbein et al., 2016)
		tag = entry id, nested_tag = syn, nested_tag = sem, nested_tag = coh-relation, text = THE_SENSE;
		
- examples of the connectives for each semantic relations 
		tag = entry id, nested_tag = syn, nested_tag = sem, nested_tag = example, text = THE_EXAMPLE
		
- possible alignments with lexicon of connectives in other languages 
		tag = entry id, nested_tag = commento, text = THE_ALIGNEMENTS



=== Entry Example ===================================================

  <entry id="30">
    <orth type="cont">
      <part type="phrasal" var="orth">ciononostante</part>
    </orth>
    <orth type="cont">
      <part type="phrasal" var="orth">nonostante ciò</part>
    </orth>
    <orth type="cont">
      <part type="phrasal" var="orth">ciò nonostante</part>
    </orth>
    <syn type="coodinating">
      <sem>
        <coh-relation>COMPARISON:Concession:Arg2-as-denier</coh-relation>
        <example>Entrambe le pagine annunciavano un secondo incontro per martedì. Ciononostante le lotte nei campi andarono avanti anche il lunedì.</example>
        <example>Adesso la procura della repubblica ha ordinato la restituzione dell'esemplare confiscato. Ciononostante l'istruttoria contro la casa editrice prosegue.</example>
        <example>Lui non ha valutato correttamente la situazione della politica interna nella sua patria. Ciononostante è ritornato da quella parte in ogni caso.</example>      
      </sem>
    </syn>
    <commento>DimLex.xml/id="k62"</commento>
    <commento>DimLex.xml/id="k78"</commento>
    <commento>DimLex.xml/id="k107"</commento>
    <commento>DimLex.xml/id="k143"</commento>
  </entry>

  
=== References of this readme ==============================================

Ines Rehbein, Merel Scholman, and Vera Demberg. 2016. Annotating Discourse Relations in Spoken Language: A Comparison of the PDTB and CCR Frameworks. In Proceedings of the Tenth International Conference on Language Resources and Evaluation (LREC 2016), Portoroˇz, Slovenia, May.

Tatjana Scheffler and Manfred Stede. 2016. Adding Semantic Relations to a Large-Coverage Connective Lexicon of German. In Proceedings of the Tenth International Conference on Language Resources and Evaluation (LREC 2016), Portoroˇz, Slovenia, May.

Manfred Stede.  2002. DiMLex: A Lexical Approach to Discourse Markers. In: A. Lenci, V. Di Tomaso (eds.): Exploring the Lexicon - Theory and Computation. Alessandria (Italy): Edizioni dell'Orso, 2002.

Bonnie Webber, Rashmi Prasad, Alan Lee, and Aravind Joshi. 2016. A Discourse-Annotated Corpus of Conjoined VPs. In Proceedings of the 10th Linguistic Annotation Workshop held in conjunction with ACL 2016 (LAW-X 2016), pages 22–31. Association for Computational Linguistics.
