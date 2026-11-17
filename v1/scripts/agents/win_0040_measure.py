import librosa, numpy as np, soundfile as sf
D='/home/user/Listener/v1/data/t_birdwalk/'
S,T=40,60
def ld(p):
    y,sr=sf.read(p,always_2d=True); return y,sr
mix,sr=ld(D+'audio/song.wav')
print('sr',sr,'dur',len(mix)/sr)
seg=mix[int(S*sr):int(T*sr)]
print('peak dBFS win',20*np.log10(abs(seg).max()), 'whole',20*np.log10(abs(mix).max()))
m=seg.mean(1);
for a,b in[(40,47),(47,59),(59,60)]:
    x=mix[int(a*sr):int(b*sr)].mean(1)
    sc=librosa.feature.spectral_centroid(y=x,sr=sr).mean()
    print(a,b,'rms dB',20*np.log10(np.sqrt((x**2).mean())),'centroid',sc, 'hf>5k share',(np.abs(np.fft.rfft(x))**2)[np.fft.rfftfreq(len(x),1/sr)>5000].sum()/(np.abs(np.fft.rfft(x))**2).sum())
st={}
for n in['drums','bass','vocals','other']:
    y,_=ld(D+f'stems_raw/htdemucs/song/{n}.wav'); st[n]=y.mean(1)
# kick onsets from drums, low band
from scipy.signal import butter,sosfilt
d=st['drums'];
sos=butter(4,150,'low',fs=sr,output='sos'); lo=sosfilt(sos,d)
env=librosa.onset.onset_strength(y=d,sr=sr,hop_length=256)
on=librosa.onset.onset_detect(onset_envelope=env,sr=sr,hop_length=256,units='time',backtrack=False)
on=on[(on>=S)&(on<T)]
print('drum onsets',np.round(on,2))
print('IOI',np.round(np.diff(on),2))
# bass onsets
for n in['bass']:
    e=librosa.onset.onset_strength(y=st[n],sr=sr,hop_length=256)
    o=librosa.onset.onset_detect(onset_envelope=e,sr=sr,hop_length=256,units='time'); o=o[(o>=S)&(o<T)]
    print('bass onsets',np.round(o,2))
# 10ms env per stem rms in 0.5s steps
hop=int(.01*sr)
for n,x in list(st.items())+[('mix',mix.mean(1))]:
    r=np.array([np.sqrt((x[i:i+hop]**2).mean()) for i in range(int(44*sr)//hop*hop,int(62*sr),hop)])
for n,x in list(st.items())+[('mix',mix.mean(1))]:
    out=[]
    for a in np.arange(44,62,1.0):
        seg=x[int(a*sr):int((a+1)*sr)]; out.append(round(20*np.log10(np.sqrt((seg**2).mean())+1e-9),1))
    print(n,out)
