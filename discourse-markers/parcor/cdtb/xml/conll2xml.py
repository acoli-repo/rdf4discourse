# read CoNLL-style file with discourse annotations from ../conll from stdin
# write XML-enriched conll to stdout

import sys,re,os,traceback
from pprint import pprint

lines=[]
id2line={}
id2head={}

for line in sys.stdin:
	line=line.strip()	
	fields=line.split("\t")
	try:
		id=int(fields[0])
		id2line[id]=len(lines)
		for i in range(4,len(fields)):	
			# without coref, better use range(4,len(lines),2), this will be problematic if numbers occur as annotations (which shouldn't happen, though)
			try:
				head=int(fields[i])
				id2head[id]=head
				break
			except:
				pass
		lines.append(line)
	except:
		if not line.startswith("#"):
			line="# "+line
		lines.append(line)

head2deps={}
for id in id2line:
	if not id in head2deps:
		head2deps[id]=[id]
	else:
		head2deps[id].append(id)
	
	parents=[id]
	while(parents[-1] in id2head) and len(parents)==len(set(parents)):	# break cycles
		parents.append(id2head[parents[-1]])
		if not parents[-1] in head2deps:
			head2deps[parents[-1]]=[id]
		else:
			head2deps[parents[-1]].append(id)
	if len(parents)>len(set(parents)):
		sys.stderr.write("\twarning: heuristic cycle break for "+"-".join([str(p) for p in parents])+"\n")
		sys.stderr.flush()

# sort heads
head2start={}
head2len={}
heads=[]
for head in head2deps:
	head2start[head]=head2deps[head][0]
	head2len[head]=len(head2deps[head])
	for i in range(len(heads)):
		cmp=heads[i]
		if head2start[cmp] > head2start[head] or (head2start[cmp]==head2start[head] and head2len[cmp]<head2len[head]):
			heads=heads[0:cmp]+[head]+heads[cmp:]
			break
	if not head in heads:
		heads.append(head)
			
line=0
print("<node head=\"Text\">")
for id in id2line:
	while(line<id2line[id]):
		print(lines[line])
		line+=1
	for head in heads:
		if len(head2deps[head])>1:
			if head2deps[head][0]==id:
				# print("<node head=\""+lines[id2line[head]].split("\t")[0]+"\">")
				discourse=lines[id2line[head]].split("\t")[7]
				if(discourse!="_"):	# only discourse annotations
					print("<node rel=\""+discourse+"\">")
	print(lines[line])
	for head in reversed(heads):
		if len(head2deps[head])>1:
			if head2deps[head][-1]==id:
				# print("</node head=\""+lines[id2line[head]].split("\t")[0]+"\">")
				discourse=lines[id2line[head]].split("\t")[7]
				if(discourse!="_"):	# only discourse annotations
					print("</node>")
	line+=1
print("</node>")
	
		