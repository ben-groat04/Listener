import librosa, numpy as np, json
D='/home/user/Listener/v1/data/video1/'
nm=['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
yo,sr=librosa.load(D+'stems_raw/htdemucs/song/other.wav',sr=22050)
yb,_=librosa.load(D+'stems_raw/htdemucs/song/bass.wav',sr=22050)
print('tuning other (semitones)',librosa.estimate_tuning(y=yo,sr=sr),'mix',librosa.estimate_tuning(y=librosa.load(D+'audio/song.wav',sr=22050)[0],sr=sr))
hop=2048
# fine pc spectrum from CQT with 3 bins/semitone, tuning-agnostic: sum over octaves
C=np.abs(librosa.cqt(yo,sr=sr,hop_length=hop,fmin=librosa.note_to_hz('C2'),n_bins=12*5*3,bins_per_octave=36))
t=librosa.frames_to_time(np.arange(C.shape[1]),sr=sr,hop_length=hop)
pc=np.zeros((12,C.shape[1]))
for b in range(C.shape[0]):
    pc[(b//3 +0)%12]+= C[b]**2 if False else 0
# bins: bin b -> semitone b/3 from C2 ; centre each semitone on bins 3k..3k+2 (middle 3k+1 is exact if tuned)
semi=np.arange(C.shape[0])//3
for s in range(C.shape[0]//3):
    pc[s%12]+=(C[3*s:3*s+3]**2).sum(0)
def rep(a,b,lab):
    m=(t>=a)&(t<b); v=pc[:,m].mean(1); v/=v.max()
    fr=(pc[5,m]>pc[6,m]).mean()
    print(f'{lab} {a}-{b}: ',' '.join(f'{nm[i]}={v[i]:.2f}' for i in np.argsort(-v)[:8]),f'| F>F# frames {fr:.2f}')
for a,b,l in [(20,40,'0:20-0:40'),(87,100,'1:27-1:40'),(169,188,'2:49-3:08'),(1,8,'0:01-0:08'),(75,87,'1:15-1:27'),(135,160,'2:15-2:40'),(120,135,'2:00-2:15'),(100,116,'1:40-1:56'),(60,75,'1:00-1:15')]:
    rep(a,b,l)
# bass freq in D sections: peak freq of bass stem spectrum
def peakf(y,a,b):
    seg=y[int(a*sr):int(b*sr)]
    S=np.abs(np.fft.rfft(seg*np.hanning(len(seg)),n=len(seg)*8)); f=np.fft.rfftfreq(len(seg)*8,1/sr)
    m=(f>28)&(f<120); return f[m][np.argmax(S[m])]
for a,b in [(45,55),(170,185),(125,128),(130,133),(145,148),(105,115)]:
    print('bass peak',a,b,round(peakf(yb,a,b),2))
# chord change timing vs bass drops
ch=json.load(open(D+'music_views/chords.json'))
rms=librosa.feature.rms(y=yb,frame_length=1024,hop_length=256)[0]; tr=librosa.times_like(rms,sr=sr,hop_length=256)
db=20*np.log10(rms+1e-9)
# drop onsets: crossing up through -40dB after being below
on=[]
for i in range(1,len(db)):
    if 118<tr[i]<160 and db[i]>-45 and db[i-1]<=-45: on.append(tr[i])
print('bass onsets',[round(x,2) for x in on])
d0=on[0] if on else 121.2
chg=[c['start'] for c in ch if c['chord']!='N' and c['start']>1]
print('n chord changes',len(chg))
for name,P in [('3.07',3.07),('6.14',6.14),('1.535',1.535),('0.767',0.767)]:
    ph=((np.array(chg)-d0)%float(P))/float(P)
    h,_=np.histogram(ph,bins=8,range=(0,1)); print('phase hist rel. first drop',name,h.tolist())
# restricted to 2:00-2:40
c2=np.array([x for x in chg if 118<x<160])
print('2:00-2:40 changes',[round(x-d0,2) for x in c2])
# G and E periodicity 20-40
for p in (7,4):
    m=(t>=20)&(t<40); x=pc[p,m]-pc[p,m].mean(); ac=np.correlate(x,x,'full')[len(x)-1:]; ac/=ac[0]
    dt=hop/sr; lags=np.arange(len(ac))*dt
    k=[(round(lags[i],2),round(ac[i],2)) for i in range(2,len(ac)-1) if ac[i]>ac[i-1] and ac[i]>ac[i+1]][:5]
    print(nm[p],'acf peaks 20-40',k)
