import librosa, numpy as np, json
p='/home/user/Listener/v1/data/video1/audio/song.wav'
out='/home/user/Listener/v1/data/video1/audio_features/extra/'
y,sr=librosa.load(p,sr=22050,mono=True)
# bass root per section via chroma on low band & fine tempo
yl=librosa.effects.preemphasis(y)
ch=librosa.feature.chroma_cqt(y=y,sr=sr,fmin=librosa.note_to_hz('C1'),n_octaves=3,hop_length=2048)
names=['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
fps=sr/2048
res={}
for a,b in [(0,15),(15,66),(66,75),(75,88),(88,109),(109,119),(119,134),(134,159),(159,189)]:
    c=ch[:,int(a*fps):int(b*fps)].mean(1); idx=np.argsort(c)[::-1][:4]
    res[f'{a}-{b}']=[(names[i],round(float(c[i]/c.max()),2)) for i in idx]
print(res)
# bass-note track: pitch of low band
yb=librosa.effects.harmonic(y)
f0,vf,vp=librosa.pyin(y,fmin=40,fmax=200,sr=sr,frame_length=4096,hop_length=1024)
t=librosa.times_like(f0,sr=sr,hop_length=1024)
for a,b in [(0,15),(15,66),(66,75),(75,88),(88,109),(109,119),(119,134),(134,159),(159,189)]:
    m=(t>=a)&(t<b)&~np.isnan(f0)
    nn=[names[int(round(librosa.hz_to_midi(x)))%12] for x in f0[m]]
    from collections import Counter
    print(a,b,Counter(nn).most_common(5))
# beat tracking with fixed tempo hypotheses and downbeat guess via low-band onset
oenv=librosa.onset.onset_strength(y=y,sr=sr,hop_length=512)
for st in (76,78,152):
    tp,bt=librosa.beat.beat_track(onset_envelope=oenv,sr=sr,hop_length=512,start_bpm=st,tightness=200)
    print(st,float(np.atleast_1d(tp)[0]),len(bt))
# beat period stability: IBI of tracked beats
tp,bt=librosa.beat.beat_track(onset_envelope=oenv,sr=sr,hop_length=512,start_bpm=152,tightness=100)
bt_t=librosa.frames_to_time(bt,sr=sr,hop_length=512); ibi=np.diff(bt_t)
print('ibi median',np.median(ibi),'bpm',60/np.median(ibi))
for a in range(0,189,20):
    m=(bt_t[:-1]>=a)&(bt_t[:-1]<a+20); print(a,round(60/np.median(ibi[m]),1) if m.any() else None)
# spectral-flux first 12s detail, and seconds 108-120,148-160
rms=librosa.feature.rms(y=y,hop_length=512)[0]; ft=librosa.times_like(rms,sr=sr,hop_length=512)
for a,b in [(0,4),(14,16),(65,67),(75,76.5),(87,89),(109,113),(118,123),(133,135),(148,156),(186,189)]:
    m=(ft>=a)&(ft<b); print(a,b,np.round(rms[m][::max(1,m.sum()//10)],2))
json.dump(res,open(out+'chroma_sections.json','w'))
