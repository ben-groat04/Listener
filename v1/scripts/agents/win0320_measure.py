import numpy as np, librosa, json
D='/home/user/Listener/v1/data/t_cshells_cshore/'
names={'mix':D+'audio/song.wav'}
for s in ['vocals','drums','bass','other']: names[s]=D+f'stems_raw/htdemucs/song/{s}.wav'
sr=22050
def db(x): return 20*np.log10(np.maximum(x,1e-9))
res={}
for n,p in names.items():
    y,_=librosa.load(p,sr=sr,mono=True)
    res[n]=y
    h=int(.01*sr)
    # 1s rms 316..350
    print(n,'peak dBFS whole',round(db(np.abs(y).max()),1))
    print(' 2s rms 316-350:',[round(db(np.sqrt(np.mean(y[int(t*sr):int((t+2)*sr)]**2))),0) for t in range(316,360,2)])
y=res['mix']
h=int(.01*sr)
env=lambda y:np.sqrt(np.convolve(y**2,np.ones(h)/h,'same'))[::h]
e=db(env(y)); t=np.arange(len(e))*.01
for a,b in [(340,343.5),(343.5,350),(350,360)]:
    m=(t>=a)&(t<b); print('mix',a,b,'max env dB',round(e[m].max(),1))
idx=np.where(e>-60)[0]; print('last >-60 dB env at',t[idx[-1]],'; >-70',t[np.where(e>-70)[0][-1]],'; >-80',t[np.where(e>-80)[0][-1]])
print('last 3 s env dB at 1s steps (mix):',[round(e[(t>=a)&(t<a+1)].mean(),1) for a in (357.98,358.98,359.98)], 'final',e[-5:])
for n in ['vocals','drums','bass','other']:
    ee=db(env(res[n])); print(n,'last3s min/max',round(ee[-300:].min(),1),round(ee[-300:].max(),1),'last >-60:',t[np.where(ee>-60)[0][-1]] if (ee>-60).any() else None, ' 342-343.5 max',round(ee[(t>=342)&(t<343.5)].max(),1))
# mix level around cut
for a in range(338,346): print(a,round(db(np.sqrt(np.mean(y[a*sr:(a+1)*sr]**2))),1), end=' | ')
print()
# tempo / onsets in drums 320-336
d=res['drums'];seg=d[320*sr:337*sr]
oe=librosa.onset.onset_strength(y=seg,sr=sr)
tempo=librosa.feature.rhythm.tempo(onset_envelope=oe,sr=sr);print('drum tempo',tempo)
on=librosa.onset.onset_detect(onset_envelope=oe,sr=sr,units='time');print('n onsets',len(on),np.round(on+320,2)[:40])
# bands, hf
from scipy.signal import butter,sosfilt
for a,b in [(320,330),(330,334),(334,336),(337,340),(341,343)]:
    s=y[a*sr:b*sr];S=np.abs(np.fft.rfft(s))**2;f=np.fft.rfftfreq(len(s),1/sr)
    c=(S*f).sum()/S.sum();print('mix',a,b,'centroid',round(c),'energy>5k %',round(100*S[f>5000].sum()/S.sum(),2))
# loop regularity: autocorr of mix chroma 320-335 at bar (123bpm -> 1.95s)
bt=json.load(open(D+'audio_features/beat_times.json'));print(type(bt))
