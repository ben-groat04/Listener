import numpy as np, librosa, json, sys
D='/home/user/Listener/v1/data/t_dl_mirror/'
T0,T1=160,180
def load(p): 
    y,sr=librosa.load(p,sr=22050,mono=False); return y,sr
mix,sr=librosa.load(D+'audio/song.wav',sr=22050,mono=True)
st={k:librosa.load(D+f'stems_raw/htdemucs/song/{k}.wav',sr=22050,mono=True)[0] for k in ['vocals','drums','bass','other']}
sl=slice(T0*sr,T1*sr)
print('mix peak 160-180 dBFS',20*np.log10(np.abs(mix[sl]).max()), 'whole song peak',20*np.log10(np.abs(mix).max()))
# stereo
y2,_=librosa.load(D+'audio/song.wav',sr=22050,mono=False); print('shape',y2.shape)
if y2.ndim==2: 
    s=y2[:,sl]; print('L-R rms dB',20*np.log10(np.sqrt(np.mean((s[0]-s[1])**2))+1e-9),'mid',20*np.log10(np.sqrt(np.mean(((s[0]+s[1])/2)**2))))
# kick: drums low-band onsets
d=st['drums'][sl]
lo=librosa.effects.preemphasis(d,coef=0)
import scipy.signal as ss
b,a=ss.butter(4,[40/(sr/2),130/(sr/2)],'band'); k=ss.filtfilt(b,a,d)
env=librosa.onset.onset_strength(y=k,sr=sr,hop_length=128)
on=librosa.onset.onset_detect(onset_envelope=env,sr=sr,hop_length=128,units='time',backtrack=False,delta=0.15)
print('kick onsets',len(on)); print(np.round(on+T0,2).tolist())
ioi=np.diff(on); print('IOI median',np.median(ioi),'quantised hist',np.round(ioi,2).tolist())
# tempo
bt=json.load(open(D+'audio_features/beat_times.json'));bt=np.array(bt if isinstance(bt,list) else bt.get('beats',bt))
b=bt[(bt>=T0)&(bt<T1)];print('beats',len(b),'median ibi',np.median(np.diff(b)),'bpm',60/np.median(np.diff(b)))
# grid deviation of kicks relative to fixed grid 
beat=np.median(np.diff(b))
# fit grid phase to kicks at 16th level
for div,name in [(1,'beat'),(2,'8th'),(4,'16th')]:
    g=beat/div; ph=((on)%g); 
    ang=2*np.pi*ph/g; R=np.abs(np.mean(np.exp(1j*ang))); mu=np.angle(np.mean(np.exp(1j*ang)))/(2*np.pi)*g
    dev=((ph-mu+g/2)%g)-g/2
    print(name,'grid',round(g,3),'R',round(R,2),'dev ms sd',round(dev.std()*1000,1),'max',round(np.abs(dev).max()*1000,1))
# per-stem 1s RMS dB and 1s bass presence
for k in st:
    x=st[k][sl]; r=[20*np.log10(np.sqrt(np.mean(x[i*sr:(i+1)*sr]**2))+1e-9) for i in range(20)]
    print(k,np.round(r,0).tolist())
# bass event times: 10ms env
bx=st['bass'][sl]; e=np.sqrt(np.convolve(bx**2,np.ones(220)/220,'same')); eD=20*np.log10(e+1e-9)
on_b=eD>-45
ch=np.flatnonzero(np.diff(on_b.astype(int)))
print('bass on/off (s):',np.round((ch/sr)+T0,2).tolist())
# bass fundamental during events
# spectral centroid mix, brightness
S=np.abs(librosa.stft(mix[sl],n_fft=2048))
f=librosa.fft_frequencies(sr=sr,n_fft=2048)
tot=S.sum()
for lo_,hi in [(0,200),(200,2000),(2000,8000),(8000,11025)]:
    print('band',lo_,hi,round(S[(f>=lo_)&(f<hi)].sum()/tot*100,1),'% energy-amp share')
print('centroid',librosa.feature.spectral_centroid(S=S,sr=sr).mean())
# loop regularity: bar-level correlation of drum stem, bar = 4 beats
bar=beat*4; n=int(bar*sr)
x=st['drums'][sl]; 
st0=int((b[0]-T0)*sr)
bars=[x[st0+i*n:st0+(i+1)*n] for i in range((len(x)-st0)//n)]
cs=[]
for i in range(len(bars)-1):
    a_,b_=bars[i],bars[i+1]; a_=np.abs(a_);b_=np.abs(b_)
    ea=np.convolve(a_,np.ones(441)/441,'same')[::100];eb=np.convolve(b_,np.ones(441)/441,'same')[::100]
    cs.append(np.corrcoef(ea,eb)[0,1])
print('drum env corr adjacent bars',np.round(cs,2).tolist())
# mix-wide
j=0
