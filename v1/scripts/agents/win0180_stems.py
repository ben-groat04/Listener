import numpy as np,librosa,json
from scipy.signal import butter,sosfiltfilt
D='/home/user/Listener/v1/data/t_cshells_cshore/stems_raw/htdemucs/song/'
sr=22050
st={n:librosa.load(D+n+'.wav',sr=sr,offset=170,duration=40)[0] for n in['drums','bass','vocals','other']}
mix=sum(st.values())
def db(x,a,b): 
    s=x[int(a*sr):int(b*sr)]; return round(20*np.log10(np.sqrt((s**2).mean())+1e-9),1)
# times relative to 170
for lo,hi in [(10,14),(14,17),(17,20),(20,23),(23,26),(26,29),(29,33),(33,36),(36,40)]:
    print(f'{lo+170}-{hi+170}',{n:db(x,lo,hi) for n,x in {**st,'mix':mix}.items()})
# kick: drums lowpass 120Hz onsets
sos=butter(4,120,'low',fs=sr,output='sos')
k=sosfiltfilt(sos,st['drums'])
env=librosa.onset.onset_strength(y=k,sr=sr,hop_length=128)
on=librosa.onset.onset_detect(onset_envelope=env,sr=sr,hop_length=128,units='time')+170
on=on[(on>180)&(on<200)]
print('kick onsets',np.round(on,2)); i=np.diff(on);print('IOI median',np.median(i),'n',len(on))
bt=json.load(open('/home/user/Listener/v1/data/t_cshells_cshore/audio_features/beat_times.json'))
bt=np.array(bt if isinstance(bt,list) else bt['beats']);
d=[np.min(np.abs(bt-t)) for t in on];print('kick-to-tracker-beat dev ms median',np.median(d)*1000,'p90',np.percentile(d,90)*1000)
# loop regularity of bass: correlation of bass env bars (4 beats=1.952s)
be=librosa.feature.rms(y=st['bass'],hop_length=256)[0]
# 10ms spread
print('bass env 5-sec bins',[round(float(np.mean(be[int(t*sr/256):int((t+1)*sr/256)])),3) for t in range(8,30)])
# 10ms envelopes of other around 18.3-19.5 (198-199.5) & mix at 193
h=int(sr*0.01)
def env10(x,a,b):
    s=x[int(a*sr):int(b*sr)];n=len(s)//h;return 20*np.log10(np.sqrt((s[:n*h].reshape(n,h)**2).mean(1))+1e-9)
for n in ['other','bass','drums']:
    e=env10(st[n],27.5,30); print(n,'198-200 0.25s steps',np.round(e[::25],0))
e=env10(mix,22.5,24.5);print('mix 192.5-194.5',np.round(e[::10],0))
