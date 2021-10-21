import sys,os,re
import gzip, bz2
import xml.etree.ElementTree as ET
import tempfile
from pprint import pprint
import systran_align

""" provide word alignments for CoNLL files
    args: file1 file2

    requires pre-existing sentence alignment over CoNLL files, either by position or explicit sent_id properties
    output as CoNLL file to stdout, with file2 annotations appended to corresponding file1 rows

"""

class WordAligner:
    """
        input is sentence-aligned CoNLL files, output is a file merged along word alignment, currently using FastText (Systran reimplementation)
    """

    file2id2buffer={}
    """ filename -> sent_id -> buffer, in this context, a buffer is an array of conll rows (arrays) that represent one sentence each """

    file2width={}
    """ if we have no alignment, we fill it up with question marks, but we need column width """

    file2word_cols={}
    """ defines the alignment column """

    lcase_files=[]
    nopunct_files=[]
    """ files to be normalized before alignment """

    def __init__(self, ids=True):
        """ if ids=False, do not generate IDs. Use only if no multi-word alignment is required """
        self.ids=ids
        self.file2id2buffer={}

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
            sent_id is a sentence id, if None per buffer, use (string representations of integers), if the same id re-occurs, then concatenate
            buffer is a list of rows that represents a single conll sentence
            """
        file2id2buffer=self.file2id2buffer
        if not file in file2id2buffer:
            file2id2buffer[file]={}
        if not word_col in self.file2word_cols:
            self.file2word_cols[file]=word_col
        if word_col != self.file2word_cols[file]:
            raise Exception("word_col mismatch: failed to override "+str(self.file2word_cols[file])+" with "+str(word_col))

        if type(buffer)==list:

            if sent_id==None:
                sent_id=str(len(file2id2buffer[file]))

            # append to sentence, nmormally the sentence will be initially []
            if sent_id in file2id2buffer[file]:
                file2id2buffer[file][sent_id]+=buffer
            else:
                file2id2buffer[file][sent_id]=buffer
        else:
            format,my_open=self.guess_format(file)
            if format=="conll":
                with my_open(file, "r") as input:
                    sys.stderr.write("reading "+file+"\r")
                    # we strip all CoNLL comments and split at empty lines
                    sent_id=None
                    buffer=[]

                    for line in input:
                        line=line.strip()
                        if line.startswith("#"):
                            line=line[1:].strip()
                            if "=" in line:
                                fields=line.split("=")
                                if fields[0].strip()=="sent_id":
                                    sent_id=fields[1]
                        else:
                            if line=="":
                                if len(buffer)>0:
                                    self.add(file,word_col,sent_id=sent_id, buffer=buffer)
                                    buffer=[]
                            else:
                                if not "\t" in line:
                                    if file in file2id2buffer:
                                        file2id2buffer.pop(file)
                                    raise Exception("not a CoNLL/TSV format, line \""+line+"\" does not contain a tabulator")
                                else:
                                    fields=line.split("\t")
                                    buffer.append(fields)
                                    if not file in self.file2width:
                                        self.file2width[file]=len(fields)

                    if len(buffer)>0:
                        self.add(file,word_col,sent_id=sent_id, buffer=buffer)

            else:
                    raise Exception("Support for format "+format+" not implemented yet")

            sys.stderr.write("reading "+file+": "+str(len(file2id2buffer[file]))+" sentences\n")

        self.file2id2buffer=file2id2buffer

    def lower(self,files=None):
        """ can be specified for different input files """
        if files==None:
            files=self.file2id2buffer.keys()
        self.lcase_files=files

    def nopunct(self,files=None):
        """ can be specified for different input files """
        if files==None:
            files=self.file2id2buffer.keys()
        self.nopunct_files=files


    def print_parallel_data(self, format="fast_align"):
        """ write fast_align training data into a file """

        result=""
        if format=="fast_align":
            files=list(self.file2id2buffer.keys())
            if len(files)==0:
                raise Exception("please provide two texts for alignment")
            if len(files)==1:
                sys.stderr.write("warning: only one text given, we perform self-alignment\n")
                files.append(files[0])
            if len(files)>2:
                sys.stderr.write("warning: fast_align supports alignment between only two texts, restricting to "+files[0]+" and "+files[1])
                files=files[0:2]
            if len(files)==2:
                for sent_id in self.file2id2buffer[files[0]].keys():
                    pairs=[]

                    for file in files:
                        if sent_id in self.file2id2buffer[file]:
                            toks=self._get_toks(file, self.file2id2buffer[file][sent_id])
                            toks=" ".join(toks)
                            pairs.append(toks)
                        else:
                            break
                    if len(pairs)==len(files):
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
        if file in self.nopunct_files:
            src_toks=[ re.sub(r"[,.:;!?()\[\]{}\"\'\-\\/_]+","",tok) for tok in src_toks ]
        src_toks=[ tok if len(tok) > 0 else "_" for tok in src_toks ]
        src_toks=[ re.sub(r"\s+","_",tok) for tok in src_toks ]
        if file in self.lcase_files:
            src_toks = [ tok.lower() for tok in src_toks ]
        return src_toks

    def align(self):
        """ calls systran_align.Aligner """
        fw_path, bw_path=self._align()

        # the following line causes a segdump
        aligner=systran_align.Aligner(fw_path,bw_path)

        if len(self.file2id2buffer)!=2:
            raise Exception("we currently provide bilingual alignment only, we need two files")

        files=list(self.file2id2buffer.keys())

        for sent_id in self.file2id2buffer[files[0]]:

            src_buffer=self.file2id2buffer[files[0]][sent_id]
            src_toks=self._get_toks(files[0], src_buffer)

            if sent_id in self.file2id2buffer[files[1]]:
                tgt_buffer=self.file2id2buffer[files[1]][sent_id]
                tgt_toks=self._get_toks(files[1], tgt_buffer)

                alignment = aligner.align(src_toks,tgt_toks)
                print("# sent_id = "+sent_id)
                self.print_alignment(src_buffer,tgt_buffer,alignment, src_file=files[0], tgt_file=files[1])

            else:
                # unaligned
                print("# sent_id = "+sent_id)
                print("# text = "+" ".join(src_toks))
                output=[ row + ["?"]*self.file2width[files[1]] for row in src_buffer ]
                output=[ "\t".join(row) for row in output ]
                print("\n".join(output)+"\n")

        os.remove(fw_path)
        os.remove(bw_path)

    def print_alignment(self, src_buffer: list, tgt_buffer:list, alignments:dict, src_file=None, tgt_file=None):
        """ write CoNLL format
            src_buffer and tgt_buffer are one CoNLL buffer each that is position-aligned via alignments
        """

        if src_file in self.file2word_cols:
            print("# text:  "+" ".join([ row[self.file2word_cols[src_file]] for row in src_buffer ]))
        if tgt_file in self.file2word_cols:
            print("# trans: "+" ".join([ row[self.file2word_cols[tgt_file]] for row in tgt_buffer ]))

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

        src_width=len(src_buffer[0])
        tgt_width=len(tgt_buffer[0])

        tgts=[] # previously printed tgts
        for s,src_row in enumerate(src_buffer):

            anno=[str(s+1)]+src_row
            if self.ids==False:
                anno=anno=src_row

            if not s in src2tgt:
                anno+=["?"]*tgt_width
                print("\t".join(anno))
            else:
                for t in src2tgt[s]:
                    if not self.ids==False:
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
                            anno=["?"]+["?"]*src_width+[str(t+1)]+tgt_buffer[t]
                            if self.ids==False:
                                anno=["?"]*src_width+tgt_buffer[t]
                            print("\t".join(anno))
                            tgts.append(t)
                    anno=[str(s+1)]+["*"]*src_width
                    if self.ids==False:
                        anno=["*"]*src_width
        for t in range(len(tgt_buffer)):
            if not t in tgts:
                anno=["?"]+["?"]*src_width+[str(t+1)]+tgt_buffer[t]
                if self.ids==False:
                    anno=["?"]*src_width+tgt_buffer[t]
                print("\t".join(anno))
        print()

if not "-silent" in sys.argv or len(sys.argv)<=2:
    sys.stderr.write("synopsis: "+sys.argv[0]+" conll1[=col1] conll2[=col2] [-low] [-silent] [-noids] [-nopunct]\n")
    sys.stderr.write("  conlli    CoNLL file(s), must be sentence-aligned\n"+\
                     "  coli      column over which the alignment is to be performed, defaults to 1 (second column, WORD/FORM column in CoNLL-U)\n"+\
                     "  -low      perform alignment over lower case\n"+\
                     "  -nopunct  strip punctuation before doing alignment, helpful for whitespace tokenization\n"+\
                     "  -noids    suppress id generation (not recommended, breaks alignment of multi-word tokens)\n"+\
                     "  -silent   skip usage information\n"+\
                     "In the resulting CoNLL data, the following notations are used for n:m alignment:\n"+\
                     "   * (for source/conll1 annotations) m:1 the last aligned source word is aligned with the current target word\n"+\
                     "   ? (for source/conll1 annotations) 0:1 the current target word does not have a source alignment\n"+\
                     "   ? (for target/conll2 annotations) 1:0 the current source word does not have a target alignment\n"+\
                     "There is no special notation for 1:n alignments, the target/conll2 annotation is just repeated.\n"+\
                     "For n and m > 1, n:m alignments are represented as a series of m:1 and 1:n alignments.")

if len(sys.argv) >2:
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

    ids=True
    if "-noids" in sys.argv:
        sys.stderr.write("suppress ID generation\n")
        ids=False

    alignment=WordAligner(ids=ids)
    alignment.add(file1,col1)
    alignment.add(file2,col2)

    if "-low" in sys.argv:
        sys.stderr.write("lower case\n")
        alignment.lower()

    if "-nopunct" in sys.argv:
        sys.stderr.write("strip punctuation\n")
        alignment.nopunct()

    # print(alignment.print_parallel_data())
    alignment.align()
