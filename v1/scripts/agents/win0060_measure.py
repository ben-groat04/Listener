import json,numpy as np,librosa
D='/home/user/Listener/v1/data/t_cshells_cshore/'
y,sr=librosa.load(D+'audio/song.wav',sr=None,mono=False)
m=y.mean(0) if y.ndim>1 else y
print('sr',sr,'peak 60-80',np.abs(y[:,60*sr:80*sr]).max(), 'dB',20*np.log10(np.abs(y[:,60*sr:80*sr]).max()))
print('global peak dB',20*np.log10(np.abs(y).max()))
pl=json.load(open(D+'music_views/per_second_levels.json'))
for r in pl[56:84]: print(r['t'],r['dbfs'],r['width'],r['vocals'],r['drums'],r['bass'],r['other'])
st={}
for n in ['vocals','drums','bass','other']:
    st[n],_=librosa.load(D+f'stems_raw/htdemucs/song/{n}.wav',sr=sr)
h=int(sr*0.01)
def env(x,a,b):
    s=x[int(a*sr):int(b*sr)];n=len(s)//h
    return 20*np.log10(np.sqrt((s[:n*h].reshape(n,h)**2).mean(1))+1e-9)
for a,b in [(60,61),(64.5,66),(68.5,70),(72.5,74),(76.5,78)]:
    print(a,b,{k:round(float(env(v,a,b).max()),1) for k,v in {'mix':m,**st}.items()})
# onsets drums
d=st['drums'][60*sr:80*sr]
on=librosa.onset.onset_detect(y=d,sr=sr,units='time',backtrack=False)
print('drum onsets',np.round(on+60,2))
# low-band kick
import scipy.signal as ss
sos=ss.butter(4,150,'low',fs=sr,output='sos');k=ss.sosfilt(sos,d)
on=librosa.onset.onset_detect(y=k,sr=sr,units='time');print('kick',np.round(on+60,2),np.round(np.diff(on),3))
bt=json.load(open(D+'audio_features/beat_times.json'));bt=bt if isinstance(bt,list) else bt.get('beats',bt)
print([round(b,2) for b in bt if 58<b<82] if isinstance(bt,list) else str(bt)[:200])
# stem rms per window
for n in st:
    for a,b in [(60,64.6),(64.8,68.6),(68.8,72.8),(73,76.6),(77,80)]:
        s=st[n][int(a*sr):int(b*sr)];print(n,a,b,round(20*np.log10(np.sqrt((s**2).mean())+1e-9),1),end=' | ')
    print()
# spectral centroid
for a in range(60,80,4):
    s=m[a*sr:(a+4)*sr];print(a,round(float(librosa.feature.spectral_centroid(y=s,sr=sr).mean())))
