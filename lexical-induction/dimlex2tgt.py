import os,sys,re, argparse, gzip, copy

aggregators=["all", "avg", "max", "median" ] 

args=argparse.ArgumentParser(description="extrapolate DimLexes, note that we lowercase DimLexes")
args.add_argument("--dimlex", "-dimlex", action="extend", type=str, nargs="+", help="DimLex dictionaries, expect columns WORD LANG PDTB1 PDTB2 PDTB3")
args.add_argument("--dicts", action="extend", type=str, nargs="+", help="bilingual dictionaries, require TIAD TSV files with Turtle language tag at words")
args.add_argument("--symm", "-sym", action="store_true", help="symmetric closure over dictionaries")
args.add_argument("--lang", "-l",type=str, help="target language (BCP47 code), if omitted, then extrapolated from --gold dictionary", default=None)
args.add_argument("--rel", "-r", type=int, default=0, help="column that contains the relations, this is either 0 or a value from 1 (is a discourse marker) over 2 (= col PDTB1) to 4 (= col PDTB3); if 0, iterate from 1 to 4")
args.add_argument("--gold", "-g", type=str, nargs="*", action="extend", help="dimlexes for the target language(s), if multiple dimlexes are provided, each is evaluated individually, if --lang is set, this overrides the language(s) defined in these files")
args.add_argument("--agg", "-agg", type=str, help="aggregator function one of "+", ".join(aggregators)+", defaults to "+aggregators[0], default=aggregators[0])
args.add_argument("--mwe", "-mwe", action="store_true", help="include multiword expressions from evaluation (default: exclude, as these cannot be retrieved from dictionary)")

args=args.parse_args()
if not args.agg in aggregators:
	sys.stderr.write("warning: invalid aggregator function \""+args.agg+"\", choose one of "+", ".join(aggregators)+", changing to "+aggregators[0]+"\n")
	sys.stderr.flush()
	args.agg=aggregators[0]	
			
lang2lang2tgt2src2score={}
for file in args.dicts:
	input=None
	if file.endswith("gz"):
		input=gzip.open(file,"r")
	else:
		input=open(file,"r")
	
	for line in input:		
		line=line.decode("utf-8")
		line.rstrip()
		if not line.startswith("#"):
			fields=line.split("\t")
			tgt=fields[0]
			if(not "@" in tgt):
				print("warning: no language ID found in \""+tgt+"\", skipping")
			else:
				src=None
				for f in range(2,len(fields)):
					if "@" in fields[f]:
						src=fields[f]
				if(not src):
					print("warning: no language ID found in \""+src+"\", skipping")
				else:
					tlang=re.sub(r".*@","",tgt)
					tgt=re.sub(r"^.(.*).$",r"\1",re.sub(r"@.*$","",tgt))
					slang=re.sub(r".*@","",src)
					src=re.sub(r"^.(.*).$",r"\1",re.sub(r"@.*$","",src))
					score=1.0
					if not tlang in lang2lang2tgt2src2score:
						lang2lang2tgt2src2score[tlang]={ slang : { tgt : { src : score }}}
					elif not slang in lang2lang2tgt2src2score[tlang]:
						lang2lang2tgt2src2score[tlang][slang] = { tgt : { src : score }}
					elif not tgt in lang2lang2tgt2src2score[tlang][slang]:
						lang2lang2tgt2src2score[tlang][slang][tgt] = { src : score }
					elif not src in lang2lang2tgt2src2score[tlang][slang][tgt]:
						lang2lang2tgt2src2score[tlang][slang][tgt][src] = score
					else:
						lang2lang2tgt2src2score[tlang][slang][tgt][src] += score
					
					if args.symm:
						if not slang in lang2lang2tgt2src2score:
							lang2lang2tgt2src2score[slang]={ tlang : { src : { tgt : score }}}
						elif not tlang in lang2lang2tgt2src2score[slang]:
							lang2lang2tgt2src2score[slang][tlang] = { src : { tgt : score }}
						elif not src in lang2lang2tgt2src2score[slang][tlang]:
							lang2lang2tgt2src2score[slang][tlang][src] = { tgt : score }
						elif not tgt in lang2lang2tgt2src2score[slang][tlang][src]:
							lang2lang2tgt2src2score[slang][tlang][src][tgt] = score
						else:
							lang2lang2tgt2src2score[slang][tlang][src][tgt] += score
					sys.stderr.write(file+" => "+tlang+" -> "+slang+": "+str(len(lang2lang2tgt2src2score[tlang][slang]))+" words")
					if(args.symm):
						sys.stderr.write(", "+slang+" -> "+tlang+": "+str(len(lang2lang2tgt2src2score[slang][tlang]))+" words")
					sys.stderr.write("\r")
					sys.stderr.flush()
					
	sys.stderr.write("\n")
	sys.stderr.flush()
	input.close()
	
