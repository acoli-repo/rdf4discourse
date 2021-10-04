# given parallel annotation, induce annotations
import sys,os,re,traceback
import argparse
from pprint import pprint
from io import StringIO
from copy import copy, deepcopy

def induce_dimlex(stream, words_col, dm_confidence_col=None, dm_col=None,rel_confidence_col=None, min_freq=10, min_conf=0.25):

    # retrieve all potential discourse markers
    cues=[]

    sentences=stream.read().split("\n\n")
    for sentence in sentences:
        sentence = sentence.split("\n")
        sentence = [ row.strip().split("\t") for row in sentence if "\t" in row and not row.strip().startswith("#") ]
        cand=""
        for nr,row in enumerate(sentence):
            if nr==0 or sentence[nr-1][dm_col] != row[dm_col]:
                if len(cand)>0:
                    if not cand in cues:
                        cues.append(cand)
                        sys.stderr.write("dimlex induction: "+str(len(cues))+" candidates\r")
                cand=""
            if row[dm_col]!="_":
                cand=(cand+" "+row[words_col]).strip()
        if len(cand)>0:
            if not cand in cues:
                cues.append(cand)
    sys.stderr.write("dimlex induction: "+str(len(cues))+" candidates\n")


    # we now have a list of all (potential) discourse markers
    # we record all scores
    word2cues={}
    for cue in cues:
        word = cue.split()[0]
        if not word in word2cues:
            word2cues[word]=[cue]
        else:
            word2cues[word].append(cue)

    cue2total={ cue: 0 for cue in cues }
    cue2scores={ cue: [] for cue in cues }       # these are recorded as a *list*
    cue2rel2scores={ cue: {}  for cue in cues}   # -"-
    sents=0
    for sentence in sentences:
        sents+=1
        sys.stderr.write("dimlex induction: "+str(sents)+" sentences\r")
        sentence = sentence.split("\n")
        sentence = [ row.strip().split("\t") for row in sentence if "\t" in row and not row.strip().startswith("#")  ]
        words=[row[words_col] for row in sentence ]
        for nr,row in enumerate(sentence):
            if words[nr] in word2cues:
                text=" "+" ".join(words[nr:])+" "
                for cue in word2cues[words[nr]]:
                    if text.startswith(" "+cue+" ") and not row[dm_col] != "?" : # do not count alignment errors
                        cue2total[cue]+=1

                        # simplification: we only consider annotations of the first word
                        if row[dm_col] not in [ "_" , "?" ]:

                            cue2scores[cue].append(float(row[dm_confidence_col]))
                            rel_score=float(row[rel_confidence_col])
                            rels=row[dm_col].split("|")
                            rel_score=rel_score/len(rels)
                            for rel in rels:
                                if not rel in cue2rel2scores[cue]:
                                    cue2rel2scores[cue][rel]=[rel_score]
                                else:
                                    cue2rel2scores[cue][rel].append(rel_score)
    sys.stderr.write("dimlex induction: "+str(sents)+" sentences\n")

    # now we aggregate
    rels=0
    dimlex={ }   # for every cue, we have confidence scores and *all* relation scores
    for cue in cues:
        if cue2total[cue]>min_freq and len(cue2scores[cue])/cue2total[cue] > min_conf:
            dimlex[cue]= {}

            dimlex[cue]["freq"] = cue2total[cue]

            dimlex[cue]["confidence"] = len(cue2scores[cue])/cue2total[cue]

            sum_score=0
            for score in cue2scores[cue]:
                sum_score+=score
            dimlex[cue]["avgscore"]=sum_score/len(cue2scores[cue])

            rel2avg={}
            for rel in cue2rel2scores[cue]:
                rels+=1
                sum=0
                for score in cue2rel2scores[cue][rel]:
                    sum+=score
                rel2avg[rel] = sum/len(cue2rel2scores[cue][rel])
            dimlex[cue]["rels"]= rel2avg
            sys.stderr.write("dimlex induction: "+str(sents)+" relations\r")

    sys.stderr.write("dimlex induction: "+str(sents)+" relations\n")

    return dimlex

