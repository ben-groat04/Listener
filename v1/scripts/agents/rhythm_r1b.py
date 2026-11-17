import numpy as np, librosa, json, scipy.signal as ss
D='/home/user/Listener/v1/data/video1/stems_raw/htdemucs/song/'
y,sr=librosa.load(D+'drums.wav',sr=22050,mono=True); hop=256; fps=sr/hop
bt=np.array(json.load(open('/home/user/Listener/v1/data/video1/audio_features/beat_times.json')))
S=np.abs(librosa.stft(y,n_fft=2048,hop_length=hop)); f=librosa.fft_frequencies(sr=sr,n_fft=2048)
def on(lo,hi):
    B=S[(f>=lo)&(f<hi)].sum(0); return np.maximum(0,np.diff(np.log1p(B*10),prepend=0))
def prof(lo,hi,t0=0,t1=999,shift=0.0):
    o=on(lo,hi); out=np.zeros(16); 
    for i in range(len(bt)-1):
        if not(t0<=bt[i]<t1): continue
        for s in range(4):
            # sample onset strength max in window around slot centre
            c=bt[i]+(bt[i+1]-bt[i])*(s/4+shift)
            a=int((c-0.04)*fps); b=int((c+0.04)*fps)
            out[(i%4)*4+s]+=o[a:b].max()
    return out
# estimate shift: lag of peak in phase hist ~ 2/16 beat after beat time -> shift
for sh in [0.0,0.125]:
    pass
for name,(lo,hi) in {'kick':(40,120),'snare':(150,2500),'snarehi(1.5-5k)':(1500,5000),'hat':(6000,11000)}.items():
    p=prof(lo,hi,shift=0.15); print(name,'16 steps over 4 beats (offset mod4 unknown):',np.round(p/p.max(),2).tolist())
# section-wise kick density per second and fill detection: onsets/sec
o=on(150,11000); pk,_=ss.find_peaks(o,height=np.percentile(o,80),distance=int(0.08*fps)); t=pk/fps
dens=np.histogram(t,bins=np.arange(0,190,10))[0]/10
print('onsets/s per 10s:',np.round(dens,1).tolist())
# tempo curve via autocorr of mixed onset in 10s windows (global 78 vs 156 test)
oenv=librosa.onset.onset_strength(y=y,sr=sr,hop_length=hop)
tg=librosa.feature.tempogram(onset_envelope=oenv,sr=sr,hop_length=hop,win_length=384)
bpms=librosa.tempo_frequencies(tg.shape[0],sr=sr,hop_length=hop)
m=(bpms>30)&(bpms<320)
avg=tg.mean(1)
idx=np.argsort(avg[m])[::-1][:6]; print('tempogram top bpm',[(round(bpms[m][i],1),round(avg[m][i],2)) for i in idx])
# beat-interval stability & beat-vs-drum-peak alignment
ib=np.diff(bt); print('IBI std',ib.std(),'min',ib.min(),'max',ib.max(), 'gaps>0.8:',[(round(bt[i],1),round(ib[i],2)) for i in range(len(ib)) if ib[i]>0.82])
