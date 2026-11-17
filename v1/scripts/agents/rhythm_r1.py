import numpy as np, librosa, json, scipy.signal as ss
D='/home/user/Listener/v1/data/video1/stems_raw/htdemucs/song/'
y,sr=librosa.load(D+'drums.wav',sr=22050,mono=True)
hop=256
def band_onset(y,lo,hi):
    S=np.abs(librosa.stft(y,n_fft=2048,hop_length=hop))
    f=librosa.fft_frequencies(sr=sr,n_fft=2048)
    B=S[(f>=lo)&(f<hi)].sum(0)
    o=np.maximum(0,np.diff(np.log1p(B*10),prepend=0))
    return o
fps=sr/hop
bands={'kick(40-120)':(40,120),'snare/mid(150-2500)':(150,2500),'hat(6k-11k)':(6000,11000)}
res={}
for n,(lo,hi) in bands.items():
    o=band_onset(y,lo,hi)
    # autocorr
    ac=np.correlate(o-o.mean(),o-o.mean(),'full')[len(o)-1:]
    ac/=ac[0]
    lags=np.arange(len(ac))/fps
    m=(lags>0.1)&(lags<3.5)
    pk,_=ss.find_peaks(ac[m],height=0.05)
    pl=lags[m][pk]; ph=ac[m][pk]
    top=sorted(zip(ph,pl),reverse=True)[:8]
    print(n,[(round(l,3),round(h,2)) for h,l in top])
# beat phase histogram per band relative to beat grid
bt=np.array(json.load(open('/home/user/Listener/v1/data/video1/audio_features/beat_times.json')))
print('beat median ibi',np.median(np.diff(bt)),'n',len(bt),'last',bt[-1])
for n,(lo,hi) in bands.items():
    o=band_onset(y,lo,hi)
    pk,_=ss.find_peaks(o,height=np.percentile(o,85),distance=int(0.06*fps))
    t=pk/fps
    ph=[]
    for x in t:
        i=np.searchsorted(bt,x)-1
        if 0<=i<len(bt)-1: ph.append((x-bt[i])/(bt[i+1]-bt[i]))
    h,_=np.histogram(ph,bins=16,range=(0,1))
    print(n,'phase hist (16 bins over one 78bpm beat):',h.tolist())
# bar position: group beats by 4, kick phase over 4-beat bar using beat index mod 4 (and test offsets)
o=band_onset(y,40,120); pk,_=ss.find_peaks(o,height=np.percentile(o,85),distance=int(0.06*fps)); t=pk/fps
for name,(lo,hi) in [('kick',(40,120)),('snare',(150,2500))]:
    o=band_onset(y,lo,hi); pk,_=ss.find_peaks(o,height=np.percentile(o,85),distance=int(0.06*fps)); t=pk/fps
    cnt=np.zeros((8,4))
    for x in t:
        i=np.searchsorted(bt,x)-1
        if 0<=i<len(bt)-1:
            ph=(x-bt[i])/(bt[i+1]-bt[i]); cnt[i%8,min(3,int(ph*4))]+=1
    print(name,'beat-in-8 x sixteenth\n',cnt.astype(int))
