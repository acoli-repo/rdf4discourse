import re,os,sys
from urllib.request import urlopen
# write TSV into stdout
# note that we don't create a lemon data set, because this does contain any structured data, but is just a plain word list
# also note that we add PDTB2 senses by plain lookup (1.0) or similarity

# knn: https://www.programmersought.com/article/18164891346/
# knn => 

url="https://raw.githubusercontent.com/synapse-developpement/Discovery/master/data/markers_list.txt"
lang="en"
reference="../../tsv/pdtb2.tsv"

cue2senses={}

with open(reference,"r") as input:
	for line in input:
		if not line.startswith("#"):
			line=line.strip()
			fields=line.split("\t")
			if len(fields)>4:
				for word in [ fields[0], fields[0].lower() ]:
					if(not word in cue2senses):
						cue2senses[word]=[fields[4]]
					elif not fields[4] in cue2senses[word]:
						cue2senses[word].append(fields[4])

with urlopen(url) as input:
	for line in input:
		line=line.decode('utf-8').rstrip()
		line=re.sub(r"\[[^\]]*\]","",line).strip()
		if(len(line)>0):
			cue=line.split(",")[0]
			cue=re.sub("_"," ",cue).strip()
			if not cue in cue2senses:
				print(cue,lang,"_","_","_","0.0",sep="\t")
			else:
				for sense in cue2senses[cue]:
					pdtb3=sense
					pdtb2=re.sub(r"^([^:]*:[^:]*):.*$",r"\1",sense)
					pdtb1=re.sub(r":.*","",sense)
					print(cue,lang,pdtb1,pdtb2,pdtb3,"1.0",sep="\t")

