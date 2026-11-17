import numpy as np, librosa, soundfile as sf, json
D='/home/user/Listener/v1/data/t_birdwalk/'
S=D+'stems_raw/htdemucs/song/'
mix,sr=sf.read(D+'audio/song.wav'); 
if mix.ndim>1: mixm=mix.mean(1)
else: mixm=mix
print('sr',sr,'dur',len(mixm)/sr,'peak',np.abs(mix).max(), 'n>=0.999',(np.abs(mix)>=0.999).sum())
st={k:sf.read(S+k+'.wav')[0] for k in['drums','bass','vocals','other']}
st={k:(v.mean(1) if v.ndim>1 else v) for k,v in st.items()}
# end envelope
def env(x,hop=0.01):
    n=int(hop*sr); m=len(x)//n; return 20*np.log10(np.sqrt((x[:m*n].reshape(m,n)**2).mean(1))+1e-9)
for k,v in [('mix',mixm)]+list(st.items()):
    e=env(v); t=np.arange(len(e))*0.01
    last=e[-300:]; 
    print('END',k,'last3s min/max',last.min().round(1),last.max().round(1),'env at -0.5s',e[-50:].mean().round(1))
em=env(mixm); t=np.arange(len(em))*.01
for thr in(-60,-70,-80): 
    idx=np.where(em>thr)[0]; print('last >',thr,'dB at',t[idx[-1]].round(2))
print('last 3s mix env 0.25s steps',[round(em[i:i+25].mean(),1) for i in range(len(em)-300,len(em),25)])
# peaks in last 3 s of envelope
from scipy.signal import find_peaks
p,_=find_peaks(em[-300:],prominence=3); print('env peaks last3s',(t[-300:][p]).round(2),em[-300:][p].round(1))
# drums onsets
d=st['drums']
oenv=librosa.onset.onset_strength(y=d,sr=sr,hop_length=256)
on=librosa.onset.onset_detect(onset_envelope=oenv,sr=sr,hop_length=256,units='time',backtrack=False)
np.save('/tmp/claude-0/drum_on.npy',on)
print('n drum onsets',len(on))
# per-section IOI medians
secs=[0,12.1,24,47,59.4,70.4,83,93.8,120,131.4,143,156.4,170.3,176.5,188.2]
beat=60/152
for a,b in zip(secs[:-1],secs[1:]):
    o=on[(on>=a)&(on<b)]; i=np.diff(o)
    if len(i)>2:
        print(f'{a:6.1f}-{b:6.1f} n={len(o)} medIOI={np.median(i):.3f} IOI/beat={np.median(i)/beat:.2f}  hits/s={len(o)/(b-a):.2f}')
# kick band onsets
from scipy.signal import butter,sosfilt
sos=butter(4,150,'low',fs=sr,output='sos')
kb=sosfilt(sos,d); ke=librosa.onset.onset_strength(y=kb,sr=sr,hop_length=256)
kon=librosa.onset.onset_detect(onset_envelope=ke,sr=sr,hop_length=256,units='time')
print('kick-band onsets',len(kon))
# bass onsets
bs=st['bass']; be=librosa.onset.onset_strength(y=bs,sr=sr,hop_length=256)
bon=librosa.onset.onset_detect(onset_envelope=be,sr=sr,hop_length=256,units='time')
np.save('/tmp/claude-0/bass_on.npy',bon); np.save('/tmp/claude-0/kick_on.npy',kon)
bt=np.array(json.load(open(D+'audio_features/beat_times.json')) if True else [])
print('beats',bt[:5] if bt.ndim==1 else bt[:3])