#    raise Exception("discourse marker induction not yet implemented")

def _predict(row : list, ensemble_cols: list, dm_threshold=0.0, dimlex_entry=None, conf_threshold=-1.0):
        """ row is a single CoNLL line, split at \t
        returns probability of row encoding a discourse marker, top senses, and top score
        if a dimlex entry is given, use dimlex information for disambiguation
        however, we do not override ensemble scores

        conf_threshold means that we only annotate if this value is exceeded
        """

        fields=row
        pred=ensemble_cols

        senses=[]
        dm_score=0.0
        top_senses="_"
        top_score=0.0
        if pred!=None:
            dm_true=0
            dm_total=0
            sense2positives={}

            for p in pred:
                if fields[p] == "_":
                    dm_total+=1
                elif fields[p]!= "?":
                    dm_true+=1
                    dm_total+=1
                    for sense in fields[p].split("|"):
                        if not sense in senses:
                            senses.append(sense)
                            if not sense in sense2positives:
                                sense2positives[sense]=0

            dm_score=dm_true/max(1,dm_total)

            if dm_true>max(dm_threshold,0.0): # and (conf_threshold<=0 or (dimlex_entry!=None and dimlex_entry["confidence"]>conf_threshold)):
                for p in pred:
                    if not fields[p] in ["_","?"]:
                        positive=set(fields[p].split("|"))
                        for sense in senses:
                            if sense in positive:
                                sense2positives[sense]+=1
                sense2score= { sense : sense2positives[sense]/dm_true for sense in senses }
                top_score=max(sense2score.values())
                sense2score= { sense : score for sense,score in sense2score.items() if score==top_score }

                # disambiguate using dimlex
                if len(sense2score)>1 and dimlex_entry!=None:
                    # print(sense2score)
                    sense2score= dict( (sense,dimlex_entry["rels"][sense]) if sense in dimlex_entry["rels"] else (sense , 0) for sense,_ in sense2score.items() )
                    # print(sense2score)
                    sense2score= { sense : score for sense,score in sense2score.items() if score==max(sense2score.values())}
                    #print(sense2score)

                # predict top sense(s)
                top_senses="|".join(sorted(sense2score.keys()))

        return dm_score, top_senses, top_score

def _apply_dimlex(buffer, dimlex, words_col):
    """ buffer is a list of conll rows for one sentence as one string, no comments, no line breaks, no gaps
        return longest matching dimlex entry for every row """
    row2cue=[None]*len(buffer)
    words=[ row.split("\t")[words_col] for row in buffer ]
    for nr,w in enumerate(words):
        if w in dimlex: # this is a hack
            text=" "+" ".join(words[nr:])+" "

            # we annotate the longest match
            for cue in dimlex:
                if cue.startswith(w):
                    if text.startswith(" "+cue+" "):
                        for x in range(len(cue.split())):
                            if row2cue[x+nr]==None or len(row2cue[x+nr].split()) > len(cue.split()):
                                row2cue[x+nr]=cue

    result=[]
    for cue in row2cue:
        if cue in dimlex:
            result.append(dimlex[cue])
        else:
            result.append(None)
    return result

