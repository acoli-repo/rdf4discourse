import traceback,json
import sys,os,re,argparse,gzip
from copy import copy, deepcopy

args=argparse.ArgumentParser(description=\
	"""perform discourse marker induction
		Note that we calculate the symmetric closure of all dictionaries
		Note on evaluation: depth 0: True if discourse marker, depth 1: PDTB top-level, depth 2: (up to) PDTB second-level, dept 3: (up to) PDTB full
		Note that we assume completeness, so elements not found in a dimlex are assumed not to be discourse markers

		The input format can be configured using --cols, with TAB-separated columns such as WORD LANG PDTB1 PDTB2 PDTB3 or WORD LANG RST.
		If multiple levels are provided, all granularities are merged in the output.
		Note that Turtle-type language tags ("tree"@en) are automatically expanded to two TAB-separated columns WORD LANG.
		If the column label PDTB is used, this is expanded into PDTB1 PDTB2 PDTB3. We expect "." as separator symbol (e.g., COMPARISON.Contrast).
		The column label PDTB_INVERSE indicates that all levels are connected by ".", but in reverse order (e.g., Contrast.COMPARISON)

		If a third column is provided infer "Level 0" (whether or not it is a discourse marker) as true.
	""")

# for Python 3.x < 3.8 compliancy
class ExtendAction(argparse.Action):

    def __call__(self, parser, namespace, values, option_string=None):
        items = getattr(namespace, self.dest) or []
        items.extend(values)
        setattr(namespace, self.dest, items)

args.register('action', 'extend', ExtendAction)

# default columns
cols="WORD LANG PDTB1 PDTB2 PDTB3".split()

# parameter define different induction and filtering functions
args.add_argument("--dimlex", type=str, action="extend", nargs="+", help="dimlex files, TSV format (uncompressed), must contain language codes as second column; column structure  word lang pdtb1 pdtb2 pdtb3", required=True)
args.add_argument("--dict", type=str, action="extend", nargs="+", help="bilingual dictionaries, TIAD-TSV format or gzipped TIAD-TSV format, must contain language codes", required=True)
args.add_argument("--tgt", type=str, action="extend", nargs="+", help="target language(s), if these are among DIMLEX arguments, exclude these from training and evaluate against the DIMLEXes",required=True)
args.add_argument("--max_senses", type=int, help="restrict projected results to the top elements, if <=0, test all possible values, defaults to -1", default=-1)
args.add_argument("--no_out", action="store_true", help="if set, do not return inductions, only evaluate")
args.add_argument("--silent", action="store_true", help="if set, return only best evaluation results, entails --no_out")
args.add_argument("--dict_size", type=int, action="extend", nargs="*", help="restrict projection to  language pairs with at least this number of translation pairs, use 0 for using all data (default), if multiple values are provided, all are being tested", default=[])
args.add_argument("--write_output", action="store_true", help="if set, write induced discourse marker inventories to stdout")
args.add_argument("-c", "--cols", type=str, nargs="+", action="extend", help="columns for input, defaults to "+" ".join(cols), default=None)

thresh = args.add_mutually_exclusive_group(required=True)
thresh.add_argument("--threshold", type=float, help="extraction threshold: set to fixed value")
thresh.add_argument("--th_steps", type=int, help="extraction threshold: test this number of equally distributed thresholds from [0:1]")

piv = args.add_mutually_exclusive_group()
piv.add_argument("--min_pivots", type=int, help="minimum number of incoming edges to conduct an induction, must be >=1, defaults to 1, note that this number should not be larger than the number of languages from which to project", default=1)
piv.add_argument("--test_pivots", type=int, help="run comparative evaluation with --min_pivots from 1 to pivots", default=None)

pivlang = args.add_mutually_exclusive_group()
pivlang.add_argument("--min_pivlangs", type=int, help="minimum number of languages required for induction, must not be larger than the number of languages from which to project nor the minimum number of pivot words, defaults to 1", default=1)
pivlang.add_argument("--test_pivlangs", type=int, help="run comparative evaluation with --min_pivlangs from 1 to pivlangs", default=None)


