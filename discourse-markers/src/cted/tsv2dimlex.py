import re,sys,os,traceback
from pprint import pprint

cue2sense2freq={}
senses=[]
for line in sys.stdin:
        line=line.strip()
        fields=line.split("\t")
        if len(fields)>2:
            cue=fields[1]
            sense=fields[2]
            freq=int(fields[0])
            if "|" in sense:
                freq=0  #   no unambiguous reading
            for sense in sense.split("|"):
                if not cue in cue2sense2freq:
                    cue2sense2freq[cue]={ sense : freq }
                elif not sense in cue2sense2freq[cue]:
                    cue2sense2freq[cue][sense] = freq
                else:
                    cue2sense2freq[cue][sense]+=freq
                if not sense in senses:
                    senses.append(sense)

sys.stderr.write("relations:\n"+"\n".join(sorted(set("|".join(senses).split("|"))))+"\n\n")
sys.stderr.flush()

# write xml to stdout
print("""<?xml version='1.0' encoding='UTF-8'?>
<dimlex>""")
for nr,cue in enumerate(sorted(cue2sense2freq.keys())):
    cue=cue.strip()
    print('<entry id="'+str(nr+1)+'" word="'+cue+'">')
    print('  <orths>\n    <orth>\n      <part>'+cue+'</part>\n    </orth>\n  </orths>')
    print('  <syn>')
    for sense in sorted(set("|".join(cue2sense2freq[cue]).split("|"))):
        print('    <sem>\n      <pdtb3_relation sense="'+sense+'"', end="")
        if sense in cue2sense2freq[cue]:
            print(' freq="'+str(cue2sense2freq[cue][sense])+'"',end="")
        print("/>\n    </sem>")
    print("  </syn>\n</entry>")
print("</dimlex>")
