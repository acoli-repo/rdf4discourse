# cf. https://www.programmersought.com/article/18164891346/
import torch,re,math,sys
import torchtext.vocab as vocab

def knn(W, x, k):
		 # 1e-9 added is for numerical stability
	cos = torch.matmul(W, x.view((-1,))) / (
		(torch.sum(W * W, dim=1) + 1e-9).sqrt() * torch.sum(x * x).sqrt())
	_, topk = torch.topk(cos, k=k)
	topk = topk.cpu().numpy()
	return topk, [cos[i].item() for i in topk]
	
# direct lookup, but implements fallbacks
def get_vector(word, embed):
	for match in [ word, word.lower(), re.sub(r"[^a-zA-Z0-9 ]","",word), re.sub(r"[^a-zA-Z0-9 ]","",word).lower() ]: 
		if match in embed.stoi:
			return embed.vectors[embed.stoi[match]]
	return None
	
def get_similarity(x1, x2, embed):
	e1=[]
	e2=[]
	for w in x1.split():
		e1.append(get_vector(w,embed))
		if e1[-1]==None:
			e1=e1[:-1]
	for w in x2.split():
		e2.append(get_vector(w,embed))
		if e2[-1]==None:
			e2=e2[:-1]
	
	if(len(e1)==0): return None
	if(len(e2)==0): return None
	
	a=e1[0]/len(e1)
	for i in range(1,len(e1)):
		a+=e1[i]/len(e1)
	b=e2[0]/len(e2)
	for i in range(2,len(e2)):
		b+=e2[i]/len(e2)
		
	
	# cos
	ab=0.0
	a2=0.0
	b2=0.0
	for i in range(len(a)):
		ab+=a[i]*b[i]
		a2+=a[i]*a[i]
		b2+=b[i]*b[i]
	b2=math.sqrt(b2)
	a2=math.sqrt(a2)
	return float(ab / (a2*b2))
		

def get_similar_tokens(query_token, k, embed):
	topk, cos = knn(embed.vectors,
					embed.vectors[embed.stoi[query_token]], k+1)
	for i, c in zip(topk[1:], cos[1:]): # Remove input word
		print('cosine sim=%.3f: %s' % (c, (embed.itos[i])))
		#print(get_similarity(query_token,embed.itos[i],embed))

		
cache_dir = "../embeddings"
# glove = vocab.pretrained_aliases["glove.840B.300d"](cache=cache_dir)
glove = vocab.pretrained_aliases["glove.6B.50d"](cache=cache_dir)
#glove = vocab.GloVe(name='840B', dim=300, cache=cache_dir)

# get_similar_tokens('chip', 3, glove)

cue2senses={}
lang="en"
unclassified=[]
try:
	sys.stderr.write("reading DimLex TSV")
	sys.stderr.flush()
	with open(sys.argv[1],"r") as input:
		sys.stderr.write(" from "+sys.argv[1]+"\n")
		sys.stderr.flush()
		for line in input:
			if not line.startswith("#"):
				line=line.strip()
				fields=line.split("\t")
				cue=fields[0]
				lang=fields[1]
				sense="_"
				if(len(fields)>4):					
					sense=fields[4]
				if sense == "_":
					unclassified.append(cue)
				if sense != "_":
					if not cue in cue2senses:
						cue2senses[cue]=[sense]
					elif not sense in cue2senses[cue]:
						cue2senses[cue].append(sense)
except:
	# dummy entries
	cue2senses={ "while" : ["temporal","adversative"], "when" : ["temporal"], "but" : ["adversative"] }
					
for x1 in sorted(set(list(cue2senses.keys()) + unclassified)):
	try:
		if x1 in cue2senses:
			for sense in cue2senses[x1]:
				pdtb3=sense
				pdtb2=re.sub(r"^([^:]*:[^:]*):.*$",r"\1",sense)
				pdtb1=re.sub(r":.*","",sense)
				print(x1,lang,pdtb1,pdtb2,pdtb3,"1.0",sep="\t")
		else:
			cue2score={}
			#print(cue2senses)
			for cue in cue2senses:
#				try:
				cue2score[cue]=get_similarity(x1,cue,glove)
				# except:
					# pass
			cues=sorted(cue2score.items(), key=lambda x: x[1],reverse=True)
			#print(cues)
			sense2score={}
			top_senses=[]
			supporters=[]
			for cue,score in cues:
				if cue in cue2senses:
					for sense in cue2senses[cue]:
						if not sense in sense2score:
							sense2score[sense]=cue2score[cue]/len(cue2senses[cue])
						else:
							sense2score[sense]+=cue2score[cue]/len(cue2senses[cue])
					top_senses=[]
					for s in sense2score:
						if len(top_senses)==0 or sense2score[s]>sense2score[top_senses[0]]:
							top_senses=[s]
						elif sense2score[s]==sense2score[top_senses[0]]:
							top_senses.append(s)
					supporters.append(cue)
					if(len(top_senses)==1):
						tmp=[]
						for s in supporters:
							if top_senses[0] in cue2senses[s]:
								tmp.append(s)
						supporters=tmp
						break

			score=cue2score[supporters[0]]
			for sense in top_senses:
				pdtb3=sense
				pdtb2=re.sub(r"^([^:]*:[^:]*):.*$",r"\1",sense)
				pdtb1=re.sub(r":.*","",sense)
				print(x1,lang,pdtb1,pdtb2,pdtb3,score,"# inferred from "+", ".join(supporters), sep="\t")
				
#			print(cues)
						
	except:
		pass
	