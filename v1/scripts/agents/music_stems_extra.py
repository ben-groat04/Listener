import sys,json,numpy as np,librosa
d=sys.argv[1]; out=d+'/audio_features/extra'
sr=22050
st={k:librosa.load(f'{d}/stems/{k}.mp3',sr=sr)[0] for k in ['vocals','drums','bass','other']}
bt=np.array(json.load(open(d+'/audio_features/beat_times.json')))
beat=0.627
# 1) vocal stem activity: seconds with rms>0.03 -> contiguous spans (gap<2s merged)
v=st['vocals']; r=np.array([np.sqrt((v[i*sr:(i+1)*sr]**2).mean()) for i in range(len(v)//sr)])
act=r>0.04
spans=[];s=None
for i,a in enumerate(act):
    if a and s is None:s=i
    if not a and s is not None:
        spans.append([s,i]);s=None
if s is not None:spans.append([s,len(act)])
m=[]
for sp in spans:
    if m and sp[0]-m[-1][1]<=2:m[-1][1]=sp[1]
    else:m.append(sp)
print('vocal spans',m)
# 2) kick/snare/hat from drums stem: band onsets and time within bar
dr=st['drums']
def band(y,lo,hi):
    S=np.abs(librosa.stft(y,n_fft=2048,hop_length=256));f=librosa.fft_frequencies(sr=sr,n_fft=2048)
    return S[(f>=lo)&(f<hi)].sum(0)
for nm,(lo,hi) in {'kick':(30,120),'snare':(1500,4000),'hat':(7000,11000)}.items():
    e=band(dr,lo,hi); o=librosa.onset.onset_detect(onset_envelope=np.maximum(0,np.diff(e,prepend=e[0])),sr=sr,hop_length=256,units='time',backtrack=False)
    # phase within 4-beat bar, anchored on first beat in a window 30-70s where drums steady
    ph=((o-bt[0])/beat)%4
    h,_=np.histogram(ph,bins=16,range=(0,4))
    print(nm,len(o),'per 16th-step histogram',h.tolist())
# 3) bass stem: share of time silent (rms<0.01 per 0.1s) per section
b=st['bass'];fr=int(sr*0.1)
br=np.array([np.sqrt((b[i*fr:(i+1)*fr]**2).mean()) for i in range(len(b)//fr)])
for a,e in [(0,10),(10,30),(30,71),(71,92),(92,133),(133,152),(152,194),(194,215),(215,230)]:
    x=br[a*10:e*10];print('bass',a,e,'silent frac',round(float((x<0.02).mean()),2),'mean',round(float(x.mean()),3))
# 4) pitch of bass notes (f0) in verse and hook
f0,vf,_=librosa.pyin(b[sr*35:sr*50],fmin=30,fmax=200,sr=sr)
nn=librosa.hz_to_note(f0[vf]) if vf.any() else []
from collections import Counter
print('bass notes verse 35-50s',Counter(nn).most_common(6))
f0,vf,_=librosa.pyin(b[sr*12:sr*27],fmin=30,fmax=200,sr=sr)
print('bass notes hook 12-27s',Counter(librosa.hz_to_note(f0[vf])).most_common(6) if vf.any() else None)
# vocal pitch range for hook (sung) 
f0,vf,_=librosa.pyin(v[sr*13:sr*28],fmin=80,fmax=700,sr=sr)
print('hook vocal notes',Counter(librosa.hz_to_note(f0[vf])).most_common(8) if vf.any() else None)
f0,vf,_=librosa.pyin(v[sr*40:sr*60],fmin=70,fmax=400,sr=sr)
print('verse vocal median Hz',float(np.nanmedian(f0)), 'range',float(np.nanpercentile(f0,10)),float(np.nanpercentile(f0,90)))
# 5) syllable rate: vocal onsets/s in verse
o=librosa.onset.onset_detect(y=v[sr*40:sr*60],sr=sr,units='time');print('verse vocal onsets/s',len(o)/20)
