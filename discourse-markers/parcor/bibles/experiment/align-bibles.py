import sys,os,re
import gzip, bz2
import xml.etree.ElementTree as ET
import tempfile
from pprint import pprint
import systran_align

""" provide word alignments for bibles in CES/XML and TSV formats
    args: file1 file2
    output as CoNLL file to stdout, for every source line
    requires the use of identical verse IDs in both resources
"""

class Bible:
    """ for us, a Bible is a list of pairs of verse IDs and the corresponding lines,
        no restriction in terms of content, so, feel free to use this for anything
        non-biblical ;) However, it is important to keep consistent verse IDs across
        different editions.
     """

    def __init__(self):
         self.file2verse2line={}

    def guess_format(self, file:str):
        """ return format and open method """
        name=file.lower()

        my_open=open
        if name.endswith(".gz"):
            name=name[0:-3]
            my_open=gzip.open
        if name.endswith(".bz2"):
            name=name[0:-4]
            my_open=bz2.open

        if name.endswith("xml"):
            return "xml",my_open
        if name.endswith("tsv"):
            return "tsv",my_open
        with my_open(file,"r") as input:
            for line in input:
                line=line.strip()
                if line.startswith("<"):
                    return "xml", my_open
                if not line.startswith("#") and not line=="":
                    if "\t" in line:
                        return "tsv", my_open
        return name.split(".")[-1], my_open

    def add(self, file:str, verse_id=None, line=None):
        """ add a file that contains a monolingual bible edition, note that these are later identified by their file name """
        file2verse2line=self.file2verse2line
        if not file in file2verse2line:
            file2verse2line[file]={}
        if not None in [verse_id,line]:
                # add a line
                if not verse_id in file2verse2line[file]:
                                        file2verse2line[file][verse_id]=line
                                        sys.stderr.write("reading "+file+": "+str(len(file2verse2line[file]))+" verses\r")
                else:
                                        file2verse2line[file][verse_id]+=" "+line
                return
        else: # add a file
                format,my_open=self.guess_format(file)
                if format=="tsv":
                    # we expect verse_id<TAB>tok1<SPACE>tok2<SPACE>...
                    with my_open(file, "r") as input:
                        sys.stderr.write("reading "+file+"\r")
                        for line in input:
                            line=line.strip()
                            if not line.startswith("#") and not line=="":
                                fields=line.split("\t")
                                if len(fields)==2:
                                    self.add(file,fields[0],fields[1].strip())

                elif format=="xml":
                    # we expect a CES-compliant file
                    doc = ET.parse(my_open(file))
                    for seg in doc.findall(".//seg"):   # note that XPath filtering for attribute values doesn't work
                        try:
                            self.add(file,seg.get("id"),seg.text.strip())
                        except:
                            pass

                else:
                    raise Exception("Support for format "+format+" not implemented yet")

        sys.stderr.write("reading "+file+": "+str(len(file2verse2line[file]))+" verses\n")
        self.file2verse2line=file2verse2line

    def tokenize(self, files=None):
        if files==None:
            files=self.file2verse2line.keys()
        for file in files:
            for verse in self.file2verse2line[file]:
                line= self.file2verse2line[file][verse]
                line=re.sub(r"([!?.;:,()\"'\./])",r" \1 ",line)
                line=re.sub(r"\s+"," ",line).strip()
                self.file2verse2line[file][verse]=line

    def lower(self,files=None):
        if files==None:
            files=self.file2verse2line.keys()
        for file in files:
            for verse in self.file2verse2line[file]:
                line= self.file2verse2line[file][verse].lower()
                self.file2verse2line[file][verse]=line

    def print_parallel_data(self, format="fast_align"):
        result=""
        if format=="fast_align":
            files=list(self.file2verse2line.keys())
            if len(files)==0:
                raise Exception("please provide two texts for alignment")
            if len(files)==1:
                sys.stderr.write("warning: only one text given, provide training data for self-alignment\n")
                files.append(files[0])
            if len(files)>2:
                sys.stderr.write("warning: fast_align supports alignment between only two texts, restricting to "+files[0]+" and "+files[1])
                files=files[0:2]
            for verse in self.file2verse2line[files[0]]:
                verses=[]
                for file in files:
                    if verse in self.file2verse2line[file]:
                        verses.append(self.file2verse2line[file][verse])
                    else:
                        break
                if len(verses)==2:
                    result+=" ||| ".join(verses)+"\n"
        else:
            raise Exception("unsupported output format \""+format+"\"")

        return result

    def replace(self, src,tgt="", files=None):
        if files==None:
            files=self.file2verse2line.keys()
        for file in files:
            for verse in self.file2verse2line[file]:
                line=self.file2verse2line[file][verse]
                line=re.sub(src,tgt,line)
                line=re.sub(r"\s+"," ",line).strip()
                self.file2verse2line[file][verse]=line

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

    def align(self):
        """ calls systran_align.Aligner """
        fw_path, bw_path=self._align()
        aligner=systran_align.Aligner(fw_path,bw_path)

        if len(self.file2verse2line)!=2:
            raise Exception("we currently provide bilingual alignment only, we need two files")

        files=list(self.file2verse2line.keys())

        for verse in self.file2verse2line[files[0]]:
            if verse in self.file2verse2line[files[1]]:
                src=self.file2verse2line[files[0]][verse].split()
                tgt=self.file2verse2line[files[1]][verse].split()
                alignment = aligner.align(src,tgt)
                self.print_alignment(src,tgt,alignment)

        os.remove(fw_path)
        os.remove(bw_path)

    def print_alignment(self,src: list, tgt:list, alignments:dict):
        """ write CoNLL format """

        print("# text: "+" ".join(src))
        print("# translation: "+ " ".join(tgt))
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

        # print(src2tgt)
        # print(tgt2src)
        # print(src)
        # print(tgt)

        tgts=[] # oreviously printed tgts
        for s,word in enumerate(src):
            anno=[str(s+1),word]
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
                        anno.append(tgt[t])
                        tgts.append(t)
                        print("\t".join(anno))
                        while(t+1<len(tgt) and not t+1 in tgts and not t+1 in tgt2src):
                            t=t+1
                            print("_\t_\t"+str(t+1)+"\t"+tgt[t])
                            tgts.append(t)
                    anno=[anno[0],"*"]
        for t in range(len(tgt)):
            if not t in tgts:
                print("_\t_\t"+str(t+1)+"\t"+tgt[t])
        print()

sys.stderr.write("synopsis: "+sys.argv[0]+" bib1 bib2 [-low] [-tok]\n")
sys.stderr.write("  bibi      bible in CES/XML or TSV format\n"+\
                 "  -low      lower case\n"+\
                 "  -tok      tokenize\n"+\
                 "  -no-punct remove everything matching [^a-zA-ZäöüÄÖÜß]")

bible=Bible()
bible.add(sys.argv[1])
bible.add(sys.argv[2])

if "-tok" in sys.argv:
    sys.stderr.write("tokenize\n")
    bible.tokenize()

if "-low" in sys.argv:
    sys.stderr.write("lower case\n")
    bible.lower()

if "-no-punct" in sys.argv:
    sys.stderr.write("remove punctuation\n")
    bible.replace(r"[^a-zA-Z0-9öäüÖÄÜß\s]+", "")

#print(bible.print_parallel_data())
bible.align()
