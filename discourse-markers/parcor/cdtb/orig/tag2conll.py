import sys,io,re,traceback
from pprint import pprint

# args are files

for file in sys.argv[1:]:
	with open(file,"r",errors="replace") as input:
		print(file)
		for line in input:
			line=line.strip()
			if line.startswith("</s>"):
				print("\n")
			elif line.startswith("<W"):
				id=0
				try:
					id=int(re.sub(r'.* id="([0-9]+)".*',r'\1',line))
				except ValueError:
					print("# invalid id annotation")
					#traceback.print_exc()
					print()
					break
				word=re.sub(r".*>([^<]*)<.*",r"\1",line)
				deps=re.sub(r'.* in="([^"]*)".*',r'\1',line)
				pos=re.sub(r'.* msd="([^"]+)".*',r"\1",line)
				print(id,word,pos,deps, sep="\t",end="\t")
				keys=["syntax","discourse","discourse-cue"]	# we ignore "technical","secondary","other","coref"
				anno={}
				for dep in deps.split("|"):
					if dep!="":
						try:
							head=int(re.sub(r":.*","",dep))
							dep=re.sub(r".*:","",dep)
							key=None
							if dep.startswith("[") or dep.startswith("&lt;"):
								key="secondary"
							elif re.sub(r"[^a-z]","",dep) in ["relr","appr","xpl","expl","agent","numm","numa","modp","nobj","mod","pnct","pobj","vobj","dobj","subj","conj","voc","title","coord","predo","possd", "preds","iobj","neg","part","possr", "correl","cons","appa"] or "obj" in dep or "name" in dep:
								key="syntax"
							elif "ref" in dep or "assoc" in dep:
								key="coref"
							elif re.sub(r"[^A-Z]","",dep) in ["ATTRIBUTION","BACKGROUND","CAUSE","COMMENT","COMPARISON","CONDITION","CONTR","CONTRAST","ELABORATION","ENABLEMENT","EVALUATION","EXPLANATION","JOINT","MANNER","MEANS","SUMMARY","TEMPORAL"]:
								key="discourse"
							elif "conc" in dep or "discmark" in dep or "contr" in dep or "cause" in dep or "add" in dep or "xtop" in dep or "time" in dep:
								key="discourse-cue"
							elif re.match(r"^[^a-zA-Z]*$",dep):
								key="technical"
							else:
								key="other" # unclear
#								print("\t","unclear",head,dep)
							if key:
								if not key in anno:
									anno[key]={dep : [head]}
								elif not dep in anno[key]:
									anno[key][dep]=[head]
								elif not head in anno[key][dep]:
									anno[key][dep].append(head)
						except:
							traceback.print_exc()
							sys.stderr.write("while processing \""+dep+"\"\n")
							sys.stderr.flush()
				for key in keys:
					if key=="coref":
						# can contain multiple values, these are thus aggregated
						if not key in anno:
							print("_",end="\t")
						else:
							deps=""
							for dep in anno[key]:
								for val in anno[key][dep]:
									val=str(id+int(val))
									deps=deps+val+":"+dep
							deps=re.sub(r"[|]$","",deps)
							print(deps,sep="\t",end="\t")
					else:
						if not key in anno:
							print("_","_",sep="\t",end="\t")
						else:
							val=list(anno[key].values())[0][0]
							val=str(id+int(val))
							dep=list(anno[key].keys())[0]
							print(val,dep,sep="\t",end="\t")
							if(len(anno[key])>1 or len(list(anno[key].values())[0])>1):
								sys.stderr.write("warning: multiple values for "+key+" in "+str(anno[key])+"\n")
								sys.stderr.flush()
				print()
					
			elif line.startswith("<"):
				print("#",line)
			else:
				print("# warning, unprocessable:",line)
