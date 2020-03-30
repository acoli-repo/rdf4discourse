import java.io.*;
import java.util.*;

public class PDTB2dimlex {

	final String lang;
	final Map<String,Map<String,Integer>> form2rel2freq = new TreeMap<String,Map<String,Integer>>();
	final Vector<String> files = new Vector<String>();
	final Map<String,Integer> form2freq = new Hashtable<String,Integer>();
	
	PDTB2dimlex(String lang) {
		this.lang=lang;
	}

	public static void main(String[] argv) throws Exception {
		System.err.println("synopsis: PDTB2dimlex LANG RAW1 [.. RAWn] -ann ANN1 [.. ANNn]\n"+
			"\tLANG BCP language tag\n"+
			"\tRAWi text file that PDTB3-style annotations point to\n"+
			"\tANNi PDTB3-style standoff annotation to file RAWi\n"+
			"We store discourse markers and alternative lexicalizations together with the frequency of their explicit realization, write as DimLex-like XML.\n"+
			"Note that we don't do automatic lowercasing, but that we count uppercase attestations of lowercase-attested elements for the latter, too.\n"+
			"We return counts for upper case entries only if no corresponding lowercase entry does exist.");
			
		String lang = argv[0];
		Vector<String> txt = new Vector<String>();
		Vector<String> ann = new Vector<String>();
		int i = 1;
		while(i<argv.length && !argv[i].equals("-ann"))
			txt.add(argv[i++]);
		i++;
		while(i<argv.length)
			ann.add(argv[i++]);
			
		if(txt.size()!=ann.size()) {
			System.err.println("error: number of raw and annotation files not matching: "+txt.size()+" raw files, but "+ann.size()+" annotation files");
		} else {
			
			PDTB2dimlex me = new PDTB2dimlex(lang);
			
			for(i = 0; i<txt.size(); i++)
				me.add(new File(txt.get(i)), new File(ann.get(i)));
			
			System.out.println(me.asDimlex());
		}
		
	}
	
	/** implicits do not contribute to counts */
	public void add(File txt, File ann) throws IOException {
		
		StringWriter tmp = new StringWriter();
		BufferedReader in = new BufferedReader(new FileReader(txt));
		for(int c = in.read(); c!=-1; c=in.read())
			tmp.write(c);
		in.close();
		tmp.flush();
		
		String raw = tmp.toString();
		tmp.close();		
		
		in = new BufferedReader(new FileReader(ann));
		for(String line = in.readLine(); line!=null; line=in.readLine()) {
			String fields[] = line.split("\\|");
			int freq = 0;
			String marker = "";
			String rel = null;
			if(	fields[0].equalsIgnoreCase("Implicit") ) {
				marker = fields[7];
				rel = fields[8];
			} else if(	
				fields[0].equalsIgnoreCase("Explicit") || 
				fields[0].equalsIgnoreCase("AltLex") ) {
					rel = fields[8];
					String pos = fields[1].trim();
					while(pos.length()>0) {
						int start = Integer.parseInt(pos.replaceFirst("[^0-9].*",""));
						pos=pos.replaceFirst("^[0-9]+[^0-9]+","");
						int end = Integer.parseInt(pos.replaceFirst("[^0-9].*",""));
						pos = pos.replaceFirst("[0-9]*[^0-9]*","");
						if(!marker.equals("")) marker=marker+" ... ";
						marker=marker+raw.substring(start,end);
					}
					freq++;
				}
			if(marker!=null && !marker.trim().equals("") && rel!=null && !rel.trim().equals("")) {
				marker=marker.replaceAll("\\s+"," ").trim();
				if(form2rel2freq.get(marker)==null) form2rel2freq.put(marker, new TreeMap<String,Integer>());
				if(form2rel2freq.get(marker).get(rel)==null) 
					form2rel2freq.get(marker).put(rel,freq);
				else form2rel2freq.get(marker).put(rel,form2rel2freq.get(marker).get(rel)+freq);
			}
		}
		in.close();
		files.add(ann.getName());
		
		// frequency counts for all non-markers (single words only)
		for(String s : raw.split("\\s+")) {
			s=s.replaceAll("[,\\.!?\"()-:;0-9]+","");
			if(!s.equals("")) {
				if(form2rel2freq.get(s)==null) {
					if(form2freq.get(s)==null) form2freq.put(s,1);
					else form2freq.put(s,form2freq.get(s)+1);
					if(!s.equals(s.toLowerCase())) {
						s=s.toLowerCase();
						if(form2rel2freq.get(s)==null) {
							if(form2freq.get(s)==null) form2freq.put(s,1);
							else form2freq.put(s,form2freq.get(s)+1);
						}
					}						
				}
			}
		}
		
		// frequency counts for all markers (incl. known phrases -- note that we replace ... by .*)
		raw=raw.replaceAll("\\s+"," ").replaceAll("([.!?])","$1\n"); // sentence splitting
		for(String m : form2rel2freq.keySet()) {
			String myraw = raw;
			String pattern=m.replaceAll("\\([^\\)]*\\)","").trim().replaceAll("([?\\(\\)\\[\\]\\\\{}])","\\\\$1").replaceAll(" \\.\\.\\. "," [^\\n]* ");
			if(!pattern.equals("")) {
				int f = 0;
				while(myraw.matches(".*"+pattern+".*")) {
					f++;
					myraw=myraw.replaceFirst(".*"+pattern,"");
				}
				if(form2freq.get(m)==null) form2freq.put(m,f);
				else form2freq.put(m,form2freq.get(m)+f);
				
				if(!m.equals(m.toLowerCase())) {
					m=m.toLowerCase();
					myraw = raw.toLowerCase();
					pattern=m.replaceAll("\\([^\\)]*\\)","").trim().replaceAll("([?\\(\\)\\[\\]\\\\{}])","\\\\$1").replaceAll(" \\.\\.\\. "," [^\\n]* ");
					f = 0;
					while(myraw.matches(".*"+pattern+".*")) {
						f++;
						myraw=myraw.replaceFirst(".*"+pattern,"");
					}
					if(form2freq.get(m)==null) form2freq.put(m,f);
					else form2freq.put(m,form2freq.get(m)+f);
				}
			}
		}
	}
	
