import numpy as np, librosa, soundfile as sf
d='/home/user/Listener/v1/data/t_birdwalk/'
b=d+'stems_raw/htdemucs/song/'
dr,sr=sf.read(b+'drums.wav'); dr=dr.mean(1)
# kick: lowpass band onsets
import scipy.signal as ss
sos=ss.butter(4,150,'low',fs=sr,output='sos'); k=ss.sosfilt(sos,dr)
hop=441
ke=librosa.feature.rms(y=k,frame_length=1323,hop_length=hop)[0]
on=librosa.onset.onset_detect(onset_envelope=np.diff(ke,prepend=0).clip(0),sr=sr,hop_length=hop,units='time',backtrack=False,delta=0.01)
on=on[(on>=176)&(on<=188)]
print('kick onsets',np.round(on,2)); print('IOI',np.round(np.diff(on),3))
# drum onsets full
o=librosa.onset.onset_detect(y=dr,sr=sr,units='time',delta=0.2)
o=o[(o>=176)&(o<=188)];print('drum onsets',np.round(o,2))
for nm in ['drums','bass','other','vocals']:
    y,_=sf.read(b+nm+'.wav');y=y.mean(1)
    for a,e in [(176,180),(180,183),(183,185),(185,188)]:
        s=y[int(a*sr):int(e*sr)]; print(nm,a,e,'rms dB',round(20*np.log10(np.sqrt((s**2).mean())+1e-9),1),'centroid',round(librosa.feature.spectral_centroid(y=s,sr=sr).mean()))
y,_=sf.read(d+'audio/song.wav');L=y[:,0];R=y[:,1]
for a,e in [(165,170),(170,176),(176,180),(180,185)]:
    s=y.mean(1)[int(a*sr):int(e*sr)];S=np.abs(librosa.stft(s))**2;f=librosa.fft_frequencies(sr=sr)
    c=np.cumsum(S.sum(1))/S.sum();print(a,e,'rolloff95',f[np.searchsorted(c,.95)],'rolloff99',f[np.searchsorted(c,.99)],'rms',round(20*np.log10(np.sqrt((s**2).mean())),1),'peak',round(20*np.log10(np.abs(y[int(a*sr):int(e*sr)]).max()),1))
# tempo & beat
bt=np.array(__import__('json').load(open(d+'audio_features/beat_times.json')))
bb=bt[(bt>=176)&(bt<=188)];print('beats',np.round(bb,2),'IBI',np.round(np.diff(bb).mean(),3))
# bar loop regularity: correlate 4-beat chroma/onset env
oe=librosa.onset.onset_strength(y=dr,sr=sr,hop_length=hop)
t=np.arange(len(oe))*hop/sr
# 1.58s bar, compare successive bars from 160 to 180
bar=0.395*4
for st in np.arange(160,178,bar):
    a=oe[(t>=st)&(t<st+bar)];c=oe[(t>=st+bar)&(t<st+2*bar)];n=min(len(a),len(c))
    print(round(st,2),round(np.corrcoef(a[:n],c[:n])[0,1],2),end=' | ')
print()
# last two hits at 185.23,186.43,187.22 band energies
yy=y.mean(1)
for t0 in (185.2,186.4,187.2):
    s=yy[int(t0*sr):int((t0+.15)*sr)];S=np.abs(np.fft.rfft(s*np.hanning(len(s))));f=np.fft.rfftfreq(len(s),1/sr)
    print(t0,'peak freq',f[S.argmax()].round(0))
