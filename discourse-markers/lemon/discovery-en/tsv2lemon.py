import sys,re,os,traceback
from urllib.parse import quote as escape

# operates on the output of infer-senses.py

tsv_file="Inferred.tsv"
basename="https://raw.githubusercontent.com/synapse-developpement/Discovery/master/data/markers_list.txt"
lang="en"

print("\
PREFIX dimlex: <https://github.com/discourse-lab/dimlex/blob/master/DimLex.dtd#>\n\
PREFIX pdtb3: <https://raw.githubusercontent.com/discourse-lab/dimlex/master/inventory-pdtb3-senses.txt#> \n\
PREFIX ontolex: <http://www.w3.org/ns/lemon/ontolex#>\n\
PREFIX synsem: <http://www.w3.org/ns/lemon/synsem#>\n\
PREFIX decomp: <http://www.w3.org/ns/lemon/decomp#>\n\
PREFIX vartrans: <http://www.w3.org/ns/lemon/vartrans#>\n\
PREFIX lime: <http://www.w3.org/ns/lemon/lime#>\n\
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n\
PREFIX rdf: <http://www.w3.org/2000/01/rdf-schema#>\n\
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>\n\
PREFIX xml: <http://www.w3.org/TR/xml/#>\n\
PREFIX : <"+basename+"#>\n")

with open(tsv_file,"r") as input:
	lastcue=None
	for line in input:
		if not line.startswith("#"):
			line=line.strip()
			fields=line.split("\t")
			if len(fields)> 4:
				cue=fields[0]
				lang=fields[1]
				pdtb1=fields[2]
				pdtb2=fields[3]
				pdtb3=fields[4]
				score=1.0
				comment=None
				if len(fields)>5:
					score=float(fields[5])
				if len(fields)>6:
					comment=re.sub(r"^[^#]*#","",fields[6]).strip()
				try:
					escaped=escape(cue)
					if(lastcue!=cue):
						if lastcue!=None:
							print(" ] ] ] .\n")
						print(":"+escaped)
						print("\t a ontolex:LexicalEntry ;")
						print("\t ontolex:canonicalForm [") 
						if(" " in cue):
							print("\t\t dimlex:type \"phrasal\";")					
						print("\t\t ontolex:writtenRep \""+cue+"\"@"+lang+"];")
						print("\t dimlex:syn [")
						print("\t\t dimlex:sem [")
						print("\t\t\t dimlex:pdtb2_relation\n\t\t\t\t [",end="")
					if lastcue==cue:
						print("],\n\t\t\t\t [",end="") 
					# note that we have to make up dimlex:confidence, there is no vocabulary element in OntoLex we could directly use
					if comment!=None:
						print("rdfs:comment \""+comment+"\"; ",end="")		
					print("dimlex:sense \""+pdtb3+"\"; "+
						  "dimlex:confidence \""+str(score)+"\"; "+
						  "a ontolex:LexicalSense; ontolex:isSenseOf :"+escaped,end="")
					lastcue=cue
				except:
					traceback.print_exc()
					print("weiter")
	print(" ] ] ] .\n")