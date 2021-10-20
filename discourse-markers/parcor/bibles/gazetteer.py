import os,sys,re,traceback,argparse
from copy import copy
from pprint import pprint

args=argparse.ArgumentParser(description="annotation of parallel (translated) text in CoNLL format, using gazeteers, annotations of each gazeteer are appended at the end of every non-comment line, if none applies, _ is written instead")
args.add_argument("input",type=str,help="input file, should be one word per line, tab-separated; use - (single hyphen) to read from stdin")
args.add_argument("gazetteers",type=str,nargs="+",help="one or multiple gazetteers; format: one phrase per line, line: \"TOKS\"@LANG<TAB>\"ANNO1\"[<TAB>\"ANNO2\"...]; TOKS are space-separated strings to match against, @LANG is a BCP47 language code")
args.add_argument("-tgt", "--target_word_column", type=int, default=1, help="column that contains the text whose annotation is to be bootstrapped from the annotation of the word_column, for non-translated text, this can be identical to word_column, defaults to 1 (second col); this feature is checked in slim mode only")
args.add_argument("-word", "--word_column", type=int, default=1, help="word column to match the gazetteer against, can, for example, be a translation, then, not necessarily in text order, defaults to 1 (second col)")
args.add_argument("-order", "--order_column", type=int, default=None, help="column that encodes the order of words in the --word_column, if different from text order, defaults to None")
args.add_argument("-slim", "--skip_translations", action="store_true", help="by default, we preserve translations in the output, with this option, we skip translations and information about the match")

args=args.parse_args()

