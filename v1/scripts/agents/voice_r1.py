import numpy as np, librosa, json
D='/home/user/Listener/v1/data/t_birdwalk/stems_raw/htdemucs/song/'
v,sr=librosa.load(D+'vocals.wav',sr=None,mono=False)
print(sr,v.shape)
m=v.mean(0)
hop=int(sr*0.01)
rms=librosa.feature.rms(y=m,frame_length=hop*2,hop_length=hop)[0]
db=20*np.log10(rms+1e-9)
# 1s vocal levels -> segments of vocal-active (>-45)
t=np.arange(len(db))*0.01
sec=[db[(t>=s)&(t<s+1)].mean() for s in range(188)]
act=[s for s in range(188) if np.percentile(db[(t>=s)&(t<s+1)],90)>-40]
# print runs
runs=[];st=None
for s in range(189):
    a = s in act
    if a and st is None: st=s
    if not a and st is not None: runs.append((st,s));st=None
print('active runs',runs)
# gaps within >0.25s below -50 (p10 level of 10ms) 
low=db<-50
i=0;gaps=[]
while i<len(low):
    if low[i]:
        j=i
        while j<len(low) and low[j]: j+=1
        if (j-i)*0.01>=0.15: gaps.append((round(t[i],2),round((j-i)*0.01,2)))
        i=j
    else:i+=1
print('gaps>=0.15s',len(gaps)); print([g for g in gaps if 0<g[0]<190 and g[1]>=0.3][:80])
# stereo of vocal: side/mid per segment
L,R=v[0],v[1]
for a,b in [(0,12),(12,47),(47,59),(60,110),(110,167),(140,167),(168,177)]:
    s=slice(int(a*sr),int(b*sr)); M=(L[s]+R[s])/2;S=(L[s]-R[s])/2
    print(a,b,'side/mid',round(np.sqrt((S**2).mean()/((M**2).mean()+1e-12)),3),'rms dB',round(20*np.log10(np.sqrt((m[s]**2).mean())+1e-9),1))
# spectral centroid vocal per window
for a,b in [(1,9),(9,12.5),(13,20),(25,40),(47,59),(60,70),(80,100),(120,140),(140,146),(157,163),(177,179)]:
    s=m[int(a*sr):int(b*sr)];
    c=librosa.feature.spectral_centroid(y=s,sr=sr).mean(); print('cent',a,b,round(c))
# onset rate of vocal stem in segments
oe=librosa.onset.onset_strength(y=m,sr=sr,hop_length=hop*5)
on=librosa.onset.onset_detect(onset_envelope=oe,sr=sr,hop_length=hop*5,units='time',backtrack=False)
np.save('/tmp/claude-0/v_on.npy',on)
for a,b in [(1,12),(25,40),(47,59),(60,70),(80,100),(120,140),(140,147),(157,163)]:
    n=((on>=a)&(on<b)).sum();print('vocal onset/s',a,b,round(n/(b-a),2))
