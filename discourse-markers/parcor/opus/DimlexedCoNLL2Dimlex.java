import java.io.*;
import java.util.*;

public class DimlexedCoNLL2Dimlex {
	
	public String help() {
		return
			"synopsis: "+this.getClass()+
				" WORD_COL SENSE_COL [SENSE_COL1..n] [-silent]\n"+
			"\tWORD_COL column in the input file that contains the WORD (or LEMMA), first is 0\n"+
			"\tSENSE_COL column in the input file that contains the disambiguated sense (set to -1 if none)\n"+
			"\tSENSE_COLi column in the input file that contains a possible sense, e.g., projected from one particular source\n"+
			"\t-silent suppress help message\n"+
			"Builds a discourse marker inventory from a SENSE-annotated CoNLL file.\n"+
			"Read CoNLL file from stdin, write dimlex.xml to stdout\n";
	}
	
	public static void main(String[] argv) throws Exception {
		DimlexedCoNLL2Dimlex me = new DimlexedCoNLL2Dimlex();
		
		int lastCol = 0;
		boolean silent = Arrays.asList(argv).toString().toLowerCase().replaceAll("[^\\-a-z0-9]+"," ").contains(" -silent ");
		if(!silent)
			System.err.println(me.help());
		
		int word = Integer.parseInt(argv[0]);
		lastCol=word;
		int senseCol = Integer.parseInt(argv[1]);
		lastCol=Math.max(lastCol,senseCol);
		Vector<Integer> senseCols = new Vector<Integer>();
		for(int i = 2; i<argv.length; i++) {
			try {
				senseCols.add(Integer.parseInt(argv[i]));
				lastCol=Math.max(lastCol,Integer.parseInt(argv[i]));
			} catch (NumberFormatException e) {}
		}
		
		if(!silent)
			System.err.println("run with parameters COL_WORD="+word+" COL_SENSE="+senseCol+" COL_SENSE1..n="+senseCols+" silent="+silent);
		
		Hashtable<String, Integer> word2freq = new Hashtable<String,Integer>();
		Hashtable<String, Hashtable<String, Integer>> marker2sense2freq = new Hashtable<String, Hashtable<String, Integer>>();
		// Hashtable<String, Hashtable<String, String>> marker2sense2example = new Hashtable<String, Hashtable<String, String>>(); // maybe later
		Hashtable<String, Hashtable<Integer, Hashtable<String,Integer>>> marker2src2sense2freq = new Hashtable<String, Hashtable<Integer, Hashtable<String,Integer>>>();
		
		BufferedReader in = new BufferedReader(new InputStreamReader(System.in));
		int i = 0;
		System.err.print("read from stdin\r");
		for(String line=""; line!=null; line=in.readLine()) {
			line=line.replaceFirst("([^\\\\])#.*$","$1").replaceFirst("^#.*$","");
			String[] fields = line.split("\t");
			if(fields.length>lastCol) {
				i++;
				String marker = fields[word];
				
				// word freq
				if(word2freq.get(marker)==null) word2freq.put(marker,0);
				word2freq.put(marker,word2freq.get(marker)+1);
				
				// sense freq (disambiguated only)
				if(senseCol>=0 && fields[senseCol].replaceAll("[^a-zA-Z]","").length()>0) {
					if(marker2sense2freq.get(marker)==null) 
						marker2sense2freq.put(marker, new Hashtable<String, Integer>());
					if(marker2sense2freq.get(marker).get(fields[senseCol])==null)
						marker2sense2freq.get(marker).put(fields[senseCol],0);					
					marker2sense2freq.get(marker).put(fields[senseCol],marker2sense2freq.get(marker).get(fields[senseCol])+1);
				} else // sense freqs (alternative senseCols: only if disambiguation failed)
					for(int j = 0; j<senseCols.size(); j++) {
					  int senseColi = senseCols.get(j);
					  if(fields[senseColi].replaceAll("[^a-zA-Z]","").length()>0) {
						if(marker2src2sense2freq.get(marker)==null)
							marker2src2sense2freq.put(marker, new Hashtable<Integer, Hashtable<String,Integer>>());
						if(marker2src2sense2freq.get(marker).get(senseColi)==null)
							marker2src2sense2freq.get(marker).put(senseColi, new Hashtable<String,Integer>());
						if(marker2src2sense2freq.get(marker).get(senseColi).get(fields[senseColi])==null)
							marker2src2sense2freq.get(marker).get(senseColi).put(fields[senseColi], 0);
						marker2src2sense2freq.get(marker).get(senseColi).put(fields[senseColi], marker2src2sense2freq.get(marker).get(senseColi).get(fields[senseColi])+1);
					  }
					}
			}
			if(i % 123 == 0 && !silent) System.err.print("read "+i+" tokens with "+marker2sense2freq.size()+" discourse markers\r");
		}
		System.err.println("read "+i+" tokens with "+marker2sense2freq.size()+" discourse markers ... done");
		
		if(!silent)
			System.err.println(marker2sense2freq);
		
		System.err.println("consolidate ..");
		// disambiguate senses
		for(String marker : new TreeSet<String>(marker2sense2freq.keySet())) {
			// get the most frequent unambiguous sense
			Vector<String> unambiguous = new Vector<String>();
			for(String sense : marker2sense2freq.get(marker).keySet()) 
				if(!sense.matches(".*[,;].*") && sense.trim().length()>0) {
					for(int k = 0; k<unambiguous.size() && !unambiguous.contains(sense); k++)
						if(marker2sense2freq.get(marker).get(sense)>marker2sense2freq.get(marker).get(unambiguous.get(k)))
							unambiguous.insertElementAt(sense,k);
					if(!unambiguous.contains(sense)) unambiguous.add(sense);
				}
			
			// organize ambiguous senses: within each ;-group, reorder ,-separated senses alphabetically
			// disambiguate ,;-separated senses => most frequent unambiguous sense
			for(String sense : new HashSet<String>(marker2sense2freq.get(marker).keySet()))
				if(sense.matches(".*[,;].*")) { // ambiguous senses
					String newSense = "";
					String[] senseGroups = sense.split(" *; *");
					for(i = 0; i<senseGroups.length; i++) {
						List<String> senses = new ArrayList<String>(new TreeSet<String>(Arrays.asList(senseGroups[i].replaceAll("[ \t,]+"," ").trim().split(" "))));
						String subsense = "";
						for(int j = 0; j<senses.size(); j++) {
							subsense=subsense+senses.get(j);
							if(j<senses.size()-1)
								subsense=subsense+", ";
						}
						newSense = newSense+subsense;
						if(i<senseGroups.length-1)
							newSense=newSense+"; ";
					}
					if(!newSense.equals(sense)) {
						int freq = marker2sense2freq.get(marker).get(sense);
						marker2sense2freq.get(marker).remove(sense);
						if(marker2sense2freq.get(marker).get(newSense)==null)
							marker2sense2freq.get(marker).put(newSense,0);
						marker2sense2freq.get(marker).put(newSense, marker2sense2freq.get(marker).get(newSense)+freq);
						if(!silent)
							System.err.println("normalize: "+marker+"/"+newSense+ " += "+freq+ "("+marker+"/"+sense+")");
					}
				}

			
			// disambiguate ,;-separated senses => most frequent unambiguous sense => star (*)-marked
			for(String sense : new HashSet<String>(marker2sense2freq.get(marker).keySet()))
				if(sense.matches(".*[,;|].*")) { // ambiguous senses
					HashSet<String> subsenses = new HashSet<String>(Arrays.asList(sense.replaceAll("[|,;\t ]+"," ").trim().split(" ")));
					String mainSense = null;
					for(i = 0; i<unambiguous.size() && mainSense==null; i++)
						if(subsenses.contains(unambiguous.get(i))) mainSense=unambiguous.get(i);
					if(mainSense!=null) {
						int freq = marker2sense2freq.get(marker).get(sense);
						marker2sense2freq.get(marker).remove(sense);
						if(marker2sense2freq.get(marker).get(mainSense+"*")==null) {
							marker2sense2freq.get(marker).put(mainSense+"*",marker2sense2freq.get(marker).get(mainSense));
						}
						marker2sense2freq.get(marker).put(mainSense+"*", marker2sense2freq.get(marker).get(mainSense+"*") + freq);
						if(!silent)
							System.err.println("disambiguate: "+marker+"/"+mainSense+ "* += "+freq+ "("+marker+"/"+sense+")");
					}
				}
			
			// add resolvable senses from SENSE_COLi (statistics are skewed *only* if we have no SENSE, but multiple SENSE_COLs for the same word)
			// note that we check for *containment* only, as this is the matching criteria for sense aggregation
			if(marker2src2sense2freq.get(marker)!=null)
			  for(int src : marker2src2sense2freq.get(marker).keySet())
				for(String sense : marker2src2sense2freq.get(marker).get(src).keySet()) {
					int freq = marker2src2sense2freq.get(marker).get(src).get(sense);
					String origSense = sense;
					sense = (" "+sense+" ").replaceAll("[^a-zA-Z0-9]+"," ");
					String mainSense = null;
					for( i = 0; i<unambiguous.size() && mainSense==null; i++)
						if(sense.contains(unambiguous.get(i).replaceAll("[^a-zA-Z0-9]+"," "))) mainSense=unambiguous.get(i);
					if(mainSense!=null) {
						marker2src2sense2freq.get(marker).get(src).remove(sense);
						if(marker2sense2freq.get(marker).get(mainSense+"*")==null)
							marker2sense2freq.get(marker).put(mainSense+"*", marker2sense2freq.get(marker).get(mainSense));
						marker2sense2freq.get(marker).put(
							mainSense+"*",
							marker2sense2freq.get(marker).get(mainSense)+
							freq);
						if(!silent)
							System.err.println("expand: "+marker+"/"+mainSense+ "* += "+freq+ "("+marker+"/"+origSense+"["+src+"])");
					}
				}

			// presentation order: frequency
			Vector<String> ranking = new Vector<String>();
			for(String sense : unambiguous) {
				for(i = 0; i<ranking.size() && !ranking.contains(sense); i++)
					if(marker2sense2freq.get(marker).get(sense) > marker2sense2freq.get(marker).get(ranking.get(i)))
						ranking.insertElementAt(sense,i);
				if(!ranking.contains(sense)) ranking.add(sense);
			}
			for(String sense : new HashSet<String>(unambiguous)) {
				sense = sense+"*";
				if(marker2sense2freq.get(marker).get(sense)!=null) {
					unambiguous.add(sense); // for the sublist
					for(i = 0; i<ranking.size() && !ranking.contains(sense); i++)
						if(marker2sense2freq.get(marker).get(sense) > marker2sense2freq.get(marker).get(ranking.get(i)))
							ranking.insertElementAt(sense,i);
					if(!ranking.contains(sense)) ranking.add(sense);
				}
			}
			for(String sense : new TreeSet<String>(marker2sense2freq.get(marker).keySet()))
				if(!unambiguous.contains(sense)) {
					for(i = 0; i<ranking.size() && !ranking.contains(sense); i++) 
						if(marker2sense2freq.get(marker).get(sense)>marker2sense2freq.get(marker).get(ranking.get(i)))
							ranking.insertElementAt(sense,i);
					if(!ranking.contains(sense))
						ranking.add(sense);
				}

				
			int discourse = 0;
			for(String sense : ranking)
				if(!ranking.contains(sense+"*"))
					discourse+=marker2sense2freq.get(marker).get(sense);
			System.out.println(marker+" (total: "+word2freq.get(marker)+", discourse>="+discourse+", i.e., "+(int)(0.5+(100.0*discourse)/(double)word2freq.get(marker))+"%)");
			for(String sense : ranking)
				System.out.println("\t"+sense+"\t"+marker2sense2freq.get(marker).get(sense) + " ("+(int)(0.5+(100.0*marker2sense2freq.get(marker).get(sense))/(double)word2freq.get(marker))+"%)");
		}
	}
}