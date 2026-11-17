import librosa,numpy as np,soundfile as sf
R='stems_raw/htdemucs/song/'
def load(n,a=95,d=30):
    y,sr=librosa.load(n,sr=22050,offset=a,duration=d,mono=True);return y,sr
mix,sr=load('audio/song.wav'); 
y,s=sf.read('audio/song.wav'); seg=y[int(100*s):int(120*s)]
print('samplepeak dBFS 100-120',20*np.log10(np.abs(seg).max()), 'whole', 20*np.log10(np.abs(y).max()), 'rms', 20*np.log10(np.sqrt((seg**2).mean())))
if seg.ndim>1: print('L/R corr',np.corrcoef(seg[:,0],seg[:,1])[0,1], 'S/M', np.sqrt(((seg[:,0]-seg[:,1])**2).mean())/np.sqrt(((seg[:,0]+seg[:,1])**2).mean()))
d,_=load(R+'drums.wav')
# kick: low band onsets
import scipy.signal as sg
sos=sg.butter(4,150,'low',fs=sr,output='sos'); k=sg.sosfilt(sos,d)
env=librosa.onset.onset_strength(y=k,sr=sr,hop_length=128)
on=librosa.onset.onset_detect(onset_envelope=env,sr=sr,hop_length=128,units='time',backtrack=False)+95
on=on[(on>=100)&(on<120)]
print('kick onsets',np.round(on,2))
ioi=np.diff(on);print('IOI',np.round(ioi,2))
bt=np.array(__import__('json').load(open('audio_features/beat_times.json')));bt=bt[(bt>=99)&(bt<121)]
print('beat IOI median',np.median(np.diff(bt)),'bpm',60/np.median(np.diff(bt)))
# grid: fit fixed
for g in [np.median(np.diff(bt))]:
    ph=(on-on[0])/g; print('kick phase dev (beats)',np.round(ph-np.round(ph),2), 'std s',np.std((ph-np.round(ph))*g))
# snare band
sos=sg.butter(4,[1500,6000],'band',fs=sr,output='sos'); sn=sg.sosfilt(sos,d)
e2=librosa.onset.onset_strength(y=sn,sr=sr,hop_length=128)
o2=librosa.onset.onset_detect(onset_envelope=e2,sr=sr,hop_length=128,units='time')+95
print('hi onsets 100-108',np.round(o2[(o2>=100)&(o2<108)],2))
# bass 10ms env
b,_=load(R+'bass.wav'); hop=int(.01*sr); rm=librosa.feature.rms(y=b,frame_length=hop*2,hop_length=hop)[0]; t=np.arange(len(rm))*.01+95
db=20*np.log10(rm+1e-9)
on_=db>-45; ch=np.flatnonzero(np.diff(on_.astype(int))); 
print('bass on/off transitions',[(round(t[i],2),'on' if on_[i+1] else 'off') for i in ch if 99<t[i]<121])
# vocals activity
v,_=load(R+'vocals.wav'); rv=librosa.feature.rms(y=v,frame_length=hop*2,hop_length=hop)[0]; dv=20*np.log10(rv+1e-9)
print('vocal db min/median/max 100-120',dv[(t>=100)&(t<120)].min(),np.median(dv[(t>=100)&(t<120)]),dv[(t>=100)&(t<120)].max())
vm=(dv>-45)[(t>=100)&(t<120)]; print('vocal active frac',vm.mean())
# other chroma / hpss centroid
o,_=load(R+'other.wav'); print('other centroid',librosa.feature.spectral_centroid(y=o,sr=sr).mean(),'mix',librosa.feature.spectral_centroid(y=mix,sr=sr).mean())
S=np.abs(librosa.stft(mix))**2;f=librosa.fft_frequencies(sr=sr)
for lo,hi in [(0,150),(150,2000),(2000,8000),(8000,11025)]: print(lo,hi,10*np.log10(S[(f>=lo)&(f<hi)].sum()/S.sum()))
# bar loop regularity: bass-drum envelope self-sim at 4-beat lag
env=librosa.onset.onset_strength(y=d,sr=sr,hop_length=256)
fr=256/sr; 
