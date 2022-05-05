
import java.io.*;
import java.net.URI;
import java.net.URL;
import java.util.*;
import java.util.zip.GZIPInputStream;

/**
 * retrieve written reps and synsets
 *     * */
public class WN31Reader {

	public WN31Reader() {
	}
	
	public static void main(String[] argv) throws Exception {
		String wordnet = "http://wordnet-rdf.princeton.edu/wn31.nt.gz";
		String wordnetfile = wordnet.replaceAll(".*/", "");
		System.err.println("synopsis: WN31Reader [Wordnet.nt.gz] \n"+
			"\tWORDNET.nt.gz WordNet in gzipped NT format as used for WN3.1, defaults to "+wordnetfile+", resp., "+wordnet+"\n"+
			"Take a WordNet in nt format and retrieve synsets, pos and written reps, write as TSV\n");

		if(argv.length>0)
			wordnet = argv[0];

		wordnetfile = wordnet.replaceAll(".*/", "");
		
		File wnfile = new File(wordnet);
		if(!wnfile.exists())
			wnfile = new File(wordnetfile);
		if(!wnfile.exists()) {
			URL wn = new URL(wordnet);
			System.err.println("retrieving "+wnfile+" from "+wordnet);
			InputStream in = wn.openStream();
			FileOutputStream out = new FileOutputStream(wnfile);
			for(int c = in.read(); c!=-1; c=in.read()) {
				out.write(c);
			}
			in.close();
			out.close();
		}
		
		System.err.println("reading "+wnfile);
		BufferedReader in = new BufferedReader(new InputStreamReader(new GZIPInputStream(new FileInputStream(wnfile))));
		TreeMap<String,LinkedHashSet<String>> writtenRep = new TreeMap<String,LinkedHashSet<String>>(); // lemon:writtenRep: Form -> String
		TreeMap<String,LinkedHashSet<String>> canonicalForm = new TreeMap<String,LinkedHashSet<String>>(); // lemon:canonicalForm: LexicalEntry -> Form
		TreeMap<String,LinkedHashSet<String>> isSenseOf = new TreeMap<String,LinkedHashSet<String>>(); // inverse of lemon:sense: LexicalEntry -> Sense
		TreeMap<String,LinkedHashSet<String>> lexicalizedSense = new TreeMap<String,LinkedHashSet<String>>(); // inverse of lemon:isLexicalizedSenseOf: Sense -> Concept
		TreeMap<String,LinkedHashSet<String>> narrower = new TreeMap<String,LinkedHashSet<String>>(); // inverse of wn:hyponym, instance_hyponym, similar, exemplifies, pertainym: Concept -> (super)Concept
				
		// full relation set:
//			<http://wordnet-rdf.princeton.edu/ontology#also>
//			<http://wordnet-rdf.princeton.edu/ontology#antonym>
//			<http://wordnet-rdf.princeton.edu/ontology#attribute>
//			<http://wordnet-rdf.princeton.edu/ontology#causes>
//			<http://wordnet-rdf.princeton.edu/ontology#definition>
//			<http://wordnet-rdf.princeton.edu/ontology#derivation>
//			<http://wordnet-rdf.princeton.edu/ontology#domain_region>
//			<http://wordnet-rdf.princeton.edu/ontology#domain_topic>
//			<http://wordnet-rdf.princeton.edu/ontology#entails>
//			<http://wordnet-rdf.princeton.edu/ontology#exemplifies>
//			<http://wordnet-rdf.princeton.edu/ontology#has_domain_region>
//			<http://wordnet-rdf.princeton.edu/ontology#has_domain_topic>
//			<http://wordnet-rdf.princeton.edu/ontology#holo_member>
//			<http://wordnet-rdf.princeton.edu/ontology#holo_part>
//			<http://wordnet-rdf.princeton.edu/ontology#holo_substance>
//			<http://wordnet-rdf.princeton.edu/ontology#hypernym>
//			<http://wordnet-rdf.princeton.edu/ontology#hyponym>
//			<http://wordnet-rdf.princeton.edu/ontology#instance_hypernym>
//			<http://wordnet-rdf.princeton.edu/ontology#instance_hyponym>
//			<http://wordnet-rdf.princeton.edu/ontology#is_exemplified_by>
//			<http://wordnet-rdf.princeton.edu/ontology#mero_member>
//			<http://wordnet-rdf.princeton.edu/ontology#mero_part>
//			<http://wordnet-rdf.princeton.edu/ontology#mero_substance>
//			<http://wordnet-rdf.princeton.edu/ontology#participle>
//			<http://wordnet-rdf.princeton.edu/ontology#partOfSpeech>
//			<http://wordnet-rdf.princeton.edu/ontology#pertainym>
//			<http://wordnet-rdf.princeton.edu/ontology#similar>

		for(String line = in.readLine(); line!=null; line=in.readLine()) {
			String[] triple = line.trim().replaceFirst("\\.$","").trim().split("\\s+");
			if(triple.length>2) {
				String sbj = triple[0];
				String pred = triple[1].replaceAll("[<>]", "");
				String obj = triple[2];
				for(int i = 3;i<triple.length; i++)	// note that literal can span over multiple triple fields
					obj=obj+" "+triple[i];
				if(pred.endsWith("writtenRep"))
					writtenRep=add(writtenRep, sbj, obj);
				if(pred.endsWith("canonicalForm"))
					canonicalForm=add(canonicalForm, sbj, obj);
				if(pred.endsWith("sense"))
					isSenseOf=add(isSenseOf,obj,sbj);
				if(pred.endsWith("isLexicalizedSenseOf"))
					lexicalizedSense=add(lexicalizedSense, obj, sbj);
				if(pred.endsWith("hypernym"))
						// || pred.endsWith("pertainym") || pred.endsWith("similar")) 
					//  || pred.endsWith(") // || pred.endsWith("similar") || pred.endsWith("exemplifies") || pred.endsWith("pertainym"))
					narrower = add(narrower, obj,sbj);	// check direction, something is weird here
				// wn:hyponym, instance_hyponym, similar, exemplifies, pertainym				
			}
			System.err.print("reading "+lexicalizedSense.size()+" synsets, "+writtenRep.size()+" forms\r");
		}
		in.close();
		System.err.println();
		
		TreeMap<String,LinkedHashSet<String>> concept2word = new TreeMap<String,LinkedHashSet<String>>();
		for(String synset : lexicalizedSense.keySet()) {
			for(String wordsense : lexicalizedSense.get(synset))
				if(isSenseOf.get(wordsense)!=null)
					for(String lexicalEntry : isSenseOf.get(wordsense))
						if(canonicalForm.get(lexicalEntry)!=null)
							for(String form : canonicalForm.get(lexicalEntry))
								if(writtenRep.get(form)!=null)
									for(String string : writtenRep.get(form))
										concept2word = add(concept2word,synset,string.replaceAll("\\([^\\)]*\\)",""));
			System.err.print("consolidating: "+concept2word.size()+" synsets\r");
			}

		lexicalizedSense.clear();
		isSenseOf.clear();
		canonicalForm.clear();
		writtenRep.clear();
		System.err.println();
		
		for(String c : concept2word.keySet())
			for(String w : concept2word.get(c))
				System.out.println(c+"\t"+c.replaceFirst(".*\\-([a-z]+)>","$1")+"\t"+w);
	}

	

	/** add entry to value *set* */
	protected static TreeMap<String, LinkedHashSet<String>> add(TreeMap<String, LinkedHashSet<String>> head2dep, String head, String dep) {
		if(head2dep.get(head)==null)
			head2dep.put(head, new LinkedHashSet<String>());
		head2dep.get(head).add(dep);
		return head2dep;
	}

}
