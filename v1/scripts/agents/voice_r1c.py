import numpy as np, librosa, json
B='/home/user/Listener/v1/data/t_birdwalk/'
D=B+'stems_raw/htdemucs/song/'
bt=np.array(json.load(open(B+'audio_features/beat_times.json')) if not isinstance(json.load(open(B+'audio_features/beat_times.json')),dict) else json.load(open(B+'audio_features/beat_times.json'))['beat_times'])
print('beat IOI median',np.median(np.diff(bt)))
d,sr=librosa.load(D+'drums.wav',sr=22050,mono=True)
v,_=librosa.load(D+'vocals.wav',sr=22050,mono=True)
hop=110
def ons(y,lo=None):
    oe=librosa.onset.onset_strength(y=y,sr=sr,hop_length=hop)
    return librosa.onset.onset_detect(onset_envelope=oe,sr=sr,hop_length=hop,units='time',delta=0.2), oe
vo,voe=ons(v)
# kicks: drums low band
import scipy.signal as ss
sos=ss.butter(4,[40,150],'bp',fs=sr,output='sos');k=ss.sosfilt(sos,d)
ko,_=ons(k)
def phase(on,a,b,per):
    o=on[(on>=a)&(on<b)];ph=(o%per)/per*2*np.pi
    return len(o),round(float(abs(np.exp(1j*ph).mean())),3)
# local beat period from tracker: use grid anchored at nearest beats
def beat_phase(on,a,b):
    o=on[(on>=a)&(on<b)]
    idx=np.searchsorted(bt,o)-1;idx=np.clip(idx,0,len(bt)-2)
    ph=(o-bt[idx])/(bt[idx+1]-bt[idx]);ph=ph*2*np.pi
    # 2 divisions per beat (8th) -> use mod pi
    return len(o),round(float(abs(np.exp(1j*ph).mean())),3),round(float(abs(np.exp(2j*ph).mean())),3)
for a,b in [(1,12),(13,47),(47,59),(60,110),(110,167),(128,140),(140,146)]:
    ioi=np.diff(ko[(ko>=a)&(ko<b)])
    print(a,b,'vocal onsets (n,R beat,R 8th)',beat_phase(vo,a,b),'kicks',((ko>=a)&(ko<b)).sum(),'kick IOI median',round(float(np.median(ioi)),3) if len(ioi) else None)
# vocal-onset spacing in 2:24-2:35
o=vo[(vo>=144)&(vo<155)];print('IOI vocal 2:24-2:35 median',np.median(np.diff(o)),'beat',np.median(np.diff(bt)))
# end of track: vocal last 3 s 10 ms envelope
for name in ['vocals','drums','bass','other']:
    y,_=librosa.load(D+name+'.wav',sr=None,mono=True)
    sr0=44100;h=441
    e=20*np.log10(np.array([np.sqrt((y[i:i+h]**2).mean()) for i in range(len(y)-3*sr0,len(y)-h,h)])+1e-9)
    print(name,'last3s 10ms dB: max',round(e.max(),1),'last',round(e[-1],1),'last>-60 at',round(len(y)/sr0-3+ (np.where(e>-60)[0].max())*0.01,2) if (e>-60).any() else 'never')
y,sr0=librosa.load(B+'audio/song.wav',sr=None,mono=True)
e=20*np.log10(np.array([np.sqrt((y[i:i+441]**2).mean()) for i in range(len(y)-3*sr0,len(y)-441,441)])+1e-9)
print('mix last3s max',e.max().round(1),'last',e[-1].round(1),'last>-60',len(y)/sr0-3+np.where(e>-60)[0].max()*0.01, 'dur',len(y)/sr0)
# vocal level around hook chop 2:40-2:47 vs gap and 0:47 
for a,b in [(167,168),(168,177)]:
    pass
