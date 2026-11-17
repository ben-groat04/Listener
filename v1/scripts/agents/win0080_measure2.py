import numpy as np,soundfile as sf,librosa,json,scipy.signal as ss
D='/home/user/Listener/v1/data/t_dl_mirror/';S=D+'stems_raw/htdemucs/song/'
def ld(f,t0,t1):
    x,sr=sf.read(f,start=int(t0*44100),stop=int(t1*44100)); return x,sr
x,sr=ld(D+'audio/song.wav',80,100);print('sr',sr,x.shape)
print('sample peak dBFS 80-100:',20*np.log10(np.abs(x).max()))
if x.ndim>1:
    print('L-R rms diff dB', 20*np.log10(np.sqrt(np.mean((x[:,0]-x[:,1])**2))+1e-12), 'mid rms',20*np.log10(np.sqrt(np.mean(((x[:,0]+x[:,1])/2)**2))))
    m=x.mean(1)
else: m=x
f,P=ss.welch(m,sr,nperseg=8192);P=10*np.log10(P+1e-20)
for lo,hi in [(20,150),(150,500),(500,2000),(2000,5000),(5000,10000),(10000,16000),(16000,20000)]:
    print('band',lo,hi,round(P[(f>=lo)&(f<hi)].mean(),1))
# 0.5s stem dB across window
def db(s):return 20*np.log10(np.sqrt(np.mean(s**2))+1e-9)
st={}
for n in ['vocals','drums','bass','other']:
    a,_=ld(S+n+'.wav',78,102);st[n]=a.mean(1) if a.ndim>1 else a
a,_=ld(D+'audio/song.wav',78,102);st['mix']=a.mean(1) if a.ndim>1 else a
print('t   mix voc drum bass other (0.5s dB)')
for i in range(48):
    s=slice(int(i*.5*sr),int((i+1)*.5*sr));print(round(78+i*.5,1),*[round(db(st[n][s]),1) for n in ['mix','vocals','drums','bass','other']])
# loop regularity: beat-synchronous chroma of other, correlation between bars (4 beats)
bt=np.array(json.load(open(D+'audio_features/beat_times.json')));bt=bt if bt.ndim==1 else bt
y,s2=librosa.load(S+'other.wav',sr=22050,offset=60,duration=60)
ch=librosa.feature.chroma_cqt(y=y,sr=s2,hop_length=512)
fr=librosa.time_to_frames(bt[(bt>=60)&(bt<120)]-60,sr=s2,hop_length=512)
cs=librosa.util.sync(ch,fr[fr<ch.shape[1]]).T
bars=[cs[i:i+4].flatten() for i in range(0,len(cs)-4,4)]
C=np.corrcoef(bars);print('bar-to-bar chroma corr (other, 60-120s), neighbours:',np.round(np.diag(C,1),2),'two-bar:',np.round(np.diag(C,2),2))
