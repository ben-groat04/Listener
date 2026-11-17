import numpy as np, librosa, soundfile as sf, sys, json
D='/home/user/Listener/v1/data/t_dl_mirror/'
S=D+'stems_raw/htdemucs/song/'
sr=44100
mix,_=sf.read(D+'audio/song.wav'); 
print('mix peak',np.abs(mix).max(), 'dBFS',20*np.log10(np.abs(mix).max()))
m=mix.mean(1)
st={k:sf.read(S+k+'.wav')[0].mean(1) for k in ['vocals','drums','bass','other']}
# 1. kick fundamental and decay: drums low band onsets
import scipy.signal as sg
sos=sg.butter(4,[30,150],'bandpass',fs=sr,output='sos')
kl=sg.sosfilt(sos,st['drums'])
env=np.abs(sg.hilbert(kl)); env=sg.sosfilt(sg.butter(2,30,'low',fs=sr,output='sos'),env)
pk,_=sg.find_peaks(env[30*sr:215*sr],height=np.percentile(env[30*sr:215*sr],90),distance=int(0.1*sr))
pk=pk+30*sr
print('kick peaks',len(pk))
# kick pitch: dominant freq in 60ms after peak
fr=[]
for p in pk[:400]:
    seg=kl[p:p+int(0.08*sr)]
    if len(seg)<100: continue
    F=np.abs(np.fft.rfft(seg*np.hanning(len(seg)),8192)); f=np.fft.rfftfreq(8192,1/sr)
    fr.append(f[np.argmax(F)])
print('kick dominant freq median/p10/p90',np.median(fr),np.percentile(fr,10),np.percentile(fr,90))
# kick decay: time for env to fall 20dB from peak
dec=[]
for p in pk[:300]:
    seg=env[p:p+int(0.5*sr)]
    if seg.max()<=0: continue
    db=20*np.log10(seg/seg.max()+1e-9)
    i=np.where(db<-20)[0]
    dec.append(i[0]/sr if len(i) else 0.5)
print('kick -20dB decay time median',np.median(dec))
# 2. hi-hat: band 5-8k drums onsets, IOIs
sos=sg.butter(4,[5000,7800],'bandpass',fs=sr,output='sos')
h=sg.sosfilt(sos,st['drums'])
on=librosa.onset.onset_detect(y=h,sr=sr,hop_length=64,units='time',backtrack=False)
on=on[(on>30)&(on<215)]
ioi=np.diff(on)
print('hat onsets',len(on),'per s',len(on)/185)
bins=[(0,0.06),(0.06,0.1),(0.1,0.13),(0.13,0.2),(0.2,0.3),(0.3,0.5)]
for a,b in bins: print('hat ioi',a,b,((ioi>=a)&(ioi<b)).sum())
# 3. bass: pyin pitch and note lengths
b=st['bass']
f0,vf,vp=librosa.pyin(b[40*sr:100*sr],fmin=30,fmax=200,sr=sr,frame_length=8192,hop_length=1024)
f0=f0[~np.isnan(f0)]
print('bass pyin f0 n',len(f0),'median',np.median(f0),'p10',np.percentile(f0,10),'p90',np.percentile(f0,90))
note=12*np.log2(f0/440)+69
print('bass pitch classes share:',{librosa.midi_to_note(int(k)):round(float((np.round(note)==k).mean()),3) for k in np.unique(np.round(note)) if (np.round(note)==k).mean()>0.03})
# bass note durations: 20ms RMS env > -45dB
hop=int(0.02*sr); e=np.array([np.sqrt((b[i:i+hop]**2).mean()) for i in range(0,len(b)-hop,hop)]); edb=20*np.log10(e+1e-9)
on=edb>-40
runs=[];s=None
for i,v in enumerate(on):
    if v and s is None:s=i
    if not v and s is not None:
        runs.append((s*0.02,(i-s)*0.02));s=None
r=[d for t,d in runs if 40<t<215]
print('bass runs n',len(r),'dur median',np.median(r),'p10',np.percentile(r,10),'p90',np.percentile(r,90),'max',max(r))
# bass decay within a note: avg dB trajectory first 1 s after onset
# 4. loop regularity: other stem chroma & mel corr at 4-bar lag (10.2s) and bar (2.554)
o=st['other']
M=librosa.feature.melspectrogram(y=o[:200*sr],sr=sr,n_mels=64,hop_length=441)
M=librosa.power_to_db(M); 
def lagcorr(M,lag):
    a=M[:,:-lag].ravel();bb=M[:,lag:].ravel(); return np.corrcoef(a,bb)[0,1]
for lag_s in [0.638,2.554,5.108,10.2,20.4,61]:
    print('other mel corr lag',lag_s,round(lagcorr(M,int(round(lag_s*100))),3))
Md=librosa.power_to_db(librosa.feature.melspectrogram(y=st['drums'][:200*sr],sr=sr,n_mels=64,hop_length=441))
for lag_s in [0.638,2.554,5.108,10.2,20.4]:
    print('drums mel corr lag',lag_s,round(lagcorr(Md,int(round(lag_s*100))),3))
# other-stem: spectral flux smallness (is it a static loop?) 
print('other frame-to-frame mel corr (10ms)',np.mean([np.corrcoef(M[:,i],M[:,i+10])[0,1] for i in range(1000,15000,50)]))
# 5. vocal pitch quantisation in hooks: pyin on vocals 10.5-30, 1:12-1:31
v=st['vocals']
for (a,bq) in [(10.5,30),(72,91),(194,215)]:
    f0,vf,vp=librosa.pyin(v[int(a*sr):int(bq*sr)],fmin=150,fmax=700,sr=sr,frame_length=4096,hop_length=256)
    ok=~np.isnan(f0); n=12*np.log2(f0[ok]/440)+69
    dev=(n-np.round(n))*100
    # frame-to-frame pitch change inside voiced runs
    d=np.abs(np.diff(n))
    print('hook',a,bq,'voiced frames',ok.sum(),'cents dev from 12TET std',round(dev.std(),1),'frac|dev|<15c',round((np.abs(dev)<15).mean(),2),'median frame step semitones',round(np.median(d[d<2]),3),'frac steps ==0 (<0.02)',round((d<0.02).mean(),2))
for (a,bq) in [(40,70),(100,130),(160,190)]:
    f0,vf,vp=librosa.pyin(v[int(a*sr):int(bq*sr)],fmin=100,fmax=400,sr=sr,frame_length=4096,hop_length=256)
    ok=~np.isnan(f0); n=12*np.log2(f0[ok]/440)+69
    dev=(n-np.round(n))*100
    print('verse',a,bq,'voiced',ok.sum(),'p10-p90 Hz',np.percentile(f0[ok],10),np.percentile(f0[ok],90),'cents std',round(dev.std(),1),'frac|dev|<15c',round((np.abs(dev)<15).mean(),2), 'frac in 3 semis of median',round((np.abs(n-np.median(n))<=3).mean(),2))
