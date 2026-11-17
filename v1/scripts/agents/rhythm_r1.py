import numpy as np, librosa, json, soundfile as sf
from scipy.signal import butter, sosfilt, find_peaks
D='/home/user/Listener/v1/data/t_cshells_cshore/'
sr=22050
def ld(p):
    y,s=sf.read(p); 
    if y.ndim>1:y=y.mean(1)
    return librosa.resample(y,orig_sr=s,target_sr=sr)
dr=ld(D+'stems_raw/htdemucs/song/drums.wav'); bs=ld(D+'stems_raw/htdemucs/song/bass.wav'); mx=ld(D+'audio/song.wav')
beats=np.array(json.load(open(D+'audio_features/beat_times.json')))
if beats.ndim>1: beats=beats[:,0]
print('beats',beats[:3],len(beats),'median IOI',np.median(np.diff(beats)),'bpm',60/np.median(np.diff(beats)))
ib=np.diff(beats); print('IOI pct',np.percentile(ib,[1,10,50,90,99]))
# tempo curve from tracker, 30s
for s in range(0,360,30):
    m=(beats>=s)&(beats<s+30)
    if m.sum()>3: print(s, round(60/np.median(np.diff(beats[m])),1), m.sum())
# kick band onsets
sos=butter(4,[40,120],'band',fs=sr,output='sos')
k=sosfilt(sos,dr); env=np.abs(k); 
hop=110 # 5ms
e=librosa.feature.rms(y=k,frame_length=441,hop_length=hop)[0]
t=np.arange(len(e))*hop/sr
d=np.maximum(0,np.diff(np.log10(e+1e-6)))
# onset env from full drums
oe=librosa.onset.onset_strength(y=dr,sr=sr,hop_length=hop)
on=librosa.onset.onset_detect(onset_envelope=oe,sr=sr,hop_length=hop,units='time',delta=0.1)
print('drum onsets total',len(on))
np.save('/tmp/on.npy',on)
# per-section density and beat-phase test with 10ms bins
secs=[(11,24),(24,40),(40,60),(60,80),(80,100),(100,120),(120,160),(160,200),(200,240),(240,300),(300,320)]
bt=beats
for a,b in secs:
    o=on[(on>=a)&(on<b)]
    if len(o)<8: print(a,b,'few',len(o));continue
    # offset from nearest beat in fraction of beat
    idx=np.searchsorted(bt,o).clip(1,len(bt)-1)
    prev=bt[idx-1];nxt=bt[idx];per=nxt-prev
    ph=(o-prev)/per
    h,_=np.histogram(ph,bins=8,range=(0,1))
    print(a,b,'n',len(o),'rate/s',round(len(o)/(b-a),2),'phase hist(8)',h.tolist())
# bass onsets
oeb=librosa.onset.onset_strength(y=bs,sr=sr,hop_length=hop)
ob=librosa.onset.onset_detect(onset_envelope=oeb,sr=sr,hop_length=hop,units='time',delta=0.1)
for a,b in [(80,100),(100,120),(140,160),(180,200),(220,240),(260,280)]:
    o=ob[(ob>=a)&(ob<b)]
    if len(o)>5: print('bass',a,b,len(o),'IOI med',np.median(np.diff(o)).round(3))
# drum presence per 10 s (rms dB)
for s in range(0,360,10):
    seg=dr[s*sr:(s+10)*sr]; sb=bs[s*sr:(s+10)*sr]
    print(s,'drum dB',round(20*np.log10(np.sqrt((seg**2).mean())+1e-9),1),'bass',round(20*np.log10(np.sqrt((sb**2).mean())+1e-9),1))
# 4s block cycle: mix envelope autocorr 40-200
env=librosa.feature.rms(y=mx,frame_length=2205,hop_length=1102)[0]; te=1102/sr
for a,b in [(60,100),(100,140),(140,200),(200,300)]:
    x=np.log(env[int(a/te):int(b/te)]+1e-6); x=x-x.mean()
    ac=np.correlate(x,x,'full')[len(x)-1:]; ac/=ac[0]
    lags=np.arange(len(ac))*te
    m=(lags>1.5)&(lags<10); i=np.argmax(ac*m); print('env AC',a,b,'peak lag',lags[i].round(2),ac[i].round(2))
# global tempo curve librosa
tg=librosa.beat.tempo(onset_envelope=oe,sr=sr,hop_length=hop,aggregate=None)
tt=librosa.times_like(tg,sr=sr,hop_length=hop)
for s in range(40,320,20):
    m=(tt>=s)&(tt<s+20); print('tempo est',s,np.median(tg[m]).round(1))
