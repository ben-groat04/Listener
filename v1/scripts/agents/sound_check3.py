import numpy as np, soundfile as sf, scipy.signal as ss, librosa, json
D='/home/user/Listener/v1/data/t_cshells_cshore/'
x,sr=sf.read(D+'audio/song.wav'); m=x.mean(1)
f,P=ss.welch(m[60*sr:320*sr],sr,nperseg=16384)
d=10*np.log10(P+1e-30)
for k in range(15000,18500,250): print(k, round(d[np.argmin(abs(f-k))],1), end=' | ')
print()
st={}
for nm in ['drums','bass','other','vocals']:
    s,_=sf.read(D+f'stems_raw/htdemucs/song/{nm}.wav'); st[nm]=s
# stems stereo S/M by section
for nm,s in st.items():
    out=[]
    for a,b in [(30,40),(65,100),(130,160),(250,300)]:
        seg=s[a*sr:b*sr]; M=(seg[:,0]+seg[:,1])/2; S=(seg[:,0]-seg[:,1])/2
        out.append(round(10*np.log10((S**2).mean()/((M**2).mean()+1e-20)+1e-20),1))
    print(nm,'S/M dB at 30-40,65-100,130-160,250-300:',out)
# kick: drums <150Hz, onsets
dr=st['drums'].mean(1)
sos=ss.butter(4,[30,150],'bp',fs=sr,output='sos'); lo=ss.sosfiltfilt(sos,dr)
bt=np.array(json.load(open(D+'audio_features/beat_times.json')) if not isinstance(json.load(open(D+'audio_features/beat_times.json')),dict) else json.load(open(D+'audio_features/beat_times.json'))['beats'])
print('beats',len(bt),'median IBI',np.median(np.diff(bt)))
for a,b in [(65,100),(120,160),(190,225),(250,300)]:
    seg=lo[a*sr:b*sr]; oe=librosa.onset.onset_strength(y=seg,sr=sr,hop_length=256)
    on=librosa.onset.onset_detect(onset_envelope=oe,sr=sr,hop_length=256,units='time',delta=0.3)+a
    ioi=np.diff(on)
    # grid: fit fixed tempo to beats within window
    bb=bt[(bt>=a)&(bt<b)]
    dev=[(o-bb[np.argmin(abs(bb-o))]) for o in on]
    dev=np.array(dev)*1000
    # fixed 123.047 BPM grid with best phase
    T=60/123.046875; ph=np.linspace(0,T,200); best=min(ph,key=lambda p:np.mean(np.abs(((on-p+T/2)%T)-T/2)))
    gd=(((on-best+T/2)%T)-T/2)*1000
    print(a,b,'kicks',len(on),'IOI median',round(np.median(ioi),3),'IOI p10/p90',np.round(np.percentile(ioi,[10,90]),3),
      '| dev from tracker beat: mean',round(dev.mean(),1),'sd',round(dev.std(),1),'| fixed grid best-phase |dev| mean',round(np.abs(gd).mean(),1),'sd',round(gd.std(),1),'(T/2=%d ms)'%(T*500))
# loop regularity: the 4s hits in 60-100: compare waveform similarity of successive 4 s cycles
hits=[60.9,64.8,68.8,72.9,76.8]
# refine hit time by envelope max in +-0.3
e=np.abs(m)
def refine(t): a=int((t-0.4)*sr); return (a+np.argmax(e[a:a+int(0.8*sr)]))/sr
ht=[refine(t) for t in hits]; print('refined hits',np.round(ht,3),'diffs',np.round(np.diff(ht),3))
# cross-corr of 1.5s after each hit (mono)
segs=[m[int(t*sr):int((t+1.5)*sr)] for t in ht]
for i in range(len(segs)-1):
    c=ss.correlate(segs[i+1],segs[i],'full'); print('hit',i,i+1,'norm xcorr',round(c.max()/np.sqrt((segs[i]**2).sum()*(segs[i+1]**2).sum()),3))
# chroma/spectral cosine similarity of cycles
S=[np.abs(librosa.stft(s,n_fft=2048,hop_length=512)).mean(1) for s in segs]
print('spectral cosine',[round(float(np.dot(S[i],S[i+1])/np.linalg.norm(S[i])/np.linalg.norm(S[i+1])),3) for i in range(4)])
