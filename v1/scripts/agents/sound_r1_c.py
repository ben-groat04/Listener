import numpy as np, soundfile as sf, scipy.signal as ss, librosa, json
D='/home/user/Listener/v1/data/t_dl_mirror/'; sr=44100
x,_=sf.read(D+'audio/song.wav'); L,R=x[:,0],x[:,1]
c=(np.abs(L)>=0.9999).astype(int); d=np.diff(np.r_[0,c,0]); st=np.nonzero(d==1)[0]; en=np.nonzero(d==-1)[0]; rl=en-st
for i in np.argsort(rl)[::-1][:6]: print('long clip run',rl[i],'at',round(st[i]/sr,2))
big=np.nonzero(rl>=10)[0]; print('runs>=10',len(big),[round(st[i]/sr,1) for i in big][:20])
# clip density per 10s first 30
for t in range(0,30,5): print(t,int(c[t*sr:(t+5)*sr].sum()),end=' | ')
print(); 
for t in range(150,180,5): print(t,int(c[t*sr:(t+5)*sr].sum()),end=' | ')
print()
di=np.nonzero(L!=R)[0]; 
print('first LR diffs',[(round(i/sr,3),round(L[i],3),round(R[i],3)) for i in di[:6]])
# mono-ness of the voice entry 10.4: 
seg=slice(int(10.3*sr),int(10.6*sr)); print('LR diff samples 10.3-10.6',(L[seg]!=R[seg]).sum())
# kick grid vs beat grid
bt=np.array(json.load(open(D+'audio_features/beat_times.json')) if True else [])
print('beats',len(bt), np.median(np.diff(bt)))
dr,_=sf.read(D+'stems_raw/htdemucs/song/drums.wav'); dr=dr.mean(1)
lo=ss.sosfilt(ss.butter(4,150,'lp',fs=sr,output='sos'),dr)
oe=librosa.onset.onset_strength(y=lo,sr=sr,hop_length=220)
on=librosa.onset.onset_detect(onset_envelope=oe,sr=sr,hop_length=220,units='time')
# distance of kick onsets to nearest beat, fraction of beat
bi=np.diff(bt).mean()
idx=np.searchsorted(bt,on)-1; ok=(idx>=0)&(idx<len(bt)-1)
ph=((on[ok]-bt[idx[ok]])/(bt[idx[ok]+1]-bt[idx[ok]]))
h,_=np.histogram(ph,bins=np.linspace(0,1,17)); print('phase hist within beat (16 bins)',h.tolist())
# stems: is there a stereo spread? 
for s in ['other','drums']:
    y,_=sf.read(D+f'stems_raw/htdemucs/song/{s}.wav'); print(s,'L-R rms dB',round(20*np.log10(np.sqrt(((y[:,0]-y[:,1])**2).mean())+1e-12),1))
# vocal brightness: sibilance band 4-8 vs 1-4 in vocals stem
v,_=sf.read(D+'stems_raw/htdemucs/song/vocals.wav'); v=v.mean(1)
f,P=ss.welch(v[40*sr:200*sr],sr,nperseg=4096)
b=lambda a,b_: 10*np.log10(P[(f>=a)&(f<b_)].sum())
print('vocal bands dB 100-300',round(b(100,300),1),'300-1k',round(b(300,1000),1),'1-4k',round(b(1000,4000),1),'4-8k',round(b(4000,8000),1))
