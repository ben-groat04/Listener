import librosa,numpy as np,json
D='/home/user/Listener/v1/data/t_dl_mirror/';S=D+'stems_raw/htdemucs/song/'
sr=22050
st={n:librosa.load(S+n+'.wav',sr=sr)[0] for n in ['drums','bass','vocals','other']}
mix=librosa.load(D+'audio/song.wav',sr=sr)[0]
st['mix']=mix
def lvl(y,a,b): 
    x=y[int(a*sr):int(b*sr)];return 20*np.log10(np.sqrt(np.mean(x**2))+1e-9)
# kick: lowband 30-100 of drums, strongest peaks
import scipy.signal as sg
d=st['drums'][int(20*sr):int(40*sr)]
sos=sg.butter(4,[35/(sr/2),110/(sr/2)],'band',output='sos');k=sg.sosfiltfilt(sos,d)
env=np.abs(sg.hilbert(k));env=np.convolve(env,np.ones(110)/110,'same')
pk,_=sg.find_peaks(env,height=env.max()*0.35,distance=int(0.12*sr))
t=pk/sr+20;print('kick peaks',len(t),np.round(t,2).tolist())
bt=np.array(json.load(open(D+'audio_features/beat_times.json')));bt=bt[(bt>=19)&(bt<41)]
g=(t-bt[0])/(0.627/4);print('dev from 16th grid (s) mean',np.mean(abs(g-np.round(g)))*0.627/4)
print('IOI',np.round(np.diff(t),2).tolist())
