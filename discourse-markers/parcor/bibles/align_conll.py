import sys,os,re
import gzip, bz2
import xml.etree.ElementTree as ET
import tempfile
from pprint import pprint
import systran_align

""" provide word alignments for CoNLL files
    args: file1 file2

    requires pre-existing sentence alignment over CoNLL files
    output as CoNLL file to stdout, with file2 annotations appended to corresponding file1 rows

"""

class WordAligner:
    """
        input is sentence-aligned CoNLL files, output is a file merged along word alignment, currently using FastText (Systran reimplementation)
    """

    file2buffers={}
    """ filename -> array of buffers, in this context, a buffer is an array of conll rows (arrays) that represent one sentence each """

    file2word_col={}
    """ defines the alignment column """

    lcase_files=[]
    """ files to be lowercased before alignment """

    def __init__(self):
         self.file2buffers={}

    def guess_format(self, file:str):
        """ return format and open method. here, the former is always "conll" """
        name=file.lower()

        my_open=open
        if name.endswith(".gz"):
            name=name[0:-3]
            my_open=gzip.open
        if name.endswith(".bz2"):
            name=name[0:-4]
            my_open=bz2.open

        # check that it is a TSV format
        with my_open(file,"r") as input:
            try:
                    for iteration in range(50):
                        line=input.readline().strip()
                        if not line.startswith("#"):
                            if line!="":
                                if "\t" in line:
                                    return "conll",my_open
            except:
                pass

        # fallback: file extension, can later lead to unsupported format exceptions
        return name.split(".")[-1], my_open

    def add(self, file:str, word_col: int, sent_id=None, buffer=None):
        """ add a file that contains a monolingual sentence-aligned CoNLL file,
            note that these are later identified by their file name
            word_col is the column that contains the text to be aligned
            sent_id is a sentence id, if None, we just count, if integer,
                    we append to an existing buffer
            buffer is a list of rows that represents a single conll sentence
            """
        file2buffers=self.file2buffers
        if not file in file2buffers:
            file2buffers[file]=[]
        if not word_col in self.file2word_col:
            self.file2word_col[file]=word_col
        if word_col != self.file2word_col[file]:
            raise Exception("word_col mismatch: failed to override "+str(self.file2word_col[file])+" with "+str(word_col))
        if sent_id==None:
            sent_id=len(file2buffers[file])
        while len(file2buffers[file])<=sent_id:
            file2buffers[file].append([])

        if type(buffer)==list:
                # append to sentence, nmormally the sentence will be initially []
                file2buffers[file][sent_id]+=buffer
        else: # ignore buffer, but add complete file
            format,my_open=self.guess_format(file)
            if format=="conll":
                with my_open(file, "r") as input:
                    sys.stderr.write("reading "+file+"\r")
                    # we strip all CoNLL comments and split at empty lines
                    buffer=[]

                    for line in input:
                        line=line.strip()
                        if not line.startswith("#"):
                            if line=="":
                                if len(buffer)>0:
                                    self.add(file,word_col,buffer=buffer)
                                    buffer=[]
                            else:
                                if not "\t" in line:
                                    if file in file2buffers:
                                        file2buffers.pop(file)
                                    raise Exception("not a CoNLL/TSV format, line \""+line+"\" does not contain a tabulator")
                                else:
                                    buffer.append(line.split("\t"))
                    if len(buffer)>0:
                        self.add(file,word_col,buffer=buffer)

            else:
                    raise Exception("Support for format "+format+" not implemented yet")

            sys.stderr.write("reading "+file+": "+str(len(file2buffers[file]))+" sentences\n")

        self.file2buffers=file2buffers

    def lower(self,files=None):
        """ overwrites the WORD/FORM column ! but keeps tokenization """
        if files==None:
            files=self.file2buffers.keys()
        self.lcase_files=files

    def print_parallel_data(self, format="fast_align"):
        """ write fast_align training data into a file """

        result=""
        if format=="fast_align":
            files=list(self.file2buffers.keys())
            if len(files)==0:
                raise Exception("please provide two texts for alignment")
            if len(files)==1:
                sys.stderr.write("warning: only one text given, we perform self-alignment\n")
                files.append(files[0])
            if len(files)>2:
                sys.stderr.write("warning: fast_align supports alignment between only two texts, restricting to "+files[0]+" and "+files[1])
                files=files[0:2]
                sents=len(file2buffers[files[0]])
                if sents != len(file2buffers[files[1]]):
                    raise Exception("alignment error: different number of sentences: "+str(sents)+" in "+file[0]+" vs. "+str(len(file2buffers[files[1]]))+" in "+file[1])

                for nr in range(sents):
                    pairs=[]

                    for file in files:
                        toks=self._get_toks(file, self.file2buffers[file][nr])
                        toks=" ".join(toks)
                        pairs.append(toks)

                    result+= " ||| ".join(pairs)+"\n"
        else:
            raise Exception("unsupported output format \""+format+"\"")

        return result

    def _align(self):
        """ calls systran_align.generate_alignment_probabilities """

        input_path=None
        fw_path=None
        bw_path=None

        with tempfile.NamedTemporaryFile(delete=False) as forward_probs:
            fw_path=forward_probs.name
        with tempfile.NamedTemporaryFile(delete=False) as backward_probs:
            bw_path=backward_probs.name
        with tempfile.NamedTemporaryFile(delete=False) as input:
            input_path=input.name
            input.write(self.print_parallel_data().encode())

        systran_align.generate_alignment_probabilities(input_path,fw_path,bw_path)

        os.remove(input_path)
        return fw_path, bw_path

    def _get_toks(self, file, src_buffer : list):
        """
            return array of normalized (!) toks.
            src_buffer is a single CoNLL sentence as array of arrays, comments stripped, no empty rows
        """

        src_col=self.file2word_cols[file]
        src_toks=[ row[src_col].strip() for row in src_buffer ]
        src_toks=[ tok if len(tok) > 0 else "_" for tok in src_toks ]
        src_toks=[ re.sub(r"\s+","_",tok) for tok in src_toks ]
        if file in self.lcase_files:
            src_toks = [ tok.lower() for tok in src_toks ]
        return src_toks

    def align(self):
        """ calls systran_align.Aligner """
        fw_path, bw_path=self._align()
        aligner=systran_align.Aligner(fw_path,bw_path)

        if len(self.file2buffers)!=2:
            raise Exception("we currently provide bilingual alignment only, we need two files")

        files=list(self.file2buffers.keys())

        for sent_nr in range(len(self.file2buffers[files[0]])):

            src_buffer=self.file2buffers[files[0]][sent_nr]
            src_toks=self._get_toks(file, src_buffer)

            tgt_buffer=self.file2buffers[files[1]][sent_nr]
            tgt_toks=self._get_toks(file, tgt_buffer)

            alignment = aligner.align(src_toks,tgt_toks)
            self.print_alignment(src_buffer,tgt_buffer,alignment, src_file=files[0], tgt_file=files[1])

        os.remove(fw_path)
        os.remove(bw_path)

    def print_alignment(self, src_buffer: list, tgt_buffer:list, alignments:dict, src_file=None, tgt_file=None):
        """ write CoNLL format
            src_buffer and tgt_buffer are one CoNLL buffer each that is position-aligned via alignments
        """

        if src_file in self.file2word_col:
            print("# text:  "+" ".join([ row[self.file2word_col[src_file]] for row in src_buffer ]))
        if tgt_file in self.file2word_col:
            print("# trans: "+" ".join([ row[self.file2word_col[tgt_file]] for row in tgt_buffer ]))

        for key in alignments:
            if key!="alignments":
                print("# "+key+": "+str(alignments[key]))

        src2tgt={}
        tgt2src={}
        for s,t in alignments["alignments"]:
            for a,b,a2b in ([(s,t,src2tgt),(t,s,tgt2src)]):
                if not a in a2b:
                    a2b[a]=[b]
                else:
                    a2b[a].append(b)

        tgts=[] # oreviously printed tgts
        for s,src_row in enumerate(src_buffer):
            anno=[str(s+1)]+src_row
            if not s in src2tgt:
                anno+=["_","_"]
                print("\t".join(anno))
            else:
                for t in src2tgt[s]:
                    anno.append(str(t+1))
                    if True: # t in tgts:
                    #     anno.append("*")
                    #     print("\t".join(anno))
                    # else:
                        anno+=tgt_buffer[t]
                        tgts.append(t)
                        print("\t".join(anno))
                        while(t+1<len(tgt_buffer) and not t+1 in tgts and not t+1 in tgt2src):
                            t=t+1
                            print("_\t_\t"+str(t+1)+"\t"+tgt_buffer[t])
                            tgts.append(t)
                    anno=[anno[0],"*"]
        for t in range(len(tgt_buffer)):
            if not t in tgts:
                print("_\t_\t"+str(t+1)+"\t"+tgt_buffer[t])
        print()

if not "-silent" in sys.argv:
    sys.stderr.write("synopsis: "+sys.argv[0]+" conll1[=col1] conll2[=col2] [-low] [-silent]\n")
    sys.stderr.write("  conlli    CoNLL file(s), must be sentence-aligned\n"+\
                     "  coli      column over which the alignment is to be performed, defaults to 1 (second column, WORD/FORM column in CoNLL-U)\n"+\
                     "  -low      perform alignment over lower case\n"+\
                     "  -silent   skip usage information")

file1=sys.argv[1]
file2=sys.argv[2]
col1=1
col2=1

if "=" in file1:
    if not os.path.exists(file1):
        col1=int(file1.split("=")[-1])
        file1="=".join(file1.split("=")[0:-1])

if "=" in file2:
    if not os.path.exists(file2):
        col2=int(file2.split("=")[-1])
        file2="=".join(file2.split("=")[0:-1])

alignment=WordAligner()
alignment.add(file1,col1)
alignment.add(file2,col2)

if "-low" in sys.argv:
    sys.stderr.write("lower case\n")
    alignment.lower()

#print(alignment.print_parallel_data())
alignment.align()
