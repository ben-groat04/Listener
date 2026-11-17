import numpy as np, librosa, json
d='stems_raw/htdemucs/song/'
sr=22050
def load(n): return librosa.load(d+n+'.wav',sr=sr,mono=True)[0]
oth=load('other'); voc=load('vocals'); bas=load('bass')
tun=librosa.estimate_tuning(y=oth,sr=sr); print('tuning(semitone frac) other',round(tun,3),'cents',round(tun*100,1))
def chroma(y,t0,t1):
    s=y[int(t0*sr):int(t1*sr)]
    c=librosa.feature.chroma_cqt(y=s,sr=sr,tuning=tun,n_octaves=5,fmin=librosa.note_to_hz('C2')).mean(1)
    return c/c.max()
N=['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
def show(l,c): print(l,' '.join(f'{N[i]}{c[i]:.2f}' for i in range(12) if c[i]>0.25))
# side-step vs static, other and bass stem
for lab,(a,b) in {'sidestep 3:19.6-3:22.1':(199.6,202.1),'sidestep 3:28.5-3:32.3':(208.5,212.3),'sidestep 0:16.7-0:19.2':(16.7,19.2),'sidestep 1:17.6-1:20.1':(77.6,80.1),'static hook 3:23-3:28':(203,208),'static verse 2:40-2:50':(160,170),'static hook 3:14-3:19':(194,199)}.items():
    show(lab+' other',chroma(oth,a,b)); show(lab+' bass',chroma(bas,a,b))
# hook vs verse other chroma
show('verse1 0:40-1:10 other',chroma(oth,40,70)); show('hook 3:14-3:35 other',chroma(oth,194,215))
# tonic vs bed: verse voice pitch class share against tuning
lead=json.load(open('music_views/lead_notes.json')); print(type(lead), (list(lead.keys())[:5] if isinstance(lead,dict) else lead[:3]))