class Annotator:

    gaz2toks2vals={}    # note that toks are matched against an extract of the --word_column, so tokenization and encoding should match
    gaz2len={}          # (max) number of columns per gazetteer, to make sure we write constent width

    def __init__(self, gazetteers, tgt_col=1, word_col=1,order_col=None):

        gaz2toks2vals={}    # note that toks are matched against an extract of the --word_column, so tokenization and encoding should match
        gaz2len={}          # (max) number of columns per gazetteer, to make sure we write constent width

        for gaz in gazetteers:
            with open(gaz,"r") as input:
                for line in input:
                    line=line.strip()
                    if line[0] not in "#?" and not line=="":
                        fields=line.split("\t")
                        if len(fields)>1:
                            toks=fields[0]
                            lang="_"
                            if "@" in toks:
                                lang=toks[toks.index("@")+1:]
                                toks=toks[0:toks.index("@")]

                            annos=[toks,lang]+fields[1:]

                            # strip surrounding "" and '' from annos
                            for x in range(len(annos)):
                                anno=annos[x]
                                if anno.startswith('"""') and anno.endswith('"""'):
                                    anno=anno[3:-3]
                                if anno.startswith('"') and anno.endswith('"'):
                                    anno=anno[1:-1]
                                if anno.startswith("'") and anno.endswith("'"):
                                    anno=anno[1:-1]
                                annos[x]=anno

                            toks=annos[0]
                            annos=annos[1:]

                            if not gaz in gaz2len:
                                gaz2len[gaz]=len(annos)
                            else:
                                gaz2len[gaz]=max(len(annos),gaz2len[gaz])
                            if not gaz in gaz2toks2vals:
                                gaz2toks2vals[gaz]={toks:annos}
                            elif not toks in gaz2toks2vals[gaz]:
                                gaz2toks2vals[gaz][toks]=annos
                            else:
                                # sys.stderr.write("warning: multiple values for \""+toks+"\" in "+gaz+", trying to merge\n")
                                for nr,(old,new) in enumerate(zip(gaz2toks2vals[gaz][toks], copy(annos))):
                                    if old==None or old in ["","_"]: old=new
                                    if new==None or new in ["","_"]: new=old
                                    if old==None:
                                        old=""

                                    vals=sorted(set(old.split("|")+new.split("|")))
                                    vals=[ val for val in vals if not val in ["_",""] ]
                                    val="|".join(vals)
                                    if val=="":
                                        val="_"
                                    annos[nr]=val
                                gaz2toks2vals[gaz][toks]=annos
        # pprint(gaz2toks2vals)
        # pprint(gaz2len)

        self.gaz2toks2vals=gaz2toks2vals
        self.gaz2len=gaz2len
        self.word_col=word_col
        self.order_col=order_col
        self.tgt_col=tgt_col
        # print(gaz2toks2vals)

    def annotate(self, buffer:str, suppress_translations=False):
        """ read conll sentence(s) in text format, append annotations according to configuration, return conll data as plain text """
        buffer=re.sub(r"\r","",buffer)
        result=""
        if "\n\n" in buffer: # break into sentences
            for sentence in buffer.split("\n\n"):
                result=result+self.annotate(sentence,suppress_translations=suppress_translations)+"\n"
            return result

        # one buffer one sentence
        else:
            rows=[]
            for line in buffer.split("\n"):
                line=line.strip()
                if(line.startswith("#")):
                    result+=line+"\n"
                elif line!="":
                    rows.append(line.split("\t"))

            words=[ row[self.word_col] for row in rows ]
            order=[ str(nr+1) for nr,_ in list(enumerate(words)) ]

            if self.order_col!=None:
                order=[ row[self.order_col] for row in rows ]

            order2word= { int(o) : w for o, w in zip(order,words) if re.match(r"^[0-9]+$",o) }
            order=sorted(order2word.keys())
            words=[]

            for o in order:
                words.append(order2word[o])

            # words now contains the translations in original order and without repetitions
            # order are the original translation IDs
            # rows in order2rows are word offsets (not WORD IDs)

            for gaz in self.gaz2toks2vals:
                cols=self.gaz2len[gaz]+1
                toks2vals=self.gaz2toks2vals[gaz]
                order2len2annos={}
                for w,o in enumerate(order):
                    text=" "+" ".join(words[w:])+" "
                    order2len2annos[o]= { 0 : ["_"]*cols }
                    for toks in toks2vals:
                        if text.startswith(" "+toks.strip()+" ") or text.lower().startswith(" "+toks.strip()+" "):
                            vals=[toks]+toks2vals[toks]
                            length=len(toks.split(" "))
                            for w_ in range(w,w+length):
                                o_ = order[w]
                                if not o_ in order2len2annos:
                                    order2len2annos[o_]={length : vals}
                                elif not length in order2len2annos[o_]:
                                    order2len2annos[o_][length] = vals
                                elif "/".join(order2len2annos[o_][length]) != "/".join(vals):
                                    sys.stderr.write("warning: conflicting annotations: \""+words[o_]+"\" is annotated as [1], we skip alternative annotation as [2]:\n"+ \
                                        "\t[1] "+"/".join(order2len2annos[o_][length])+"\n"+ \
                                        "\t[2] "+"/".join(vals)+"\n")
                                    break

                for r in range(len(rows)):
                    o=str(r+1)
                    if self.order_col!=None:
                        o=rows[r][self.order_col]
                    annos=["_"]*cols
                    try:
                        o=int(o)
                        if o in order2len2annos:
                            max_len=max(order2len2annos[o].keys())
                            annos=order2len2annos[o][max_len]
                    except:
                        pass

                    if suppress_translations:
                        if rows[r][self.word_col]=="_":
                            annos="\t".join(annos)
                            annos="?".join(annos.split("_"))
                            annos=annos.split("\t")

                        slim_row=[]
                        for n in range(len(rows[r])):
                            if not n in [self.order_col, self.word_col] :
                                slim_row.append(rows[r][n])
                        slim_row+=annos[1:]
                        rows[r]=slim_row
                    else:
                        rows[r]+=annos

            if suppress_translations:
                rows=[ row for row in rows if not row[self.tgt_col] in ["*","_"]]

            rows=[ "\t".join(row) for row in rows ]
            result+="\n".join(rows)+"\n"

            return result

annotator=Annotator(args.gazetteers, tgt_col=args.target_word_column, order_col=args.order_column, word_col=args.word_column)

input=sys.stdin

if args.input=="-":
    sys.stderr.write("reading from stdin\n")
    sys.stderr.flush()
else:
    input=open(args.input,"r")

if True:
    buffer=""
    for line in input:
        line=line.strip()
        if line=="":
            if len(buffer)>0:
                print(annotator.annotate(buffer,suppress_translations=args.skip_translations))
            buffer=""
        else:
            buffer+=line+"\n"
    if len(buffer)>0:
        print(annotator.annotate(buffer,suppress_translations=args.skip_translations))

if args.input=="-":
    input.close()
