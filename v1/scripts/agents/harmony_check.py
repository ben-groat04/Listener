import json,numpy as np,librosa,collections
D='/home/user/Listener/v1/data/t_cshells_cshore/'
ch=json.load(open(D+'music_views/chords.json'))
sh=collections.Counter()
for c in ch:
    if c['start']<350: sh[c['chord']]+=c['end']-c['start']
tot=sum(sh.values());print('chord share',[(k,round(v/tot*100,1)) for k,v in sh.most_common(10)])
R='/home/user/Listener/v1/data/t_cshells_cshore/stems_raw/htdemucs/song/'
names=['A','A#','B','C','C#','D','D#','E','F','F#','G','G#']
for stem in ['other','bass']:
    y,sr=librosa.load(R+stem+'.wav',sr=22050)
    for a,b in [(25,32),(40,60),(65,100),(100,120),(120,140),(140,180),(180,200),(200,240),(240,280),(280,300),(300,320),(320,340)]:
        seg=y[int(a*sr):int(b*sr)]
        c=librosa.feature.chroma_cqt(y=seg,sr=sr,fmin=librosa.note_to_hz('C1'),n_octaves=6).mean(1)
        c=np.roll(c,-9) # A first
        c=c/c.max()
        print(stem,a,b,' '.join(f'{n}:{v:.2f}' for n,v in zip(names,c) if v>0.3))
