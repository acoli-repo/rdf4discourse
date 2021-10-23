import gzip,os,re,sys,io,traceback,argparse,bz2

args=argparse.ArgumentParser(description="Given a TSV file with one row representing one sentence, one column representing one language, and with BCP47 code as header, split it into individual CoNLL files")
args.add_argument("tsv_file", type=str, help="TSV file with one sentence per row, one column per language and ISO 639/BCP47 as column headers, can be gzipped")
args.add_argument("dir", type=str, help="target directory, we will create one directory per docid (talkid) and one CoNLL file per language in it, using the language code as file name")
args=args.parse_args()

if not os.path.exists(args.dir):
    os.makedirs(args.dir)

my_open=open
if args.tsv_file.endswith("gz"):
    my_open=gzip.open
elif args.tsv_file.endswith("bz2"):
    my_open=bz2.open

col2lang={}
col2file={}
docid="_"
files=0
with my_open(args.tsv_file, "rt") as input:
    langs=input.readline().strip().split("\t")[1:]
    col2lang = { col+1:lang for col,lang in enumerate(langs) if re.match(r"^[a-z][a-z][a-z]?$",lang.split("-")[0]) }
    doc2col2file={}
    sentid=0
    for line in input:
        line=line.strip()
        fields=line.split("\t")
        if docid != fields[0].strip():
            if docid in doc2col2file:
                for file in doc2col2file[docid].values():
                    if file!=None:
                        file.close()
                        files-=1
        docid=fields[0].strip()
        if not docid in doc2col2file:
            if not os.path.exists(args.dir+"/"+docid):
                os.makedirs(args.dir+"/"+docid)
            doc2col2file[docid]={ col:None for col in col2lang }
        for col,sent in enumerate(fields):
            if col in doc2col2file[docid]:
                sent=sent.strip()
                if len(sent)>0:
                    if doc2col2file[docid][col]==None:
                        doc2col2file[docid][col]=open(args.dir+"/"+docid+"/"+col2lang[col]+".conll","wt")
                        files+=1
                    file=doc2col2file[docid][col]
                    file.write("# doc_id = "+docid+"\n")
                    file.write("# sent_id = "+str(sentid)+"\n")
                    for nr,tok in enumerate(sent.split()):
                        file.write(str(nr+1)+"\t"+tok+"\n")
                    file.write("\n")
                    file.flush()
            sentid+=1
            sys.stderr.write(str(sentid)+" sentences, "+str(files)+" open files \r")
            sys.stderr.flush()

for file in doc2col2file[docid].values():
        if file!=None:
            file.close()
