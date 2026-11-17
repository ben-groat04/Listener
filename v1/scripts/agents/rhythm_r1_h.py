import numpy as np, librosa, scipy.signal as ss
D='/home/user/Listener/v1/data/t_dl_mirror/'
sr=22050
dr=librosa.load(D+'stems_raw/htdemucs/song/drums.wav',sr=sr,mono=True)[0]
# for snippets of 2.5 s, search all lags 1.5..21 s ahead; report the top lag peaks (waveform xcorr normalised)
def scan(t0,L=2.5,maxlag=21):
    a=dr[int(t0*sr):int((t0+L)*sr)]
    seg=dr[int(t0*sr):int((t0+L+maxlag)*sr)]
    c=ss.fftconvolve(seg,a[::-1],'valid')
    cs=np.sqrt(np.convolve(seg**2,np.ones(len(a)),'valid'))*np.linalg.norm(a)+1e-12
    r=c/cs; lags=np.arange(len(r))/sr
    pk,_=ss.find_peaks(r,height=0.35,distance=int(0.05*sr))
    return [(round(lags[i],3),round(float(r[i]),2)) for i in pk if lags[i]>1.0][:10]
for t0 in (62,100,125,172):
    print(t0,scan(t0))
