import gzip,os,re,sys,io,traceback,argparse,bz2

args=argparse.ArgumentParser(description="Given a TSV file with one row representing one sentence, one column representing one language, and with BCP47 code as header, split it into individual CoNLL files")
args.add_argument("tsv_file", type=str, help="TSV file with one sentence per row, one column per language and ISO 639/BCP47 as column headers, can be gzipped")
args.add_argument("dir", type=str, help="target directory, we will create one CoNLL file per language, using the language code as file name")
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
with my_open(args.tsv_file, "rt") as input:
    langs=input.readline().strip().split("\t")[1:]
    col2lang = { col+1:lang for col,lang in enumerate(langs) if re.match(r"^[a-z][a-z][a-z]?$",lang.split("-")[0]) }
    col2file = { col:None for col in col2lang }
    sentid=0
    for line in input:
        line=line.strip()
        fields=line.split("\t")
        docid=fields[0].strip()
        for col,sent in enumerate(fields):
            if col in col2file:
                sent=sent.strip()
                if len(sent)>0:
                    if col2file[col]==None:
                        col2file[col]=open(args.dir+"/"+col2lang[col]+".conll","wt")
                    file=col2file[col]
                    file.write("# doc_id = "+docid+"\n")
                    file.write("# sent_id = "+str(sentid)+"\n")
                    for nr,tok in enumerate(sent.split()):
                        file.write(str(nr+1)+"\t"+tok+"\n")
                    file.write("\n")
                    file.flush()
            sentid+=1
            sys.stderr.write(str(sentid)+" sentences\r")
            sys.stderr.flush()

for file in col2file.values():
    if file!=None:
        file.close()
