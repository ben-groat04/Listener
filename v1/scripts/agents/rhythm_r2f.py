import numpy as np, json
P=0.1923;ph=0.16
bt=np.array(json.load(open('/home/user/Listener/v1/data/video1/audio_features/beat_times.json')))
x=((bt-ph)/(4*P)); d=(x-np.round(x))*4*P
print('tracker minus hat-accent grid (s): median',np.median(d),'std',d.std(),'by 40s blocks',[round(float(np.median(d[(bt>a)&(bt<a+40)])),3) for a in range(0,160,40)])
# phase of the tracker in 16-slot cycle
s=np.round((bt-ph)/P).astype(int)%16
print('tracker beat slot mod16 counts',np.bincount(s,minlength=16))
w=json.load(open('/home/user/Listener/v1/data/video1/lyrics/whisper_medium_mix_nl_transcribe.json'))
segs=w['segments'] if isinstance(w,dict) else w
for sg in segs:
    if 130<sg['start']<170:
        xs=(sg['start']-ph)/P
        print(round(sg['start'],2),round(sg['end'],2),'slot mod4=%.2f'%(xs%4),sg['text'][:40])
