import numpy as np, soundfile as sf, scipy.signal as ss
D='/home/user/Listener/v1/data/t_dl_mirror/'
tk=np.load('/tmp/kicks.npy'); g=[tk[0]]
for x in tk[1:]:
    if x-g[-1]>0.15: g.append(x)
g=np.array(g); ioi=np.diff(g)
for bpm in (93.0,93.5,94.0,94.5,95.0,95.7):
    st=60/bpm/4; h=np.round(ioi/st); pos=np.concatenate([[0],np.cumsum(h)])*st; res=g-g[0]-pos
    print(bpm,'cum residual: std ms %.0f, total drift ms %.0f'%(res.std()*1000,(res[-1]-res[0])*1000))
def env(path,hopms=10):
    x,sr=sf.read(path); 
    if x.ndim>1: x=x.mean(1)
    n=int(sr*hopms/1000); k=len(x)//n; e=np.sqrt((x[:k*n].reshape(k,n)**2).mean(1)); return 20*np.log10(e+1e-12),sr,x
# ending
for nm,p in (('mix',D+'audio/song.wav'),('drums',D+'stems_raw/htdemucs/song/drums.wav'),('bass',D+'stems_raw/htdemucs/song/bass.wav'),('other',D+'stems_raw/htdemucs/song/other.wav'),('vocals',D+'stems_raw/htdemucs/song/vocals.wav')):
    e,sr,x=env(p); T=len(x)/sr; t=np.arange(len(e))*0.01
    nz=np.where(e>-90)[0]; last=t[nz[-1]] if len(nz) else None
    a60=np.where(e>-60)[0]; 
    print(nm,'dur %.2f'%T,'last >-90dB at %.2f'%last,'last >-60dB at %.2f'%t[a60[-1]],'level there %.1f'%e[a60[-1]])
    if nm=='mix':
        m=(t>=T-3.5)&(t<T-2.6)
        print(' mix 10ms env every 100 ms 3:53-3:57:',[ (round(t[i],2),round(e[i],1)) for i in range(int((T-6.5)*100),int((T-2.4)*100),20)][:30])
        # peaks in last 3 s before last sound
        seg=e[int((last-3)*100):int(last*100)+1]; pk,_=ss.find_peaks(seg,prominence=6)
        print(' peaks (prom>6 dB) in 3 s before last sound:',[(round(last-3+i*0.01,2),round(seg[i],1)) for i in pk])
        # sample peak and true-ish
        print(' sample peak dBFS %.2f'%(20*np.log10(abs(x).max())))
