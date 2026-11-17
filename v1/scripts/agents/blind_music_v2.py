import numpy as np, librosa, json
D='/home/user/Listener/v1/data/video1/'
y,sr=librosa.load(D+'audio/song.wav',sr=22050,mono=False)
m=y.mean(0)
C=librosa.feature.chroma_cqt(y=m,sr=sr,hop_length=2048)
ct=librosa.frames_to_time(np.arange(C.shape[1]),sr=sr,hop_length=2048)
names=['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
secs=[(0,15),(15,40),(40,66),(66,76),(76,88),(88,109),(109,118),(118,134),(134,159),(159,172),(172,189)]
for a,b in secs:
    v=C[:,(ct>=a)&(ct<b)].mean(1); v=v/v.max()
    print(a,b,' '.join(f'{n}:{x:.2f}' for n,x in zip(names,v) if x>0.35))
# fine tuning offset
print('tuning',librosa.estimate_tuning(y=m,sr=sr))
# band energies from STFT with L/R
S=np.abs(librosa.stft(m,n_fft=4096,hop_length=2048))
f=librosa.fft_frequencies(sr=sr,n_fft=4096)
st=librosa.frames_to_time(np.arange(S.shape[1]),sr=sr,hop_length=2048)
bands={'sub20-60':(20,60),'bass60-200':(60,200),'lowmid200-800':(200,800),'mid800-3k':(800,3000),'pres3-8k':(3000,8000),'air8k+':(8000,11000)}
print('sec',list(bands))
for a,b in secs:
    s=(st>=a)&(st<b)
    print(a,b,[round(10*np.log10((S[(f>=lo)&(f<hi)][:,s]**2).sum(0).mean()+1e-9),1) for lo,hi in bands.values()])
# sub-bass pulses 118-158
sub=S[(f>=35)&(f<75)].sum(0)
for a,b in [(118,160)]:
    s=(st>=a)&(st<b); t=st[s]; v=sub[s]
    pk=[t[i] for i in range(1,len(v)-1) if v[i]>v[i-1] and v[i]>v[i+1] and v[i]>np.percentile(v,85)]
    print('subpk',np.round(pk,1))
# fine-grained rms for events
yy=m; hop=11025
r=librosa.feature.rms(y=yy,frame_length=11025,hop_length=2756)[0]; rt=librosa.frames_to_time(np.arange(len(r)),sr=sr,hop_length=2756)
for a,b in [(0,3),(72,80),(113,124),(146,150),(184,189)]:
    s=(rt>=a)&(rt<b); print(a,b,np.round(20*np.log10(r[s]+1e-6),0)[::2].tolist())
# stereo
L,R=y[0],y[1]
M=(L+R)/2;Sd=(L-R)/2
for a,b in secs:
    s=slice(int(a*sr),int(b*sr))
    print(a,b,'S/M dB',round(10*np.log10((Sd[s]**2).mean()/(M[s]**2).mean()),1),'corr',round(float(np.corrcoef(L[s],R[s])[0,1]),2))
# spectral flux onset density per section, crest
for a,b in secs:
    s=slice(int(a*sr),int(b*sr)); x=m[s]
    print(a,b,'crest dB',round(20*np.log10(np.abs(x).max()/np.sqrt((x**2).mean())),1))
# end: last 6 s
r2=20*np.log10(r+1e-6)
print('last',np.round(r2[-40::4],0))
