import java.io.*;
import java.util.*;
import java.net.*;
import java.util.zip.*;

public class Moses2CoNLL {
	
	static BufferedReader getBufferedReader(String fileOrUri) throws IOException {
		System.err.print("initializing "+fileOrUri+" ..");
		InputStream stream = null;
		try {							// is it a file?
			stream=new FileInputStream(fileOrUri);
		} catch (IOException e) { 		// is it a url?
			stream=(new URL(fileOrUri)).openStream();
		}
		
		if(fileOrUri.toLowerCase().matches(".*gz(ip)?$")) 		// gunzip
			stream=new GZIPInputStream(stream);
		else if(fileOrUri.toLowerCase().matches(".*\\.z(ip)$"))	// unzip
			stream=new ZipInputStream(stream);

		BufferedReader result = new BufferedReader(new InputStreamReader(stream));

		System.err.println(". ok");
		return result;
	}
	
	public static void main(String argv[]) throws Exception {
		if(!Arrays.asList(argv).toString().contains("-silent")) {
			System.err.println("synopsis: Moses2CoNLL model src tgt [-invert]\n"+
			"\tmodel    MOSES model file or URI\n"+
			"\tsrc, tgt tokenized text files as taken as MOSES/GIZA++ input\n"+
			"\t-invert  write tgt as reference column\n");
		}

		BufferedReader model = getBufferedReader(argv[0]);
		BufferedReader src = getBufferedReader(argv[1]);
		BufferedReader tgt = getBufferedReader(argv[2]);
		boolean invert = argv.length>3 && argv[3].toLowerCase().equals("-invert");
		
		System.err.print("write to stdout ..");

		String m = "";
			while(m!=null) {
				m = model.readLine();
				String s = src.readLine();
				String t = tgt.readLine();
				System.out.println("# "+s+"\n# "+t);	// write original data as CoNLL comment
				
				Vector<Integer> fromS = new Vector<Integer>();
				Vector<Integer> toT = new Vector<Integer>();
				for(String a : m.split(" ")) {
					fromS.add(Integer.parseInt(a.replaceFirst("-.*","")));
					toT.add(Integer.parseInt(a.replaceFirst(".*-","")));
				}
				
				String[] ss = s.split(" ");
				String[] ts = t.split(" ");

				if(invert) {
					String[] tmp = ss;
					ss=ts;
					ts=tmp;
					
					Vector<Integer> tmp2 = fromS;
					fromS = toT;
					toT=tmp2;
				}
				
				HashSet<Integer> processedTs = new HashSet<Integer>();

				String sid = "_";
				String sform="_";
				String tid = "_";
				String tform = "_";
				
				for(int j=0; j<ts.length && !toT.contains(j); j++) 
					  if(!processedTs.contains(j)) {
						sid="*";
						tid=""+(j+1);
						tform=ts[j];
						System.out.println(sid+"\t"+sform+"\t"+tid+"\t"+tform);
						processedTs.add(j);
					}

				
				for(int i = 0; i<ss.length; i++) {
					sid = ""+(i+1);
					sform = ss[i];
					tid = "_";
					tform = "_";
					if(!fromS.contains(i)) {
						System.out.println(sid+"\t"+sform+"\t"+tid+"\t"+tform);
					} else {
						int a = fromS.indexOf(i);
						int j=toT.get(a);
						while(fromS.contains(i)) {
							a = fromS.indexOf(i);
							j=toT.get(a);
							tid=""+(j+1);
							tform = ts[j];
							if(processedTs.contains(j)) tform="*";
							fromS.remove(a);
							toT.remove(a);
							processedTs.add(j);
							System.out.println(sid+"\t"+sform+"\t"+tid+"\t"+tform);
							sform="*";
						}
						for(++j; j<ts.length && !toT.contains(j); j++) 
						  if(!processedTs.contains(j)) {
							sid="_";
							sform="_";
							tid=""+(j+1);
							tform=ts[j];
							System.out.println(sid+"\t"+sform+"\t"+tid+"\t"+tform);
							processedTs.add(j);
						}
					}
				}
				
				for(int j = 0; j<ts.length; j++) // shouldn't happen
					if(!processedTs.contains(j)) {
						sid="*";
						tid=""+(j+1);
						tform=ts[j];
						System.out.println(sid+"\t"+sform+"\t"+tid+"\t"+tform);
						processedTs.add(j);
					}
				
				System.out.println();
			}
		model.close();
		src.close();
		tgt.close();
		
		System.err.println(". ok");		
	}
}