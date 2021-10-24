import sys,os,re,traceback,argparse

# sample call
# $> pdtb2conll.py eval/ted-mdb/en/raw/01/talk_1976_en.txt eval/ted-mdb/en/ann/01/talk_1976_en.txt
args=argparse.ArgumentParser(description="given a tokenized and a PDTB standoff file, write CoNLL to stdout, include only discourse marker classification, no span or argument marking, explicit only.")
args.add_argument("raw",type=str, help="raw (tokenized) file, no other annotation, e.g., eval/ted-mdb/en/raw/01/talk_1976_en.txt. If not tokenized, perform whitespace tokenization.")
args.add_argument("ann", type=str, help="annotated (standoff) file, e.g., eval/ted-mdb/en/ann/01/talk_1976_en.txt")
args=args.parse_args()

start2end2rel={}
with open(args.ann,"rt") as input:
    for line in input:
        blocks=line.split("|||")

        fields=blocks[0].split("|")
        if fields[0] in ["Explicit","AltLex"]:   # include AltLex ?
            span=fields[1]  # empty if REJECTED
            if len(span)>0:
                rel=blocks[1]
                for subspan in span.split(","):
                    subspan=subspan.split(".")
                    start=int(subspan[0])
                    end=int(subspan[-1])
                    if not start in start2end2rel:
                        start2end2rel[start] = { end : rel }

pos2rel={}
for start in start2end2rel:
    for end,rel in start2end2rel[start].items():
        for pos in range(start,end):
            if pos in pos2rel:
                pos2rel[pos]="|".join(sorted(set(pos2rel[pos].split("|")+rel.split("|"))))
            else:
                pos2rel[pos]=rel

with open(args.raw,"rt") as input:
    pos=0
    rel=None
    c=" "
    while(c!=""):
            c=input.read(1)
            if re.match(r"^\s$",c):
                if rel!=None:
                    rel="|".join(rel)
                    rel="|".join(sorted(set(rel.split("|"))))
                    if rel=="":
                        rel="_"
                    print("\t"+rel)
                    rel=None
            elif c!="":
                if rel==None:
                    rel=[]
                if pos in pos2rel:
                    if not pos2rel[pos] in rel:
                        rel.append(pos2rel[pos])
                print(c,end="")
            pos+=1
    if rel!=None:
        rel="|".join(rel)
        rel="|".join(sorted(set(rel.split("|"))))
        if rel=="": rel="_"
        print("\t"+rel)
