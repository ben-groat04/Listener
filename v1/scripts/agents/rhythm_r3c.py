import numpy as np, librosa
D='/home/user/Listener/v1/data/t_birdwalk/stems_raw/htdemucs/song/'
sr=22050;h=256
def ons(n):
    y,_=librosa.load(D+n+'.wav',sr=sr)
    e=librosa.onset.onset_strength(y=y,sr=sr,hop_length=h)
    return librosa.onset.onset_detect(onset_envelope=e,sr=sr,hop_length=h,units='time',backtrack=False),y
td,yd=ons('drums');tb,yb=ons('bass');to,yo=ons('other')
np.save('/tmp/r3ons.npy',dict(d=td,b=tb,o=to),allow_pickle=True)
# Q lineage: IOI hist in dense stretches
for a,b in [(94,120),(168,177),(0,200)]:
    s=td[(td>=a)&(td<b)];i=np.diff(s);i=i[(i>0.04)&(i<0.5)]
    print('drum IOI',a,b,len(s),np.histogram(i,bins=[.04,.08,.10,.14,.17,.21,.23,.27,.31,.35,.43,.5])[0])
# grid fit: phase of drum onsets in dense stretch vs 0.1875 grid, and 0.125 (triplet-16th at 80 = 0.125)
for a,b in [(94,120),(168,177)]:
    s=td[(td>=a)&(td<b)]
    for p in (0.1875,0.125,0.25):
        ph=2*np.pi*(s%p)/p;print(a,p,'R',round(abs(np.exp(1j*ph).mean()),2))
# pickups: drum onsets in 2s before each bass return
for name,t0,loop in [('return1',59.3,60.4),('return2',131.3,132.4),('cut1',47.2,48.4),('cut2',119.2,120.4),('cut3',143.5,144.7)]:
    x=td[(td>t0-3)&(td<t0+1)]; print(name,t0,np.round(x-t0,2).tolist())
# bass entries relative to nearest drum onset, then other onsets vs drum grid
for a,b in [(40,47),(62,80)]:
    s=to[(to>=a)&(to<b)];dd=np.array([np.min(abs(td-t)) for t in s]);print('other-vs-drum',a,b,len(s),'frac<40ms',round((dd<.04).mean(),2),'median',round(np.median(dd),3))
# tempo from drum-only
for a,b in [(12,47),(60,95),(95,119),(131,143),(155,177)]:
    seg=yd[int(a*sr):int(b*sr)];t,_=librosa.beat.beat_track(y=seg,sr=sr,start_bpm=80,tightness=100);print('drum-only tempo',a,b,np.round(t,1))
# bass-only tempo for contrast
for a,b in [(12,47),(60,95)]:
    seg=yb[int(a*sr):int(b*sr)];t,_=librosa.beat.beat_track(y=seg,sr=sr,start_bpm=80);print('bass-only tempo',a,b,np.round(t,1))
# first groove: drum onsets 11-14 and bass
print('bass',np.round(tb[(tb>11)&(tb<15)],2).tolist());print('drum',np.round(td[(td>11)&(td<15)],2).tolist())
