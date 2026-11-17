import librosa, numpy as np, json, sys
D='/home/user/Listener/v1/data/video1/stems_raw/htdemucs/song/'
sr=22050
dr,_=librosa.load(D+'drums.wav',sr=sr,mono=True)
hop=256
# band-split drums: low (kick) <150, mid (snare) 150-2500, high >5k
S=np.abs(librosa.stft(dr,n_fft=1024,hop_length=hop))
f=librosa.fft_frequencies(sr=sr,n_fft=1024)
def env(lo,hi):
    e=S[(f>=lo)&(f<hi)].sum(0); return np.maximum(0,np.diff(np.log1p(e*10),prepend=0))
bands={'low':env(30,150),'mid':env(150,2500),'high':env(5000,10000)}
fr=sr/hop
# overall onset env tempo
oe=librosa.onset.onset_strength(y=dr,sr=sr,hop_length=hop)
ac=librosa.autocorrelate(oe-oe.mean(),max_size=int(4*fr))
lags=np.arange(len(ac))/fr
pk=[(round(lags[i],3),round(float(ac[i]/ac[0]),3)) for i in range(5,len(ac)-1) if ac[i]>ac[i-1] and ac[i]>=ac[i+1] and ac[i]/ac[0]>0.08]
print('AC peaks (lag s, rel):',pk[:20])
# IOI hist
on=librosa.onset.onset_detect(onset_envelope=oe,sr=sr,hop_length=hop,units='time',delta=0.1)
ioi=np.diff(on); print('n onsets',len(on),'median ioi',np.median(ioi))
h,e=np.histogram(ioi,bins=np.arange(0,1.6,0.04));print([ (round(e[i],2),int(h[i])) for i in range(len(h)) if h[i]>10])
# beat phase pattern of 16 steps per bar using beats file
bt=np.array(json.load(open('/home/user/Listener/v1/data/video1/audio_features/beat_times.json')))
bt=np.array(bt if bt.ndim==1 else bt)
print('beats',len(bt),bt[:3],np.median(np.diff(bt)),'std',np.std(np.diff(bt)))
d=np.diff(bt); print('beat gap min/max',d.min(),d.max(),'gaps >0.85:',[round(b,1) for b,g in zip(bt,d) if g>0.85][:20])
# step-grid: refine period via fitting. grid 16th = beat/4
P=np.median(d)/4
# fit phase/period over whole track using onset env sum
best=None
for per in np.arange(P*0.98,P*1.02,P*0.0005):
  for ph in np.arange(0,per,per/20):
    t=np.arange(ph,len(oe)/fr,per); v=oe[(t*fr).astype(int).clip(0,len(oe)-1)].mean()
    if best is None or v>best[0]: best=(v,per,ph)
print('best 16th period',best[1],'=> BPM',60/(best[1]*4),'phase',best[2])
per,ph=best[1],best[2]
for name,e_ in bands.items():
    steps=np.arange(ph,len(e_)/fr,per)
    vals=np.array([e_[int(s*fr):int(s*fr)+3].max() for s in steps if int(s*fr)+3<len(e_)])
    n=len(vals)//16*16
    for pos in (4,8,16):
        m=vals[:n].reshape(-1,pos).mean(0); print(name,pos,np.round(m/m.max(),2))
np.save('/tmp/steps.npy',np.array([per,ph]))
# per 20s: pattern
