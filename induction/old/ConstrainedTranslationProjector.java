import java.io.*;
import java.util.*;
import java.util.zip.GZIPInputStream;

public class ConstrainedTranslationProjector {
	public static void main(String argv[]) throws Exception {
		
		Integer maxConcepts = Integer.MAX_VALUE;
		Integer maxLexPerConcept = Integer.MAX_VALUE;
		Double minConcScore = 0.0;
		Double minLexScore = 0.0;


		System.err.print("synopsis: ConstrainedTranslationProjector lang DICT1[..n] [-wn WN1..m] -constrained [FLAGS] [-eval DICTm ]\n"+
			"\tlang              BCP47 language code for the target language, say, en for English\n"+
			"\tDICTi             TSV file with the following columns:\n"+
			"\t\twritten_rep_a\n"+
			"\t\tlex_entry_a\n"+
			"\t\tsense_a\n"+
			"\t\ttrans\n"+
			"\t\tsense_b\n"+
			"\t\tlex_entry_b\n"+
			"\t\twritten_rep_b\n"+
			"\t\tlexinfo POS\n"+
			"\tWNi               wordnet TSV file with the following columns:\n"+
			"\t\tsynset ID\n"+
			"\t\tWN POS\n"+
			"\t\twritten_rep\n"+
			"\t-eval             if provided, use the following dictionary for evaluation\n"+
			"\t-constrained      constrain concept/translation projection to one per lexeme; TODO: distinguish possible strategies\n"+
			"\tFLAGS             one or several of the following attribute-value pairs, applying to source-target language pairs, only\n"+
			"\t-maxConcepts INT      maximum number of target language concepts for translation inference, defaults to "+maxConcepts+"\n"+
			"\t-maxLexPerConcept INT maximum number of target language lexemes for translation concept, defaults to "+maxLexPerConcept+"\n"+
			"\t-minConcScore DOUBLE  minimum concept score for translation concepts, defaults to "+minConcScore+"\n"+
			"\t-minLexScore DOUBLE   minimum translation score for translation, aggregate over all concepts, defaults to "+minLexScore+"\n"+
			"reads src language input from stdin, returns tgt language expressions for every concept\n"+
			"TODO: enable wordnets\n"+
			"NOTE: DICTi arguments *MUST* follow the following naming conventions:\n"+
			"\t\"trans_\"$SRC\"-\"$TGT\".tsv\", with $SRC and $TGT BCP47 language codes (case-insensitive)\n"+
			"");
			
		// for reference words
		ArrayList<String> words = new ArrayList<String>();
		
		// for vocabulary gaps: store the entire graph
		Hashtable<String,HashSet<String>> src2tgt = new Hashtable<String,HashSet<String>>();
		
		int i = 0;
		
		String lang = argv[i++].toLowerCase();
		System.err.println("lang: "+lang);

		ArrayList<String> dicts = new ArrayList<String>();
		Hashtable<String,String> dict2src = new Hashtable<String,String>();
		Hashtable<String,String> dict2tgt = new Hashtable<String,String>();
		
		while(i<argv.length && !argv[i].startsWith("-")) {
			dicts.add(argv[i]);
			String[] x = argv[i].split("[_\\-\\.]");
			dict2src.put(argv[i], x[1].toLowerCase());
			dict2tgt.put(argv[i], x[2].toLowerCase());
			System.err.println("dictionary "+argv[i]+": "+x[1].toLowerCase()+ " > "+x[2].toLowerCase());
			i++;
		}
		
		// infer concepts from tgt (gloss) to src (lexical entry)
		Map<String,Map<String,Integer>> tgt2lang2freq = new TreeMap<String,Map<String,Integer>>();
		Map<String,Map<String,Integer>> src2lang2freq = new TreeMap<String,Map<String,Integer>>();

		
		for(String dict : dicts) {
			BufferedReader in = new BufferedReader(new FileReader(dict));
			in.readLine(); // skip first line
			for(String line = in.readLine(); line!=null; line=in.readLine()) {
				String[] fields = line.split("\t");
				if(fields.length>7) {
					String src = fields[0].trim();
					String slang = dict2src.get(dict);
					if(src.matches(".*\"@[^\"]+$"))
						slang=src.replaceAll(".*@","").trim();
					src=src.replaceFirst("\"@[^\"]+$","").replaceAll("\"", "").trim();
					src="\""+src+"\"@"+slang;
					
					if(src2tgt.get(src)==null)
						src2tgt.put(src, new HashSet<String>());
					
					String tgt = fields[6].trim();
					String tlang=dict2tgt.get(dict);
					if(tgt.matches(".*\"@[^\"]+$"))
						tlang=tgt.replaceAll(".*@","").trim();
					tgt=tgt.replaceFirst("\"@[^\"]+$","").replaceAll("\"", "").trim();
					tgt="\""+tgt+"\"@"+tlang;
					src2tgt.get(src).add(tgt);
					// System.err.println(src+" -> "+tgt);
					
					if(src2lang2freq.get(src)==null)
						src2lang2freq.put(src,new Hashtable<String,Integer>());
					if(src2lang2freq.get(src).get(tlang)==null)
						src2lang2freq.get(src).put(tlang,1);
					else 
						src2lang2freq.get(src).put(tlang,src2lang2freq.get(src).get(tlang)+1);

					if(tgt2lang2freq.get(tgt)==null)
						tgt2lang2freq.put(tgt,new Hashtable<String,Integer>());
					if(tgt2lang2freq.get(tgt).get(slang)==null)
						tgt2lang2freq.get(tgt).put(slang,1);
					else 
						tgt2lang2freq.get(tgt).put(slang,tgt2lang2freq.get(tgt).get(slang)+1);
					
					System.err.print("\rdictionaries: "+src2tgt.size()+" src lexemes, "+tgt2lang2freq.size()+" tgt lexemes");
				}
			}
			in.close();
		}
		System.err.println();

		Map<String,Map<String,Set<String>>> lang2lex2concept = new Hashtable<String,Map<String,Set<String>>>();
		Map<String,Map<String,Set<String>>> concept2lang2lex = new TreeMap<String,Map<String,Set<String>>>();

		if(argv.length > i && argv[i].equals("-wn")) {
			i++;
			int languageConcept = 0;
			while(i<argv.length && !argv[i].startsWith("-")) {
				BufferedReader in = new BufferedReader(new FileReader(argv[i]));
				for(String line = in.readLine(); line!=null; line=in.readLine()) {
					String fields[] = line.split("\t");
					if(fields.length>2) {
						String c = fields[0];
						String l = fields[2]; // we expect the same encoding as for dictionaries
						lang = l.replaceAll(".*@","");
						if(lang2lex2concept.get(lang)==null) lang2lex2concept.put(lang, new TreeMap<String,Set<String>>());
						if(lang2lex2concept.get(lang).get(l)==null) lang2lex2concept.get(lang).put(l,new HashSet<String>());
						if(concept2lang2lex.get(c)==null) concept2lang2lex.put(c,new Hashtable<String,Set<String>>());
						if(concept2lang2lex.get(c).get(lang)==null) concept2lang2lex.get(c).put(lang, new HashSet<String>());
						lang2lex2concept.get(lang).get(l).add(c);
						concept2lang2lex.get(c).get(lang).add(l);
						System.err.print("\rwordnets: "+(++languageConcept)+" lexicalizations for "+concept2lang2lex.size()+" concepts");
					}
				}
				in.close();
				i++;
			}
			System.err.println();
		}
		
		// no WordNets, then use target language expressions as concepts
		if(lang2lex2concept.size()==0) {
			int languageConcept = 0;
			for(String s : src2tgt.keySet())
				for(String t: src2tgt.get(s))
					if(t.endsWith("@"+argv[0])) {
						if(lang2lex2concept.get(argv[0])==null)
							lang2lex2concept.put(argv[0],new TreeMap<String,Set<String>>());
						if(lang2lex2concept.get(argv[0]).get(t)==null)
							lang2lex2concept.get(argv[0]).put(t,new HashSet<String>());
						lang2lex2concept.get(argv[0]).get(t).add(t);
						if(concept2lang2lex.get(t)==null) concept2lang2lex.put(t,new Hashtable<String,Set<String>>());
						if(concept2lang2lex.get(t).get(argv[0])==null) concept2lang2lex.get(t).put(argv[0],new HashSet<String>());
						concept2lang2lex.get(t).get(argv[0]).add(t);
						System.err.print("\rtarget language translations: "+(++languageConcept)+" lexicalizations for "+concept2lang2lex.size()+" concepts");
					}
			System.err.println();
		}

		boolean constrained = false;
		if(i<argv.length && argv[i].equals("-constrained")) {
			constrained=true;
			System.err.println("constrained projection");
			i++;
		} else {
			System.err.println("unconstrained projection");
		}
		
		while(i<argv.length && argv[i].startsWith("-") && !argv[i].equals("-eval")) {
			if(argv[i].equals("-maxConcepts"))
				maxConcepts=Integer.parseInt(argv[i+1]);
			else if(argv[i].equals("-maxLexPerConcept"))
				maxLexPerConcept=Integer.parseInt(argv[i+1]);
			else if(argv[i].equals("-minConcScore"))
				minConcScore=Double.parseDouble(argv[i+1]);
			else if(argv[i].equals("-minLexScore"))
				minLexScore=Double.parseDouble(argv[i+1]);
			i=i+2;
		}
		
		System.err.println("running with -maxConcepts "+maxConcepts+" -maxLexPerConcept "+maxLexPerConcept+" -minConcScore "+minConcScore+" -minLexScore "+minLexScore);

		
		Map<String,Set<String>> src2tgtGold = new TreeMap<String,Set<String>>();		
		if(i<argv.length && argv[i].equals("-eval")) {
						
			Set<String> tgts = new HashSet<String>();
			String dict = argv[i+1];

			String[] x = dict.split("[_\\-\\.]");
			dict2src.put(dict, x[1].toLowerCase());
			dict2tgt.put(dict, x[2].toLowerCase());
			System.err.println("dictionary "+dict+": "+x[1].toLowerCase()+ " > "+x[2].toLowerCase());
			
			BufferedReader in = new BufferedReader(new FileReader(dict));
			in.readLine(); // skip first line
			for(String line = in.readLine(); line!=null; line=in.readLine()) {
				String[] fields = line.split("\t");
				if(fields.length>7) {
					String src = fields[0].trim();
					String slang = dict2src.get(dict);
					if(src.matches(".*\"@[^\"]+$"))
						slang=src.replaceAll(".*@","").trim();
					src=src.replaceFirst("\"@[^\"]+$","").replaceAll("\"", "").trim();
					src="\""+src+"\"@"+slang;
					
					String tgt = fields[6].trim();
					String tlang=dict2tgt.get(dict);
					if(tgt.matches(".*\"@[^\"]+$"))
						tlang=tgt.replaceAll(".*@","").trim();
					tgt=tgt.replaceFirst("\"@[^\"]+$","").replaceAll("\"", "").trim();
					tgt="\""+tgt+"\"@"+tlang;
					// System.err.println(src+" -> "+tgt);
					
					if(src2tgtGold.get(src)==null)
						src2tgtGold.put(src,new HashSet<String>());
					src2tgtGold.get(src).add(tgt);
					tgts.add(tgt);
					
					System.err.print("\rgold data: "+src2tgtGold.size()+" src lexemes, "+tgts.size()+" tgt lexemes");
				}
			}
			in.close();
			System.err.println();
		}
		
		// consolidate (init P(lex|concept) and P(concept|lex))
		Map<String,Map<String,Double>> concept4lex2p = new TreeMap<String,Map<String,Double>>();
		Map<String,Map<String,Double>> lex4concept2p = new TreeMap<String,Map<String,Double>>();
		i=0;
		for(String l : lang2lex2concept.keySet())
			for(String lex : lang2lex2concept.get(l).keySet()) 
				for(String concept : lang2lex2concept.get(l).get(lex)) {
					if(concept4lex2p.get(concept)==null) concept4lex2p.put(concept, new TreeMap<String,Double>());
					if(lex4concept2p.get(lex)==null) lex4concept2p.put(lex, new TreeMap<String,Double>());
					concept4lex2p.get(concept).put(lex,(1.0/(double)lang2lex2concept.get(l).get(lex).size()));
					lex4concept2p.get(lex).put(concept,(1.0/(double)concept2lang2lex.get(concept).get(l).size()));
					System.err.print("consolidation: "+(++i)+" entries\r");
				}
		System.err.println();

		lang2lex2concept.clear();
		concept2lang2lex.clear();
		
		// induce from tgt to src, but constrained
		List<String> srces = new ArrayList<String>(src2tgt.keySet()); // TreeMap => sorted (reproducible)
		Integer total = srces.size();
		boolean modified=true;
		while(modified) {
			modified=false;
			for(i = 0; i<srces.size(); i++) {
				String src = srces.get(i);
				String slang = src.replaceAll(".*@","");
				if(lex4concept2p.get(src)!=null) {
					srces.remove(i--);
					modified=true;
				} else {
					Map<String,Double> src4concept2p = new TreeMap<String,Double>();
					Map<String,Double> concept4src2p = new TreeMap<String,Double>();
					for(String tgt : src2tgt.get(src)) 
						if(lex4concept2p.get(tgt)!=null) {
							String tlang = tgt.replaceAll(".*@","");				
							for(String concept : lex4concept2p.get(tgt).keySet()) {

								// P(src|concept)=\sum_tgt P(src|tgt) P(tgt|concept)
								if(src4concept2p.get(concept)==null)
									src4concept2p.put(concept,0.0);
								src4concept2p.put(concept,src4concept2p.get(concept)+
									(1.0/(double)tgt2lang2freq.get(tgt).get(slang)) *
									lex4concept2p.get(tgt).get(concept));

								// P(concept|src)=\sum_tgt P(concept|tgt) P(tgt|src)	
								if(concept4src2p.get(concept)==null)
									concept4src2p.put(concept,0.0);
								concept4src2p.put(concept,concept4src2p.get(concept)+
									(1.0/(double)src2lang2freq.get(src).get(tlang)) *
									concept4lex2p.get(concept).get(tgt));
							}
						}
					if(src4concept2p.size()>0) {
						if(constrained) {
							Hashtable<String,Double> src4conceptPruned = new Hashtable<String,Double>();
							Hashtable<String,Double> concept4srcPruned = new Hashtable<String,Double>();
							for(String tgt : src2tgt.get(src)) {
								HashSet<String> cand1 = new HashSet<String>();
								Double s4c1 = null;
								Double c4s1 = null;
								HashSet<String> cand2 = new HashSet<String>();
								Double s4c2 = null;
								Double c4s2 = null;
								if(lex4concept2p.get(tgt)!=null)
									for(String c : lex4concept2p.get(tgt).keySet()) {
										if(cand1.size()==0 || src4concept2p.get(c)>s4c1 || 
											(src4concept2p.get(c)==s4c1 && concept4src2p.get(c)>c4s1))  {
												cand1.clear(); cand1.add(c);
												c4s1=concept4src2p.get(c);
												s4c1=src4concept2p.get(c);
											} 
										else if(src4concept2p.get(c)==s4c1 && concept4src2p.get(c)== c4s1)
											cand1.add(c);
										if(cand2.size()==0 || concept4src2p.get(c)>c4s2 ||
											(src4concept2p.get(c)>s4c2 && concept4src2p.get(c)==c4s2)) {
												cand2.clear(); cand2.add(c);
												c4s2=concept4src2p.get(c);
												s4c2=src4concept2p.get(c);
										} else if(src4concept2p.get(c)==s4c2 && concept4src2p.get(c)== c4s2)
											cand2.add(c);
									}
								for(String c : cand1) 
									src4conceptPruned.put(c,src4concept2p.get(c));
								for(String c : cand2)
									concept4srcPruned.put(c,concept4src2p.get(c));								
							}							
							src4concept2p=src4conceptPruned;
							concept4src2p=concept4srcPruned;
						}
						lex4concept2p.put(src,src4concept2p);
						for(String concept : src4concept2p.keySet()) {
							if(concept4lex2p.get(concept)==null)
								concept4lex2p.put(concept, new TreeMap<String,Double>());
							concept4lex2p.get(concept).put(src,src4concept2p.get(concept));
						}
						modified=true;
						srces.remove(i--);
					}
				}
				System.err.print("\rprojection: "+(100.0-(100.0*srces.size())/(double)total)+"%   ");
			}
		}
		System.err.println();

		lang = argv[0].toLowerCase();
			
		// eval
		if(src2tgtGold.size()>0) {
			int evalCount = 0;
			Map<String,Integer> eval = new Hashtable<String,Integer>();
			for(String lex : src2tgtGold.keySet()) {
				if(lex4concept2p.get(lex)==null) {
					System.out.println(lex+"\t"+null);
					if(eval.get("total")==null) 	eval.put("total",1); 	else eval.put("total",eval.get("total")+1);
					if(eval.get("oovTarget")==null) eval.put("oovTarget",src2tgtGold.get(lex).size()); 	else eval.put("oovTarget",eval.get("oovTarget")+src2tgtGold.get(lex).size());
				} else {
					eval = predict(lex, lang, lex4concept2p, concept4lex2p, new OutputStreamWriter(System.out), src2tgtGold, eval, maxConcepts, maxLexPerConcept,  minConcScore, minLexScore);
					// System.err.print("eval: "+((100.0*(++evalCount)))/(double)src2tgtGold.size()+"%   \r";
					
					// print result scores
					Integer tp = eval.get("tp"); if(tp==null) tp=0;
					Integer fp = eval.get("fp"); if(fp==null) fp=0;
					Integer fn = eval.get("fn"); if(fn==null) fn=0;
					Integer cov = eval.get("cov"); if(cov==null) cov=0; // coverage (of source lexemes)
					total = eval.get("total"); if(total==null) total=0; // total (of source lexemes)	

					double rec = ((double)tp)/(double)(tp+fn);
					double prec = ((double)tp)/(double)(tp+fp);
					double f = 2*prec*rec/(prec+rec);
					System.err.print("cov:\t"+((double)cov)/(double)total+"\t("+cov+"/"+total+")\t");
					System.err.print("\tprec:\t"+prec);
					System.err.print("\trec:\t"+rec);
					System.err.println("\tf:\t"+f);
				}
			}
			System.err.println();
			
			// print result scores
			System.out.print("# ConstrainedTranslationProjector");
			for(String a : argv) 
				System.out.print(" "+a);
			System.out.println();
			
			Integer tp = eval.get("tp"); if(tp==null) tp=0;
			Integer fp = eval.get("fp"); if(fp==null) fp=0;
			Integer fn = eval.get("fn"); if(fn==null) fn=0;
			Integer cov = eval.get("cov"); if(cov==null) cov=0; // coverage (of source lexemes)
			total = eval.get("total"); if(total==null) total=0; // totalerage (of source lexemes)
			
			double rec = ((double)tp)/(double)(tp+fn);
			double prec = ((double)tp)/(double)(tp+fp);
			double f = 2*prec*rec/(prec+rec);
			System.out.print("# cov:\t"+((double)cov)/(double)total+"\t("+cov+"/"+total+")");
			System.out.print("\tprec:\t"+prec);
			System.out.print("\trec:\t"+rec);
			System.out.println("\tf:\t"+f);

			if(eval.get("oovTarget")!=null)
				fn=fn + eval.get("oovTarget"); // translations for 
			
			rec = ((double)tp)/(double)(tp+fn);
			prec = ((double)tp)/(double)(tp+fp);
			f = 2*prec*rec/(prec+rec);
			System.out.print("# incl. OOV words:\t"+(total-cov)+"\t");
			System.out.print("\tprec:\t"+prec);
			System.out.print("\trec:\t"+rec);
			System.out.println("\tf:\t"+f);			
		} else {

		// spell out
			System.err.println("read source language expressions from stdin, cancel with <ENTER>");
			BufferedReader in = new BufferedReader(new InputStreamReader(System.in));
			for(String lex = in.readLine(); lex!=null && !lex.equals(""); lex=in.readLine()) {
				lex=lex.trim();
				if(lex4concept2p.get(lex)==null) {
					System.out.println(lex+"\t"+null);
				} else {
					predict(lex, lang, lex4concept2p, concept4lex2p, new OutputStreamWriter(System.out), src2tgtGold, null, maxConcepts, maxLexPerConcept,  minConcScore, minLexScore);
				}
			}
		} 
		
	}
	
