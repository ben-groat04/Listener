import numpy as np, librosa
S='/home/user/Listener/v1/data/video1/stems_raw/htdemucs/song/'
y,sr=librosa.load(S+'drums.wav',sr=22050,mono=True)
on=librosa.onset.onset_detect(y=y,sr=sr,hop_length=256,units='time',backtrack=False)
for a in [(0,20),(20,40),(40,60),(60,75),(75,88),(88,110),(110,118),(118,134),(134,158),(158,168),(168.5,188)]:
    o=on[(on>=a[0])&(on<a[1])]; print(a,'%.2f/s'%(len(o)/(a[1]-a[0])),'median IOI %.3f'%np.median(np.diff(o)))
# bass activity: fraction of seconds bass > -35 dB
import json
d=json.load(open('/home/user/Listener/v1/data/video1/music_views/per_second_levels.json'))
off=[r['t'] for r in d if r['bass']<-50 and r['t']>5]
runs=[];s=off[0];p=off[0]
for t in off[1:]:
    if t!=p+1: runs.append((s,p));s=t
    p=t
runs.append((s,p))
print('bass-off runs (s):',[(f'{a//60}:{a%60:02d}',f'{b//60}:{b%60:02d}') for a,b in runs])
