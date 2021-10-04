# read TSV file from stdin , write all columns as Comments
# except for target column (the last one), this one is SPACE-split and written as CoNLL

import sys,os,re,traceback

tgt_col=-1
if len(sys.argv)>1:
    tgt_col=int(sys.argv[1])

for line in sys.stdin:
    line=line.strip()
    if line.startswith("#") or line=="":
        print(line)
    else:
        fields=line.split("\t")
        for col,f in enumerate(fields):
            print("# "+f)
        for nr,tok in enumerate(fields[tgt_col].split()):
            print(str(nr+1)+"\t"+tok)
        print()
