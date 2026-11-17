import numpy as np, librosa, json
D='/home/user/Listener/v1/data/t_cshells_cshore/'
b=np.array(json.load(open(D+'audio_features/beat_times.json')));print('beats range',b[0],b[-1])
bb=b[(b>=238)&(b<262)];print('beat ioi mean',np.diff(bb).mean(),'std ms',np.diff(bb).std()*1000)
dr,s=librosa.load(D+'stems_raw/htdemucs/song/drums.wav',sr=22050,offset=235,duration=30)
env=librosa.onset.onset_strength(y=dr,sr=s,hop_length=128);t=librosa.times_like(env,sr=s,hop_length=128)+235
on=librosa.onset.onset_detect(onset_envelope=env,sr=s,hop_length=128,units='time')+235
on=on[(on>=240)&(on<260)]
bi=0.4915
# phase relative to beat grid at 8th and 16th
for sub,name in [(1,'beat'),(2,'8th'),(4,'16th')]:
    d=[]
    for o in on:
        k=np.argmin(np.abs(bb-o));g=bb[k]; step=bi/sub;n=np.round((o-g)/step);d.append((o-g-n*step)*1000)
    d=np.array(d);print(name,'n',len(d),'within30ms',np.mean(np.abs(d)<30).round(2),'rand expectation',round(60/(step*1000),2))
# bass pitch in 252-259
bs,_=librosa.load(D+'stems_raw/htdemucs/song/bass.wav',sr=22050,offset=250,duration=10)
f0,vf,vp=librosa.pyin(bs,fmin=30,fmax=200,sr=s,frame_length=4096)
tt=librosa.times_like(f0,sr=s,hop_length=1024)+250
for i in range(0,len(f0),8):
    if not np.isnan(f0[i]): print(round(tt[i],1),librosa.hz_to_note(f0[i]),end='; ')
print()
# mix 10ms peak / crest, stereo width and drum onset density per 5s
for t in range(240,260,5):
    print(t,'drum onsets',((on>=t)&(on<t+5)).sum())
# mix clipping fraction
a,sr=librosa.load(D+'audio/song.wav',sr=None,mono=False,offset=240,duration=20)
print('samples >=-0.1dBFS',int((np.abs(a)>0.989).sum()),'of',a.size)
