import sys,gzip,re

lang2lang2src2tgt={}

for file in sys.argv[1:]:
	with gzip.open(file,"r") as input:
		for line in input:
			line=line.decode("utf-8")
			line=line.rstrip()
			fields=line.split("\t")
			if(len(fields)>7):
				for (src, tgt) in [ (fields[0], fields[7]), (fields[7], fields[0]) ]:
					slang=re.sub(r".*@","",src)
					tlang=re.sub(r".*@","",tgt)
					if slang < tlang:
						if not slang in lang2lang2src2tgt:
							lang2lang2src2tgt[slang] = { tlang : { src : set([ tgt ]) } }
						if not tlang in lang2lang2src2tgt[slang]:
							lang2lang2src2tgt[slang][tlang] = { src : set([ tgt ]) }
						if not src in lang2lang2src2tgt[slang][tlang]:
							lang2lang2src2tgt[slang][tlang][src] = set([ tgt ])
						else: 
							lang2lang2src2tgt[slang][tlang][src].add(tgt)

for lang1 in sorted(lang2lang2src2tgt.keys()):
	for lang2 in sorted(lang2lang2src2tgt[lang1].keys()):
		freq=0
		for src in lang2lang2src2tgt[lang1][lang2]:
			freq+=len(lang2lang2src2tgt[lang1][lang2][src])
		print(lang1, lang2, freq, sep="\t")
