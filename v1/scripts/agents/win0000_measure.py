import json,numpy as np,librosa,soundfile as sf
d='/home/user/Listener/v1/data/t_dl_mirror/'
L=json.load(open(d+'music_views/per_second_levels.json'))

c=json.load(open(d+'music_views/clap_tags.json'))

sr=22050
y,_=librosa.load(d+'audio/song.wav',sr=None,mono=False)
print('shape',y.shape)
m=y if y.ndim==1 else y
mono=y.mean(0) if y.ndim>1 else y
print('sample peak 0-20 dBFS',20*np.log10(np.abs(y[...,:int(20*44100)]).max()), 'whole',20*np.log10(np.abs(y).max()))
S={}
for n in ['drums','bass','vocals','other']:
    x,s=sf.read(d+'stems_raw/htdemucs/song/'+n+'.wav'); x=x.mean(1) if x.ndim>1 else x; S[n]=(x,s)
x,s=S['drums']
x=x[:int(25*s)]
lo=librosa.effects.preemphasis(x)
import scipy.signal as sg
sos=sg.butter(4,[40,120],'bp',fs=s,output='sos'); k=sg.sosfiltfilt(sos,x)
env=np.abs(sg.hilbert(k));
on=librosa.onset.onset_detect(y=k,sr=s,units='time',backtrack=False,delta=0.15)
on=on[on<20]
print('kick-band onsets',np.round(on,2)); ioi=np.diff(on);print('ioi',np.round(ioi,2))
# 16th-ish grid: beat times
bt=np.array(json.load(open(d+'audio_features/beat_times.json')));bt=bt[bt<21]
print('beat ioi',np.round(np.diff(bt),3),'mean',np.diff(bt).mean(), 'bpm',60/np.diff(bt).mean())
# dev of kick onsets from nearest 8th note grid at tracker bpm
per=np.diff(bt).mean()/2
g=np.arange(bt[0],21,per)
dev=[(o-g[np.abs(g-o).argmin()])*1000 for o in on]
print('kick dev from 8th grid ms',np.round(dev,0), 'std',np.std(dev))
# onset env of drums, whole range, strong peaks
oe=librosa.onset.onset_strength(y=x,sr=s,hop_length=256); t=librosa.times_like(oe,sr=s,hop_length=256)
pk=librosa.util.peak_pick(oe,pre_max=8,post_max=8,pre_avg=20,post_avg=20,delta=1.0,wait=10)
print('drum onsets',np.round(t[pk][t[pk]<20],2))
# band stats per second of mix
mx=mono[:20*44100]
for lab,(lo_,hi) in {'<200':(20,200),'200-2k':(200,2000),'2k-8k':(2000,8000),'8k+':(8000,20000)}.items():
    sos=sg.butter(4,[lo_,min(hi,20000)],'bp',fs=44100,output='sos');f=sg.sosfiltfilt(sos,mx)
    print(lab,[round(20*np.log10(np.sqrt((f[i*44100:(i+1)*44100]**2).mean())+1e-9),1) for i in range(0,20,2)])
# spectral rolloff
ro=librosa.feature.spectral_rolloff(y=mx,sr=44100,roll_percent=0.99);print('rolloff99 median Hz',np.median(ro))
# stereo width
if y.ndim>1:
    mid=(y[0]+y[1])/2;side=(y[0]-y[1])/2
    for a_,b_ in [(0,10),(10,20)]:
        sl=slice(a_*44100,b_*44100);print('side/mid dB',a_,20*np.log10(np.sqrt((side[sl]**2).mean())/np.sqrt((mid[sl]**2).mean())+1e-9))
# bar-repeat regularity: tempo, chroma/onset autocorr
tmp=librosa.feature.tempo(onset_envelope=oe,sr=s,hop_length=256);print('tempo',tmp)
# loop regularity: correlate drum stem 0.28-? one bar (4 beats) vs next
beat=np.diff(bt).mean();bar=4*beat
for nm in ['drums','other']:
    z=S[nm][0]
    def seg(t0):return z[int(t0*s):int((t0+bar)*s)]
    for t0 in [0.28,0.28+bar,0.28+2*bar]:
        a_=seg(t0);b_=seg(t0+bar);n=min(len(a_),len(b_))
        print(nm,'bar corr',round(t0,2),round(np.corrcoef(a_[:n],b_[:n])[0,1],3))