args.add_argument("--prune_senses", action="store_true", help="during projection, limit projected senses to those that cover all incoming edges")

# additional features:
# pivot languages
# project top k senses, only

args=args.parse_args()

# print(cols)
if args.cols!=None:
	cols=args.cols
# print(cols)

if(args.max_senses<=0):
	args.max_senses=-1
if(args.silent):
	args.no_out=True
if(args.dict_size == []):
	args.dict_size=[0]
	
# read dimlexes
warned=False
lang2marker2depth2rels={}
for d in args.dimlex:
	sys.stderr.write("adding dimlex "+d+"\n")
	with open(d,"r") as input:
		for line in input:
			if(not line.startswith("#")):
				line=re.sub(r"(^\\)#.","$1",line)
				line="\t".join(line.split("\"@"))
				line="".join(line.split('"'))
				line=line.rstrip()
				fields=line.split("\t")
				# print(fields)
				# print(cols)
				if(len(fields)>=len(cols)):
					if not "WORD" in cols:
						raise Exception("please provide column label \"WORD\"")
					word=fields[cols.index("WORD")]
					if not "LANG" in cols:
						raise Exception("please provide column label \"LANG\"")
					lang=fields[cols.index("LANG")]

					# for non-PDTB annotations
					pdtb1=fields[2]
					pdtb2=None
					pdtb3=None

					if "PDTB" in cols:
						pdtb=fields[cols.index("PDTB")].split(".")
						pdtb1=pdtb[0]
						pdtb2=".".join(pdtb[0:2])
						pdtb3=".".join(pdtb)
					
					if "PDTB_INVERSE" in cols:
						pdtb=list(reversed(fields[cols.index("PDTB_INVERSE")].split(".")))
						pdtb1=pdtb[0]
						pdtb2=".".join(pdtb[0:2])
						pdtb3=".".join(pdtb)
					
					if "PDTB1" in cols:
						pdtb1 = fields[cols.index("PDTB1")]
					if "PDTB2" in cols:
						pdtb2 = fields[cols.index("PDTB2")]
					if "PDTB2" in cols:
						pdtb2 = fields[cols.index("PDTB3")]

					if pdtb2==None:
						if "RST" in cols:
							pdtb1=fields[cols.index("RST")]
						elif " CCR" in " ".join(cols):
							pdtb1=[]
							for col,field in zip(cols,fields):
								if col.startswith("CCR"):
									pdtb1.append(field)
							pdtb1=" ".join(pdtb1)
						elif not warned:
							sys.stderr.write("warning: did not find a known type of discourse annotation, using "+cols[2]+", instead\n")
							sys.stderr.write("supported labels include PDTB PDTB1 PDTB2 PDTB3 PDTB_INVERSE RST CCR\n")
							sys.stderr.write("note that we annotate one type of schema only, with PDTB preferred over RST over CCR\n")
							sys.stderr.flush()
							warned=True

					if(not lang in lang2marker2depth2rels):
						lang2marker2depth2rels[lang]={ word: [ set([True]), set([pdtb1]), set([pdtb2]), set([pdtb3]) ] }
					elif(not word in lang2marker2depth2rels[lang]):
						lang2marker2depth2rels[lang][word] = [ set([True]), set([pdtb1]), set([pdtb2]), set([pdtb3]) ]
					else:
						lang2marker2depth2rels[lang][word][1].add(pdtb1)
						lang2marker2depth2rels[lang][word][2].add(pdtb2)
						lang2marker2depth2rels[lang][word][3].add(pdtb3)
					for l in lang2marker2depth2rels:
						sys.stderr.write(" "+l+": "+str(len(lang2marker2depth2rels[l])))
					sys.stderr.write("\r")
					sys.stderr.flush()
	sys.stderr.write("\n")

