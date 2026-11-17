import numpy as np, librosa, json
D='/home/user/Listener/v1/data/t_dl_mirror/'
sr=22050
mix=librosa.load(D+'audio/song.wav',sr=sr)[0]; dr=librosa.load(D+'stems_raw/htdemucs/song/drums.wav',sr=sr)[0]; ot=librosa.load(D+'stems_raw/htdemucs/song/other.wav',sr=sr)[0]
bt=np.array(json.load(open(D+'audio_features/beat_times.json')))
bt=bt[(bt>=220)&(bt<236)]-220
a=220*sr
for s in [0,5,10,14,15]:
    x=mix[a+int(s*sr):a+int((s+1)*sr)]; sp=np.abs(np.fft.rfft(x))**2; f=np.fft.rfftfreq(len(x),1/sr)
    print(s,'centroid',round((f*sp).sum()/sp.sum()),'>4k',round(sp[f>4000].sum()/sp.sum(),4),'>8k',round(sp[f>8000].sum()/sp.sum(),5),'<150',round(sp[f<150].sum()/sp.sum(),3))
# last hits band
x=mix[int(235.9*sr):int(236.6*sr)]; sp=np.abs(np.fft.rfft(x))**2; f=np.fft.rfftfreq(len(x),1/sr); print('last hits peak freq',f[sp.argmax()],'centroid',(f*sp).sum()/sp.sum())
# chroma sustained pad
for t0,t1 in [(223.7,225),(233.8,235.5),(235.5,236.4)]:
    c=librosa.feature.chroma_cqt(y=ot[int(t0*sr):int(t1*sr)],sr=sr).mean(1); n=['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']; print(t0,t1,[(n[i],round(c[i]/c.max(),2)) for i in np.argsort(-c)[:5]])
# bar loop corr
bl=int(round(4*np.median(np.diff(bt))*sr/512)); print('bar frames',bl,'beat bpm',60/np.median(np.diff(bt)))
for nm,x in [('mix',mix),('drums',dr),('other',ot)]:
    m=np.log(librosa.feature.melspectrogram(y=x[a:a+16*sr],sr=sr,hop_length=512)+1e-6)
    print(nm,np.round([np.corrcoef(m[:,i*bl:(i+1)*bl].ravel(),m[:,(i+1)*bl:(i+2)*bl].ravel())[0,1] for i in range(5)],3))
# drum onsets vs 16th grid (beat/4)
o=librosa.onset.onset_detect(y=dr[a:a+16*sr],sr=sr,units='time'); g=np.median(np.diff(bt))/4
ph=[(x-bt[0]+g/2)%g-g/2 for x in o]; print('drum onset dev from 16th grid ms: median abs',np.median(np.abs(ph))*1000,'p90',np.percentile(np.abs(ph),90)*1000,'grid ms',g*1000)
# kick via low band 40-100 in drums, beat grid dev
import scipy.signal as sg
k=sg.sosfilt(sg.butter(4,[35,90],'bp',fs=sr,output='sos'),dr[a:a+16*sr]); e=np.abs(sg.hilbert(k)); 
pk,_=sg.find_peaks(e,height=e.max()*0.35,distance=int(.2*sr)); pt=pk/sr; print('low-band peaks',np.round(pt,2)); print('IOI',np.round(np.diff(pt),2))
print('dev from beat grid ms',np.round([min(abs(p-bt))*1000 for p in pt]))