	/** destructive to eval, returns fn,tp,etc., score is P(x|y) * P(y|x) */
	private static Map<String,Integer> predict(String lex, String lang, Map<String,Map<String,Double>> lex4concept2p, Map<String,Map<String,Double>> concept4lex2p, Writer out, Map<String,Set<String>> src2tgtGold, Map<String,Integer> eval, Integer maxConcepts, Integer maxLexPerConcept, Double minConcScore, Double minLexScore) 
	throws IOException {

		LinkedHashSet<String> result = new LinkedHashSet<String>();
	
		// decoding strategy:
		// 1. spell out max aggregate lexicalization
		// 2. maxLexPerConcept iterations
		// 	a. iterate over the top maxConcepts concepts with score >= minConcScore
		// 	b. initially maxLexSet = empty
		// 	c. for the current concept, add the maxLex value (if score [over all concepts] >= minLexScore) to the maxLexSet
		// 	d. spell out maxLexSet, remove its content from lexicalization candidates, iterate in a.
		
		if(maxConcepts==null || maxConcepts<1) maxConcepts=Integer.MAX_VALUE;
		if(maxLexPerConcept==null || maxLexPerConcept<1) maxLexPerConcept=Integer.MAX_VALUE;
		if(minLexScore==null || minLexScore<0.0) minLexScore=0.0;
		if(minConcScore==null || minConcScore<0.0) minConcScore=0.0;

		Map<String,Double> concept2score = new TreeMap<String,Double>();
		Map<String,Double> tgt2score = new TreeMap<String,Double>();
		
		if(lex4concept2p.get(lex)!=null) {
			for(String concept : lex4concept2p.get(lex).keySet()) {
				concept2score.put(concept, lex4concept2p.get(lex).get(concept)*concept4lex2p.get(concept).get(lex));
				for(String tgt : concept4lex2p.get(concept).keySet())
					if(tgt.endsWith("@"+lang)) {
						if(tgt2score.get(tgt)==null)
							tgt2score.put(tgt,concept2score.get(concept)*(lex4concept2p.get(tgt).get(concept)*concept4lex2p.get(concept).get(tgt)));
						else
							tgt2score.put(tgt,tgt2score.get(tgt)+
											  concept2score.get(concept)*(lex4concept2p.get(tgt).get(concept)*concept4lex2p.get(concept).get(tgt)));
					}
			}

			// sort concepts by score
			Vector<String> concepts = new Vector<String>();
			for(String c : concept2score.keySet()) {
				for(int i= 0; i<concepts.size() && !concepts.contains(c);i++)
					if(concept2score.get(concepts.get(i))<concept2score.get(c))
						concepts.insertElementAt(c,i);
				if(!concepts.contains(c)) concepts.add(c);
			}
			
			// exclude marginal concepts // as long as their scores differ
			while(concepts.size()>maxConcepts) // && concept2score.get(concepts.get(concepts.size()-1))<concept2score.get(concepts.get(maxConcepts)))
				concepts.remove(concepts.size()-1);

			// System.err.println("concepts.size()="+concepts.size()+", should be <= "+maxConcepts);
						
			// enforce minimal concept score (as long as there is at least one // and their scores differ)
			while(concepts.size()>1 && concept2score.get(concepts.get(concepts.size()-1)) < minConcScore) //&& concept2score.get(concepts.get(concepts.size()-1))<concept2score.get(concepts.get(0))) 
				concepts.remove(concepts.size()-1);
			
			// order and reorganize concept2score
			LinkedHashMap<String,Double> tmp = new LinkedHashMap<String,Double>();
			for(String c : concepts) 
				tmp.put(c,concept2score.get(c));
			concept2score=tmp;
			// System.err.println("concept2score.size()="+concept2score.size()+", should be <= "+maxConcepts);
			
			// 1. max. lexicalization(s)
			LinkedHashSet<String> cands = new LinkedHashSet<String>();
			Double score = -Double.MAX_VALUE;
			for(String tgt : tgt2score.keySet()) {
				if(tgt2score.get(tgt)>score) {
					cands.clear();
					cands.add(tgt);
					score=tgt2score.get(tgt);
				}
				if(tgt2score.get(tgt)==score)
					cands.add(tgt);
			}
			result.addAll(cands);
			
			// 2. iterate over maxLexPerConcept iterations 
			HashSet<String> spelledOut = new HashSet<String>();
			while(cands.size()>0 && maxLexPerConcept>0) {
				// System.err.print("!");
				maxLexPerConcept=maxLexPerConcept-1;

				// 	a. initially cands = empty
				cands.clear();
				
				// 	b. iterate over the top maxConcepts concepts with score >= minConcScore, i.e., all in concept2score [cf. pruning above]
				for(String concept : concepts) {
					//System.err.print(".");
					String cand = null;
					score = -Double.MAX_VALUE;
					for(String tgt : new TreeSet<String>(concept4lex2p.get(concept).keySet())) 
						if(tgt.endsWith("@"+lang) && !spelledOut.contains(tgt)) {
							double tScore = concept4lex2p.get(concept).get(tgt) * lex4concept2p.get(tgt).get(concept);
							//System.err.println("cand: "+cand);
							//System.err.println("tgt: "+tgt);
							//if(cand!=null) System.err.println("tgt2score("+cand+"): "+tgt2score.get(cand));
							//if(tgt!=null) System.err.println("tgt2score("+tgt+"): "+tgt2score.get(tgt));
							
							if(cand==null || tScore > score || (tScore==score && tgt2score.get(tgt)!=null && (
								tgt2score.get(cand)==null || 
								tgt2score.get(tgt)>tgt2score.get(cand)))) { // secondary criterion: overall popularity
								score=tScore;
								cand=tgt;
								//System.err.println("=> "+cand);
							}
						}

				// 	c. for the current concept, add the maxLex value (if score [over all concepts] >= minLexScore) to the cands
					if(cand!=null && score>=minLexScore)
						cands.add(cand);
				}
				
				// 	d. spell out cands, remove its content from lexicalization candidates, iterate in a.
				spelledOut.addAll(cands);
				result.addAll(cands);				
				// System.err.println("cands "+cands);
				// System.err.println("result "+result);
			}
			
		}
		
		// 3. structured output & eval.
		Integer tp = 0; if(eval!=null && eval.get("tp")!=null) tp=eval.get("tp");
		Integer fp = 0; if(eval!=null && eval.get("fp")!=null) fp=eval.get("fp");
		Integer fn = 0; if(eval!=null && eval.get("fn")!=null) fn=eval.get("fn");
		Integer cov = 0; if(eval!=null && eval.get("cov")!=null) cov=eval.get("cov");	// coverage (of source lexemes)
		Integer total = 0; if(eval!=null && eval.get("total")!=null) total=eval.get("total");
		total++;
		
		// System.err.println("result "+result+"\n");
		if(result.size()>0)
			cov++;
		for(String tgt : result) {
			// System.err.print(lex+"\t"+tgt+"\t"+tgt2score.get(tgt)+"\n");
			out.write(lex+"\t"+tgt+"\t"+tgt2score.get(tgt)+"\n");
			out.flush();
			
			//if(src2tgtGold.size()>0) { 
				//System.err.println("src2tgtGold sample key: "+src2tgtGold.keySet().iterator().next());
				//System.err.println("src2tgtGold sample val: "+src2tgtGold.get(src2tgtGold.keySet().iterator().next()));
			//}
			if(src2tgtGold.get(lex)!=null) {
				if(src2tgtGold.get(lex).contains(tgt))
					tp++;
				else fp++;
			}
			// todo: log concept(s)
		}	

		if(src2tgtGold.get(lex)!=null) {
			for(String t : src2tgtGold.get(lex))
				if(!result.contains(t))
					fn=fn+1;
			eval.put("tp",tp);
			eval.put("fp",fp);
			eval.put("fn",fn);
			eval.put("cov",cov);
			eval.put("total",total);
		}
						
		return eval;
	}

	
	/** aux. routine, replaces String.format() as this produces errors (locale-related???), 
	 *  slow, using float precision, only<br/>
	 *  however, note that the approach produces rounding errors */
	protected static String cleanFormat(Double d) {
		if(d<0) return "-"+cleanFormat(d*-1.0);
		String result = String.format(Locale.US, "%f", d).replaceAll("([\\.])?0+$","");
		if(Math.abs(Double.parseDouble(result)-d) < 0.000001) return result;
		System.err.print("warning: String.format("+d+")=\""+result+"\"");
		result="";
		int dimension = (int)Math.log10(d);
		if(dimension<0) result="0.";
		while(d>(double)Float.MIN_VALUE) {
			// System.err.print("cleanFormat("+d+")=");
			double base = Math.pow(10.0, (double)dimension);
			result=result+(int)(d/base);
			if(d % base>(double)Float.MIN_VALUE) {
				d=d % base;
				if(dimension==0 && d>(double)Float.MIN_VALUE)
					result=result+".";
				dimension--;
			} else d=(double)Float.MIN_VALUE;
			// System.err.println(result);
		}
		System.err.println(" => \""+result+"\"");
		return result;
	}
	
