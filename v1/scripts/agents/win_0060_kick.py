import numpy as np, librosa, soundfile as sf, json
D='/home/user/Listener/v1/data/t_birdwalk/stems_raw/htdemucs/song/'
def env(n,lo,hi,t0=56,t1=86):
    y,sr=sf.read(D+n+'.wav'); y=y.mean(1) if y.ndim>1 else y
    from scipy.signal import butter,sosfiltfilt
    sos=butter(4,[lo,hi],btype='band',fs=sr,output='sos'); y=sosfiltfilt(sos,y)
    h=int(sr*0.005); e=np.sqrt(np.convolve(y**2,np.ones(h)/h,'same'))[int(t0*sr):int(t1*sr)]
    return e[::h//1 if False else 1],sr
def peaks(n,lo,hi,thr_db=-12,mind=0.12):
    e,sr=env(n,lo,hi); d=20*np.log10(e+1e-9); t=np.arange(len(e))/sr+56
    from scipy.signal import find_peaks
    # onset = rise
    ds=np.convolve(e,np.ones(int(sr*0.01))/int(sr*0.01),'same')
    p,_=find_peaks(ds,height=ds.max()*0.2,distance=int(sr*mind))
    return t[p],d[p]
for n,lo,hi in [('drums',40,120),('drums',150,500),('drums',5000,12000),('bass',30,150)]:
    t,d=peaks(n,lo,hi)
    t=t[(t>=58)&(t<=84)]
    print(n,lo,hi,len(t));print(np.round(t,2).tolist())
    print(' IOI',np.round(np.diff(t),2).tolist())
