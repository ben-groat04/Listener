import numpy as np,soundfile as sf,librosa,json,scipy.signal as ss
D='/home/user/Listener/v1/data/t_dl_mirror/';S=D+'stems_raw/htdemucs/song/'
x,sr=sf.read(D+'audio/song.wav',start=80*44100,stop=100*44100);m=x.mean(1)
print('samples at |x|>=0.999:',int((np.abs(x)>=0.999).sum()),'of',x.size)
f,P=ss.welch(m,sr,nperseg=8192);P=10*np.log10(P+1e-20)
for fr in [4000,6000,8000,9000,10000,11000,12000,14000]:
    print(fr,round(P[np.argmin(abs(f-fr))],1))
d,_=sf.read(S+'drums.wav',start=80*44100,stop=100*44100);d=d.mean(1)
b,a=ss.butter(4,[40/(sr/2),120/(sr/2)],'band');k=ss.filtfilt(b,a,d)
env=np.abs(ss.hilbert(k));env=ss.filtfilt(*ss.butter(2,30/(sr/2)),env)
pk,_=ss.find_peaks(env,height=0.35*env.max(),distance=int(0.15*sr))
kt=pk/sr+80
print('kick peaks',len(kt),np.round(kt,2).tolist())
bt=np.array(json.load(open(D+'audio_features/beat_times.json')));bt=bt[(bt>=79)&(bt<=101)]
off=[(t-bt[np.argmin(abs(bt-t))])*1000 for t in kt]
print('kick offset from nearest tracker beat ms: median',np.median(off),'std',np.std(off))
# on 16th grid of fixed 95.7 BPM anchored at beat
q=60/95.703125/4
ph=[((t-bt[0])/q)%1 for t in kt]
dev=[(p if p<.5 else p-1)*q*1000 for p in ph]
print('kick dev from 16th grid (95.7bpm, anchored 1st beat) ms: std',np.std(dev),'mean abs',np.mean(np.abs(dev)))
ioi=np.diff(kt);print('kick IOI (s)',np.round(ioi,2).tolist());print('IOI in beats',np.round(np.median(ioi)/0.627,2))
# drum bar loop regularity: onset env per bar
y,_=librosa.load(S+'drums.wav',sr=22050,offset=78,duration=26)
oe=librosa.onset.onset_strength(y=y,sr=22050,hop_length=256)
bf=np.array(json.load(open(D+'audio_features/beat_times.json')))
bfw=bf[(bf>=78)&(bf<104)]-78
bars=[]
for i in range(0,len(bfw)-4,4):
    a0=int(bfw[i]*22050/256);a1=int(bfw[i+4]*22050/256);seg=oe[a0:a1];seg=np.interp(np.linspace(0,len(seg)-1,64),np.arange(len(seg)),seg);bars.append(seg)
C=np.corrcoef(bars);print('drum bar-bar onset corr',np.round(np.diag(C,1),2),'start beats at',np.round(bfw[0:len(bfw)-4:4]+78,1))
# stereo of stems? mono check
for n in ['vocals','drums','bass','other']:
    s,_=sf.read(S+n+'.wav',start=80*44100,stop=90*44100);print(n,'L-R diff dB',round(20*np.log10(np.sqrt(np.mean((s[:,0]-s[:,1])**2))+1e-12),1))
