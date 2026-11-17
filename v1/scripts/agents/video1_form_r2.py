import librosa,numpy as np
D='data/video1/stems_raw/htdemucs/song/'
b,sr=librosa.load(D+'bass.wav',sr=22050,mono=True)
o,_=librosa.load(D+'other.wav',sr=22050,mono=True)
m,_=librosa.load('data/video1/audio/song.wav',sr=22050,mono=True)
h=256
def rms(x): return librosa.amplitude_to_db(librosa.feature.rms(y=x,frame_length=1024,hop_length=h)[0]+1e-9)
rb,ro,rm=rms(b),rms(o),rms(m); T=librosa.frames_to_time(np.arange(len(rb)),sr=sr,hop_length=h)
def jump(r,lo,hi,name):
    s=(T>=lo)&(T<=hi); d=np.diff(r[s],n=1); i=np.argmax(np.abs(r[s][8:]-r[s][:-8])) 
    seg=T[s]; k=np.argmax(np.abs(np.convolve(np.diff(r[s]),np.ones(8),'same')))
    print(name,lo,hi,'max-step at',round(seg[k],2))
for n,r,l,h2 in [('bass',rb,99,101.5),('bass',rb,154,157),('bass',rb,157,160),('bass',rb,75,77.5),('bass',rb,157,160),('bass',rb,157,160),('other',ro,86,89),('other',ro,132,135),('bass',rb,157,160),('bass',rb,156.5,158),('bass',rb,157,160)]:
    pass
for n,r,l,h2 in [('bass',rb,98.5,101.5),('bass',rb,74.5,77.5),('other',ro,86.5,89),('other',ro,132.5,135.5),('bass',rb,156.5,159),('other',ro,116,120),('bass',rb,114,117)]:
    jump(r,l,h2,n)
i=np.argmin(rm[(T>166)&(T<170)]);print('dip min',T[(T>166)&(T<170)][i])
d=rm[(T>166.5)&(T<169)];t=T[(T>166.5)&(T<169)];print('dip <-20 dB rel:',t[d<d.max()-8][[0,-1]])
