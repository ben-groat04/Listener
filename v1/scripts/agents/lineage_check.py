import librosa,numpy as np
b='data/video1/stems_raw/htdemucs/song/'
n=['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
for stem,(t0,t1) in [('other',(0,188)),('other',(100,120)),('other',(150,188)),('bass',(0,188))]:
    y,sr=librosa.load(b+stem+'.wav',sr=22050,offset=t0,duration=t1-t0)
    c=librosa.feature.chroma_cqt(y=y,sr=sr).mean(1);c/=c.max()
    print(stem,t0,t1,' '.join(f'{n[i]}:{c[i]:.2f}' for i in np.argsort(-c)[:7]))
y,sr=librosa.load(b+'drums.wav',sr=22050,offset=60,duration=60)
oe=librosa.onset.onset_strength(y=y,sr=sr)
t=librosa.feature.tempo(onset_envelope=oe,sr=sr,aggregate=None)
print('drum tempo median',np.median(t))
ac=librosa.autocorrelate(oe-oe.mean());ac/=ac[0];fps=sr/512
for lag in range(5,200):
    if ac[lag]>ac[lag-1] and ac[lag]>ac[lag+1] and ac[lag]>0.15: print('lag s',round(lag/fps,3),'bpm',round(60/(lag/fps),1),round(ac[lag],2))
