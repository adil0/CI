
  
wts=[]
for a in range(0,10,1):
    for b in range(0,10,1):
        for c in range(0,10,1):
            for d in range(0,10,1):
                wt=[round(a*0.1,2),round(b*0.1,2),round(c*0.1,2),round(d*0.1,2)]
                if(sum(wt)==1):
#                     print(wt)
                    wts.append(wt)
    

for wt in wts:
    print(wt)