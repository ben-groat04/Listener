import numpy as np, librosa
D='/home/user/Listener/v1/data/video2/stems_raw/htdemucs/song/'
sr=22050
v,_=librosa.load(D+'vocals.wav',sr=sr,mono=True)
hop=int(0.05*sr)
rms=librosa.feature.rms(y=v,frame_length=2048,hop_length=hop)[0]
db=20*np.log10(rms+1e-9);t=np.arange(len(db))*0.05
G0,P=0.133,0.49995
def bursts(a,b,thr=-52,mn=0.3,gap=0.2):
    m=(db>thr)&(t>=a)&(t<b);out=[];s=None;last=None
    for i,x in enumerate(m):
        if x:
            if s is None:s=i
            last=i
        elif s is not None and (i-last)*0.05>gap:
            if (last-s)*0.05>=mn:out.append((t[s],t[last]))
            s=None
    return out
bs=bursts(204,280)
print(len(bs),'bursts 3:24-4:40')
bar=[];beat=[];cell=[]
for a,b in bs:
    bp=((a-G0)/P)%4; bar.append(bp); cell.append(((a-156.8)/2.0)%6)
    print('%d:%04.1f dur %.1f beat-in-bar %.2f barcell %.2f'%(a//60,a%60,b-a,bp,((a-156.8)/2.0)%6))
bar=np.array(bar)
print('beat-of-bar histogram (0.5 beat bins):',np.histogram(bar,bins=np.arange(0,4.5,0.5))[0])
# onset (rising edge) spacing
st=np.array([a for a,b in bs]);print('median gap',np.median(np.diff(st)),'durations',np.round([b-a for a,b in bs],1))
for lo,hi in [(204,228),(228,252),(252,277)]:
    sel=[(a,b) for a,b in bs if lo<=a<hi];print(lo,hi,'n',len(sel),'mean dur %.2f'%np.mean([b-a for a,b in sel]) if sel else '')
# fraction of seconds voiced by zone
for lo,hi in [(204,228),(228,289),(289,300),(240,277)]:
    print('voiced frac',lo,hi,'%.2f'%np.mean(db[(t>=lo)&(t<hi)]>-52))
