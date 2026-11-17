import numpy as np,soundfile as sf,json,scipy.signal as ss
D='/home/user/Listener/v1/data/t_dl_mirror/';S=D+'stems_raw/htdemucs/song/'
sr=44100
d,_=sf.read(S+'drums.wav',start=80*sr,stop=100*sr);d=d.mean(1)
k=ss.sosfiltfilt(ss.butter(4,[40,120],'band',fs=sr,output='sos'),d)
env=np.abs(ss.hilbert(k));env=ss.sosfiltfilt(ss.butter(2,20,'low',fs=sr,output='sos'),env)
pk,_=ss.find_peaks(env,height=0.2*env.max(),prominence=0.1*env.max(),distance=int(0.12*sr))
kt=pk/sr+80;print(len(kt),np.round(kt,2).tolist())
bt=np.array(json.load(open(D+'audio_features/beat_times.json')));bt=bt[(bt>=79)&(bt<=101)]
off=np.array([(t-bt[np.argmin(abs(bt-t))])*1000 for t in kt]);print('offset to nearest beat: median',np.median(off),'std',off.std(),'frac within 40ms',np.mean(abs(off)<40))
q=0.627/4
dev=np.array([(((t-bt[0])/q+.5)%1-.5)*q*1000 for t in kt]);print('16th-grid dev std ms',dev.std(),'mean abs',abs(dev).mean())
ioi=np.diff(kt);h,e=np.histogram(ioi/0.627,bins=[0,.2,.35,.6,.9,1.1,1.4,1.7,2.1,3]);print(h,e)
print('IOI',np.round(ioi,2).tolist())
