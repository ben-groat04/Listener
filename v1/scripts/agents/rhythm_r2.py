import librosa, numpy as np, sys
D='/home/user/Listener/v1/data/t_birdwalk/stems_raw/htdemucs/song/'
sr=22050
def on(n,lo=None):
    y,_=librosa.load(D+n+'.wav',sr=sr,mono=True)
    e=librosa.onset.onset_strength(y=y,sr=sr,hop_length=256)
    t=librosa.onset.onset_detect(onset_envelope=e,sr=sr,hop_length=256,units='time',backtrack=False)
    return t,e,y
td,ed,yd=on('drums'); tb,eb,yb=on('bass'); tv,ev,yv=on('vocals'); to,eo,yo=on('other')
np.save('/tmp/ons.npy',dict(d=td,b=tb,v=tv,o=to),allow_pickle=True)
def m(t):return '%d:%05.2f'%(t//60,t%60)
# 1 drum hit spacing in sparse sections
for a,b in [(0,12),(47,59),(120,131),(155,160)]:
    s=td[(td>=a)&(td<b)];print('drums',a,b,[round(x,2) for x in s][:30])
# bass onsets relative to nearest drum hit in groove 12-47 and 60-83
for a,b in [(12,47),(60,83),(135,143),(155,167)]:
    bb=tb[(tb>=a)&(tb<b)]; dd=td[(td>=a)&(td<b)]
    if len(dd)==0: continue
    d=[x-dd[np.argmin(abs(dd-x))] for x in bb]
    print('bass-drum offset',a,b,len(bb),'within40ms',np.mean(np.abs(d)<0.04).round(2),'median abs',np.median(np.abs(d)).round(3))
# first bass onsets after re-entries
for t0 in [12.4,59.3,131.3,155.7,107]:
    print('bass after',t0,[round(x,2) for x in tb[(tb>=t0-1)&(tb<t0+9)]])