	public String asDimlex() {
		String result = "<dimlex>";
		int i = 0;
		for(String entry : form2rel2freq.keySet())
		  if(form2rel2freq.get(entry.toLowerCase())==null) { // if so, this is counted there, only
			result=result+
				"<entry id=\"k"+(++i)+"\" word=\""+entry+"\">\n"+
				"  <orths>\n"+
				"    <orth>\n";
			if(entry.matches(".*\\s.*")) {
			  result=result+
				"      <part type=\"phrasal\">"+entry+"</part>\n";
			} else {
				result=result+
				"      <part type=\"single\">"+entry+"</part>\n";
			}
			result=result+
				"    </orth>\n"+
				"  </orths>\n";
			if(form2freq.get(entry)!=null) {
				int discFreq = form2freq.get(entry);
				for(String rel : form2rel2freq.get(entry).keySet())
					discFreq = discFreq-form2rel2freq.get(entry).get(rel);
				if(discFreq>0 || form2rel2freq.get(entry).size()>1) {
					result=result+"<ambiguity>\n";
					if(discFreq>0)
						result=result+"<non_conn freq=\""+discFreq+"\">1</non_conn>\n";
					if(form2rel2freq.get(entry).size()>1)
						result=result+"<sem_ambiguity>1</sem_ambiguity>\n";
					result=result+"</ambiguity>\n";
				}
				if(discFreq>0)
					result=result+
						"<non_conn_reading>\n"+
						"  <example tfreq=\""+discFreq+"\"/>\n"+
						"</non_conn_reading>\n";
			}
			result=result+"<syn>\n";
			for(String rel : form2rel2freq.get(entry).keySet())
				result=result+
					"<sem>\n"+
					"  <pdtb3_relation sense=\""+rel+"\" freq=\""+form2rel2freq.get(entry).get(rel)+"\"/>\n"+
					"</sem>\n";
			result=result+
				"</syn>\n"+
				"</entry>\n";
		}
		result=result+"</dimlex>";
		return result;
	}
}