import numpy as np,librosa,scipy.signal as ss
S='/home/user/Listener/v1/data/t_birdwalk/stems_raw/htdemucs/song/'
t0,t1=17,43
env={}
for n in ['drums','bass','vocals','other']:
    y,sr=librosa.load(S+n+'.wav',sr=22050,offset=t0,duration=t1-t0)
    h=220  # 10ms
    e=20*np.log10(np.sqrt(np.convolve(y**2,np.ones(h)/h,'same'))[::h]+1e-9)
    env[n]=e
t=np.arange(len(env['drums']))*0.01+t0
# dropouts: drum env < -50 for >0.2s
for n in env:
    low=env[n]<(-55 if n=='drums' else -60)
    segs=[];s=None
    for i,l in enumerate(low):
        if l and s is None:s=i
        if not l and s is not None:
            if (i-s)>20: segs.append((round(t[s],2),round(t[i],2)))
            s=None
    print(n,'quiet segs',segs)
# drum hits: peaks in 10ms env
d=env['drums']
pk,_=ss.find_peaks(d,height=-30,distance=15,prominence=8)
print('drum peaks',np.round(t[pk],2).tolist())
print('drum IOI',np.round(np.diff(t[pk]),2).tolist())
# bass 10ms env peaks
b=env['bass']
pk2,_=ss.find_peaks(b,distance=15,prominence=6)
print('bass peaks',np.round(t[pk2],2).tolist())
# kick in drum stem: lowband 40-120Hz
y,sr=librosa.load(S+'drums.wav',sr=22050,offset=t0,duration=t1-t0)
bb,aa=ss.butter(4,[40/(sr/2),120/(sr/2)],'band');lo=ss.filtfilt(bb,aa,y)
e=np.sqrt(np.convolve(lo**2,np.ones(220)/220,'same'))[::220]
pk3,_=ss.find_peaks(e,height=e.max()*0.25,distance=30)
k=t[pk3];print('kick(40-120Hz drum stem)',np.round(k,2).tolist());print('kick IOI',np.round(np.diff(k),2).tolist())
# mix band limit
m,sr=librosa.load('/home/user/Listener/v1/data/t_birdwalk/audio/song.wav',sr=None,offset=20,duration=20)
f,P=ss.welch(m,sr,nperseg=4096);P=10*np.log10(P+1e-15)
for lo_,hi in [(100,500),(1000,2000),(4000,5000),(5000,6000),(6000,8000),(10000,16000)]:
    print(lo_,hi,round(P[(f>=lo_)&(f<hi)].mean(),1))
# sample peak
print('peak',np.abs(m).max())
# loop regularity: autocorr of mix onset env 20-40
y2=m
oe=librosa.onset.onset_strength(y=y2,sr=sr,hop_length=512)
ac=librosa.autocorrelate(oe-oe.mean());ac/=ac[0];fr=sr/512
lags=np.arange(len(ac))/fr
for lo_,hi in [(5.5,8.5)]:
    sel=(lags>lo_)&(lags<hi);i=np.argmax(ac[sel]);print('AC peak',lags[sel][i],ac[sel][i])
sel=(lags>0.3)&(lags<2);i=np.argmax(ac[sel]);print('short AC',lags[sel][i],ac[sel][i])
