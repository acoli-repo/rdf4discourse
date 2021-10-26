import re,sys,os,traceback,argparse

args=argparse.ArgumentParser(description="extract table of markers with surface form and discurse relation")
args.add_argument("raw", type=str, help="text file")
args.add_argument("ann", type=str, help="annotated file, standoff")
args=args.parse_args()

pos2rels={}
with open(args.ann) as input:
    for line in input:
        blocks=line.split("|||")
        rels="|".join(sorted(set(blocks[1].split("|"))))
        fields=blocks[0].split("|")
        category=fields[0] # Explicit, etc.
        if category in ["Explicit"]:
                try:
                    span=fields[1]
                    while(len(span)>0):
                        start=re.sub(r"[^0-9].*","",span)
                        span=span[len(start):]
                        try:
                            pos=int(start)
                            if pos in pos2rels:
                                if not rels in pos2rels[pos]:
                                    pos2rels[pos]+="|"+rels
                            else:
                                pos2rels[pos]=rels
                        except: pass
                        if span.startswith(".."):
                            if span.startswith(".."+str(pos+1)):
                                span=span[len(".."+str(pos+1)):]
                            else:
                                span=str(pos+1)+span
                        if span[0] in ",;/|":
                            span=span[1:]
                except: pass

with open(args.raw) as input:
    pos=0
    c=" ";
    word=""
    rels=None
    while(len(c)>0):
        c=input.read(1)
        if re.match(r"\s",c):
            if rels!=None:
                rels="|".join(sorted(set("|".join(rels).split("|"))))
                if len(rels)>0 and len(word.strip())>0:
                    print(word+"\t"+rels)
            rels=None
            word=""
        else:
            if rels==None:
                rels=[]
            word+=c
            if pos in pos2rels:
                rel=pos2rels[pos]
                if not rel in rels:
                    rels.append(rel)
        pos+=1

    if rels!=None:
        rels="|".join(sorted(set("|".join(rels).split("|"))))
        if len(rels)>0 and len(word.strip())>0:
            rels="_"
        print(word+"\t"+rels)
