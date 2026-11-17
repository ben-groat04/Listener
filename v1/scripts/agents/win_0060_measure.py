import numpy as np, librosa, json, sys
D='/home/user/Listener/v1/data/t_birdwalk/'
def rms(y,sr,t0,t1,h=0.5):
    out=[]
    for a in np.arange(t0,t1,h):
        s=y[int(a*sr):int((a+h)*sr)]
        out.append(20*np.log10(np.sqrt(np.mean(s**2))+1e-9))
    return out
sr=22050
st={}
for n in ['vocals','drums','bass','other']:
    st[n],_=librosa.load(D+f'stems_raw/htdemucs/song/{n}.wav',sr=sr,mono=True)
mix,_=librosa.load(D+'audio/song.wav',sr=sr,mono=True)
print('mix sample peak (22k mono) dBFS',20*np.log10(np.abs(mix).max()))
import soundfile as sf
y,s0=sf.read(D+'audio/song.wav'); print('native sr',s0,'peak full',20*np.log10(np.abs(y).max()),'peak 60-80',20*np.log10(np.abs(y[60*s0:80*s0]).max()))
# boundaries
for T in [58.5,59.0,70.4,70.8,71.0,83.0]:
    print('T',T,{n:(round(np.mean(rms(st[n],sr,T-2,T,1)),1),round(np.mean(rms(st[n],sr,T,T+2,1)),1)) for n in st},'mix',round(np.mean(rms(mix,sr,T-2,T,1)),1),round(np.mean(rms(mix,sr,T,T+2,1)),1))
# kicks: drum stem low band onsets
d=st['drums']
lo=librosa.effects.preemphasis(d)  # unused
S=np.abs(librosa.stft(d,n_fft=2048,hop_length=256))
f=librosa.fft_frequencies(sr=sr,n_fft=2048)
for name,(a,b) in {'low':(30,120),'snare/mid':(150,400),'hat':(5000,10000)}.items():
    e=S[(f>=a)&(f<b)].sum(0)
    on=librosa.onset.onset_detect(onset_envelope=np.diff(e,prepend=0).clip(0),sr=sr,hop_length=256,units='time',backtrack=False,delta=np.percentile(e,70)*0.1)
    on=on[(on>=58)&(on<=82)]
    print(name,len(on),np.round(on,2).tolist())
    if name=='low':
        ioi=np.diff(on); print('kick IOI',np.round(ioi,2).tolist())
# bass onsets
b=st['bass'];e=librosa.onset.onset_strength(y=b,sr=sr,hop_length=256)
on=librosa.onset.onset_detect(onset_envelope=e,sr=sr,hop_length=256,units='time'); on=on[(on>=58)&(on<=82)]
print('bass on',np.round(on,2).tolist())
# bass pitch
f0=librosa.yin(b[58*sr:82*sr],fmin=30,fmax=200,sr=sr,frame_length=4096,hop_length=512)
t=np.arange(len(f0))*512/sr+58
for a in range(58,82,2):
    m=(t>=a)&(t<a+2); r=rms(b,sr,a,a+2,2)[0]
    print(a,'bass f0 median',round(float(np.median(f0[m])),1),'dB',round(r,1))
# spectral centroid mix / bands
for a in [50,56,60,66,70,74,78,82,86]:
    s=mix[a*sr:(a+4)*sr]; c=librosa.feature.spectral_centroid(y=s,sr=sr).mean()
    S2=np.abs(librosa.stft(s))**2; ff=librosa.fft_frequencies(sr=sr)
    print(a,'centroid',round(c),'sub<120 share',round(S2[ff<120].sum()/S2.sum(),3),'>8k',round(S2[ff>8000].sum()/S2.sum(),4))
# vocal pitch regions
f0v,vf,_=librosa.pyin(st['vocals'][55*sr:85*sr],fmin=70,fmax=500,sr=sr,frame_length=2048)
tv=np.arange(len(f0v))*512/sr+55
for a in range(55,85,3):
    m=(tv>=a)&(tv<a+3)&vf
    print(a,'vocal f0 median',round(float(np.nanmedian(f0v[m])),1) if m.sum() else None, 'voiced',int(m.sum()))
# loop regularity: correlation of bar-length (4 beats @152 => 1.58s) mix segments
beat=60/152.0
for a,bb in [(60,61.58)]: pass
bar=4*0.3947
def seg(n,t,L=bar): return st[n][int(t*sr):int((t+L)*sr)]
for n in ['drums','bass','other']:
    cs=[]
    for t in np.arange(60,76,bar):
        x=librosa.feature.melspectrogram(y=seg(n,t),sr=sr,n_mels=40); y2=librosa.feature.melspectrogram(y=seg(n,t+bar),sr=sr,n_mels=40)
        m=min(x.shape[1],y2.shape[1]); cs.append(np.corrcoef(np.log(x[:,:m]+1e-6).ravel(),np.log(y2[:,:m]+1e-6).ravel())[0,1])
    print(n,'bar-to-bar logmel corr',np.round(cs,2).tolist())