	/** store all translation pairs in a single graph, note that we do not include POS information, but only word@lang */
	protected static Map<String, HashSet<String>> buildTranslationGraph(String dictFile, String srcLang, String tgtLang) throws IOException {
		System.err.print("proccessing "+dictFile);
		Hashtable<String,HashSet<String>> result = new Hashtable<String,HashSet<String>>();
		BufferedReader in = new BufferedReader(new FileReader(dictFile));
			in.readLine(); // skip first line
			int lines = 0;
			for(String line = in.readLine(); line!=null; line=in.readLine()) {
				String[] fields = line.split("\t");
					if(fields.length>7) {
						System.err.print("\rprocessing "+dictFile+": "+(++lines)+" lines");
							String src = fields[0].replaceAll("\"", "").replaceFirst("@.*","").trim();
							String tgt = fields[6].replaceAll("\"", "").replaceFirst("@.*","").trim();
							// String pos = fields[7].replaceAll("\"", "").trim();
							
							// no pos mode
							src = "\""+src+"\"@"+srcLang; 
							tgt = "\""+tgt+"\"@"+tgtLang;
							
							if(result.get(src)==null) result.put(src,new HashSet<String>());
							result.get(src).add(tgt);
						}
					System.err.print("\rproccessing "+dictFile+": "+result.size()+" source words");
						
					}
		in.close();
		System.err.println();
		return result;
	}
}