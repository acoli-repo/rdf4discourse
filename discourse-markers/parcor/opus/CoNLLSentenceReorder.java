import java.io.*;
import java.util.*;

/** reorder rows within a sentence:
 * this class allows to re-sort sentences, this is an auxiliary function helpful when working with 
 *  CoNLL representations of aligned bitext, with source and target language represented in on CoNLL
 *  file, but with different (original) word orders that may be reflected in numerical or complex IDs
 *  Note that we only reorder *within a sentence*, i.e., sentence boundaries remain intact
 *  
 * @author chiarcos
 *
 */
public class CoNLLSentenceReorder {
	
	private final static boolean DEBUG = false;
	
	protected enum Mode {
		STRING, NUMERICAL, MIXED
	}
	
	public static void main(String[] argv) throws IOException {
		
		Mode mode = Mode.MIXED;
		
		System.err.println("synopsis: CoNLLSentenceReorder [-mode=MODE] [COL1 ... COLn]\n"+
			"	-mode=MODE specify reordering mode\n"+
			"	     str[ing]    sort lexicographically by string values\n"+
			"	     num[erical] sort *only* according to numerical keys (doubles), otherwise, ignore non-numbers\n"+
			"	     mix[ed]     segment key strings into numerical and non-numerical subsequences,\n"+
			"	     (=default)  numerical sort for integers (substrings matching \"[0-9]+\"), \n"+
			"	                 lexicographic sort for other substrings, _ not evaluated\n"+
			"	                 i.e., s1.2 precedes s1.10, s1.2a precedes s1.2b, s1_19 precedes s1_020\n"+
			"	COLi       stacked ranking for reorder keys: default 0 to end\n"+
			"read CoNLL from stdin, reorder rows within a sentence, writen to stdout\n"+
			"sort for each key individually, with priority given from left to right\n"+
			"comments are written before the sentence, other lines without key are left in place\n");
		
		Vector<Integer> cols = new Vector<Integer>();
		for(String arg : argv) {
			try {
				cols.add(Integer.parseInt(arg));
			} catch (NumberFormatException e) {};
		}
		
		if(argv.length>0)
			for(String arg : argv) 
				if(arg.toLowerCase().startsWith("-mode=")) {
					String a = arg.replaceFirst("[^=]*=","").toLowerCase();
					for(Mode m : Mode.values()) 
						if(a.startsWith(m.toString().replaceFirst("^(...).*$","$1").toLowerCase()))
							mode=m;
				}
		
		System.err.print("running CoNLLSentenceReorder -mode="+mode);
		for(Integer col : cols)
			System.err.print(" "+col);
		System.err.println();
		
		BufferedReader in = new BufferedReader(new InputStreamReader(System.in));
		Writer out = new OutputStreamWriter(System.out);
		String buffer = "";
		for(String line = in.readLine(); line!=null; line=in.readLine()) {
			if(line.trim().equals("")) {
				reorder(Arrays.asList(buffer.split("\r?\n")), out, cols, mode);
				buffer="";
			} else 
				buffer=buffer+line+"\n";
		}
		
		reorder(Arrays.asList(buffer.split("\r?\n")), out, cols, mode);
		out.flush();
		out.close();
	}
		
	protected static String[] getKey(String string) {
		return string.replaceAll("([0-9]+)([^0-9])","$1\t$2").replaceAll("([^0-9])([0-9]+)","$1\t$2").split("\t");
	}
	
	static boolean greaterThan(String[] line1, String[] line2, List<Integer> cols, Mode mode) {
		if(cols.size()==0) {
			int i = 0;
			for(String col : line1) 
				cols.add(i++);
		}

		boolean result = greaterThanInternal(line1,line2,cols,mode);
		
		if(DEBUG) {
			System.err.print("greaterThan([");
			for(Integer col : cols) {
				if(line1.length>col)
					System.err.print(line1[col]);
				else System.err.print("null");
				System.err.print(" ");
			}
			System.err.print("], [");
			for(Integer col : cols) {
				if(line2.length>col)
					System.err.print(line2[col]);
				else System.err.print("null");
				System.err.print(" ");
			}
			System.err.println("], "+mode+")="+result);
		}
		
		return result;
	}
	
	private static boolean greaterThanInternal(String[] line1, String[] line2, List<Integer> cols, Mode mode) {
		for(Integer col : cols) 
			if(line1.length>col && line2.length>col) {
				switch(mode) {
					case NUMERICAL:
						try {
							if(Double.parseDouble(line1[col]) > Double.parseDouble(line2[col])) return true;
							if(Double.parseDouble(line1[col]) < Double.parseDouble(line2[col])) return false;
						} catch (NumberFormatException e) {
							//System.err.println(e.getClass()+" when comparing "+line1[col]+" and "+line2[col]);
						}
						break;
					case STRING:
						if(line1[col].compareTo(line2[col]) < 0) return false;
						if(line1[col].compareTo(line2[col]) > 0) return true;
						break;
					case MIXED:
						if(!line1[col].trim().equals("_") && !line1[col].trim().equals("_")) { // don't compare _
							String[] key1 = getKey(line1[col]);
							String[] key2 = getKey(line2[col]);
							for(int i = 0; i<Math.min(key1.length, key2.length); i++) {
								int diff = 0;
								try {
									diff = Integer.parseInt(key1[i])-Integer.parseInt(key2[i]);
								} catch (NumberFormatException e) {
									diff = key1[i].compareTo(key2[i]);
								}
								if(diff!=0) return diff>0;
							 }
							if(key1.length>key2.length) return true;
							if(key2.length<key1.length) return false;
						}
					break;
				}
			}			
		return false; // equal
	}
	
	static void reorder(List<String> lines, Writer out, List<Integer> cols, Mode mode) throws IOException {
		lines = new ArrayList<String>(lines);
		for(int i = 0; i<lines.size(); i++) {
			if(lines.get(i).trim().startsWith("#")) {
				out.write(lines.get(i)+"\n");
				lines.remove(i);
				i--;
			}
		}

		String[][] fields = new String[lines.size()][];
		for(int i = 0; i<lines.size(); i++) {
			fields[i]=lines.get(i).split("\t");
		}

		Vector<Integer> ranking = new Vector<Integer>();
		for(int i = 0; i<fields.length; i++) {
			boolean inserted = false;
			for(int j = 0; j<ranking.size() && !inserted; j++)
				if(greaterThan(fields[ranking.get(j)],fields[i],cols,mode)) {
					ranking.insertElementAt(i,j);
					inserted=true;
				}
			if(!inserted)
				ranking.add(i);
			
			if(DEBUG)
				if(cols.size()>0)
					for(Integer rank : ranking) {
						System.err.print("[");
						for(Integer c : cols) {
							if(fields[rank].length>c) {
								System.err.print(fields[rank][c]+" ");
							} else
								System.err.print("null ");
						}
						System.err.println("]");
					}					
					
		}
		
		for(Integer i : ranking) {
			String line = "";
			for(String f : fields[i]) 
				line=line+f+"\t";
			out.write(line.replaceFirst("\t$","")+"\n");
			out.flush();
		}
		out.write("\n");
		out.flush();
	}	
}