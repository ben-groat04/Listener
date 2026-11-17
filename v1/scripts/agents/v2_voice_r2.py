import numpy as np, librosa
D='/home/user/Listener/v1/data/video2/stems_raw/htdemucs/song/'
sr=22050
v,_=librosa.load(D+'vocals.wav',sr=sr,mono=True)
d,_=librosa.load(D+'drums.wav',sr=sr,mono=True)
hop=int(0.05*sr)
rms=librosa.feature.rms(y=v,frame_length=2048,hop_length=hop)[0]
db=20*np.log10(rms+1e-9)
t=np.arange(len(db))*0.05
def bursts(a,b,thr=-52):
    m=(db>thr)&(t>=a)&(t<b); out=[];s=None
    for i,x in enumerate(m):
        if x and s is None:s=i
        if not x and s is not None:
            if (i-s)*0.05>=0.3:out.append((t[s],t[i]))
            s=None
    return out
G0,P=0.133,0.49995
def beatpos(x): # beats since grid, mod 4
    return (((x-G0)/P)%4)
print('narration phrases -> beat-in-bar (grid, bar=4 beats; 0=beat1)')
for a,b in bursts(40,160)+bursts(145,157):
    print('%.1f-%.1f start %.2f end %.2f'%(a,b,beatpos(a),beatpos(b)))
print('late bursts 3:24-5:00')
for a,b in bursts(204,300):
    seg=v[int(a*sr):int(b*sr)]
    f0,vf,vp=librosa.pyin(seg,fmin=70,fmax=900,sr=sr,frame_length=2048)
    f=f0[~np.isnan(f0)]
    S=np.abs(librosa.stft(seg,n_fft=2048))
    fr=librosa.fft_frequencies(sr=sr,n_fft=2048)
    cs=S.sum(1);cum=np.cumsum(cs)/cs.sum();ro=fr[np.searchsorted(cum,0.95)]
    cen=(fr*cs).sum()/cs.sum()
    mn=librosa.hz_to_note(np.median(f)) if len(f)>3 else '-'
    print('%d:%04.1f dur %.1f beat %.2f dB %.0f f0med %s (voiced %d/%d) roll95 %d cen %d'%(a//60,a%60,b-a,beatpos(a),db[(t>=a)&(t<b)].max(),mn,len(f),len(f0),ro,cen))
# narration comparison
for a,b in [(64.5,70.5),(145.4,148.5),(149,152)]:
    seg=v[int(a*sr):int(b*sr)];S=np.abs(librosa.stft(seg,n_fft=2048));fr=librosa.fft_frequencies(sr=sr,n_fft=2048)
    cs=S.sum(1);cum=np.cumsum(cs)/cs.sum();print('narr',a,'roll95',fr[np.searchsorted(cum,0.95)],'cen',(fr*cs).sum()/cs.sum())
# 4:38.5 burst: drum-stem vs vocal-stem onset
for a,b in [(277.5,279.5)]:
    seg=slice(int(a*sr),int(b*sr))
    print('4:38 vocals rms dB',20*np.log10(np.sqrt((v[seg]**2).mean())),'drums',20*np.log10(np.sqrt((d[seg]**2).mean())))
    ev=np.abs(v[seg]);i=np.argmax(ev);print('peak at',a+i/sr)
    S=np.abs(librosa.stft(v[seg],n_fft=2048));fr=librosa.fft_frequencies(sr=sr,n_fft=2048);cs=S.sum(1);print('centroid',(fr*cs).sum()/cs.sum())
