import re,sys,os,traceback,json
from pprint import pprint

cue2sense2freq={}
senses=[]
for file in sys.argv[1:]:
    with open(file) as input:
        for line in input:
            data=json.loads(line)
            sense="|".join(sorted(set(data["Sense"])))
            if not sense in senses:
                senses.append(sense)
            if data["Type"]=="Explicit":
                cue=data["Connective"]["RawText"]
                if not cue in cue2sense2freq:
                    cue2sense2freq[cue]={ sense : 1 }
                elif not sense in cue2sense2freq[cue]:
                    cue2sense2freq[cue][sense] = 1
                else:
                    cue2sense2freq[cue][sense]+=1

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
        print('    <sem>\n      <chdt_relation sense="'+sense+'"', end="")
        if sense in cue2sense2freq[cue]:
            print(' freq="'+str(cue2sense2freq[cue][sense])+'"',end="")
        print("/>\n    </sem>")
    print("  </syn>\n</entry>")
print("</dimlex>")