# normalize scores
for tlang in lang2lang2tgt2src2score:
	for tgt in lang2lang2tgt2src2score[tlang]:
		for slang in lang2lang2tgt2src2score[tlang][tgt]:
			total=float(sum(lang2lang2tgt2src2score[tlang][tgt][slang].values()))
			for src in lang2lang2tgt2src2score[tlang][tgt][slang]:
				lang2lang2tgt2src2score[tlang][tgt][slang][src]=lang2lang2tgt2src2score[tlang][tgt][slang][src]/total

rels=[args.rel]
if args.rel==0:
	rels=list(range(1,5))

for rel in rels:
	args.rel=rel
	lang2lex2sense2score={}

	for file in args.dimlex:
		with open(file,"r") as input:
			for line in input:
				if(not line.startswith("#")):
					fields=line.split("\t")
					if(len(fields)>args.rel):
						rel="cue"	# is a discourse marker
						if(args.rel>1):
							rel=fields[args.rel]
						lex=fields[0]
						lex=lex.lower()	# upper case not in dict
						if(not " " in lex or args.mwe):
							lang=fields[1]
							score=1.0
							if(len(fields)>5):
								try:
									score=float(fields[5])
								except:
									pass
							if(not lang in lang2lex2sense2score):
								lang2lex2sense2score[lang]= { lex : { rel : score } }
							elif not lex in lang2lex2sense2score[lang]:
								lang2lex2sense2score[lang][lex] = { rel : score }
							elif not rel in lang2lex2sense2score[lang][lex]:
								lang2lex2sense2score[lang][lex][rel] = score
							else:					
								lang2lex2sense2score[lang][lex][rel] += score
							# verzerrung für higher-level senses
					
	# normalize scores to 1
	for lang in lang2lex2sense2score:
		for lex in lang2lex2sense2score[lang]:
			total=float(sum(lang2lex2sense2score[lang][lex].values()))
			for sense in lang2lex2sense2score[lang][lex]:
				lang2lex2sense2score[lang][lex][sense]=lang2lex2sense2score[lang][lex][sense]/total
					
	#print(lang2lang2tgt2src2score.keys())
	
	aggs=[args.agg]
	if args.agg=="all":
		aggs=aggregators
	
	old_lang2lex2sense2score=lang2lex2sense2score
	old_agg=args.agg	
	
	for agg in aggs:
		if agg!="all":
			args.agg=agg
			lang2lex2sense2score=copy.deepcopy(old_lang2lex2sense2score)
						
			# project, using the shortest path per word
			additions=None
			iterations=1
			langs=sorted(lang2lex2sense2score.keys())
			while (iterations==1 or additions>0) and not args.lang in langs :
				#print(args.lang,langs,lang2lang2tgt2src2score.keys(),lang2lex2sense2score.keys())
				additions=0
				for tlang in lang2lang2tgt2src2score:	# project using the shortest path
					if not tlang in langs and not args.lang in langs:
						#print(args.lang,langs,tlang)
						tgt2slang2sense2score={} 
						slangs=[]
						for slang in langs:
							#print(tlang,"<-",slang)
							if slang in lang2lang2tgt2src2score[tlang]:
								slangs.append(slang)
								for tgt in lang2lang2tgt2src2score[tlang][slang]:
									#print(tgt)
									total=1.0*len(lang2lang2tgt2src2score[tlang][slang][tgt])
									for src in lang2lang2tgt2src2score[tlang][slang][tgt]:
										if src in lang2lex2sense2score[slang]:
											for sense in lang2lex2sense2score[slang][src]:
												score=lang2lex2sense2score[slang][src][sense]/total
												if not tgt in tgt2slang2sense2score:
													tgt2slang2sense2score[tgt] = { slang : { sense : score } }
												elif not slang in tgt2slang2sense2score[tgt]:
													tgt2slang2sense2score[tgt][slang] = { sense : score }
												elif not sense in tgt2slang2sense2score[tgt][slang]:
													tgt2slang2sense2score[tgt][slang][sense] = score
												else:
													tgt2slang2sense2score[tgt][slang][sense] += score
					
						# normalize
						lang2lex2sense2score[tlang]={}
						for lex in tgt2slang2sense2score:
							
							if args.agg=="avg":
								norm=1.0* len(slangs)
								for slang in tgt2slang2sense2score[lex]:
									for sense in tgt2slang2sense2score[lex][slang]:
										score=tgt2slang2sense2score[lex][slang][sense]/norm
										if not lex in lang2lex2sense2score[tlang]:
											lang2lex2sense2score[tlang][lex] = { sense : score }
										elif not sense in lang2lex2sense2score[tlang][lex]:
											lang2lex2sense2score[tlang][lex][sense] = score
											#print(tlang,lex,sense,score)
										else:
											lang2lex2sense2score[tlang][lex][sense] += score
							elif args.agg=="max":
								for slang in tgt2slang2sense2score[lex]:
									for sense in tgt2slang2sense2score[lex][slang]:
										score=tgt2slang2sense2score[lex][slang][sense]/norm
										if not lex in lang2lex2sense2score[tlang]:
											lang2lex2sense2score[tlang][lex] = { sense : score }
										elif not sense in lang2lex2sense2score[tlang][lex]:
											lang2lex2sense2score[tlang][lex][sense] = score
										elif score > lang2lex2sense2score[tlang][lex][sense]:
											lang2lex2sense2score[tlang][lex][sense] += score
								# normalisierung
								for lex in lang2lex2sense2score[tlang]:
									total=1.0*sum(lang2lex2sense2score[tlang][lex].values())
									for sense in lang2lex2sense2score[tlang][lex]:
										lang2lex2sense2score[tlang][lex][sense]=lang2lex2sense2score[tlang][lex][sense]/total
							elif args.agg=="median": # keine normalisierung nötig
								if len(tgt2slang2sense2score) > len(slangs)/2:
									sense2scores = {}
									for slang in tgt2slang2sense2score[lex]:
										for sense in tgt2slang2sense2score[lex][slang]:
											if not sense in sense2scores:
												sense2scores[sense]=[ tgt2slang2sense2score[lex][slang][sense] ]
											else:
												sense2scores[sense].append(tgt2slang2sense2score[lex][slang][sense])
									for sense in sense2scores:
										if len(sense2scores[sense]) > len(slangs)/2:
											scores=sense2scores[sense]
											scores.sort()
											scores.reverse() # decreasing
											score=scores[int(len(slangs)/2)]
											if(not tlang in lang2lex2sense2score):
												lang2lex2sense2score[tlang] = { lex : { sense : score } }
											elif not lex in lang2lex2sense2score[tlang]:
												lang2lex2sense2score[tlang][lex] = { sense : score }
											elif not sense in lang2lex2sense2score[tlang][lex]:
												lang2lex2sense2score[tlang][lex][sense] = score
											else:
												print("warning: multiple results for sense "+sense+", skipping")
											
							if lex in lang2lex2sense2score[tlang]:
								additions+=1
								sys.stderr.write("iteration "+str(iterations)+" ... "+str(additions)+" "+str(langs)+"\r")
								sys.stderr.flush()
				
					# disabling this will currently lead to infinite loops; also cuts off any indirect loops
					langs=lang2lex2sense2score.keys()
					
				sys.stderr.write("\n")
				iterations+=1								

			# eval
			old_lang=args.lang
			lex2senses={}
			for gold in args.gold:
				with open(gold,"r") as input:
					for line in input:
						if(not line.startswith("#")):
							fields=line.split("\t")
							if(len(fields)>args.rel):
								lex=fields[0]
								lex=lex.lower()	# upper case not in dict
								if(not args.lang):
									args.lang=fields[1]
									sys.stderr.write("set target language to \""+args.lang+"\"\n")
									sys.stderr.flush()
								if(not " " in lex or args.mwe):
									sense="cue"
									if(args.rel>1):
										sense=fields[args.rel]
									if not lex in lex2senses:
										lex2senses[lex] = [sense]
									else:
										lex2senses[lex].append(sense)
									lex2senses[lex]=sorted(set(lex2senses[lex]))				

				if not args.lang in lang2lex2sense2score:
					print("warning: could not project onto "+args.lang)
				else:
					
					# also check filters

					thresholds = []
					steps=100
					for x in range(steps+1):
						thresholds.append(x/float(steps))

					thresholds=sorted(set(thresholds))

					# threshold 2 subscore, sense-level
					t2tp_senses={}	# for every correct sense
					t2fp_senses={}	# for all predicted senses
					t2fn_senses={} # for every missing sense

					for t in thresholds:
						t2tp_senses[t]=0.0
						t2fp_senses[t]=0.0
						t2fn_senses[t]=0.0

					for t in thresholds:
						for lex in lex2senses:
							if  lex in lang2lex2sense2score[args.lang]:
								for sense in lex2senses[lex]:
									if sense in lang2lex2sense2score[args.lang][lex]:
										score=lang2lex2sense2score[args.lang][lex][sense]
										if score<t:	# no prediction
											t2fn_senses[t]+=1
										else:
											t2tp_senses[t]+=1
							else:
								t2fn_senses[t]+=len(lex2senses[lex])
						
						for lex in lang2lex2sense2score[args.lang]:
							if not lex in lex2senses: # false positive
								for score in lang2lex2sense2score[args.lang][lex].values():
									if score >= t:
										t2fp_senses[t]+=1

					# threshold 2 subscore, marker-level
					t2tp_lex={}	# if one sense is correct
					t2fp_lex={}	# for all predicted discourse markers
					t2fn_lex={} # for every missing dimlexes

					for t in thresholds:
						t2tp_lex[t]=0.0
						t2fp_lex[t]=0.0
						t2fn_lex[t]=0.0

					for t in thresholds:
						for lex in lex2senses:	
							if lex in lang2lex2sense2score[args.lang]:
								overlap=False
								for sense in lex2senses[lex]:
									if not overlap and sense in lang2lex2sense2score[args.lang][lex]:
										if(lang2lex2sense2score[args.lang][lex][sense]>=score):
											overlap=True
								if overlap:
									t2tp_lex[t]+=1
								else:
									t2fn_lex[t]+=1
							else:
								t2fn_lex[t]+=1
						
						for lex in lang2lex2sense2score[args.lang]:
							if not lex in lex2senses: # false positive
								prediction=False
								for score in lang2lex2sense2score[args.lang][lex].values():
									if not prediction and score >= t:
										prediction=True
								if prediction:
									t2fp_lex[t]+=1

					# best thresholds
					max_t={ "p_lex" : 0.0, "r_lex": 0.0, "f_lex": 0.0, "p_senses" : 0.0, "r_senses" : 0.0, "f_senses" : 0.0 }
					max_score={ "p_lex" : 0.0, "r_lex": 0.0, "f_lex": 0.0, "p_senses" : 0.0, "r_senses" : 0.0, "f_senses" : 0.0 }

					for t in thresholds:
						tp_lex=t2tp_lex[t]
						fp_lex=t2fp_lex[t]
						fn_lex=t2fn_lex[t]

						p_lex=0.0
						try:
							p_lex=tp_lex / (tp_lex + fp_lex)
						except: 
							pass
						
						r_lex=0.0
						try:
							r_lex=tp_lex / (tp_lex + fn_lex)
						except:
							pass
							
						f_lex=0.0
						try:	
							f_lex=2.0*p_lex*r_lex / ( p_lex+r_lex)
						except:
							pass
						
						tp_senses=t2tp_senses[t]
						fp_senses=t2fp_senses[t]
						fn_senses=t2fn_senses[t]

						p_senses=0.0
						try:
							p_senses=tp_senses / (tp_senses + fp_senses)
						except: 
							pass
						
						r_senses=0.0
						try:
							r_senses=tp_senses / (tp_senses + fn_senses)
						except:
							pass
							
						f_senses=0.0
						try:	
							f_senses=2.0*p_senses*r_senses / ( p_senses+r_senses)
						except:
							pass
						

						if p_lex > max_score["p_lex"]:
							max_t["p_lex"]=t
							max_score["p_lex"]=p_lex
						if r_lex > max_score["r_lex"]:
							max_t["r_lex"]=t
							max_score["r_lex"]=r_lex
						if f_lex > max_score["f_lex"]:
							max_t["f_lex"]=t
							max_score["f_lex"]=f_lex
						
						if p_senses > max_score["p_senses"]:
							max_t["p_senses"]=t
							max_score["p_senses"]=p_senses
						if r_senses > max_score["r_senses"]:
							max_t["r_senses"]=t
							max_score["r_senses"]=r_senses
						if f_senses > max_score["f_senses"]:
							max_t["f_senses"]=t
							max_score["f_senses"]=f_senses
							
						# print(t, "|", int(tp_lex), int(fp_lex), int(fn_lex), round(p_lex,2), round(r_lex,2), round(f_lex,2), " || ", int(tp_senses), int(fp_senses), int(fn_senses), round(p_senses,2), round(r_senses,2), round(f_senses,2), sep="\t")

					# print()

					print("th","|", "tp_l", "fp_l", "fn_l", "p_l", "r_l", "f_l", " || ", "tp_s", "fp_s", "fn_s", "p_s", "r_s", "f_s", sep="\t")
					print("-------","+------", "-------", "-------", "-------", "-------", "-------", "-------", "-++----", "-------", "-------", "-------", "-------", "-------", "-------", sep="-")
					
					# best scores plus context
					max_t=list(max_t.values())
					for t in sorted(set(max_t)):
						for i in range(-2,+2):
							i=i/float(steps)
							if t+i in t2tp_lex:
								max_t.append(t+i)

					max_t=sorted(set(max_t))

					
					for t in max_t:
						tp_lex=t2tp_lex[t]
						fp_lex=t2fp_lex[t]
						fn_lex=t2fn_lex[t]

						p_lex=0.0
						try:
							p_lex=tp_lex / (tp_lex + fp_lex)
						except: 
							pass
						
						r_lex=0.0
						try:
							r_lex=tp_lex / (tp_lex + fn_lex)
						except:
							pass
							
						f_lex=0.0
						try:	
							f_lex=2.0*p_lex*r_lex / ( p_lex+r_lex)
						except:
							pass
						
						tp_senses=t2tp_senses[t]
						fp_senses=t2fp_senses[t]
						fn_senses=t2fn_senses[t]

						p_senses=0.0
						try:
							p_senses=tp_senses / (tp_senses + fp_senses)
						except: 
							pass
						
						r_senses=0.0
						try:
							r_senses=tp_senses / (tp_senses + fn_senses)
						except:
							pass
							
						f_senses=0.0
						try:	
							f_senses=2.0*p_senses*r_senses / ( p_senses+r_senses)
						except:
							pass
						

						if p_lex > max_score["p_lex"]:
							max_t["p_lex"]=t
							max_score["p_lex"]=p_lex
						if r_lex > max_score["r_lex"]:
							max_t["r_lex"]=t
							max_score["r_lex"]=r_lex
						if f_lex > max_score["f_lex"]:
							max_t["f_lex"]=t
							max_score["f_lex"]=f_lex
						
						if p_senses > max_score["p_senses"]:
							max_t["p_senses"]=t
							max_score["p_senses"]=p_senses
						if r_senses > max_score["r_senses"]:
							max_t["r_senses"]=t
							max_score["r_senses"]=r_senses
						if f_senses > max_score["f_senses"]:
							max_t["f_senses"]=t
							max_score["f_senses"]=f_senses
						
						print(t,"|", int(tp_lex), int(fp_lex), int(fn_lex), round(p_lex,2), round(r_lex,2), round(f_lex,2), " || ", int(tp_senses), int(fp_senses), int(fn_senses), round(p_senses,2), round(r_senses,2), round(f_senses,2), sep="\t")

					print(args)
					print()
				args.agg=old_agg
				args.lang=old_lang