def _annotate_buffer(buffer: list, pred=None, eval=None, dimlex=None, words_col=1, pred_threshold=0.0, eval_threshold=0.0, conf_threshold=-1.0, output=sys.stdout, slim_output=False):
    """ buffer is a list of conll rows for one sentence as one string, no comments, no line breaks, no gaps
        add three columns for pred predictions (dm probability, top relations, top relation score)
        add three more columns for eval (or three "_" if not specified)
        write results to output

        if eval is specified:
            return values are dm_tp, dm_fp, rel_tp, rel_fp, fn, tn, i.e.,
            rel_ predicted discourse relation is (not) [contained in] gold discourse relations
            dm_ predicted discourse cue is (not) gold discourse cue
            _tp: true positives (dm_tp: predicted=gold, rel_tp: *all* senses contained in gold sense)
            _fp: false positives (predicted, but no _tp)
            fn: false negatives (not predicted, but in gold; rel_fn=dm_fn)
            tn: true negatives (not predicted, not in gold; rel_fn=dm_fn)

        for evaluation, we only count gold annotations if these there is a clear alignment
    """

    dm_tp, dm_fp, rel_tp, rel_fp, fn, tn = ([0]*6)

    row2dimlex=[None]*len(buffer)
    if dimlex!=None:
        row2dimlex=_apply_dimlex(buffer, dimlex, words_col)

    for nr,line in enumerate(buffer):
        fields=line.split("\t")

        dm_score, top_senses, top_score=_predict(fields, pred, dm_threshold=pred_threshold, dimlex_entry=row2dimlex[nr], conf_threshold=conf_threshold)
        if eval!=None:
            ev_score, ev_senses, ev_score=_predict(fields, eval, dm_threshold=eval_threshold, conf_threshold=conf_threshold)
            if ev_senses=="_":
                evs=sorted(set([ fields[e] for e in eval ]))
                if len(evs)==1 and evs[0]=="?":
                    ev_senses="?"
        else:
            ev_score, ev_senses, ev_score="_","_","_"

        if eval!=None:
            if ev_senses!="?":
                if top_senses=="_":
                    if ev_senses=="_":
                        tn+=1
                    else:
                        fn+=1
                else:
                    if ev_senses=="_":
                        dm_fp+=1
                    else:
                        dm_tp+=1

                    # relationals
                    true_positive=True
                    for sense in top_senses.split("|"):                             # cond (1)
                        if not sense in ev_senses:
                            # we allow an ev sense to be more generic, i.e.
                            # pred COMPARISON.Contrast vs. gold COMPARISON.Contrast :   tp (trivial)
                            # pred COMPARISON.Contrast vs. gold COMPARISON :            tp (cond 2)
                            # pred COMPARISON.Concession vs. gold COMPARISON.Contrast:  fp (trivial)
                            # pred COMPARISON          vs. gold COMPARISON.Contrast :   tp (cond1)
                            # pred COMPARISON          vs. COMPARISON|TEMPORAL :        tp (cond1)
                            # pred COMPARISON|TEMPORAL vs. COMPARISON:                  fp (viol cond 1)
                            # pred COMPARISON          vs. _:                           fp (trivial)
                            false_positive=True
                            for esense in ev_senses.split("|"):
                                if esense in sense:                                 # cond (2)
                                    false_positive=False
                                    break
                            if false_positive:
                                true_positive=False
                                break
                    if true_positive:
                        rel_tp+=1
                    else:
                        rel_fp+=1

        if slim_output:
                tmp=[]
                for x in range(len(fields)):
                    if x==words_col or (pred!=None and x in pred) or (eval!=None and x in eval):
                        tmp.append(fields[x])
                fields=tmp

        fields+=[str(dm_score),top_senses,str(top_score)]
        fields+=[str(ev_score),ev_senses,str(ev_score)]

        output.write("\t".join(fields)+"\n")
        output.flush()
        return dm_tp, dm_fp, rel_tp, rel_fp, fn, tn

