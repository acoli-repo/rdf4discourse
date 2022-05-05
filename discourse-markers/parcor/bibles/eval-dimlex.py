import os,sys,re,traceback,argparse,json
import unidecode

args=argparse.ArgumentParser(description="given an automatically induced discourse marker frequency lexicon (by ensemble.py) and a gazetteer, test and evaluate extraction parameters")
args.add_argument("induced", type=str, help="automatically induced discourse marker frequency inventory (JSON format, generated by ensemble.py)")
args.add_argument("gazetteer", type=str, help="reference gazetteer in TSV format, we assume the surface form is ")
args.add_argument("-col","--gaz_column", type=int, nargs="?", default=1, help="gazetteer column (for the relations, strings are supposed to be in first column), defaults to second column (1)")
args.add_argument("-exact", "--exact_match", action="store_true", help="if set, compare strings literally, by default we perform a comparison that is insensitive to spaces, capitalization and punctuation")
args.add_argument("-c", "--min_confidence", nargs="?", type=float, help="minimum confidence for induced dimlex entries, defaults to 0", default=0.0)
args.add_argument("-f", "--min_freq", type=int, nargs="?", help="minimum frequency for induced dimlex entries, defaults to 0", default=0)
args.add_argument("-r", "--min_rel", type=float,nargs="?",  help="minimum score for induced relations, defaults to 0",default=0.0)
args.add_argument("-s", "--min_score", type=float, nargs="?", help="minimum average score for induced dimlex entries, defaults to 0", default=0.0)
args.add_argument("-depth", "--recursion_limit", type=int, nargs="?", help="set maximum recursion depth in Python (not recommended)", default=None)
args.add_argument("-auto", "--auto_configure", action="store_true", help="if set, estimate optimal parameters using a relaxation method, prioritizing parameters with the highest variability; note that this is not guaranteed to lead to a global minimum")
args.add_argument("-mean","--mean", type=str, nargs="?", help="aggregate function for -auto optimization, defaults to average", default="average")

def do_normalize(string: str):
    return re.sub(r"[,.:;?()\[\]{}!\-_/\\\s0-9'\"]+","",unidecode.unidecode(string)).lower()

# means
def first(*objects):
    # return first argument
    if len(objects)==0:
        return 0
    if len(objects)==1:
        if type(objects[0])==list:
            return first(*(objects[0]))
        else:
            return float(objects[0])
    else:
        for o in objects:
            if type(o)==list:
                return first(*o)
            else:
                return float(o)

def last(*objects):
    # return last argument
    if len(objects)==0:
        return 0
    if len(objects)==1:
        if type(objects[0])==list:
            return last(*(objects[0]))
        else:
            return float(objects[0])
    else:
            o=objects[-1]
            if type(o)==list:
                return last(*o)
            else:
                return float(o)


def average(*objects):
    if len(objects)==0:
        return 0
    if len(objects)==1:
        if type(objects[0])==list:
            return average(*(objects[0]))
        else:
            return float(objects[0])
    else:
        sum=0
        for o in objects:
            if type(o)==list:
                sum+=average(*o)
            else:
                sum+=float(o)
        return sum/len(objects)

def harmonic(*objects):
    if len(objects)==0:
        return 0
    if len(objects)==1:
        if type(objects[0])==list:
            return harmonic(*(objects[0]))
        else:
            return float(objects[0])
    else:
        sum=0
        for o in objects:
            if isinstance(o,list):
                sum+=harmonic(*o)
            else:
                if o!=0:
                    sum+=1.0/float(o)
        if sum==0:
            return 0
        return len(objects)/sum


def geometric(*objects):
    if len(objects)==0:
        return 1.0
    if len(objects)==1:
        if type(objects[0])==list:
            return geometric(*(objects[0]))
        else:
            return float(objects[0])
    else:
        prod=1.0
        for o in objects:
            if isinstance(o,list):
                prod*=geometric(*o)
            else:
                if o!=0:
                    prod*=float(o)
        prod=abs(prod)
        return prod**(1.0/float(len(objects)))

# print([1,2,3],geometric(1,2,3))
# print([.1,.2,.3],geometric(.1,.2,.3))
# print([.1,.2,.3],geometric([.1,.2,[.3]  ]))

