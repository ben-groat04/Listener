import json,numpy as np,soundfile as sf,librosa
D='/home/user/Listener/v1/data/video2/'
L={r['t']:r for r in json.load(open(D+'music_views/per_second_levels.json'))}
print('vox',[(t,L[t]['vocals']) for t in (208,212,216,220,224,236,240,260)])
v,sr=sf.read(D+'stems_raw/htdemucs/song/vocals.wav'); v=v.mean(1)
def pk(a,b):
    s=v[int(a*sr):int(b*sr)]; h=int(.05*sr); n=len(s)//h
    r=10*np.log10((s[:n*h].reshape(n,h)**2).mean(1)+1e-12); return round(r.max(),1)
print('vox peak 208-216',pk(208,216),'226-276',pk(226,276))
calls=[286.6+2*i for i in range(7)]
print('calls',[pk(c-.2,c+1.6) for c in calls])
# drums onsets per bar
d,_=sf.read(D+'stems_raw/htdemucs/song/drums.wav'); d=d.mean(1)
on=librosa.onset.onset_detect(y=d,sr=sr,units='time',hop_length=256,backtrack=False)
res=[]
for e in range(int(88.61+2*10),300,2):
    pass
bars=np.arange(88.61,300,2.0)
cnt=[(round(b+2,1),int(((on>=b)&(on<b+2)).sum())) for b in bars]
print('bars',[c for c in cnt if c[1]>=10])
# bass cqt dominant pitch class 4-s blocks 270-300
b,_=sf.read(D+'stems_raw/htdemucs/song/bass.wav'); b=b.mean(1)
for t in range(272,296,4):
    C=librosa.feature.chroma_cqt(y=b[t*sr:(t+4)*sr],sr=sr,fmin=librosa.note_to_hz('C1'),n_octaves=4)
    print(t,librosa.midi_to_note(60+int(C.mean(1).argmax()))[:-1],end='; ')
print()
o,_=sf.read(D+'stems_raw/htdemucs/song/other.wav'); o=o.mean(1)
nm=['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
for t in range(0,28,4):
    c=librosa.feature.chroma_cqt(y=o[t*sr:(t+4)*sr],sr=sr).mean(1); c/=c.max()
    print(t,[(nm[i],round(c[i],2)) for i in np.argsort(-c)[:4]])
# bass level 0.1s around 4:37
bb=b[int(276*sr):int(284*sr)];h=int(.1*sr);n=len(bb)//h
print(np.round(10*np.log10((bb[:n*h].reshape(n,h)**2).mean(1)+1e-12),0))
