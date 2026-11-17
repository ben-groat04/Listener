import json,numpy as np,librosa,soundfile as sf
D='/home/user/Listener/v1/data/t_dl_mirror/'
ch=json.load(open(D+'music_views/chords.json'))
# side-steps: runs where Gm/G/F/C/Am appear
steps=[];cur=None
for c in ch:
    if c['chord'] in('Gm','G','F','C','Am','A#','F#m'):
        if cur and c['start']-cur[1]<1.5: cur[1]=c['end'];cur[2].append(c['chord'])
        else:
            if cur:steps.append(cur)
            cur=[c['start'],c['end'],[c['chord']]]
if cur:steps.append(cur)
for s in steps:print('step %d:%05.2f-%05.2f %s'%(s[0]//60,s[0]%60,s[1],' '.join(s[2])))
gm=[s[0] for s in steps if 'Gm' in s[2] or 'G' in s[2]]
print('G-starts',[round(x,1) for x in gm]); print('gaps',np.round(np.diff(gm),1))
tot=sum(c['end']-c['start'] for c in ch)
for n in['D','Dm','Gm','G','F','Am','C']:print(n,round(sum(c['end']-c['start'] for c in ch if c['chord']==n),1))
# chroma of stems
for nm in['other','bass','vocals']:
    y,sr=librosa.load(D+'stems_raw/htdemucs/song/%s.wav'%nm,sr=22050,mono=True)
    C=librosa.feature.chroma_cqt(y=y,sr=sr,hop_length=2048)
    names='C C# D D# E F F# G G# A A# B'.split()
    t=librosa.frames_to_time(np.arange(C.shape[1]),sr=sr,hop_length=2048)
    print('==',nm)
    for a in range(0,240,30):
        m=(t>=a)&(t<a+30)
        if m.sum()==0:continue
        v=C[:,m].mean(1);v=v/v.max()
        print(a,' '.join('%s%.2f'%(names[i],v[i]) for i in np.argsort(-v)[:6]))
    if nm=='other':
        # loop regularity: autocorrelation of chroma
        Cn=C/ (np.linalg.norm(C,axis=0)+1e-9)
        fps=sr/2048
        seg=Cn[:, int(40*fps):int(100*fps)]  # steady section
        ac=[]
        for lag in range(int(1*fps),int(12*fps)):
            ac.append((seg[:,:-lag]*seg[:,lag:]).sum(0).mean())
        ac=np.array(ac);lags=(np.arange(len(ac))+int(1*fps))/fps
        for i in np.argsort(-ac)[:5]:print('lag %.2f ac %.3f'%(lags[i],ac[i]))
        # F vs F# vs Bb vs C
        for a,b in[(2,10),(40,60),(100,130),(160,200),(225,235)]:
            m=(t>=a)&(t<b);v=C[:,m].mean(1);v/=v.max()
            print('third %d-%d F %.2f F# %.2f D %.2f A %.2f Bb %.2f'%(a,b,v[5],v[6],v[2],v[9],v[10]))
x,sr=sf.read(D+'audio/song.wav');print('peak',20*np.log10(np.abs(x).max()))
