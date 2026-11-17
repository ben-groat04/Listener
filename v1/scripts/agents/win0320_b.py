import numpy as np, librosa, json
D='/home/user/Listener/v1/data/t_cshells_cshore/'
sr=22050
def db(x): return 20*np.log10(np.maximum(x,1e-9))
L=lambda p:librosa.load(p,sr=sr,mono=True)[0]
y=L(D+'audio/song.wav');dr=L(D+'stems_raw/htdemucs/song/drums.wav');ba=L(D+'stems_raw/htdemucs/song/bass.wav');vo=L(D+'stems_raw/htdemucs/song/vocals.wav');ot=L(D+'stems_raw/htdemucs/song/other.wav')
h=int(.01*sr)
def env(x): return db(np.sqrt(np.convolve(x**2,np.ones(h)/h,'same'))[::h])
# 1s rms table 316..344 all stems
print('t mix voc drm bas oth')
for a in range(318,345):
    f=lambda x:round(float(db(np.sqrt(np.mean(x[a*sr:(a+1)*sr]**2)))),0)
    print(a,f(y),f(vo),f(dr),f(ba),f(ot))
# last audible sound & end
e=env(y);t=np.arange(len(e))*.01
print('last env>-90:',t[np.where(e>-90)[0][-1]],' first digital zero(<-150):',t[np.where(e>-150)[0][0]] if (e>-150).any() else None)
nz=np.where(np.abs(y)>1e-6)[0];print('last sample >1e-6:',nz[-1]/sr)
print('len',len(y)/sr)
# final hits peaks in env 343-344
m=(t>342)&(t<344);ee=e[m];tt=t[m]
from scipy.signal import find_peaks
pk,_=find_peaks(ee,prominence=3);print('peaks 342-344:',[(round(tt[i],2),round(ee[i],1)) for i in pk])
# drums onset 318-324
oe=librosa.onset.onset_strength(y=dr[316*sr:326*sr],sr=sr);on=librosa.onset.onset_detect(onset_envelope=oe,sr=sr,units='time')+316;print('drum onsets',np.round(on,2))
bt=json.load(open(D+'audio_features/beat_times.json'));bt=np.array(bt if isinstance(bt,list) else list(bt.values())[0]);b=bt[(bt>316)&(bt<345)];print('beats',np.round(b,2),'ioi',np.round(np.diff(b),3))
# low-band kick onsets in drums (<150Hz) 300-322
from scipy.signal import butter,sosfilt
sos=butter(4,150,'low',fs=sr,output='sos');k=sosfilt(sos,dr[300*sr:322*sr]);oe=librosa.onset.onset_strength(y=k,sr=sr,hop_length=128);on=librosa.onset.onset_detect(onset_envelope=oe,sr=sr,hop_length=128,units='time',delta=0.3)+300
print('kick-ish onsets',np.round(on,2));print('IOI median',np.median(np.diff(on)));
# centroid & HF share, stereo
for a,b2 in [(320,330),(332,336),(337,340),(341,343)]:
    s=y[a*sr:b2*sr];S=np.abs(np.fft.rfft(s))**2;f=np.fft.rfftfreq(len(s),1/sr)
    print(a,b2,'centroid',round((S*f).sum()/S.sum()),'>5k %',round(100*S[f>5000].sum()/S.sum(),2),'<200Hz %',round(100*S[f<200].sum()/S.sum(),1))
# loop regularity: chroma self-similarity at 1 bar lag
C=librosa.feature.chroma_cqt(y=y[318*sr:332*sr],sr=sr,hop_length=2048);
print('chroma frames/s',sr/2048)
# peak
yy,_=librosa.load(D+'audio/song.wav',sr=None,mono=False);print('native sr',_,'shape',yy.shape,'peak',db(np.abs(yy).max()),'peak in 316-344',db(np.abs(yy[:,316*_:344*_]).max()))
