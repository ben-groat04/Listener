import librosa, numpy as np
D='/home/user/Listener/v1/data/video1/stems_raw/htdemucs/song/'
sr=22050;hop=256
dr,_=librosa.load(D+'drums.wav',sr=sr);bs,_=librosa.load(D+'bass.wav',sr=sr);ot,_=librosa.load(D+'other.wav',sr=sr)
fr=sr/hop
oe=librosa.onset.onset_strength(y=dr,sr=sr,hop_length=hop)
on=librosa.onset.onset_detect(onset_envelope=oe,sr=sr,hop_length=hop,units='time',delta=0.1)
print('onsets per 10s:',[int(((on>=a)&(on<a+10)).sum()) for a in range(0,190,10)])
def rms(x,w=0.05):
    n=int(w*sr);m=len(x)//n;return np.sqrt((x[:m*n].reshape(m,n)**2).mean(1))
for nm,x in [('drums',dr),('bass',bs),('other',ot)]:
    r=20*np.log10(rms(x)+1e-6)
    # dropouts: runs below (median-18dB) lasting >=0.15 s
    med=np.median(r);low=r<med-18;runs=[];i=0
    while i<len(r):
        if low[i]:
            j=i
            while j<len(r) and low[j]:j+=1
            if (j-i)*0.05>=0.15 and (nm!='bass'):runs.append((round(i*0.05,2),round((j-i)*0.05,2)))
            i=j
        else:i+=1
    print(nm,'median dB',round(med,1),'dropouts(start,len):',runs[:30])
# beat-period 5s windows density of 'gap' IOIs ~0.37 vs 0.19
ioi=np.diff(on)
for a in range(0,190,20):
    m=(on[:-1]>=a)&(on[:-1]<a+20);i=ioi[m]
    print(a,'frac ~0.19:',round(((i>0.15)&(i<0.23)).mean(),2),'frac ~0.38:',round(((i>0.33)&(i<0.43)).mean(),2),'frac<0.15:',round((i<0.15).mean(),2))
# last 6 s detail and drum RMS
r=rms(dr,0.1);print('drum dB 183-189:',np.round(20*np.log10(r[1830:1887]+1e-6),0)[::3])
