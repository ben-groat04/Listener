import json,numpy as np,librosa,sys
D='/home/user/Listener/v1/data/t_cshells_cshore/'
p=json.load(open(D+'music_views/per_second_levels.json'))
for r in p[16:44]: print(r)
b=json.load(open(D+'audio_features/beat_times.json'));
bt=np.array(b['beats'] if isinstance(b,dict) else b)
print('beats',bt[(bt>18)&(bt<42)].round(2))
sr=22050
def ld(n,s=18,d=24): return librosa.load(D+n,sr=sr,offset=s,duration=d,mono=False)
y,_=ld('audio/song.wav')
ym=y.mean(0) if y.ndim>1 else y
print('peak',np.abs(y).max(), 20*np.log10(np.abs(y).max()))
hop=220 # 10ms
def env(x): return librosa.feature.rms(y=x,frame_length=441*2,hop_length=hop)[0]
t0=18
e=env(ym);tt=np.arange(len(e))*hop/sr+t0
for a in range(20,41):
    m=(tt>=a)&(tt<a+1);print(a,'mixdB %.1f'%(20*np.log10(e[m].mean()+1e-9)),end=' | ')
print()
st={}
for n in ['drums','bass','vocals','other']:
    s,_=librosa.load(D+f'stems_raw/htdemucs/song/{n}.wav',sr=sr,offset=t0,duration=24,mono=True);st[n]=s
    es=env(s)
    print(n,' '.join('%d:%.0f'%(a,20*np.log10(es[(tt>=a)&(tt<a+1)].mean()+1e-9)) for a in range(20,41)))
# onsets in drums
d=st['drums']
on=librosa.onset.onset_detect(y=d,sr=sr,hop_length=hop,units='time',backtrack=False)+t0
print('drum onsets',on[(on>=20)&(on<=40)].round(2))
# low-band kick onsets
import scipy.signal as ss
sos=ss.butter(4,150,'low',fs=sr,output='sos');k=ss.sosfilt(sos,d)
ok=librosa.onset.onset_detect(y=k,sr=sr,hop_length=hop,units='time')+t0
ok=ok[(ok>=20)&(ok<=40)];print('kick onsets',ok.round(3));print('IOI',np.diff(ok).round(3))
# stereo width
if y.ndim>1:
    for a in (20,24,26,30,36):
        m=(np.arange(y.shape[1])/sr+t0>=a)&(np.arange(y.shape[1])/sr+t0<a+2)
        l,r=y[0][m],y[1][m];mid=(l+r)/2;sd=(l-r)/2;print(a,'S/M dB %.1f'%(20*np.log10((sd.std()+1e-9)/(mid.std()+1e-9))))
# spectral centroid
c=librosa.feature.spectral_centroid(y=ym,sr=sr,hop_length=512)[0];tc=librosa.frames_to_time(np.arange(len(c)),sr=sr,hop_length=512)+t0
for a in range(20,40,2): print(a,'cent %.0f'%c[(tc>=a)&(tc<a+2)].mean(),end=' | ')