def annotate(stream, pred=None, eval=None, dimlex=None, pred_threshold=0.0, conf_threshold=-1.0, eval_threshold=0.0, words_col=1, output=sys.stdout, slim_output=False):
    """ annotate a CoNLL stream, annotate two columns for pred predictions, if eval!=None, annotate two more columns for eval predictions """
    buffer=[]
    stream.seek(0)
    toks=0
    scores=[0]*6
    # dm_tp, dm_fp, rel_tp, rel_fp, fn, tn = ([0]*6)
    for line in stream:
        line=line.strip()
        if line.startswith("#"):
            output.write(line+"\n")
        elif line=="":
            if len(buffer)>0:
                scores=[ score+delta for score,delta in \
                    zip(scores,\
                        _annotate_buffer(buffer,pred, eval=eval, dimlex=dimlex, pred_threshold=pred_threshold, eval_threshold=eval_threshold, conf_threshold=conf_threshold, output=output, slim_output=slim_output)\
                    ) ]
                #dm_tp, dm_fp, rel_tp, rel_fp, fn, tn += \
                toks+=len(buffer)
                sys.stderr.write("ensemble prediction: "+str(toks)+" tokens\r")
                buffer=[]
                output.write("\n\n")
                output.flush()
        else:
            buffer.append(line)
    if len(buffer)>0:
        #dm_tp, dm_fp, rel_tp, rel_fp, fn, tn += \
        scores=[ score+delta for score,delta in \
                zip(scores,\
                    _annotate_buffer(buffer,pred, eval=eval, dimlex=dimlex, pred_threshold=pred_threshold, eval_threshold=eval_threshold, conf_threshold=conf_threshold, output=output, slim_output=slim_output)\
                ) ]
        toks+=len(buffer)
        output.write("\n\n")
    sys.stderr.write("ensemble prediction: "+str(toks)+" tokens\n")
    output.flush()

    dm_tp, dm_fp, rel_tp, rel_fp, fn, tn = scores

    if pred!=None and len(pred)>0 and eval!=None and len(eval)>0:
        # print eval to stderr
        total=dm_tp+dm_fp+tn+fn

        acc_dm=(dm_tp+tn)/total
        acc_rel=(rel_tp+tn)/total

        sys.stderr.write("predicted dm\tgold dm\ttp\t|\tacc_dm\tp_dm\tr_dm\tf_dm\t|\tacc_r\tp_r\tr_r\tf_r\n")

        sys.stderr.write(str(dm_tp+dm_fp)+"\t") # predicted discourse markers
        sys.stderr.write(str(dm_tp+fn)+"\t")    # gold discourse markers
        sys.stderr.write(str(dm_tp)+"\t")       # true positives
        sys.stderr.write("|\t")

        # dm scores
        prec=dm_tp/(dm_tp + dm_fp)
        rec=dm_tp/(dm_tp + fn)
        f=2*prec*rec/(prec+rec)

        sys.stderr.write(str(acc_dm)+"\t")      # accuracy (discourse marker)
        sys.stderr.write(str(prec)+"\t")        # precision (discourse marker)
        sys.stderr.write(str(rec)+"\t")         # recall (discourse marker)
        sys.stderr.write(str(f)+"\t")           # f1 (discourse marker)
        sys.stderr.write("|\t")

        # rel scores
        prec=rel_tp/(rel_tp + rel_fp)
        rec=rel_tp/(rel_tp + fn)
        f=2*prec*rec/(prec+rec)
        sys.stderr.write(str(acc_rel)+"\t")     # accuracy (relation)
        sys.stderr.write(str(prec)+"\t")        # precision (relation)
        sys.stderr.write(str(rec)+"\t")         # recall (relation)
        sys.stderr.write(str(f)+"\t")           # f1 (relation)
        sys.stderr.write("\n")
        sys.stderr.flush()

#
# aux
#######

def get_all_sublists(l: list):
    """ return non-empty lists only """
    l=sorted(set(l))
    result=[l]
    if len(l)>1:
        for nr in range(len(l)):
            result+=get_all_sublists(l[0:nr]+l[nr+1:])
    result= { str(l): l for l in result }
    result=list(result.values())
    return result

#
# setup
#########

args=argparse.ArgumentParser(description="if a text has been annotated by multiple tools according to the same schema, run a number of bootstrapping experiments")
args.add_argument("input", type=str, help="CoNLL file to read from, if omitted, read from stdin",default=None)
args.add_argument("-p", "--predictor", type=int, nargs="+", action="extend", help="columns that contain the invidual input predictions")
args.add_argument("-e", "--evaluator", type=int, nargs="*", action="extend", help="columns that constitute an ensemble that the predictor is evaluated against")
args.add_argument("-dimlex", "--dimlex_mode", action="store_true", help="instead of doing annotation, bootstrap a discourse marker inventory, note that this requires input to be a file")
args.add_argument("-iterate", "--self_supervision", action="store_true", help="bootstrap a discourse marker inventory, then use it to re-annotate the input, note that this requires input to be a file")
args.add_argument("-w", "--words_col", type=int, default=1, help="WORDS/FORM column, needed for -iterate/--self_supervision")
args.add_argument("-th", "--pred_threshold", type=float, default=0.4, help="threshold for predictions: predict only if probability for a discourse marker is at least at this value, 0.4 is a good guess")
args.add_argument("-c", "--min_confidence", type=float, default=0.4, help="threshold for predictions: predict only if dimlex confidence >= min_confidence, in iterative mode, only")
    # TODO: --min_confidence is not working yet, I guess dimlex linking fails?
