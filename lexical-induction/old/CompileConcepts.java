import java.io.*;
import java.util.*;
import java.util.zip.*;

public class CompileConcepts {

	public static void main(String[] argv) throws Exception {
		System.err.println("synopsis: CompileConcepts LANG DEPTHS -dimlex DIMLEX[1..m].TSV [-dict DICT[1..n].TSV] [-wn WN[1..o].TSV] \n"+
			"\tLANG        BCP47 language code, should be the same as used in the other lexical resources\n"+
			"\tDEPTHS      PDTB hierarchy depths 1: top-level, 3: max depth, if multiple values are provided, just list all of them\n"+
			"\tDIMLEXi.TSV discourse marker lexicon in TSV format, see ../tsv/*.tsv, columns:\n"+
			"\t              FORM  string value, no language tags\n"+
			"\t              LANG  BCP47 language tag\n"+
			"\t              PDTB1 PDTB-top-level category\n"+
			"\t              PDTB2 PDTB category, second hierarchy level\n"+
			"\t              PDTB3 full PDTB category\n"+
			"\tDICTj.TSV dictionary in TSV format as provided by https://github.com/acoli-repo/acoli-dicts, cols:\n"+
			"\t              SRC     source language string, Turtle string with language code\n"+
			"\t              SRC_LEX source lexical entry URI\n"+
			"\t              SRC_SNS source lexical sense URI\n"+
			"\t              TRANS   translation or concept URI\n"+
			"\t              TGT_SNS target lexical sense URI\n"+
			"\t              TGT_LEX target lexical entry URI\n"+
			"\t              TGT     target language string, Turtle string with language code\n"+
			"\t              POS     source = target language part-of-speech (lexinfo URI)\n"+
			"\tWNk.TSV   WordNet in OMW TSV format, cols:\n"+
			"\t              SYNSET  synset id\n"+
			"\t              POS     part-of-speech (WN tags)\n"+
			"\t              LEMMA   form, Turtle string with language code\n"+
			"Compile a TIAD TSV file that maps all LANG words to Dimlex, WordNet or lexical concepts\n"+
			"Lexical concepts are FORM[/POS], we only return results from the first DICTj.TSV in which a form is found.\n"+
			"We do, however, return synset IDs from all wordnets, so don't mix schemes.");

		int i = 0;
		String lang = argv[i++];
		Set<Integer> depths = new TreeSet<Integer>();
		while(i<argv.length && !argv[i].startsWith("-")) {
			int depth = Integer.parseInt(argv[i++]);
			if(i<1 || i>3) {
				depth=Math.max(Math.min(3,depth),1);
				System.err.println("warning: depth must be 1 (top-level), 2 or 3 (max depth), normalized to "+depth);
			}			
			depths.add(depth);
		}
		
		if(depths.size()==0) {
			System.err.println("no depth specified, set depth=1");
			depths.add(1);
		}
		
		Map<String,Map<String,Set<String>>> form2dict2concept = new TreeMap<String,Map<String,Set<String>>>();
		
		// dimlexes
		if(i<argv.length && argv[i].equals("-dimlex")) {
			i++;
			while(i<argv.length && !argv[i].startsWith("-")) {
				String dict = argv[i++];
				InputStream raw = new FileInputStream(dict);
				if(dict.endsWith("gz"))
					raw = new GZIPInputStream(raw);
				if(dict.endsWith("zip"))
					raw = new ZipInputStream(raw);
				BufferedReader in = new BufferedReader(new InputStreamReader(raw));
				for(String line = in.readLine(); line!=null; line=in.readLine()) {
					String[] fields = line.split("\t");
					for(int depth : depths)
						if(fields.length>1+depth && fields[1].equals(lang)) {
							String form = "\""+fields[0]+"\"@"+fields[1];
							if(form2dict2concept.get(form)==null);
								form2dict2concept.put(form, new Hashtable<String,Set<String>>());
							if(fields.length>1+depth && fields[1+depth].matches(".*[a-zA-Z].*")) {
								String concept = fields[1+depth];
								if(form2dict2concept.get(form).get("dimlex") ==null)
									form2dict2concept.get(form).put("dimlex",new TreeSet<String>());
								form2dict2concept.get(form).get("dimlex").add(concept);
							}
						}
					System.err.print("\r"+form2dict2concept.size()+" forms ("+dict+")");
				}
				in.close();
				System.err.println();
			}

			// consolidation
			for(String form : new HashSet<String>(form2dict2concept.keySet())) {
				if(!form.equals(form.toLowerCase()))
					if(form2dict2concept.get(form.toLowerCase())==null) {
						form2dict2concept.put(form.toLowerCase(), new Hashtable<String,Set<String>>());
						for(String dict : form2dict2concept.get(form).keySet())
							if(form2dict2concept.get(form.toLowerCase()).get(dict)==null) 
								form2dict2concept.get(form.toLowerCase()).put(dict,form2dict2concept.get(form).get(dict)); // note that we double-link (!) the upper case dictionary
						System.err.print("\r"+form2dict2concept.size()+" forms (consolidation)");
					}
			}
			System.err.println();
		} else {
			System.err.println("warning: no dimlex found");
		}
		
		// dict concepts: word+pos (use if no other information given)
		if(i<argv.length && argv[i].equals("-dict")) {
			i++;
			while(i<argv.length && !argv[i].startsWith("-")) {
				String dict = argv[i++];
				InputStream raw = new FileInputStream(dict);
				if(dict.endsWith("gz"))
					raw = new GZIPInputStream(raw);
				if(dict.endsWith("zip"))
					raw = new ZipInputStream(raw);
				BufferedReader in = new BufferedReader(new InputStreamReader(raw));
				for(String line = in.readLine(); line!=null; line=in.readLine()) {
					String[] fields = line.split("\t");
					Vector<String> forms = new Vector<String>();
					if(fields[0].endsWith("@"+lang))
						forms.add(fields[0].replaceFirst("^[\"]+(.*)[\"]+@"+lang+"$","$1"));
					if(fields.length>7 && fields[7].endsWith("@"+lang))
						forms.add(fields[7].replaceFirst("^[\"]+(.*)[\"]+@"+lang+"$","$1"));
					String pos = "";
					if(fields.length>8) pos=fields[8].replaceAll(".*[\\\\/#]","");
					if(pos.replaceAll("[a-zA-Z]","").trim().length()>0) pos="/"+pos; else pos="";
					for(String form : forms) {
						form="\""+form+"\"@"+lang;
						if(form2dict2concept.get(form)==null)
							form2dict2concept.put(form, new LinkedHashMap<String,Set<String>>());
						if(form2dict2concept.get(form).get(dict)==null)
							form2dict2concept.get(form).put(dict,new HashSet<String>());
						form2dict2concept.get(form).get(dict).add(form+pos);
						System.err.print("\r"+form2dict2concept.size()+" forms ("+argv[i-1]+")");
					}
				}
				in.close();
				System.err.println();
			}
		}
		
		// wordnets
		if(i<argv.length && argv[i].equals("-wn")) {
			i++;
			while(i<argv.length && !argv[i].startsWith("-")) {
				String dict=argv[i++];
				InputStream raw = new FileInputStream(dict);
				if(dict.endsWith("gz"))
					raw = new GZIPInputStream(raw);
				if(dict.endsWith("zip"))
					raw = new ZipInputStream(raw);
				BufferedReader in = new BufferedReader(new InputStreamReader(raw));
				for(String line = in.readLine(); line!=null; line=in.readLine()) {
					String[] fields = line.split("\t");
					if(fields.length>2 && (fields[2].endsWith("@"+lang) || !fields[2].contains("@"))) {
						String form = fields[2].trim().replaceAll("^\"(.*)\"@[^\"]+$","$1");
						form="\""+form+"\"@"+lang;
						if(form2dict2concept.get(form)==null)
							form2dict2concept.put(form, new Hashtable<String,Set<String>>());
						if(form2dict2concept.get(form).get("wn")==null)
							form2dict2concept.get(form).put("wn", new HashSet<String>());
						form2dict2concept.get(form).get("wn").add(fields[0]);
						System.err.print("\r"+form2dict2concept.size()+" forms ("+dict+")");
					}
				}
				in.close();
				System.err.println();
			}
		}
		
		System.err.println("spellout");
		System.out.println("# TIAD format, with source lexeme natural language and target 'lexeme' concept");
		for(String form : form2dict2concept.keySet()) {
			LinkedHashSet<String> concepts = new LinkedHashSet<String>();
			Hashtable<String,String> concept2src = new Hashtable<String,String>();
			for(String dict : new String[] {"dimlex","wn"})
				if(form2dict2concept.get(form).get(dict)!=null)
					for(String c : form2dict2concept.get(form).get(dict)) {
						concepts.add(c);
						concept2src.put(c,dict);
					}
			if(concepts.size()==0 && !form.contains(" "))
				for(String dict : form2dict2concept.get(form).keySet())
					if(concepts.size()==0) 
						for(String c : form2dict2concept.get(form).get(dict)) {
							concepts.add(c);
							concept2src.put(c,dict);
						}
			for(String c : concepts) {
				c=concept2src.get(c)+":"+c;
				System.out.print(
					form+"\t"+	// SRC source language string, Turtle string with language code
					"\t"+		// SRC_LEX source lexical entry URI\n"+
					"\t"+       // SRC_SNS source lexical sense URI\n"+
					"\t"+       // TRANS   translation or concept URI\n"+
					"\t"+       // TGT_SNS target lexical sense URI\n"+
					c+"\t"+       // TGT_LEX target lexical entry URI\n"+
					"\""+c+"\"@CONCEPT\t"+       // TGT     target language string, Turtle string with PSEUDO-language code\n"+
					"\n");        // POS     source = target language part-of-speech (lexinfo URI)\n"+
			}			
		// TODO: keep all foreign language wordnet synsets ("blacklist" for projection)
		// (not necessary, just create multiple target files)
		}
		

		
	}
}