def eval(induced_cue2entry : dict, cue2rels : dict, normalize=False, min_conf=[0,1], min_freq=[0,1000], min_rel=[0,1], min_score=[0,1], mean=average):
    """ return f_dm and f_rel
        mean is the function used to aggregate over both
    """
    if type(min_conf) != list and type(min_freq!=list) and type(min_rel!=list) and type(min_score!=list):
        tp_dm=0
        fp_dm=0
        fn_dm=0

        # here rel scores are only calculated for correctly identified discourse markers
        tp_rel=0
        fp_rel=0
        fn_rel=0
        for cue,entry in induced_cue2entry.items():
            if normalize:
                cue=do_normalize(cue)
            cue=cue.strip()
            if cue!="":
                if entry["freq"] >= min_freq and entry["confidence"]>= min_conf and entry["avgscore"] >= min_score:
                    if not cue in cue2rels:
                        fp_dm+=1
                    else:
                        tp_dm+=1

                        rels="|".join(cue2rels[cue])
                        for rel in entry["rels"]:
                            true_positive=(rel in rels)
                            if not true_positive:
                                for r in cue2rels[cue]:
                                    if r in rel:
                                        true_positive=True
                                        break
                            if true_positive:
                                tp_rel+=1
                            else:
                                fp_rel+=1

                        rels="|".join(entry["rels"])
                        for r in cue2rels[cue]:
                            false_negative=not r in rels
                            if false_negative:
                                for rel in entry["rels"]:
                                    if rel in r:
                                        false_negative=False
                                        break
                            if false_negative:
                                fn_rel+=1

                    # old aggregate scores, taking dm identication into account
                    # false_positive=False
                    # for rel in entry["rels"]:
                    #     if not cue in cue2rels:
                    #         false_positive=True
                    #         break
                    #     if not rel in "|".join(cue2rels[cue]):
                    #         true_positive=False
                    #         for r in cue2rels[cue]:
                    #             if r in rel:
                    #                 true_positive=True
                    #         if not true_positive:
                    #             false_positive=True
                    #             break
                    # if false_positive:
                    #     fp_rel+=1
                    # else:
                    #     tp_rel+=1
        fn_dm=len(cue2rels)-tp_dm

        p_dm=tp_dm/max(1,tp_dm+fp_dm)
        r_dm=tp_dm/max(1,tp_dm+fn_dm)
        f_dm=0
        if p_dm+r_dm != 0:
            f_dm = 2*p_dm*r_dm/(p_dm+r_dm)

        p_rel=tp_rel/max(1,tp_rel+fp_rel)
        r_rel=tp_rel/max(1,tp_rel+fn_rel)
        f_rel=0
        if p_rel+r_rel != 0:
            f_rel = 2*p_rel*r_rel/(p_rel+r_rel)

        sys.stderr.write("min_conf="+str(min_conf)+"\tmin_freq="+str(min_freq)+"\tmin_rel="+str(min_rel)+"\tmin_score="+str(min_score)+\
                         "\ttp_dm\t"+str(tp_dm)+"\tp_dm\t"+str(p_dm)+"\tr_dm\t"+str(r_dm)+"\tf_dm\t"+str(f_dm)+"\t"+\
                         "\ttp_rel\t"+str(tp_rel)+"\tp_rel\t"+str(p_rel)+"\tr_rel\t"+str(r_rel)+"\tf_rel\t"+str(f_rel)+"\n")
        sys.stderr.flush()
        return f_dm,f_rel

    else:
        if type(min_conf)!=list:
            return eval(induced_cue2entry, cue2rels, normalize=normalize, min_conf=[min_conf,min_conf], min_freq=min_freq, min_rel=min_rel, min_score=min_score, mean=mean)
        elif type(min_freq)!=list:
            return eval(induced_cue2entry, cue2rels, normalize=normalize, min_conf=min_conf, min_freq=[min_freq,min_freq], min_rel=min_rel, min_score=min_score, mean=mean)
        elif type(min_rel)!=list:
            return eval(induced_cue2entry, cue2rels, normalize=normalize, min_conf=min_conf, min_freq=min_freq, min_rel=[min_rel,min_rel], min_score=min_score, mean=mean)
        elif type(min_score)!=list:
            return eval(induced_cue2entry, cue2rels, normalize=normalize, min_conf=min_conf, min_freq=min_freq, min_rel=min_rel, min_score=[min_score,min_score], mean=mean)
        else: # all params are in a range
            # mid_dm,mid_rel = eval(induced_cue2entry, cue2rels, normalize=normalize, \
            #     min_conf=average(min_conf[0],min_conf[-1]), \
            #     min_freq=average(min_freq[0], min_freq[-1]), \
            #     min_rel=average(min_rel[0], min_freq[-1]), \
            #     min_score=average(min_score[0],min_score[-1]))
            updated=False
            mini_dm,mini_rel= eval(induced_cue2entry, cue2rels, normalize=normalize, min_conf=min_conf[0], min_freq=average(min_freq), min_rel=average(min_rel), min_score=average(min_score), mean=mean)
            if min_conf[0]!=min_conf[-1]:
                maxi_dm,maxi_rel= eval(induced_cue2entry, cue2rels, normalize=normalize, min_conf=min_conf[-1], min_freq=average(min_freq), min_rel=average(min_rel), min_score=average(min_score), mean=mean)
                if mini_dm==maxi_dm and mini_rel==maxi_rel:
                    min_conf=[min_conf[0], min_conf[0]]
                elif mean(maxi_dm,maxi_rel)>mean(mini_dm,mini_rel):
                    min_conf=[average(min_conf[0],min_conf[0],min_conf[-1]), min_conf[-1]]
                else:
                    min_conf=[min_conf[0], average(min_conf[0],min_conf[-1],min_conf[-1])]
                updated=True
            if min_freq[0]!=min_freq[-1]:
                mini_dm,mini_rel= eval(induced_cue2entry, cue2rels, normalize=normalize, min_freq=min_freq[0], min_conf=average(min_conf), min_rel=average(min_rel), min_score=average(min_score), mean=mean)
                maxi_dm,maxi_rel= eval(induced_cue2entry, cue2rels, normalize=normalize, min_freq=min_freq[-1], min_conf=average(min_conf), min_rel=average(min_rel), min_score=average(min_score), mean=mean)
                if mini_dm==maxi_dm and mini_rel==maxi_rel:
                    min_freq=[min_freq[0], min_freq[0]]
                elif mean(maxi_dm,maxi_rel)>mean(mini_dm,mini_rel):
                    new_min=int(average(min_freq[0],min_freq[0],min_freq[-1]))
                    if new_min!=min_freq[0]:
                        min_freq=[new_min, int(min_freq[-1])]
                        updated=True
                else:
                    new_max=int(average(min_freq[0],min_freq[-1],min_freq[-1]))
                    if new_max!=min_freq[-1]:
                        min_freq=[min_freq[0], new_max]
                        updated=True

            if min_rel[0]!=min_rel[-1]:
                mini_dm,mini_rel= eval(induced_cue2entry, cue2rels, normalize=normalize, min_rel=min_rel[0], min_conf=average(min_conf), min_freq=average(min_freq), min_score=average(min_score), mean=mean)
                maxi_dm,maxi_rel= eval(induced_cue2entry, cue2rels, normalize=normalize, min_rel=min_rel[-1], min_conf=average(min_conf), min_freq=average(min_freq), min_score=average(min_score), mean=mean)
                if mini_dm==maxi_dm and mini_rel==maxi_rel:
                    min_rel=[min_rel[0], min_rel[0]]
                elif mean(maxi_dm,maxi_rel)>mean(mini_dm,mini_rel):
                    min_rel=[average(min_rel[0],min_rel[0],min_rel[-1]), min_rel[-1]]
                else:
                    min_rel=[min_rel[0], average(min_rel[0],min_rel[-1],min_rel[-1])]
                updated=True
            if min_score[0]!=min_score[-1]:
                mini_dm,mini_score= eval(induced_cue2entry, cue2rels, normalize=normalize, min_score=min_score[0], min_conf=average(min_conf), min_freq=average(min_freq), min_rel=average(min_rel), mean=mean)
                maxi_dm,maxi_score= eval(induced_cue2entry, cue2rels, normalize=normalize, min_score=min_score[-1], min_conf=average(min_conf), min_freq=average(min_freq), min_rel=average(min_rel), mean=mean)
                if mini_dm==maxi_dm and mini_score==maxi_score:
                    min_score=[min_score[0], min_score[0]]
                elif mean(maxi_dm,maxi_score)>mean(mini_dm,mini_score):
                    min_score=[average(min_score[0],min_score[0],min_score[-1]), min_score[-1]]
                else:
                    min_score=[min_score[0], average(min_score[0],min_score[-1],min_score[-1])]
                updated=True
            if not updated:
                return mini_dm,mini_rel
            else:
                return eval(induced_cue2entry, cue2rels, normalize=normalize, min_score=min_score, min_conf=min_conf, min_freq=min_freq, min_rel=min_rel, mean=mean)

