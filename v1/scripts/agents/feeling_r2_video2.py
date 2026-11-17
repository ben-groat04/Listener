import json,numpy as np,librosa
d='data/video2/'
L=json.load(open(d+'music_views/per_second_levels.json'))
t=np.array([r['t'] for r in L]);m=np.array([r['dbfs'] for r in L])
for a,b in [(100,157),(157,217),(217,277),(100,277)]:
    s=(t>=a)&(t<b); x=m[s]; print(a,b,'mean %.1f std %.2f range %.1f'%(x.mean(),x.std(),np.ptp(x)))
# loudness vs a rolling 1-min mean: crest of macro change
for a in range(100,280,20):
    s=(t>=a)&(t<a+20);print(a, '%.1f'%m[s].mean(), end=' | ')
print()
# vocal 2 s call phase vs drum bar phase 4:44-5:00
y,sr=librosa.load(d+'stems_raw/htdemucs/song/drums.wav',sr=22050,offset=100,duration=190)
oe=librosa.onset.onset_strength(y=y,sr=sr,hop_length=256)
fr=librosa.frames_to_time(np.arange(len(oe)),sr=sr,hop_length=256)+100
# bar phase: fold 2.0s, find peak (kick-dominated low band)
ph=(fr%2.0)
h,_=np.histogram(ph,bins=40,weights=oe);print('bar phase peak (s):',(np.argmax(h)+.5)*0.05)
for v in [286.6,288.6,290.6,292.6,294.6,296.6,298.6]:
    print(v,'phase %.2f'%(v%2.0),end='; ')
