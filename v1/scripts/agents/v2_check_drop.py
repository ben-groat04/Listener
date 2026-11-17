import librosa,numpy as np
exec(open('v2_check_env.py').read().split("if __name__")[0])
e,fr=res['bass']
low=e<-50
# runs
runs=[];i=0
while i<len(low):
    if low[i]:
        j=i
        while j<len(low) and low[j]: j+=1
        runs.append((i/fr,(j-i)/fr)); i=j
    else:i+=1
for s,d in runs:
    if 88<s<290 and d>0.15: print(f"{int(s//60)}:{s%60:05.2f} dur{d:.2f}")