args=args.parse_args()

means={ "average": average, "harmonic" : harmonic, "geometric": geometric, "first": first, "last": last }

if args.mean in means:
    args.mean=means[args.mean]
else:
    raise Exception("unknown mean \""+args.mean+", choose one of "+", ".join(means))

if args.recursion_limit!= None and args.recursion_limit>1000: # python default
    sys.setrecursionlimit(args.recursion_limit)

induced_cue2entry=None
with open(args.induced) as input:
    induced_cue2entry=json.load(input)

for cue in induced_cue2entry.keys():
    induced_cue2entry[cue]["rels"] = { re.sub(r"[^a-zA-Z\.]","", rel) : score for rel,score in induced_cue2entry[cue]["rels"].items() }

#print(induced_cue2entry)

cue2rels={}
with open(args.gazetteer) as input:
    for line in input:
        line=line.strip()
        if len(line)>0 and not line[0] in "?#" and "\t" in line:
            fields=line.split("\t")
            cue=fields[0]
            if '"' in cue:
                cue=cue.split('"')[1]
            elif cue.startswith("'"):
                cue=cue.split("'")[1]
            if not args.exact_match:
                cue=do_normalize(cue)
            cue=cue.strip()
            if cue!="":
                rels=re.sub(r"[\"']","",fields[args.gaz_column])
                if cue in cue2rels:
                    cue2rels[cue]=sorted(set(cue2rels[cue]+rels.split("|")))
                else:
                    cue2rels[cue]=sorted(set(rels.split("|")))

if args.auto_configure:
    print(eval(induced_cue2entry, cue2rels, normalize=not args.exact_match, mean=args.mean))
else:
    print(eval(induced_cue2entry, cue2rels, normalize=not args.exact_match, min_conf=args.min_confidence, min_freq=args.min_freq, min_rel=args.min_rel, min_score=args.min_score, mean=args.mean))
