import numpy as np, librosa, json
d='data/video1/stems_raw/htdemucs/song/'
v,sr=librosa.load(d+'vocals.wav',sr=22050); b,_=librosa.load(d+'bass.wav',sr=22050); dr,_=librosa.load(d+'drums.wav',sr=22050)
bt=np.array(json.load(open('data/video1/audio_features/beat_times.json')))
print(type(bt),bt[:3] if bt.ndim else bt)
def rms(x,h=0.02):
    n=int(h*sr); return np.sqrt(np.convolve(x**2,np.ones(n)/n,'same'))
bs=rms(b); 
# bass bursts (onsets of bass above -35 dB after gap)
db=20*np.log10(bs+1e-9)
on=[]; prev=False
for i in range(0,len(db),int(0.05*sr)):
    cur=db[i]>-35
    if cur and not prev: on.append(i/sr)
    prev=cur
print('bass onsets 100-170s',[round(t,1) for t in on if 100<t<170])
# voice segs
vs=20*np.log10(rms(v,0.05)+1e-9); act=vs>-45
seg=[];s=None
for i in range(0,len(act),int(0.05*sr)):
    if act[i] and s is None: s=i/sr
    if not act[i] and s is not None: seg.append((s,i/sr)); s=None
m=[]
for a,b2 in seg:
    if m and a-m[-1][1]<0.35: m[-1]=(m[-1][0],b2)
    else: m.append((a,b2))
m=[x for x in m if x[1]-x[0]>0.3]
print(len(m))
bon=[t for t in on if 130<t<170]
for a,b2 in m:
    if 135<a<170: print('v',round(a,1),round(b2,1),'near bass onset',[round(t,1) for t in bon if abs(t-a)<1.0])
# drum energy in 0.1s around 27.9 and 31.7 and bar markers
dd=rms(dr,0.05)
for t in [27.0,27.5,27.9,28.3,31.2,31.7,32.2]:
    print(t,round(20*np.log10(dd[int(t*sr)]+1e-9),1))
# spectral comparison: 0:10-18, 0:20-31, 1:19-27, 2:21-36, 2:44-48
for a,b2 in [(10,18),(20,31),(41,56),(79,87),(135,155),(164,168)]:
    seg_=v[int(a*sr):int(b2*sr)]
    S=np.abs(librosa.stft(seg_,n_fft=2048))**2; f=librosa.fft_frequencies(sr=sr,n_fft=2048)
    mask=S.sum(0)>np.percentile(S.sum(0),60); P=S[:,mask].mean(1); c=np.cumsum(P)/P.sum()
    cen=(f*P).sum()/P.sum()
    print(a,b2,'cent',round(cen),'ro85',round(f[np.searchsorted(c,.85)]),'ro95',round(f[np.searchsorted(c,.95)]),'>5k %',round(100*P[f>5000].sum()/P.sum(),1),'noise floor dB(pctile10 frames)',round(10*np.log10(np.percentile(S.sum(0),10)+1e-12),1))
# vocal stem leakage check: floor at outro
for a,b2 in [(0,8),(170,185)]:
    print('floor',a,b2,round(20*np.log10(np.sqrt((v[int(a*sr):int(b2*sr)]**2).mean())+1e-9),1))
# section boundaries from audio_features
import glob; print(glob.glob('data/video1/audio_features/*.json'))