# read dictionaries
lang2src2lang2tgts={}	# dictionary
lang2lang2dicts={} 	# for calculating induction paths
for d in args.dict:
	sys.stderr.write("adding dict "+d+"\n")
	input=None
	try:
		if d.endswith("gz") or d.endswith("gzip"):
			input=gzip.open(d,"r")
		else:
			input=open(d,"r")
		for line in input:
			if(type(line)==bytes):
				line=line.decode("utf-8")
			if(not line.startswith("#")):
				line=re.sub(r"(^\\)#.","$1",line)
				line=line.rstrip()
				fields=line.split("\t")
				if(len(fields)>4):
					src=fields[0]
					slang=""
					if("@" in src):
						slang=re.sub(r".*@","",src)
					src=re.sub("@.*","",src)
					src=re.sub(r"^[']+(.*)[']+$",r"\1",src)
					src=re.sub(r"^[\"]+(.*)[\"]+$",r"\1",src)
					
					tgt=fields[-1]					
					tlang=""
					if("@" in tgt):
						tlang=re.sub(r".*@","",tgt)
					tgt=re.sub("@.*","",tgt)
					tgt=re.sub(r"^[']+(.*)[']+$",r"\1",tgt)
					tgt=re.sub(r"^[\"]+(.*)[\"]+$",r"\1",tgt)
					
					if(not re.match(r"^[a-z][a-z][a-z]?$",slang)):
						sys.stderr.write("  warning: invalid source language \""+slang+"\"\n")
					elif(not re.match(r"^[a-z][a-z][a-z]?$",tlang)):
						sys.stderr.write("  warning: invalid target language \""+tlang+"\"\n")
					else: # valid language tag
						for src, slang, tgt, tlang in [ (src, slang, tgt, tlang) , (tgt, tlang, src, slang)] :
							if(not slang in lang2src2lang2tgts):
								lang2src2lang2tgts[slang]= { src : { tlang : set([tgt]) } }
							elif(not src in lang2src2lang2tgts[slang]):
								lang2src2lang2tgts[slang][src] = { tlang : set([tgt]) }
							elif(not tlang in lang2src2lang2tgts[slang][src]):
								lang2src2lang2tgts[slang][src][tlang] = set([tgt])
							else:
								lang2src2lang2tgts[slang][src][tlang].add(tgt)
							if not slang in lang2lang2dicts:
								lang2lang2dicts[slang]={tlang : set([d])}
							if not tlang in lang2lang2dicts[slang]:
								lang2lang2dicts[slang][tlang]=set([d])
							if not d in lang2lang2dicts[slang][tlang]:
								lang2lang2dicts[slang][tlang].add(d)
							if not tlang in lang2lang2dicts:
								lang2lang2dicts[tlang]={slang : set(["^"+d])}
							if not slang in lang2lang2dicts[tlang]:
								lang2lang2dicts[tlang][slang]=set(["^"+d])
							if not d in lang2lang2dicts[tlang][slang]:
								lang2lang2dicts[tlang][slang].add("^"+d)

						for l in lang2src2lang2tgts:
							sys.stderr.write(" "+l+":"+str(len(lang2src2lang2tgts[l])))
						sys.stderr.write("\r")
						sys.stderr.flush()
		input.close()
	except :
		pass
	sys.stderr.write("\n")



lang2lang2freq={}	# number of translation pairs
if len(args.dict_size)>0:
	for slang in lang2src2lang2tgts:
		for src in lang2src2lang2tgts[slang]:
			for tlang in lang2src2lang2tgts[slang][src]:
				if not slang in lang2lang2freq:
					lang2lang2freq[slang] = { tlang: len(lang2src2lang2tgts[slang][src][tlang]) }
				elif not tlang in lang2lang2freq[slang]:
					lang2lang2freq[slang][tlang] = len(lang2src2lang2tgts[slang][src][tlang])
				else:
					lang2lang2freq[slang][tlang]+= len(lang2src2lang2tgts[slang][src][tlang])
else:
	args.dict_size=[0]
	
