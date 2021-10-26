# linked OntoLex discourse marker inventories

for every converted OntoLex discourse marker inventory
- load the OLiA PDTB ontology (http://purl.org/olia/discourse/discourse.PDTB.owl) into the local graph
- match dimlex:sense against PDTB labels
- create ontolex:reference between OntoLex sense and PDTB concept
- return OntoLex propertys or classes, prune everything else
- manually added machine-readable license information 
- attribution information added
- linked data release under http://purl.org/acoli/dimlex/*

Note that this is currently hosted by GitHub, so, no support for content negotation or redirection. Hence, the file suffix had to be included in the URIs.

## history

- 2010-05-26 PDTB.owl created
- 2012-02-10 PDTB.owl published as experimental model in the OLiA repository
- 2014-03-21 linked with olia_discourse.owl, renamed to discourse.PDTB.owl
- 2020-02-04 linking with discourse marker lexicons (via URIs)
- 2020-02-07 linking with discourse marker lexicons (via labels and altLabels)
- 2020-02-07 manual enrichment with licensing information, attribution; manual correction of Portuguese TED dataset.
- 2020-02-07 resolvable URIs in the namespace http://purl.org/acoli/dimlex
- 2021-02-04 linking revised, models:

    | language | resource family | relations | sense linking |
    |---------|---------|---------|---------|
    | Bangla  | DimLex  | PDTB    | [pdtb](http://purl.org/olia/discourse/discourse.PDTB.owl) |
    | Catalan | DiscMar | DiscMar | [pdtb](http://purl.org/olia/discourse/discourse.PDTB.owl) |
    | Czech   | CzedLex | CzedLex | [pdtb](http://purl.org/olia/discourse/discourse.PDTB.owl) |
    | German  | DimLex  | PDTB    | [pdtb](http://purl.org/olia/discourse/discourse.PDTB.owl) |
    | German  | TED-MDB | PDTB    | [pdtb](http://purl.org/olia/discourse/discourse.PDTB.owl) |
    | English | DiscMar | DiscMar | [pdtb](http://purl.org/olia/discourse/discourse.PDTB.owl) |
    | English | PDTB2   | PDTB    | [pdtb](http://purl.org/olia/discourse/discourse.PDTB.owl) |
    | English | TED-MDB | PDTB    | [pdtb](http://purl.org/olia/discourse/discourse.PDTB.owl) |
    | Spanish | DiscMar | DiscMar |  [pdtb](http://purl.org/olia/discourse/discourse.PDTB.owl) |
    | French  | LexConn | SDRT | [pdtb](http://purl.org/olia/discourse/discourse.PDTB.owl) |
    | Italian | LICO    | PDTB | [pdtb](http://purl.org/olia/discourse/discourse.PDTB.owl) |
    | Lithuanian | TED-MDB | PDTB | [pdtb](http://purl.org/olia/discourse/discourse.PDTB.owl) |
    | Dutch | DimLex | PDTB | [pdtb](http://purl.org/olia/discourse/discourse.PDTB.owl) |
    | Polish | TED-MDB | PDTB | [pdtb](http://purl.org/olia/discourse/discourse.PDTB.owl) |
    | Portuguese | DimLex | PDTB | [pdtb](http://purl.org/olia/discourse/discourse.PDTB.owl) |
    | Russian | TED-MDB | PDTB | [pdtb](http://purl.org/olia/discourse/discourse.PDTB.owl) |
    | Turkish | TED-MDB | PDTB | [pdtb](http://purl.org/olia/discourse/discourse.PDTB.owl) |
    
 - 2021-05-12 addition

    | language | resource family | relations | sense linking |
    |---------|---------|---------|---------|
    | English | Discovery   | PDTB (inferred)    | [pdtb](http://purl.org/olia/discourse/discourse.PDTB.owl) |
 
 - 2021-10-26 additions

    | language | resource family | relations | sense linking |
    |---------|---------|---------|---------|
    | Chinese | CDTB   | CDTB    | [cdtb](http://purl.org/olia/discourse/discourse.CDTB.owl) (=> [pdtb](http://purl.org/olia/discourse/discourse.PDTB.owl)) |
    | Chinese | C-TED  | PDTB | [pdtb](http://purl.org/olia/discourse/discourse.PDTB.owl) |

Christian Chiarcos
