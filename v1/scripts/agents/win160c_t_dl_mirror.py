import numpy as np, librosa, json, soundfile as sf, scipy.signal as ss
D='/home/user/Listener/v1/data/t_dl_mirror/'
T0,T1=160,180
y,fs=sf.read(D+'audio/song.wav');w=y[T0*fs:T1*fs]
d=w[:,0]-w[:,1];print('window L-R max',np.abs(d).max(),'rms dB',20*np.log10(np.sqrt((d**2).mean())+1e-12))
bad=np.flatnonzero(np.abs(y[:,0]-y[:,1])>1e-3);print('song samples L!=R',len(bad),bad[:3]/fs if len(bad) else '')
dr,_=sf.read(D+'stems_raw/htdemucs/song/drums.wav');dr=dr.mean(1)
bt=np.array(json.load(open(D+'audio_features/beat_times.json')));bb=bt[(bt>=T0-1)&(bt<=T1+1)]
x=dr[int(T0*fs):int(T1*fs)]
grid=np.array([a+(b-a)*j/4 for a,b in zip(bb[:-1],bb[1:]) for j in range(4)])
def run(lo,hi,thr,name):
    sos=ss.butter(4,[lo,hi],'band',fs=fs,output='sos');k=ss.sosfiltfilt(sos,x)
    e=np.abs(ss.hilbert(k));e=ss.sosfiltfilt(ss.butter(2,60,'low',fs=fs,output='sos'),e)
    pk,_=ss.find_peaks(e,height=thr*e.max(),distance=int(0.08*fs),prominence=0.15*e.max())
    on=pk/fs+T0
    dev=np.array([o-grid[np.argmin(abs(grid-o))] for o in on])*1000
    ioi=np.diff(on)
    print(name,'n',len(on),'dev ms mean %.1f sd %.1f absmed %.1f'%(dev.mean(),dev.std(),np.median(abs(dev))),'IOI min/med %.3f %.3f'%(ioi.min(),np.median(ioi)))
    print(' IOI/16th:',np.round(ioi/(60/95.69/4),1).tolist())
    return on,dev
k,dk=run(35,120,0.15,'kick');print(np.round(k,2).tolist())
run(150,400,0.2,'snare/low');run(7000,16000,0.2,'hat')
# loop regularity: onset-envelope correlation bar vs bar at lag of 4 beats using mix low band
bar=4*np.median(np.diff(bb))
e=np.abs(x);e=ss.sosfiltfilt(ss.butter(2,40,'low',fs=fs,output='sos'),e)[::441]
n=int(round(bar*100));print('bar frames',n)
for lag in [n,2*n,4*n]:
    print('lag bars',lag/n,'corr',np.corrcoef(e[:-lag],e[lag:])[0,1].round(2))