for tlang in args.tgt:
		
	for dict_size in args.dict_size:
	
		sys.stderr.write("initialize induction for \""+tlang+"\" with dict_size="+str(dict_size)+"\n");
		
		if dict_size > 0 :
			for lang1 in sorted(lang2lang2freq.keys()):
				for lang2 in sorted(lang2lang2freq[lang1].keys()):
					if(lang2lang2freq[lang1][lang2]>=dict_size):
						print(lang1,"--", lang2)
			print()
		
		if not tlang in lang2src2lang2tgts:
			sys.stderr.write("error: target language \""+tlang+"\" not in dictionaries, skipping\n")
			sys.stderr.flush()
		else:
			lang2marker2depth2rel2score={}
			classified=0
			for slang in lang2marker2depth2rels:
				if(not slang in lang2src2lang2tgts):
					sys.stderr.write("warning: excluding source language \""+slang+"\": no source DICT found\n")				
				else:
					if slang!=tlang:
						if not slang in lang2marker2depth2rel2score:
							lang2marker2depth2rel2score[slang] = { slang: {} }
						for marker in lang2marker2depth2rels[slang]:
							if not marker in lang2marker2depth2rel2score[slang]:
								lang2marker2depth2rel2score[slang][marker] = {}
							for depth in range(len(lang2marker2depth2rels[slang][marker])):
								if not depth in lang2marker2depth2rel2score[slang][marker]:
									lang2marker2depth2rel2score[slang][marker][depth]={}
								for rel in lang2marker2depth2rels[slang][marker][depth]:
									lang2marker2depth2rel2score[slang][marker][depth][rel]=1.0/float(len(lang2marker2depth2rels[slang][marker][depth]))
								classified+=1
								sys.stderr.write(" "+str(classified)+" forms\r")
								sys.stderr.flush()
						for word in lang2src2lang2tgts[slang]:
							if not word in lang2marker2depth2rel2score[slang]:
								lang2marker2depth2rel2score[slang][word] = { 0: {True : 0.0}, 1: {}, 2:{}, 3:{}}
								classified+=1
								sys.stderr.write(" "+str(classified)+" forms\r")
								sys.stderr.flush()
			sys.stderr.write("\n")
			
			lang2marker2depth2rel2score_gold=lang2marker2depth2rel2score
			
			# induce for different pivot configurations
			min_pivots=[]
			if(args.test_pivots):
				min_pivots=list(range(1,args.test_pivots+1))
			else:
				min_pivots=[args.min_pivots]
				
			min_pivlangs=[]
			if(args.test_pivlangs):
				min_pivlangs=list(range(1,args.test_pivlangs+1))
			else:
				min_pivlangs=[args.min_pivlangs]

			for min_pivlang in min_pivlangs:
				
				# check whether pivlang is valid
				print("induction with min_pivlang="+str(min_pivlang))
				lang2path={}
				for lang in lang2marker2depth2rel2score_gold:
					if(lang!=tlang):
						lang2path[lang]=lang
				if(len(lang2path)>0):
					additions=1
					while(additions>0):
						additions=0
						for lang in lang2lang2dicts:
							if(not lang in lang2path):
								src=sorted(set(lang2path) & set(lang2lang2dicts[lang]))
								if len(src)>=min_pivlang:
									lang2path[lang]=lang+" <= ("+",".join([lang2path[s] for s in src])+")"
									additions+=1
				if(not tlang in lang2path):
					print("no induction path from ("+",".join(sorted(lang2marker2depth2rel2score_gold.keys()))+") to "+tlang+" with min_pivlang="+str(min_pivlang))
				else:
					print("induction path: "+lang2path[tlang])
				
					# induction
					for min_pivot in min_pivots:
						if(min_pivot>=min_pivlang or not min_pivlang in min_pivots):
							lang2marker2depth2rel2score=deepcopy(lang2marker2depth2rel2score_gold)
							sys.stderr.write("induce with min_pivot=\""+str(min_pivot)+"\"\n")
							additions=-1
							while(additions!=0):
								if(additions>0):
									classified=classified+additions
								additions=0
								for lang in lang2src2lang2tgts:
									if(lang == tlang or not lang in lang2marker2depth2rels):
										#print(lang)
										try:
											for word in lang2src2lang2tgts[lang]:
												if(not lang in lang2marker2depth2rel2score or 
													not word in lang2marker2depth2rel2score[lang]):
													mytlangs = sorted(set(lang2src2lang2tgts[lang][word].keys()) & set(lang2marker2depth2rel2score.keys()))
													mytlangs= [ mytlang for mytlang in mytlangs if lang2lang2freq[lang][mytlang]>=dict_size ]
													if(len(mytlangs)>0):
														tgts=set([])
														tgtlangs=set([])
														depth2rel2tgts={}
														for mytlang in mytlangs:
															#print(word,lang,"via",mytlang)
															for tgt in lang2src2lang2tgts[lang][word][mytlang]:
																if(tgt in lang2marker2depth2rel2score[mytlang]):
																	found=True
																	tgts.add(tgt+"@"+mytlang)
																	tgtlangs.add(mytlang)
																	for depth in lang2marker2depth2rel2score[mytlang][tgt]:
																		for rel in lang2marker2depth2rel2score[mytlang][tgt][depth]:
																			if(not lang in lang2marker2depth2rel2score):
																				lang2marker2depth2rel2score[lang]={}
																			if(not word in lang2marker2depth2rel2score[lang]):
																				lang2marker2depth2rel2score[lang][word]={}
																			if(not depth in lang2marker2depth2rel2score[lang][word]):
																				lang2marker2depth2rel2score[lang][word][depth]={}
																			if(not rel in lang2marker2depth2rel2score[lang][word][depth]):
																				lang2marker2depth2rel2score[lang][word][depth][rel]=0.0
																			lang2marker2depth2rel2score[lang][word][depth][rel]+=lang2marker2depth2rel2score[mytlang][tgt][depth][rel]
																			#print(lang,word,depth,rel,lang2marker2depth2rel2score[lang][word][depth][rel])
																			
																			# for pruning
																			if(args.prune_senses):
																				if not depth in depth2rel2tgts:
																					depth2rel2tgts[depth]={ rel: set([tgt+"@"+mytlang])}
																				elif not rel in depth2rel2tgts[depth]:
																					depth2rel2tgts[depth][rel] = set([tgt+"@"+mytlang])
																				else:
																					depth2rel2tgts[depth][rel].add(tgt+"@"+mytlang)
														if len(tgts)>0 and lang in lang2marker2depth2rel2score:
															if(word in lang2marker2depth2rel2score[lang]):
																if len(tgts)>=min_pivot and len(tgtlangs)>=min_pivlang:
																	for depth in lang2marker2depth2rel2score[lang][word]:
																		if(not args.prune_senses):
																			for rel in lang2marker2depth2rel2score[lang][word][depth]:
																				lang2marker2depth2rel2score[lang][word][depth][rel]=lang2marker2depth2rel2score[lang][word][depth][rel]/float(len(tgts))
																		else:	# prune senses
																			rel2score={}
																			total=0
																			unexplained=deepcopy(tgts)
																			for rel,score in sorted(lang2marker2depth2rel2score[lang][word][depth].items(), key=lambda item: item[1]):
																				if(len(set(depth2rel2tgts[depth][rel]) & unexplained)>0):
																					rel2score[rel]=len(depth2rel2tgts[depth][rel])/float(len(tgts))
																					total+=rel2score[rel]
																					unexplained = set([ u for u in unexplained if not u in depth2rel2tgts[depth][rel] ])
																			#for rel in rel2score:
																			#	lang2marker2depth2rel2score[lang][word][depth][rel]=rel2score[rel]/total
																			# note that non-scores have True=0.0, so normalizing scores will be misleading
																																					
																	#print(lang,word)
																	additions+=1
																	sys.stderr.write("induce: "+str(classified+additions)+"\r")
																	sys.stderr.flush()
																else:
																	lang2marker2depth2rel2score[lang].pop(word)
										except Exception as e:
											sys.stderr.write("error:"+str(e)+"\n")
											sys.stderr.write(str(traceback.format_exc())+"\n")
											sys.stderr.flush()
											pass
														
															
								sys.stderr.write("\n")
								
							sys.stderr.write("\n")
							sys.stderr.flush()

							
							print("induce\nfrom",end=" ")
							for slang in lang2marker2depth2rels:
								if not slang==tlang:
									print(slang,end=" ")
							print("\nvia "," ".join(args.dict))
							print("to",tlang)


							# output
							if args.write_output:
									if tlang in lang2marker2depth2rel2score:
										score_marker=[ (feats[0][True],marker) for marker,feats in lang2marker2depth2rel2score[tlang].items() if 0 in feats and True in feats[0]]# and feats[0][True]>0 ]
										for score,marker in reversed(sorted(score_marker)):
											rel2score={}
											for depth in reversed(sorted(lang2marker2depth2rel2score[tlang][marker])):
												if depth>0:
													rel2score.update(lang2marker2depth2rel2score[tlang][marker][depth])
											for rscore,rel in reversed(sorted([ (s,r) for r,s in rel2score.items() if s > 0 and isinstance(r,str)])):
												print(f"\"{marker}\"@{tlang}\t{score}\t{rel}\t{rscore}")

										# for marker in lang2marker2depth2rel2score
										# json.dump(lang2marker2depth2rel2score[tlang],sys.stdout)
										print()
									print()


							# eval

							# keys: p,r,f,f_oov (metric)
							# keys: 0..3  (depth)
							# keys: threshold, max_senses, p, r, r_oov
							metric2depth2best_config={}
							for metric in ["p","r","f","f_oov","r_oov"]:
								metric2depth2best_config[metric]={}
								for depth in range(4):
									metric2depth2best_config[metric][depth] = { "threshold" : -1, "max_senses" : -1, "p": -1, "r" : -1 , "f": -1, "f_oov": -1, "r_oov": -1 }
								
							# we decrease the number of senses in every iteration, initialize with an ad hoc value
							max_senses=args.max_senses
							if tlang in lang2marker2depth2rels:
								while(max_senses!=0 and max_senses>=args.max_senses):

									thresholds=[]
									tp=[]
									fn=[]
									fp=[]
									fn_OOV=[]
									
									if(not args.th_steps):
										thresholds=[args.threshold]
										tp.append([0,0,0,0])
										fn.append([0,0,0,0])			
										fp.append([0,0,0,0])
									else:			
										steps=args.th_steps
										for threshold in range(steps+1):
											thresholds.append(float(threshold)/float(steps))
											tp.append([0,0,0,0])
											fn.append([0,0,0,0])			
											fp.append([0,0,0,0])
										# note that we count individual *senses*
									
									if(tlang in lang2marker2depth2rel2score):
										for marker in sorted(lang2marker2depth2rel2score[tlang]):
											for p,t in enumerate(thresholds):
												if(lang2marker2depth2rel2score[tlang][marker][0][True]<=t):
													if(marker in lang2marker2depth2rels[tlang]): # fn
														for depth in range(4):
															fn[p][depth]+=len(lang2marker2depth2rels[tlang][marker][depth])
												else: # predict as discourse marker, then check every line individually
													for depth in range(4):
														if(depth in lang2marker2depth2rel2score[tlang][marker]):
															for rel in lang2marker2depth2rel2score[tlang][marker][depth]:
																if not marker in lang2marker2depth2rels[tlang] or not rel in lang2marker2depth2rels[tlang][marker][depth]:
																	fp[p][depth]+=1
																else:
																	tp[p][depth]+=1
											if(not args.no_out):
												if lang2marker2depth2rel2score[tlang][marker][0][True]>0.0:
													for depth in sorted(lang2marker2depth2rel2score[tlang][marker]):
														for rel in sorted(lang2marker2depth2rel2score[tlang][marker][depth]):
																print(marker+"\t"+str(max_senses)+"\t"+str(depth)+"\t"+str(rel)+"\t"+str(lang2marker2depth2rel2score[tlang][marker][depth][rel]))
													print()

									fn_oov=deepcopy(fn)
									for marker in lang2marker2depth2rels[tlang]:
										if not tlang in lang2marker2depth2rel2score or not marker in lang2marker2depth2rel2score[tlang]:
											for depth in range(4):
												for t in range(len(thresholds)):
													fn_oov[t][depth]+=1
												
									for depth in range(4):
										if(not args.silent):
											print("min_pivlangs", "min_pivots","threshold","max_senses","depth","tp","fp","fn","fn_OOV", "p","r","f","p_OOV","r_OOV","f_OOV")
										for t in range(len(thresholds)):
										
											# without oov
											p = float(tp[t][depth]+fp[t][depth])
											r = float(tp[t][depth]+fn[t][depth])
											if p>0.0:
												p = tp[t][depth]/p
											if r >0.0:
												r =tp[t][depth]/r
											f=0.0
											if(r+p>0):
												f=2.0*p*r/float(r+p)
												
											# with oov					
											r_oov = float(tp[t][depth]+fn_oov[t][depth])
											if r_oov >0.0:
												r_oov =tp[t][depth]/r_oov
											f_oov=0.0
											if(r_oov+p>0):
												f_oov=2.0*p*r_oov/float(r_oov+p)
											
											# update best metrics
											for key,val in [ ("p",p), ("r",r), ("f",f), ("r_oov",r_oov), ("f_oov", f_oov) ]:
												if val>=metric2depth2best_config[key][depth][key]:
													metric2depth2best_config[key][depth]= { 
														"threshold" : thresholds[t], 
														"max_senses" : max_senses, 
														"tp":tp[t][depth],
														"p": p, 
														"r" : r , 
														"f": f, 
														"r_oov": r_oov,
														"f_oov": f_oov } 
											
											if(not args.silent):
												print(
													min_pivlang,
													min_pivot, 
													thresholds[t],max_senses, depth,tp[t][depth],fp[t][depth], fn[t][depth], fn_oov[t][depth],
													p,r,f,
													p,r_oov,f_oov)
										if(not args.silent):
											print()

									if(not args.silent):
										print()

									# reduce maximum number of senses per prediction to the top ones
									if max_senses==-1:
										for marker in lang2marker2depth2rels[tlang]:
											for depth in range(4):
												if(len(lang2marker2depth2rels[tlang][marker][depth])>max_senses):
													max_senses=len(lang2marker2depth2rels[tlang][marker][depth])
									
									max_senses-=1
										
									# limit the number of predicated senses to max_senses
									if tlang in lang2marker2depth2rel2score:
										for marker in copy(lang2marker2depth2rel2score[tlang]):
											for depth in range(4):
												if	len(lang2marker2depth2rel2score[tlang][marker])>depth and	\
													len(lang2marker2depth2rel2score[tlang][marker][depth])>max_senses:
													vals= sorted(lang2marker2depth2rel2score[tlang][marker][depth].values())
													vals.reverse()
													val=vals[max_senses-1]
													
													if max_senses>1 and vals[0]!=val:	# if indistinctive, reduce to last higher one
														i=max_senses-1
														while i > 1 and vals[i-1]==val:
															i-=1
														if i >0:
															val=vals[i-1]
														
													lang2marker2depth2rel2score[tlang][marker][depth]=\
														{ k:v for (k,v) in lang2marker2depth2rel2score[tlang][marker][depth].items() if v>=val }
													
								# spell out best results
								print()
								print("best config:")
								print("min_pivlangs", "min_pivots","threshold","max_senses","depth","tp","p","r","f","p","r_oov","f_oov", sep="\t")
								for depth in range(4):
									keys=["p","r","f","r_oov","f_oov"]
									
									for key in keys:
										if(type(metric2depth2best_config[key][depth])==dict):
										
											# format results
											length=4
											for k,v in metric2depth2best_config[key][depth].items():
												if(type(v)==float):
													v=("{:0."+str(length)+"f}").format(v)
													if(k==key):
														v=v+"*"
												else:
													v=str(v)
												
												while(len(v)<length+2+1):
													v=v+" "
												
												metric2depth2best_config[key][depth][k]=v
																	
											# print
											print(min_pivlang, min_pivot,
												  metric2depth2best_config[key][depth]["threshold"],
												  metric2depth2best_config[key][depth]["max_senses"],
												  depth,
												  metric2depth2best_config[key][depth]["tp"],
												  metric2depth2best_config[key][depth]["p"],
												  metric2depth2best_config[key][depth]["r"],
												  metric2depth2best_config[key][depth]["f"],
												  metric2depth2best_config[key][depth]["p"],
												  metric2depth2best_config[key][depth]["r_oov"],
												  metric2depth2best_config[key][depth]["f_oov"],sep="\t")
									print()
								print()
							
