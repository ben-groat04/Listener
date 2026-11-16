import librosa, numpy as np, json, sys
p='/home/user/Listener/v1/data/video1/audio/song.wav'
out='/home/user/Listener/v1/data/video1/audio_features/extra/'
y,sr=librosa.load(p,sr=22050,mono=False)
L,R=y; m=(L+R)/2; s=(L-R)/2
dur=m.shape[0]/sr
H,P=librosa.effects.hpss(m)
S=np.abs(librosa.stft(m,n_fft=2048,hop_length=512))**2
f=librosa.fft_frequencies(sr=sr,n_fft=2048)
bands={'sub<80':(20,80),'bass80-250':(80,250),'lowmid250-800':(250,800),'mid800-3k':(800,3000),'pres3-6k':(3000,6000),'air6k+':(6000,11000)}
hop=512; fps=sr/hop
def per_sec(x): # frames->seconds
    n=int(dur); return np.array([x[int(i*fps):int((i+1)*fps)].mean() for i in range(n)])
res={}
for k,(a,b) in bands.items():
    e=S[(f>=a)&(f<b)].sum(0); res[k]=per_sec(10*np.log10(e+1e-10)).round(1).tolist()
rm=lambda x: librosa.feature.rms(y=x,hop_length=hop)[0]
res['harm']=per_sec(rm(H)).round(4).tolist(); res['perc']=per_sec(rm(P)).round(4).tolist()
res['mid']=per_sec(rm(m)).round(4).tolist(); res['side']=per_sec(rm(s)).round(4).tolist()
res['width']=(np.array(res['side'])/(np.array(res['mid'])+1e-9)).round(3).tolist()
# onset strength / tempo
oenv=librosa.onset.onset_strength(y=P,sr=sr,hop_length=hop)
for a,b in [(0,15),(15,66),(66,75),(75,88),(88,118),(118,134),(134,159),(159,189)]:
    seg=oenv[int(a*fps):int(b*fps)]
    t=librosa.feature.tempo(onset_envelope=seg,sr=sr,hop_length=hop,aggregate=None)
    tg=librosa.feature.tempogram(onset_envelope=seg,sr=sr,hop_length=hop)
    ac=tg.mean(1); lags=librosa.tempo_frequencies(tg.shape[0],sr=sr,hop_length=hop)
    idx=np.argsort(ac[1:])[::-1][:3]+1
    res.setdefault('tempo_by_section',{})[f'{a}-{b}']=[round(float(lags[i]),1) for i in idx]
# global tempo candidates
tg=librosa.feature.tempogram(onset_envelope=oenv,sr=sr,hop_length=hop); ac=tg.mean(1); lags=librosa.tempo_frequencies(tg.shape[0],sr=sr,hop_length=hop)
idx=np.argsort(ac[1:])[::-1][:6]+1; res['global_tempo_peaks']=[(round(float(lags[i]),1),round(float(ac[i]),3)) for i in idx]
# silence/gaps
r=np.array(res['mid']); res['quiet_secs']=[i for i,v in enumerate(r) if v<0.08]
json.dump(res,open(out+'music_extra.json','w'))
print(dur, res['global_tempo_peaks']); print(res['tempo_by_section'])
# section table
secs=[(0,15),(15,66),(66,75),(75,88),(88,109),(109,119),(119,134),(134,159),(159,189)]
for a,b in secs:
    sl=slice(a,b); print(a,b,{k:round(float(np.mean(res[k][sl])),2) for k in list(bands)+['width']}, 'perc/harm',round(np.mean(res['perc'][sl])/np.mean(res['harm'][sl]),2),'rms',round(np.mean(res['mid'][sl]),3))
print('per-5s rms',[round(float(np.mean(res['mid'][i:i+5])),2) for i in range(0,188,5)])
print('quiet',res['quiet_secs'])
