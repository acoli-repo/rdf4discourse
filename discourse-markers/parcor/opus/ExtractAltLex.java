import java.io.*;
import java.util.*;

public class ExtractAltLex {

	public static void main(String argv[]) throws Exception {
		int min = 2;
		int length = 2; // n-gram length
		System.err.println("synopsis: ExtractAltLex COL_WORD COL_SENSE [-min=INT]"+/*"-dimlex DIMLEX.xml"+*/"\n"+
			//"\t DIMLEX.xml DimLex-conformant discourse cue dictionary [TODO]\n"+
			"\t COL_WORD   CoNLL column containing the words (or lemmas), i.e., discourse cue candidates, start with 0\n"+
			"\t COL_SENSE  CoNLL column containing the sense annotations; senses are split into [;, ]-separated strings\n"+
			"\t -min=INT   minimum number of occurrences for an AltLex to be returned for a sense, default="+min+"\n"+
			"Reads CoNLL from stdin. If for a sentence, a sense is annotated (or projected) but *not* supported by DIMLEX.xml,\n"+
			"find the word w with highest probability P(sense|w).\n"+
			"TODO: Expand to multi-word expressions w=w1..wn \n"+
			"if P(sense|w)>P(sense|wj) for all j=1..n and freq(w)>=min.\n"+
			"Return a "+/*Dimlex-like dictionary "+*/" survey of alternative candidate lexicalizations.");
		
		File tmp = File.createTempFile("ExtractAltLex.",".tmp");
		tmp.deleteOnExit();
		
		int word = Integer.parseInt(argv[0]);
		int sense = Integer.parseInt(argv[1]);
		
		for(int i = 2; i<argv.length; i++)
			if(argv[i].toLowerCase().startsWith("-min=")) min=Integer.parseInt(argv[i].replaceFirst(".*=",""));

		long words = 0;	
		Hashtable<String,Integer> sense2freq = new Hashtable<String,Integer>();
		Hashtable<String,Integer> word2freq = new Hashtable<String,Integer>();
		TreeMap<String,Hashtable<String,Integer>> word2sense2freq = new TreeMap<String,Hashtable<String,Integer>>();
		
		// initialize words2sense2freq, etc., mirror file in tmp
		BufferedReader in = new BufferedReader(new InputStreamReader(System.in));
		FileWriter out = new FileWriter(tmp);
		String sentence = "";
		for(String line =""; line!=null; line=in.readLine()) {
			out.write(line+"\n");
			if(line.trim().length()==0) {
				String[] lines = sentence.split("\n");
				String[][] fields = new String[lines.length][];
				for(int i = 0; i<lines.length; i++)
					fields[i] = lines[i].split("\t");

				HashSet<String> senses = new HashSet<String>();
				HashSet<String> cues = new HashSet<String>();

				for(int i = 0; i<lines.length; i++) { 
					if(fields[i].length>word) {
						String cue = fields[i][word];
						cues.add(cue);
						for(int j=i-1; j>=0 && j>=i-length; j--)
							if(fields[j].length>word) {
								cue=fields[j][word]+" "+cue;
								cues.add(cue);
							}
					}
					
					for(int j = Math.max(i-length,0);j<i
					if(fields[i].length>sense) 
						if(fields[i][sense].replaceAll("[^a-zA-B0-9]+","").trim().length()>0 && fields[i][sense].matches(".*[a-zA-Z0-9].*"))
							for(String s : fields[i][sense].split("[ \t\r]*[+,;|][ \t\r]*")) 
								if(s.trim().length()>0 && s.matches(".*[a-zA-Z0-9].*")) 
									senses.add(s.trim());
				}

				for(String s : senses) {
					if(sense2freq.get(s)==null) sense2freq.put(s,0);
					sense2freq.put(s,sense2freq.get(s)+1);
				}
				
				for(String w : cues) {
					if(word2freq.get(w)==null) word2freq.put(w,0);
					word2freq.put(w,word2freq.get(w)+1);
					for(String s : senses) {
						if(word2sense2freq.get(w)==null) word2sense2freq.put(w,new Hashtable<String,Integer>());
						if(word2sense2freq.get(w).get(s)==null) word2sense2freq.get(w).put(s,0);
						word2sense2freq.get(w).put(s,word2sense2freq.get(w).get(s)+1);
					}
				}
				sentence="";
			}
			
			line=line.replaceFirst("^#.*","").replaceFirst("([^\\\\])#.*","$1");
			if(!line.trim().equals("")) { // otherwise, it is a comment or dealt with before
				sentence=sentence+line+"\n";
				words=words+1;
				if(words%123==1)
					System.err.print("read "+words+" tokens, "+word2sense2freq.size()+" words, "+sense2freq.size()+" senses\r");
			}
		}
		out.write("\n");
		out.flush();
		out.close();
		in.close();
		System.err.println("read "+words+" tokens, "+word2sense2freq.size()+" words, "+sense2freq.keySet().size()+" senses");
		
		// build word2sense2prob
		Map<String,Hashtable<String,Double>> word2sense2prob = new TreeMap<String,Hashtable<String,Double>>();

		words = 0;
		for(String w : word2freq.keySet()) {
			words=words+1;
			if(word2sense2freq.get(w)!=null)
				for(String s : word2sense2freq.get(w).keySet()) {
					double pSense = ((double)sense2freq.get(s))/(double)words;
					if(word2sense2freq.get(w).get(s)>=min) {
						double pSenseGivenWord = ((double)word2sense2freq.get(w).get(s))/(double)word2freq.get(w);
						if(pSenseGivenWord > pSense) {
							if(word2sense2prob.get(w)==null) word2sense2prob.put(w,new Hashtable<String,Double>());
							word2sense2prob.get(w).put(s,pSenseGivenWord);
						}
					}
				}
			System.err.print("calculate "+(100*words)/word2freq.size()+"%\r");
		}
		System.err.println("calculate "+(100*words)/word2freq.size()+"%");
		
		// word2sense2freq: for every sentence and every sense, count the most probable word
		Vector<String> ngram = new Vector<String>();
		Map<String,Hashtable<String,Integer>> word2sense2freqRaw = word2sense2freq;
		word2sense2freq = new TreeMap<String,Hashtable<String,Integer>>();
		in = new BufferedReader(new FileReader(tmp));
		words=0;
		TreeSet<String> senses = new TreeSet<String>();
		TreeSet<String> cueWords = new TreeSet<String>();
		for(String line = ""; line!=null; line=in.readLine()) {
			if(line.trim().length()==0) {
				for(String s : senses) {
					String cue = "";
					double pSGivenCue = -1.0;
					for(String w : cueWords) 
						if(word2sense2prob.get(w)!=null)
							if(word2sense2prob.get(w).get(s)!=null)
								if(word2sense2freqRaw.get(w).get(s)>=min)
									if(pSGivenCue < 0.0 || word2sense2prob.get(w).get(s)>pSGivenCue) {
										cue = w;
										pSGivenCue = word2sense2prob.get(w).get(s);
									} 
					if(pSGivenCue >= 0.0) {
						if(word2sense2freq.get(cue)==null) word2sense2freq.put(cue,new Hashtable<String,Integer>());
						if(word2sense2freq.get(cue).get(s)==null) word2sense2freq.get(cue).put(s,0);
						word2sense2freq.get(cue).put(s,word2sense2freq.get(cue).get(s)+1);
					}
				}
				senses.clear();
				cueWords.clear();
				ngram.clear();
			}
			
			line=line.replaceFirst("^#.*","").replaceFirst("([^\\\\])#.*","$1");
			if(line.trim().length()>0) {
				String[] fields = line.split("\t");
				if(fields.length>word) {
					String cue = fields[word];
					for(int j = ngram.length()-1; j>=0 && j=; 
					ngram.add(fields[word]);
					cueWords.add(fields[word]);
					
					
				}
				if(fields.length>sense) {
					String s = fields[sense];
					if(s.replaceAll("[^a-zA-B0-9]+","").trim().length()>0 && s.matches(".*[a-zA-Z0-9].*"))
						for(String sub : s.split("[ \t\r]*[+|,;][ \t\r]*")) 
							if(sub.trim().length()>0 && sub.matches(".*[a-zA-Z0-9].*")) 
								senses.add(sub.trim());
				}
				words=words+1;
				if(words%123==1)
					System.err.print("prune "+words+" tokens, "+word2sense2freq.size()+" words\r");
			}
		}
		System.err.println("prune "+words+" tokens, "+word2sense2freq.size()+" words");
		in.close();
		
		// eval: for every sense, list the most markers in decreasing diagnocity 
		for(String s : new TreeSet<String>(sense2freq.keySet())) {
			System.out.println(s+"\t"+sense2freq.get(s));
			Vector<Integer> freqs = new Vector<Integer>();
			Vector<String> cues = new Vector<String>();
			
			// sort cues for diagnocity (not frequency)
			for(String w : word2sense2freq.keySet())
				if(word2sense2freq.get(w).get(s)!=null) 
					if(word2sense2freq.get(w).get(s)>=min) {
						int freq = word2sense2freq.get(w).get(s);
						for(int i = 0;i<freqs.size(); i++)
							//if(((double)freq)/(double)word2freq.get(w)>((double)freqs.get(i))/(double)word2freq.get(cues.get(i))) {	// diagnocity
							if(freq>freqs.get(i)) { 																				// frequency
								freqs.insertElementAt(freq,i);
								cues.insertElementAt(w,i);
								i=freqs.size();
							}
						if(!cues.contains(w)) {
							freqs.add(freq);
							cues.add(w);
						}
					}
			
			for(int i = 0; i<freqs.size();i++) {
				String w = cues.get(i);
				System.out.println("\t"+w+"\t"+
				"p("+s+"|"+w+")="+(word2sense2freq.get(w).get(s)*100)/word2freq.get(w)+"% "+
				               "("+word2sense2freq.get(w).get(s)+"/"+word2freq.get(w)+")\t"+
				"p("+s+"|"+w+")_raw="+(int)(100*word2sense2prob.get(w).get(s))+"%");
			}
		}
	}
}