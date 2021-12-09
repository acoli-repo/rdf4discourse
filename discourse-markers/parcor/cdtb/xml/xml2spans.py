# read CoNLL+XML data from stdin, extract triples: ARG1 ([nucleus of] matrix EDU), ARG2 ([nucleus of] dependent EDU), relation
import sys,os,re,traceback
from pprint import pprint
from _io import TextIOWrapper
from copy import deepcopy


class CoNLLXML:

	nodes=[]
	node2parent={}
	parent2nodes={}
	roots={}
	
	def __init__(self, fileOrStream):
	
		nodes=[]
		node2parent={}
		roots=[]
		lines=[]
		stack=[]
		parent2nodes={}
	
		if type(fileOrStream)==str:
			with open(fileOrStream,"r") as input:
				self.__init__(input)
		elif type(fileOrStream)==TextIOWrapper:
			i=0
			for line in fileOrStream:
				line=line.strip()
				i+=1
				if(line.startswith("</")):
					if len(stack)>0:
						stack.pop()
					else:
						sys.stderr.write("warning: \""+line+"\" in line "+(str(i))+" closes a non-open element\n")
						sys.stderr.flush()
				else:
					nodes.append(line)
					lines.append(i)
					node=len(nodes)-1
					if len(stack)==0:
						roots.append(node)
					else:
						node2parent[node]=stack[-1]
					if(line.startswith("<")):
						stack.append(node)

			for node in node2parent:
				parent=node2parent[node]
				if not parent in parent2nodes:
					parent2nodes[parent]=[node]
				else:
					parent2nodes[parent].append(node)
						
			if len(stack)>0:
				sys.stderr.write("warning: \""+nodes[stack[-1]]+"\" in line "+(str(lines[stack[-1]]))+" is not closed\n")
				sys.stderr.flush()
			if len(roots)>1:
				sys.stderr.write("warning: multiple roots detected:\n")
				for root in roots:
					sys.stderr.write("\t\""+nodes[root]+"\" in line "+str(lines[root])+"\n")
				sys.stderr.flush()

		self.nodes=nodes
		self.node2parent=node2parent
		self.parent2nodes=parent2nodes
		self.roots=roots
	
	# writes an XML-like tree
	def tree_out(self, node=None, indent=""):
		roots=self.roots
		nodes=self.nodes
		parent2nodes=self.parent2nodes
	
		result=""
		if node==None:
			for root in roots:
				result=result+self.tree_out(root,indent)
		else:
			if node < len(nodes):
				if nodes[node].strip().startswith("<"):
					result=indent
				result=result+nodes[node]+"\n"
				if node in parent2nodes:
					for child in parent2nodes[node]:
						result=result+self.tree_out(child, indent=indent+"  ")
				if nodes[node].startswith("<"):
					name=re.sub(r"^[^<]*<([^ >/]+)[ />].*$",r"\1",nodes[node])
					result=result+indent+"</"+name+">\n"
		return result

	def __get_text__(self, arg):
		tmp=""
		for row in arg:
			try:
				id=int(row[0])
				if len(row)>1:
					tmp=tmp+row[1]+" "
			except:
				pass
		return tmp		
		
	def __get_distance__(self, arg1,arg2):
		""" call with two arrays of conll annotations """
		arg1start=None
		arg2start=None
		arg1end=None
		arg2end=None
		for row in arg1:
			try:
				id=int(row[0])
				if(arg1start==None):
					arg1start=id
				arg1end=id
			except:
				pass
		
		for row in arg2:
			try:
				id=int(row[0])
				if(arg2start==None):
					arg2start=id
				arg2end=id
			except:
				pass

		if(arg1end < arg2start):
			direction="ARG1 ARG2"
			distance=arg1end-arg2start
		elif arg2end < arg1start:
			direction="ARG2 ARG1"
			distance=arg1start-arg2end
		elif arg2start < arg1start:
			direction="ARG2(ARG1)"
			distance=1
		else:
			direction="ARG1(ARG2)"
			distance=-1
		return distance,direction
		
	def get_training_triples(self):
		""" output is simiar to get_triples with textMode=True, but return all counterexamples, sample attested relations up """
		conll_positives=self.get_triples(textMode=False)
		positives={}	# dict: arg1 - arg2 - rel
		arg2conll={}
		for x,row in enumerate(self.get_triples(textMode=True).split("\n")):
			fields=row.split("\t")
			if len(fields)>2:
				arg1=fields[1]
				arg2=fields[2]
				
				rel,conll1,conll2=conll_positives[x]
				for arg,conll in [(arg1,conll1), (arg2,conll2)]:
					if not arg in arg2conll:
						arg2conll[arg]=conll

				if not arg1 in positives:
					positives[arg1]={ arg2 :  rel }
				elif not arg2 in positives[arg1]:
					positives[arg1][arg2]=rel

		# perform complete oversampling using a left-to-right comparison
		result=[]
		for arg1 in arg2conll:
			conll1=arg2conll[arg1]
			for arg2 in arg2conll:
				if arg1!=arg2:
					conll2=arg2conll[arg2]
					distance,_=self.__get_distance__(conll1,conll2)
					if distance <= 0:
						# negative
						rel=None
						
						# positive
						if arg1 in positives and arg2 in positives[arg1]:
							rel=positives[arg1][arg2]
						
						# inverted
						elif arg2 in positives and arg1 in positives[arg2]:
							rel="INVERTED:"+positives[arg2][arg1]
							
						result.append((rel,arg1,arg2,distance))
						if rel==None:	# oversampling
							if arg1 in positives:
								for arg2 in positives[arg1]:
									rel=positives[arg1][arg2]
									conll1=arg2conll[arg1]
									conll2=arg2conll[arg2]
									distance,_=self.__get_distance__(conll1,conll2)
									if distance > 0:
										rel="INVERTED:"+positives[arg1][arg2]
							else:
								if arg2 in positives:
									for arg1 in positives[arg2]:
										rel=positives[arg2][arg1]
									conll1=arg2conll[arg1]
									conll2=arg2conll[arg2]
									distance,_=self.__get_distance__(conll1,conll2)
									if distance <= 0:
										rel="INVERTED:"+positives[arg2][arg1]
							if rel!=None:
								result.append((rel,arg1,arg2,distance))
		return result
		
		
	def get_triples(self,node=None, textMode=False):
		""" return (".", "./text()", "../text()") for all nodes.
			by default, return full annotations.
			With textMode=True, return only the content of the second column, add direction as fourth output column, add token distance as fifth output column """
		roots=self.roots
		nodes=self.nodes
		node2parent=self.node2parent
		parent2nodes=self.parent2nodes
		result=[]
		if textMode:
			result=""
			
		if node==None:
			for root in roots:
				result=result+self.get_triples(root,textMode=textMode)
		else:
			if node < len(nodes):
				if nodes[node].strip().startswith("<") and node in node2parent:
					element=nodes[node]
					parent=node2parent[node]
					arg2=[]
					for leaf in parent2nodes[parent]:
						val=nodes[leaf]
						if(not val.strip().startswith("<")):
							arg2.append(val.split("\t"))
					arg1=[]
					if node in parent2nodes:
						for leaf in parent2nodes[node]:
							val=nodes[leaf]
							if(not val.strip().startswith("<")):
								arg1.append(val.split("\t"))
					
					if textMode:
						distance,direction=self.__get_distance__(arg1,arg2)
						arg1=self.__get_text__(arg1)
						arg2=self.__get_text__(arg2)
						
						result=result+element+"\t"+arg2.strip()+"\t"+arg1.strip()+"\t"+direction+"\t"+str(distance)+"\n"
					else:
						result.append((element,arg2,arg1))
					
			if node in parent2nodes:
				for child in parent2nodes[node]:
					result=result+self.get_triples(child,textMode=textMode)
		return result

if len(sys.argv)<=1:
	sys.stderr.write("reading from stdin\n")
	sys.stderr.flush()
	me=CoNLLXML(sys.stdin)
	print(me.get_triples(textMode=True))
	print()
	print(me.get_training_triples())
	print("\n".join( [ "\t".join( [ str(val) for val in row ] ) for row in me.get_training_triples() ] ) ) 
else:
	for file in sys.argv[1:]:
		me=CoNLLXML(file)
		print("# "+file)
		print(me.get_triples(textMode=True))
		print()
		print(me.get_training_triples())
		print("\n".join( [ "\t".join( [ str(val) for val in row ] ) for row in me.get_training_triples() ] ) ) 


	