import numpy as np, librosa, soundfile as sf
D='/home/user/Listener/v1/data/t_cshells_cshore/'
sr=22050;hop=110
def ld(p):
    y,s=sf.read(p); y=y.mean(1) if y.ndim>1 else y
    return librosa.resample(y,orig_sr=s,target_sr=sr)
for nm,p in [('mix','audio/song.wav'),('drums','stems_raw/htdemucs/song/drums.wav')]:
    y=ld(D+p); oe=librosa.onset.onset_strength(y=y,sr=sr,hop_length=hop)
    print(nm)
    for a in range(60,330,20):
        x=oe[int(a*sr/hop):int((a+20)*sr/hop)]; x=x-x.mean()
        if x.std()<1e-6: continue
        ac=np.correlate(x,x,'full')[len(x)-1:]; ac/=ac[0]
        lg=np.arange(len(ac))*hop/sr
        # fit period near 0.4-0.6 via parabolic peak; also 8-beat lag 3.7-4.3 and bar 1.8-2.2
        def pk(lo,hi):
            m=(lg>lo)&(lg<hi); i=np.where(m)[0][np.argmax(ac[m])]; return lg[i],ac[i]
        b=pk(0.44,0.56); bar=pk(1.8,2.2); b8=pk(3.7,4.3)
        print(a,'beat lag %.3f (%.2f) -> %.1f BPM | 4-beat lag %.3f (%.2f) -> %.1f | 8-beat %.3f (%.2f) -> %.1f'%(b[0],b[1],60/b[0],bar[0],bar[1],240/bar[0],b8[0],b8[1],480/b8[0]))
