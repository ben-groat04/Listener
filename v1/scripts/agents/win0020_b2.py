import librosa,numpy as np,json
D='/home/user/Listener/v1/data/t_dl_mirror/';S=D+'stems_raw/htdemucs/song/'
sr=22050
st={n:librosa.load(S+n+'.wav',sr=sr)[0] for n in ['drums','bass','vocals','other']}
mix=librosa.load(D+'audio/song.wav',sr=sr)[0]
st['mix']=mix
def lvl(y,a,b): 
    x=y[int(a*sr):int(b*sr)];return 20*np.log10(np.sqrt(np.mean(x**2))+1e-9)
for n,y in st.items():
    print(n,' '.join('%.1f:%d'%(t,round(lvl(y,t,t+.25))) for t in np.arange(23.5,25.5,.25)))
for n,y in st.items():
    print(n,' '.join('%.1f:%d'%(t,round(lvl(y,t,t+.25))) for t in np.arange(27,31,.25)))
for n,y in st.items():
    print(n,' '.join('%.1f:%d'%(t,round(lvl(y,t,t+.25))) for t in np.arange(35.5,38,.25)))
for n,y in st.items():
    print(n,' '.join('%.1f:%d'%(t,round(lvl(y,t,t+.25))) for t in np.arange(39.5,41.5,.25)))
# drum onset periodicity
d=st['drums'][int(20*sr):int(40*sr)]
oe=librosa.onset.onset_strength(y=d,sr=sr,hop_length=110)
ac=librosa.autocorrelate(oe-oe.mean());ac/=ac[0]
lag=np.arange(len(ac))*110/sr
for L in [0.157,0.3135,0.627,1.254,2.508]:
    i=np.argmin(abs(lag-L)); print('ac at',L,ac[max(0,i-2):i+3].max().round(2))
pk=np.argsort(ac[5:200])[-5:]+5;print('top lags',np.round(lag[pk],3),ac[pk].round(2))
# kick: lowband 30-100 of drums, strongest peaks
import scipy.signal as sg
b,a=sg.butter(4,[35/(sr/2),110/(sr/2)],'band');k=sg.filtfilt(b,a,d)
env=np.abs(sg.hilbert(k));env=sg.savgol_filter(env,221,2) if False else np.convolve(env,np.ones(110)/110,'same')
pk,_=sg.find_peaks(env,height=env.max()*0.35,distance=int(0.12*sr))
t=pk/sr+20;print('kick peaks',len(t),np.round(t,2).tolist())
bt=np.array(json.load(open(D+'audio_features/beat_times.json')));bt=bt[(bt>=19)&(bt<41)]
g=(t-bt[0])/(0.627/4);print('dev from 16th grid (s) mean',np.mean(abs(g-np.round(g)))*0.627/4)
print('IOI',np.round(np.diff(t),2).tolist())
