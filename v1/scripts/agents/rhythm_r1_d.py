import numpy as np, librosa, json
D='/home/user/Listener/v1/data/t_dl_mirror/'
sr=22050; hop=64; fr=sr/hop
dr,_=librosa.load(D+'stems_raw/htdemucs/song/drums.wav',sr=sr,mono=True)
oe=librosa.onset.onset_strength(y=dr,sr=sr,hop_length=hop,n_fft=1024)
# local tempo via ACF in sliding 16s windows (beat lag region 0.58-0.70 and bar-lag/4)
def acf(x):
    x=x-x.mean(); n=len(x); F=np.fft.rfft(x,2*n); a=np.fft.irfft(F*np.conj(F))[:n]; return a/a[0]
res=[]
for s in range(0,225,10):
    seg=oe[int(s*fr):int((s+20)*fr)]
    a=acf(seg); lags=np.arange(len(a))/fr
    out=[]
    for k in (1,4):
        L0=0.64*k; w=(lags>L0*0.95)&(lags<L0*1.05); i=np.argmax(np.where(w,a,-9)); y0,y1,y2=a[i-1],a[i],a[i+1]; d=0.5*(y0-y2)/(y0-2*y1+y2); out.append(60*k/((i+d)/fr))
    print(s,'beat-lag bpm %.2f bar-lag bpm %.2f'%tuple(out))
# DP beat track on drum env with start 94 and tight
tempo,bt=librosa.beat.beat_track(onset_envelope=oe,sr=sr,hop_length=hop,start_bpm=94,tightness=400,units='time')
bt=np.array(bt); ioi=np.diff(bt)
print('dp tempo',tempo,'n',len(bt),'median ioi',np.median(ioi),'bpm',60/np.median(ioi),'std ms',ioi.std()*1000)
for s in range(0,240,30):
    m=(bt[:-1]>=s)&(bt[:-1]<s+30); print(s,'bpm',round(60/np.median(ioi[m]),2),'mean ioi bpm',round(60/ioi[m].mean(),2),'std ms',round(ioi[m].std()*1000,1))
np.save('/tmp/dpbeats.npy',bt)
