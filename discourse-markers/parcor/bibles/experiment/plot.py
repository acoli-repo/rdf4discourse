import re,sys,os,traceback,argparse,math
import matplotlib.pyplot as plot

args=argparse.ArgumentParser(description=" read a TSV file from stdin, assume that the first column contains the x axis label, each following column is a data column, calculate avg and stdev over each col and plot it ")
args.add_argument("-t","--title", type=str)
args.add_argument("-min","--min_y", type=float)
args.add_argument("-max","--max_y", type=float)
args=args.parse_args()

x2col2vals={}

for line in sys.stdin:
    line=line.strip()
    fields=line.split("\t")
    if len(fields)>1:
        try:
            x=fields[0]
            if re.match(r"^[0-9]+$",x):
                x=int(x)
            for col in range(1,len(fields)):
                val=float(fields[col])
                if not x in x2col2vals:
                    x2col2vals[x]={}
                if not col in x2col2vals[x]:
                    x2col2vals[x][col]=[]
                x2col2vals[x][col].append(val)
        except:
            pass

tab=[]

for x in sorted(x2col2vals.keys()):
    row=[x]
    for col,vals in x2col2vals[x].items():
        avg=sum(vals)/len(vals)
        var=0
        for val in vals:
            var+=(val-avg)*(val-avg)

        row.append(avg)
        row.append(math.sqrt(var/len(vals)))
    tab.append(row)
    print("\t".join([ str(val)[0:5] for val in row ]))

print()

x=[ row[0] for row in tab ]

#plot.plot( x,y )
max_y=None
min_y=None
for y in range(1,len(tab[0]),2):
    if max_y==None:
        max_y=max([ row[y]+row[y+1] for row in tab ])
    else:
        max_y=max(max_y,max([ row[y]+row[y+1] for row in tab ]))
    if min_y==None:
        min_y=min([ row[y]+row[y+1] for row in tab ])
    else:
        min_y=min(min_y,min([ row[y]+row[y+1] for row in tab ]))
    plot.errorbar( x, [row[y] for row in tab] , yerr=[ [0 for row in tab],[row[y+1] for row in tab ] ], fmt="o-")

if args.min_y!=None or args.max_y!=None:
    if args.max_y==None:
        args.max_y=max_y
    if args.min_y==None:
        args.min_y=min_y
    plot.ylim(ymin=args.min_y, ymax=args.max_y)


if args.title!=None:
    plot.title(args.title)
plot.show()