args.add_argument("-eth", "--eval_threshold", type=float, default=None, help="threshold for evaluation, if evaluated against a single target annotation, defaults to --pred_threshold")
args.add_argument("-slim", "--slim_output", action="store_true", help="return only --words_col, --predictor and --evaluator columns, as well as their predictions")
args.add_argument("-silent", "--no_output", action="store_true", help="return only scores, no annotations")
args.add_argument("-auto", "--test_all_combinations", action="store_true", help="if set, explore all possible combinations, overrides all other arguments except for input, -p, -e, -w")

args=args.parse_args()

confs=[args]

if args.test_all_combinations:
    confs=[]
    es = args.predictor
    if args.evaluator!=None and len(args.evaluator)>0:
        es=args.evaluator
    for e in es:
        myp=copy(args.predictor)
        if e in myp:
            myp.remove(e)
        for p in get_all_sublists(myp):
            conf=deepcopy(args)
            conf.evaluator=[e]
            conf.predictor=p
            conf.test_all_combinations=False
            confs.append(conf)

for conf in confs:

    if conf.eval_threshold==None:
        conf.eval_threshold=conf.pred_threshold

    if os.path.exists(str(conf.input)):
        conf.input=open(conf.input,"r")
    else:
        if conf.input!=None:
            sys.stderr.write("could not find input file \""+input+"\", ")
        if len(confs)>1:
            sys.stderr.write("-auto mode requires a file to read from\n")
            sys.exit(1)
        sys.stderr.write("reading from stdin\n")
        conf.input=sys.stdin

    overlap=[]
    if conf.evaluator==None:
        conf.evaluator=[]
    overlap=[ p for p in conf.predictor if p in conf.evaluator ]
    if len(overlap)>0:
        raise Exception("overlap between predictor and evaluator: "+", ".join(overlap))

    #
    # first annotation round
    ##########################
    # adds four columns to conll file:
        # predictor confidence that it is a discourse marker
        # predictor annotation(s with confidence)
        # evaluator confidence that it is a discourse marker
        # evaluator annotation(s with confidence)
    buffer=sys.stdout
    if conf.self_supervision or conf.dimlex_mode or conf.no_output:
        buffer=StringIO()

    sys.stderr.write(str(conf.evaluator)+"\t<=\t"+str(conf.predictor)+"\n")
    annotate(conf.input, pred=conf.predictor, eval=conf.evaluator, pred_threshold=conf.pred_threshold, eval_threshold=conf.eval_threshold, output=buffer, slim_output=conf.slim_output and not conf.self_supervision)

    conf.input.close()

    if (conf.self_supervision or conf.dimlex_mode):

        #
        # induce discourse marker lexicon
        ###################################
        buffer.seek(0)
        # print(buffer, buffer.getvalue())
        #buffer.seek(0)

        dimlex=induce_dimlex(buffer, conf.words_col, dm_confidence_col=-6, dm_col=-5, rel_confidence_col=-4)

        if conf.dimlex_mode:
            pprint(dimlex)

        #
        # iterate and re-annotate using dimlex
        ########################################
        # note that we use the induced dimlex only for disambiguation, we do not override the ensemble predictions

        buffer.seek(0)

        if conf.no_output:
            output=StringIO()
        else:
            output=sys-stdout

        if conf.self_supervision:
            annotate(buffer, pred=conf.predictor, eval=conf.evaluator, dimlex=dimlex, pred_threshold=conf.pred_threshold, eval_threshold=conf.eval_threshold, conf_threshold=conf.min_confidence, words_col=conf.words_col, output=output, slim_output=conf.slim_output)
