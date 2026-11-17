import json,numpy as np,librosa
D='/home/user/Listener/v1/data/t_birdwalk/'
S=D+'stems_raw/htdemucs/song/'
t0,t1=18,42
res={}
for n in ['drums','bass','vocals','other']:
    y,sr=librosa.load(S+n+'.wav',sr=22050,offset=t0,duration=t1-t0)
    res[n]=(y,sr)
# onsets
for n in ['drums','bass']:
    y,sr=res[n]
    if n=='drums':
        y=librosa.effects.preemphasis(y)
    # low band for kick
    import scipy.signal as ss
    b,a=ss.butter(4,150/(sr/2))
    lo=ss.filtfilt(b,a,res[n][0])
    env=librosa.onset.onset_strength(y=lo,sr=sr,hop_length=256)
    on=librosa.onset.onset_detect(onset_envelope=env,sr=sr,hop_length=256,units='time',backtrack=False)+t0
    print(n,'lowband onsets',np.round(on,2).tolist())
    print(' IOI',np.round(np.diff(on),2).tolist())
# per-stem RMS per 1 s
for n in res:
    y,sr=res[n]
    r=[20*np.log10(np.sqrt(np.mean(y[i*sr:(i+1)*sr]**2))+1e-9) for i in range(t1-t0)]
    print(n,[round(x) for x in r])
# mix level + peak
y,sr=librosa.load(D+'audio/song.wav',sr=None,mono=False,offset=20,duration=20)
print('mix peak dBFS 20-40',20*np.log10(np.abs(y).max()), 'sr',sr)
m=y.mean(0);
print('mix rms',20*np.log10(np.sqrt((m**2).mean())))
# spectral rolloff / centroid
ym=librosa.to_mono(y)
print('rolloff95 Hz by 5s',[round(float(np.median(librosa.feature.spectral_rolloff(y=ym[int(a*sr):int((a+5)*sr)],sr=sr,roll_percent=.95)))) for a in range(0,20,5)])
