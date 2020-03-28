# DisCoDict - Structure

DisCoDict is based on [DiMLex](https://github.com/discourse-lab/dimlex) and has basically the same structure. The documentation below is a modified version of the [DiMLex Documentation](https://github.com/discourse-lab/dimlex/blob/master/DimLex-documentation.md).

The dictionary is constructed of a number of dictionary entries, numbered by an 'id'. 

Schematically, each entry consists of the following data fields:

**`<orths/>`** List of orthographic variants for this entry. One variant is marked as the 'canonical' spelling (canonical="1").

A connective can be 'phrasal' or a 'single' item, furthermore, phrasal connectives can be 'cont'inuous or 'discont'inuous

**`<ambiguity/>`** Information on whether this connective also has a non-connective reading (`<non_conn/>`) and whether the connective has different semantic readings (`<sem_ambiguity/>`).

**`<non_conn_reading/>`** Usage example of this item in its non-connective reading.

**`<stts/>`** Currently only contains usage example of this item in its connective reading.

**`<syn/>`** Syntactic and semantic information on this connective. 

 The syntax block is further divided into the following components:

 * **`<cat/>`** Syntactic category.

* **`<ordering/>`** Options for the linear order of arguments arg1 and arg2: *ante*, *post* and/or *insert*

* **`<sem/>`** Information on the coherence relation(s) expressed by the connective. 

**`<finiteClauseArg/>`** Specifies whether (1) or not (0) this connective can connect two finite clauses. 


 Each semantic reading is chosen from the list of PDTB 3.0 relations (see (Webber et al., 2016), LAW workshop). The inventory of senses used here is provided in the file `inventory-pdtb3-senses.txt`.
