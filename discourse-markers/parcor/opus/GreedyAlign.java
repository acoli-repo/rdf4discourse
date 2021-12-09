import java.io.*;
import java.util.*;

// preprocess data: skip deviating tokens and comments

public class GreedyAlign {
	
	protected static final int CONTENT_WORD_LENGTH = 5;
	
	public static void main(String[] argv) throws Exception {
		
		int contentWordLength = CONTENT_WORD_LENGTH;
		
		System.err.println("synopsis: GreedyAlign file1.tsv file2.tsv [-col1=coli[,colj,..,colk] [-col2=coll[,colm,..,coln]] [-length=INT]\n"+
		"\tfilei.tsv tsv (e.g., CoNLL) file, if -, read from stdin\n"+
		"\tcoli      column(s) containing the entries to be compared, by default 0\n"+
		"\t          if multiple columns are defined, their values are concatenated with <TAB> before comparison\n"+
		"\t-length=x in order to minimize alignment errors on function words, this defines\n"+
		"\t          the minimal length for *a contextually non-anchored* content word to count as a match\n"+
		"\t          by default, -length="+contentWordLength+"\n"+
		"align tsv (e.g., CoNLL) files, greedy baseline implementation:\n"+
		"\t- exact matches only,\n"+
		"\t- applies first match in the stack,\n"+
		"\t- left to right\n"+
		"no split or force mode, inserts *RETOK* and ?\n"+
		"NOTE that we append as many columns for missing right elements *as seen before*, i.e., we do not guarantee length\n"+
		"NOTE that we remove in-line comments from file1.tsv");
		
		BufferedReader left;
		BufferedReader right;
		if(argv[0].equals("-") || argv[0].equals("--")) {
			left = new BufferedReader(new InputStreamReader(System.in));
			right = new BufferedReader(new FileReader(argv[1]));
		} else {
			left=new BufferedReader(new FileReader(argv[0]));
			if(argv[1].equals("-") || argv[1].equals("--")) 
				right=new BufferedReader(new InputStreamReader(System.in));
			else right = new BufferedReader(new FileReader(argv[1]));
		}
		
		long matches = 0;
		long leftMisses = 0;
		long rightMisses = 0;
		
		Vector<String> leftStack = new Vector<String>();
		Vector<String> rightStack = new Vector<String>();
		Vector<String> leftWord = new Vector<String>();
		Vector<String> rightWord = new Vector<String>();

		Vector<Integer> colsL=new Vector<Integer>();
		Vector<Integer> colsR = new Vector<Integer>();
		
		for(int i = 2; i<argv.length; i++) {
			if(argv[i].toLowerCase().startsWith("-col1="))
				for(String v : argv[i].replaceFirst(".*=","").split(","))				
					colsL.add(Integer.parseInt(v));
			if(argv[i].toLowerCase().startsWith("-col2="))
				for(String v : argv[i].replaceFirst(".*=","").split(","))
					colsR.add(Integer.parseInt(v));
			if(argv[i].toLowerCase().startsWith("-length="))
				contentWordLength=Integer.parseInt(argv[i].replaceFirst(".*=",""));
		}
		
		if(colsL.size()==0) colsL.add(0);
		if(colsR.size()==0) colsR.add(0);
		
		int leftCols = 0;
		int rightCols = 0;
		
		String l = left.readLine();
		String r = right.readLine();
		
		// write alignments
		while(l!=null && r!=null) {
			String[] ls = l.replaceFirst("^#.*","").replaceFirst("([^\\\\])#.*","$1").split("\t");
			String[] rs = r.replaceFirst("^#.*","").replaceFirst("([^\\\\])#.*","$1").split("\t");
			
			String lKey = "";
			try {
				for(Integer colL : colsL)
					lKey=lKey+ls[colL]+"\t";
				lKey=lKey.trim();
			} catch (Exception e) {
				lKey=null;
			}
			leftWord.add(lKey);
			
			String rKey = "";
			try {
				for(Integer colR : colsR)
					rKey=rKey+rs[colR]+"\t";
				rKey=rKey.trim();
			} catch (Exception e) {
				rKey=null;
			}
			rightWord.add(rKey);
			
			// System.err.println(leftWord);
			// System.err.println(rightWord+"\n");
			
			
			leftCols=Math.max(leftCols,ls.length);
			rightCols=Math.max(rightCols,rs.length);
			
			leftStack.add(l);
			rightStack.add(r);
			
			int lMatch = -1;
			int rMatch = -1;
			
			for(int ln = 0; ln<leftWord.size() && lMatch==-1; ln++)
				if(leftWord.get(ln)!=null)
					for(int rn=0; rn<rightWord.size() && rMatch==-1; rn++)
						if(rightWord.get(rn)!=null)
							if(leftWord.get(ln).equals(rightWord.get(rn))) { // this is too greedy -- often lead astray by punctuation or function words
								boolean isContextuallyAnchored = (leftStack.size()==1 || rightStack.size()==1);
								if(!isContextuallyAnchored) {
									boolean hasRightMismatch = false;
									for(int i = 0; !hasRightMismatch && i<rn; i++)
										hasRightMismatch=rightWord.get(i)!=null;
									isContextuallyAnchored = !hasRightMismatch;
								}
								if(!isContextuallyAnchored) {
									boolean hasLeftMismatch = false;
									for(int i = 0; !hasLeftMismatch && i<rn; i++)
										hasLeftMismatch=leftWord.get(i)!=null;
									isContextuallyAnchored = !hasLeftMismatch;
								}
								boolean isContentWord = isContextuallyAnchored || (leftWord.get(ln).toLowerCase().replaceAll("[^0-9a-z]+","").length()>=contentWordLength);
								if(!isContentWord) {
									String nextR = null;
									for(int i = rn+1; nextR==null && i<rightWord.size(); i++) 
										nextR=rightWord.get(i);
									if(nextR==null) {
										try { 
											right.mark(50000);
											String[] nextRs = right.readLine().split("\t");
											try {
												nextR="";
												for(Integer colR : colsR)
													nextR=nextR+rs[colR]+"\t";
												nextR=nextR.trim();
											} catch (Exception e) {
												nextR=null;
											}
											right.reset();
										} catch (Exception e) {
											e.printStackTrace();
										}
									}
									
									if(nextR!=null) {
										String nextL = null;
										for(int i = ln+1; nextL==null && i<leftWord.size(); i++) 
											nextL=leftWord.get(i);
										if(nextL==null) {
											try { 
												left.mark(5000);
												String[] nextLs = left.readLine().split("\t");
												try {
													nextL="";
													for(Integer colL : colsL)
														nextL=nextL+rs[colL]+"\t";
													nextL=nextL.trim();
												} catch (Exception e) {
													nextL=null;
												}
												left.reset();
											} catch (Exception e) {
												e.printStackTrace();
											}
										}
										isContextuallyAnchored=(nextL!=null && nextR.equals(nextL));
									}
								}

								if(isContentWord || isContextuallyAnchored) {
									lMatch=ln;
									rMatch=rn;
								}
							}
							
			// if we have a match: write left stack
			while(lMatch>0) {
				String content = leftStack.get(0).replaceFirst("([^\\\\])#.*","$1");	// remove in-line comments
				System.out.print(content);
				if(!content.trim().startsWith("#") && content.trim().length()>0) {
					leftMisses=leftMisses+1;
					for(int i = 0; i<rightCols; i++)
						System.out.print("\t?");
				}
				System.out.println();
				leftStack.remove(0);
				leftWord.remove(0);
				lMatch--;
			}
			
			// if we have a match: write right stack, skip the matched column
			while(rMatch>0) {
				String content = rightStack.get(0);
				if(content.trim().startsWith("#")) {
					System.out.println(content);
				} else if(content.trim().length()>0) { // we ignore sentence breaks on the right side 
					rightMisses=rightMisses+1;
					for(int i = 0; i<leftCols; i++) {
						if(i==colsL.get(0)) System.out.print("*RETOK*-"+rightWord.get(0).trim().replaceFirst("\t.*",""));	// we add from the first colR
						else System.out.print("?");
						if(i<leftCols-1) System.out.print("\t");
					}
					String[] fields = content.split("\t");
					for(int i = 0; i<fields.length; i++) 
						if(i!=colsR.get(0)) // we drop the first compared row
							System.out.print("\t"+fields[i]);
				}
				System.out.println();
				rightStack.remove(0);
				rightWord.remove(0);
				rMatch--;
			}
			
			// write match
			if(lMatch==0 && rMatch==0) {
				matches=matches+1;
				String content = leftStack.get(0).replaceFirst("([^\\\\])#.*","$1");	// remove in-line comments on the left side
				System.out.print(content);
				String[] fields = rightStack.get(0).split("\t");
				for(int i = 0; i<fields.length; i++) 
					if(i!=colsR.get(0)) // we drop the first compared row
						System.out.print("\t"+fields[i]);
				System.out.println();
				rightStack.remove(0);
				rightWord.remove(0);
				leftStack.remove(0);
				leftWord.remove(0);
			}
			
			// read next lines
			l = left.readLine();
			r = right.readLine();			
			
			System.err.print("diagnostics: "+
				matches+" ("+((1+matches)*100/(1+matches+leftMisses)) +"%) matches, "+
				leftMisses+" ("+((1+leftMisses)*100/(1+matches+leftMisses))+"%) left misses, "+
				rightMisses+" ("+((1+rightMisses)*100/(1+matches+rightMisses))+"%) right misses\r");
			}
		
		while(l!=null && r!=null) {
			if(l!=null) leftStack.add(l);
			if(r!=null) rightStack.add(r);
					
			// write leftStack
			while(leftStack.size()>0) {
				String content = leftStack.get(0).replaceFirst("([^\\\\])#.*","$1");	// remove in-line comments
				System.out.print(content);
				if(!content.trim().startsWith("#") && content.trim().length()>0) {
					leftMisses=leftMisses+1;
					for(int i = 0; i<rightCols; i++)
						System.out.print("\t?");
				}
				System.out.println();
				leftStack.remove(0);
				leftWord.remove(0);
			}
			
			// write rightStack
			while(rightStack.size()>0) {
				String content = rightStack.get(0);
				if(content.trim().startsWith("#")) {
					System.out.println(content);
				} else if(content.trim().length()>0) { // we ignore sentence breaks on the right side 
					rightMisses=rightMisses+1;
					for(int i = 0; i<rightCols; i++) {
						if(i==colsL.get(0)) System.out.print("*RETOK*-"+rightWord.get(0).trim().replaceFirst("\t.*",""));	// we add from the first colR
						else System.out.print("?");
						if(i<rightCols-1) System.out.print("\t");
					}
					String[] fields = content.split("\t");
					for(int i = 0; i<fields.length; i++) 
						if(i!=colsR.get(0)) // we drop the first compared line
							System.out.print("\t"+fields[i]);
				}
				System.out.println();
				rightStack.remove(0);
				rightWord.remove(0);
			}
			
			if(l!=null) l=left.readLine();
			if(r!=null) r=right.readLine();
		}
			
			System.err.println("diagnostics: "+
				matches+" ("+(matches*100/(matches+leftMisses)) +"%) matches, "+
				leftMisses+" ("+(leftMisses*100/(matches+leftMisses))+"%) left misses, "+
				rightMisses+" ("+(rightMisses*100/(matches+rightMisses))+"%) right misses");
	}
}
		
		
		