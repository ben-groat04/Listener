import numpy as np, librosa, json, soundfile as sf, scipy.signal as ss
D='/home/user/Listener/v1/data/t_dl_mirror/'
T0,T1=160,180
i=sf.info(D+'audio/song.wav');print(i.samplerate,i.subtype,i.channels)
y,sr0=sf.read(D+'audio/song.wav');print('native sample peak dBFS',20*np.log10(np.abs(y).max()),' window',20*np.log10(np.abs(y[T0*sr0:T1*sr0]).max()))
print('L==R max diff',np.abs(y[:,0]-y[:,1]).max())
m=y.mean(1)[T0*sr0:T1*sr0]
print('window rms dBFS',20*np.log10(np.sqrt((m**2).mean())),'crest',20*np.log10(np.abs(m).max()/np.sqrt((m**2).mean())))
# fraction of samples > 0.99
print('samples >=0.98 in window',(np.abs(m)>=0.98).sum(), 'of',m.size)
# stems native
sr=22050
dr,_=sf.read(D+'stems_raw/htdemucs/song/drums.wav');dr=dr.mean(1)
from scipy.signal import resample_poly
fs=_;print('stem sr',fs)
bt=np.array(json.load(open(D+'audio_features/beat_times.json')));bb=bt[(bt>=T0-1)&(bt<=T1+1)];ibi=np.diff(bb);print('tracker ibi range',ibi.min(),ibi.max(),'bpm',60/np.median(ibi))
x=dr[int(T0*fs):int(T1*fs)]
def onsets(lo,hi,delta):
    sos=ss.butter(4,[lo/(fs/2),hi/(fs/2)],'band',output='sos');k=ss.sosfiltfilt(sos,x)
    env=librosa.onset.onset_strength(y=k,sr=fs,hop_length=64,aggregate=np.median)
    return librosa.onset.onset_detect(onset_envelope=env,sr=fs,hop_length=64,units='time',delta=delta,wait=6)+T0
def devstats(on,name):
    # nearest 16th on tracker grid
    grid=[]
    for a,b_ in zip(bb[:-1],bb[1:]): grid+= [a+(b_-a)*j/4 for j in range(4)]
    grid=np.array(grid);d=np.array([o-grid[np.argmin(abs(grid-o))] for o in on])*1000
    ib=np.diff(on)
    print(name,'n',len(on),'dev ms mean',d.mean().round(1),'sd',d.std().round(1),'abs med',np.median(abs(d)).round(1),'| IOI median',np.median(ib).round(3))
    return d
k=onsets(35,120,0.08);devstats(k,'kick')
print(np.round(k,2).tolist())
sn=onsets(150,350,0.08);devstats(sn,'snare-low')
sn2=onsets(1500,5000,0.1);devstats(sn2,'mid-hf')
hh=onsets(7000,16000,0.1);devstats(hh,'hat')
# kick position within bar (beat index relative to tracker beat 0 of window)
pos=[]
for o in k:
    j=np.argmin(abs(bb-o)); pos.append(round(((o-bb[j])/ (bb[min(j+1,len(bb)-1)]-bb[j]))%1,2)) 
print('kick offset in beat (fraction)',np.round(pos,2).tolist())
# bass stem pitch
bs,_=sf.read(D+'stems_raw/htdemucs/song/bass.wav');bs=bs.mean(1)
bx=bs[int(T0*fs):int(T1*fs)]
f0,vf,vp=librosa.pyin(bx[::2][:],fmin=30,fmax=200,sr=fs//2,frame_length=4096,hop_length=1024)
t=librosa.times_like(f0,sr=fs//2,hop_length=1024)+T0
cur=None
for tt,f in zip(t,f0):
    if not np.isnan(f): print(round(tt,1),librosa.hz_to_note(f),round(f,1),end=' | ')
print()
env=20*np.log10(np.sqrt(np.convolve(bx**2,np.ones(int(fs*0.02))/int(fs*0.02),'same'))+1e-9)
on=env>-40
ch=np.flatnonzero(np.diff(on.astype(int)))/fs+T0
# merge gaps <0.1
segs=[];s=None
for c_ in ch:
    pass
st=np.flatnonzero(np.diff(on.astype(int))==1)/fs+T0;en=np.flatnonzero(np.diff(on.astype(int))==-1)/fs+T0
ms=[]
for a in st:
    if ms and a-ms[-1][1]<0.15: continue
    b_=en[en>a]; b_=b_[0] if len(b_) else T1
    # extend
    ms.append([a,b_])
print('bass events',[(round(a,2),round(b,2)) for a,b in ms])
