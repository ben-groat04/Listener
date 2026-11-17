import librosa,numpy as np,json,sys
d='/home/user/Listener/v1/data/t_birdwalk/'
S=sys.argv[1] if len(sys.argv)>1 else ''
def ld(p,a,b):
    y,sr=librosa.load(p,sr=None,mono=False,offset=a,duration=b-a);return y,sr
y,sr=ld(d+'audio/song.wav',0,60)
m=y.mean(0) if y.ndim>1 else y
print('sr',sr,'ch',y.ndim,'peak 20-40 dBFS',20*np.log10(np.abs(y[...,20*sr:40*sr]).max()),'peak 0-60',20*np.log10(np.abs(y).max()))
st={}
for s in ['drums','bass','vocals','other']:
    st[s],_=ld(d+f'stems_raw/htdemucs/song/{s}.wav',0,60)
    st[s]=st[s].mean(0)
def env(x,hop=sr//100):
    return np.sqrt(np.convolve(x**2,np.ones(hop)/hop,'same'))[::hop]
# 1s levels per stem 17-44
for t in range(17,44):
    r=lambda x:20*np.log10(np.sqrt((x[t*sr:(t+1)*sr]**2).mean())+1e-9)
    print(t,'mix %.1f'%r(m),' '.join('%s %.1f'%(s[:2],r(st[s])) for s in st))
# drum onsets
dr=st['drums']
oe=librosa.onset.onset_strength(y=dr,sr=sr,hop_length=256)
on=librosa.onset.onset_detect(onset_envelope=oe,sr=sr,hop_length=256,units='time',backtrack=False)
on=on[(on>=19)&(on<=41)]
print('drum onsets',np.round(on,2).tolist());print('IOI',np.round(np.diff(on),2).tolist())
# low band of drums for kick
import scipy.signal as ss
b,a=ss.butter(4,150/(sr/2));lo=ss.filtfilt(b,a,dr);oe2=librosa.onset.onset_strength(y=lo,sr=sr,hop_length=256)
k=librosa.onset.onset_detect(onset_envelope=oe2,sr=sr,hop_length=256,units='time');k=k[(k>=19)&(k<=41)]
print('kick',np.round(k,2).tolist());print('kickIOI',np.round(np.diff(k),3).tolist())
bs=st['bass'];oe3=librosa.onset.onset_strength(y=bs,sr=sr,hop_length=256)
bo=librosa.onset.onset_detect(onset_envelope=oe3,sr=sr,hop_length=256,units='time');bo=bo[(bo>=19)&(bo<=41)]
print('bass on',np.round(bo,2).tolist())
# bass pitch
f0,_,_=librosa.pyin(bs[19*sr:41*sr],fmin=30,fmax=120,sr=sr,frame_length=8192)
print('bass f0 median',np.nanmedian(f0), 'by 2s',[round(float(np.nanmedian(f0[i:i+int(2*sr/512)])),1) if np.isfinite(f0[i:i+int(2*sr/512)]).any() else None for i in range(0,len(f0),int(2*sr/512))])
# band share 20-40 vs 0-12 of mix
for (a,b2) in [(5,12),(21,28),(30,38)]:
    seg=m[a*sr:b2*sr];S=np.abs(librosa.stft(seg))**2;fr=librosa.fft_frequencies(sr=sr)
    tot=S.sum();print(a,b2,{n:round(float(S[(fr>=lo)&(fr<hi)].sum()/tot),3) for n,lo,hi in [('sub',0,60),('bass',60,200),('lm',200,800),('mid',800,3000),('hi',3000,8000),('air',8000,30000)]})
# stereo width
L,R=y[0],y[1] if y.ndim>1 else (m,m)
for a,b2 in [(5,12),(21,28),(30,38)]:
    M=(L+R)/2;Sd=(L-R)/2;print('side/mid',a,b2,np.sqrt((Sd[a*sr:b2*sr]**2).mean())/np.sqrt((M[a*sr:b2*sr]**2).mean()))
# bar repetition: chroma self-similarity lag
tempo,bt=librosa.beat.beat_track(y=m[20*sr:40*sr],sr=sr);print('tempo',tempo)
