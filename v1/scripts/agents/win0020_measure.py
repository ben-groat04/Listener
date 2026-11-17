import librosa,numpy as np,json,sys
D='/home/user/Listener/v1/data/t_dl_mirror/'
S=D+'stems_raw/htdemucs/song/'
t0,t1=20,40
def load(p): 
    y,sr=librosa.load(p,sr=22050,mono=False); return y,sr
mix,sr=librosa.load(D+'audio/song.wav',sr=None,mono=False)
print('sr',sr,'shape',mix.shape)
seg=mix[...,int(t0*sr):int(t1*sr)]
print('sample peak dBFS (20-40)',20*np.log10(np.abs(seg).max()),'whole',20*np.log10(np.abs(mix).max()))
if mix.ndim>1:
    L,R=seg[0],seg[1]; print('L-R rms ratio',np.sqrt(np.mean((L-R)**2))/np.sqrt(np.mean((L+R)**2)+1e-12))
m=seg.mean(0) if seg.ndim>1 else seg
# band energy
Sx=np.abs(librosa.stft(m,n_fft=4096))**2; f=librosa.fft_frequencies(sr=sr,n_fft=4096)
tot=Sx.sum()
for lo,hi in [(0,200),(200,2000),(2000,8000),(8000,12000),(12000,16000),(16000,22050)]:
    print('band',lo,hi,'%.4f'%(Sx[(f>=lo)&(f<hi)].sum()/tot))
# rolloff
print('rolloff95 median',np.median(librosa.feature.spectral_rolloff(S=np.sqrt(Sx),sr=sr,roll_percent=0.95)))
# stems
st={}
for n in ['drums','bass','vocals','other']:
    y,s=librosa.load(S+n+'.wav',sr=22050,mono=True); st[n]=y
hop=220
for n,y in list(st.items()):
    e=librosa.feature.rms(y=y,frame_length=441,hop_length=hop)[0]
    e1=librosa.feature.rms(y=y,frame_length=22050,hop_length=22050//2)[0]
    st[n+'_e']=e
# kick: drums low band onsets
y=st['drums']; 
lo=librosa.effects.preemphasis(y)  # dummy
import scipy.signal as sg
b,a=sg.butter(4,[40/11025,120/11025],'band'); k=sg.filtfilt(b,a,y)
on=librosa.onset.onset_detect(y=k,sr=22050,hop_length=hop,units='time',backtrack=False)
on=on[(on>=t0)&(on<t1)]
print('kick onsets',len(on),np.round(on,2).tolist())
ioi=np.diff(on);print('kick IOI median',np.median(ioi),'bpm-ish',60/np.median(ioi))
bt=np.array(json.load(open(D+'audio_features/beat_times.json')));bt=bt[(bt>=t0)&(bt<t1)]
print('beat period median',np.median(np.diff(bt)),'bpm',60/np.median(np.diff(bt)))
d=[np.min(np.abs(bt-o)) for o in on];print('kick->nearest tracker beat: mean %.3f max %.3f s'%(np.mean(d),np.max(d)))
# on 16th grid
p=np.median(np.diff(bt));g=[(o-bt[0])/(p/4) for o in on];print('kick pos in 16th grid frac dev mean',np.mean(np.abs(np.array(g)-np.round(g)))*p/4)
# snare onsets band 150-400 & 2-5k? full drums onsets
on2=librosa.onset.onset_detect(y=y,sr=22050,hop_length=hop,units='time');on2=on2[(on2>=t0)&(on2<t1)];print('drum onsets all',len(on2))
# per-stem 0.5 s level in dB
for n in ['drums','bass','vocals','other']:
    y=st[n];seg=[]
    for t in np.arange(t0-2,t1+2,0.5):
        x=y[int(t*22050):int((t+0.5)*22050)];seg.append(20*np.log10(np.sqrt(np.mean(x**2))+1e-9))
    print(n,' '.join('%d'%round(v) for v in seg))
# loop regularity: bar chroma/mel self-similarity of drum stem per 4 beats
bar=np.median(np.diff(bt))*4
print('bar',bar)
def bars(y,start,n):
    out=[]
    for i in range(n):
        x=y[int((start+i*bar)*22050):int((start+(i+1)*bar)*22050)];out.append(x)
    return out
dr=bars(st['drums'],bt[0],int((t1-bt[0])//bar))
L=min(len(x) for x in dr);
M=[np.log1p(librosa.feature.melspectrogram(y=x[:L],sr=22050,n_mels=32).mean(1)) for x in dr]
M=np.array(M);c=np.corrcoef(M);print('drum bar mel-corr min/mean',c.min().round(3),c[np.triu_indices(len(M),1)].mean().round(3))
# bar waveform envelope corr
E=[]
for x in dr:
    e=librosa.feature.rms(y=x[:L],frame_length=512,hop_length=256)[0];E.append(e)
E=np.array(E);c2=np.corrcoef(E);print('drum bar envelope corr mean',c2[np.triu_indices(len(E),1)].mean().round(3), np.round(c2[0],2))
# spectral cutoff
Sd=10*np.log10(Sx.mean(1)+1e-20)
for fr in [6000,8000,9000,10000,12000,16000]:
    i=np.argmin(abs(f-fr));print('PSD dB at',fr,Sd[i].round(1))
y,_=librosa.load(D+'audio/song.wav',sr=None,mono=True)
pk=np.abs(y).reshape(-1)[:len(y)//44100*44100].reshape(-1,44100).max(1);print('frac seconds with peak>-1dBFS whole',np.mean(pk>0.89).round(2))
