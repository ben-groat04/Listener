import numpy as np, librosa, json
D='/home/user/Listener/v1/data/t_cshells_cshore/'
S=D+'stems_raw/htdemucs/song/'
sr=22050
def ld(p,a=210,b=250):
    y,_=librosa.load(p,sr=sr,offset=a,duration=b-a); return y
mix=ld(D+'audio/song.wav'); 
st={k:ld(S+k+'.wav') for k in ['vocals','drums','bass','other']}
off=210
def env(y,hop=0.1):
    h=int(sr*hop); n=len(y)//h
    return 20*np.log10(np.sqrt((y[:n*h].reshape(n,h)**2).mean(1))+1e-9)
print('peak mix dBFS (210-250)',20*np.log10(np.abs(mix).max()))
w=mix[int(10*sr):int(30*sr)]; print('peak 220-240',20*np.log10(np.abs(w).max()))
for k,y in {'mix':mix,**st}.items():
    e=env(y,0.5); print(k,' '.join(f'{off+i*0.5:.1f}:{v:.0f}' for i,v in enumerate(e) if 218<=off+i*0.5<=230))
# bass drop
e=env(st['bass'],0.1)
for i,v in enumerate(e):
    if 221<=off+i*.1<=226: print('bass',round(off+i*.1,1),round(v,1),end=' | ')
print()
em=env(mix,0.1)
for i,v in enumerate(em):
    if 222<=off+i*.1<=225.5: print('mix',round(off+i*.1,1),round(v,1),end=' | ')
print()
# drum onsets
d=st['drums']; 
oe=librosa.onset.onset_strength(y=d,sr=sr,hop_length=256)
on=librosa.onset.onset_detect(onset_envelope=oe,sr=sr,hop_length=256,units='time',backtrack=False)+off
on=on[(on>=220)&(on<240)]
print('n drum onsets 220-240',len(on)); 
# kick: low-band
import scipy.signal as sg
b,a=sg.butter(4,150/(sr/2),'low'); k=sg.filtfilt(b,a,d)
ko=librosa.onset.onset_detect(y=k,sr=sr,hop_length=256,units='time')+off
ko=ko[(ko>=220)&(ko<240)]
print('kick onsets',np.round(ko,2)); ioi=np.diff(ko); print('IOI',np.round(ioi,2),'median',np.median(ioi))
bt=np.array(json.load(open(D+'audio_features/beat_times.json')));print('beats last',bt[-3:],len(bt))
tp=librosa.feature.rhythm.tempo(onset_envelope=oe,sr=sr,hop_length=256)[0];print('tempo drums',tp)
# spectral centroid / band share
for a0,a1 in [(220,224),(224,240)]:
    seg=mix[int((a0-off)*sr):int((a1-off)*sr)]
    c=librosa.feature.spectral_centroid(y=seg,sr=sr).mean(); 
    S_=np.abs(librosa.stft(seg))**2; f=librosa.fft_frequencies(sr=sr)
    print(a0,a1,'centroid',c,'>8k share',S_[f>8000].sum()/S_.sum(),'<200 share',S_[f<200].sum()/S_.sum(), 'rolloff95',librosa.feature.spectral_rolloff(y=seg,sr=sr,roll_percent=.95).mean())
# other: pitch of sustained tone via chroma peaks / piptrack 224-232
o=st['other'][int((225-off)*sr):int((232-off)*sr)]
f0,vf,vp=librosa.pyin(o,fmin=150,fmax=1500,sr=sr)
fv=f0[~np.isnan(f0)]; print('other f0 median',np.median(fv) if len(fv) else None, np.percentile(fv,[10,90]) if len(fv) else None)
# vocals stem 224-230 
v=st['vocals'][int((223.5-off)*sr):int((231-off)*sr)]
f0,vf,vp=librosa.pyin(v,fmin=150,fmax=1500,sr=sr);fv=f0[~np.isnan(f0)];print('vocal f0',np.median(fv) if len(fv) else None,len(fv))
