import numpy as np, soundfile as sf, librosa, json
D='/home/user/Listener/v1/data/video1/'
x,sr=sf.read(D+'audio/song.wav'); M=x.mean(1)
print('samples >=0.999:',(np.abs(x)>=0.999).sum(),' >0.98:',(np.abs(x)>0.98).sum(), 'of',x.size)
sp=np.abs(librosa.stft(M,n_fft=8192)).mean(1);f=librosa.fft_frequencies(sr=sr,n_fft=8192)
for lo in [50,100,500,1000,2000,4000,8000,12000,15000,16000,17000,18000,19000,20000]:
    i=np.searchsorted(f,lo);print(lo,round(20*np.log10(sp[i:i+20].mean()+1e-12),1),end=' | ')
print()
# sub-bass 20-60 per sec vs bass stem; find bass drops
b,_=sf.read(D+'stems_raw/htdemucs/song/bass.wav');b=b.mean(1)
r=librosa.feature.rms(y=b,frame_length=22050,hop_length=22050)[0]
dbb=20*np.log10(r+1e-9)
on=[]; 
for t in range(len(dbb)):
    s='#' if dbb[t]>-35 else '.'
    on.append(s)
print(''.join(on))
# pitch of bass notes in gated regions & sub energy
sb=librosa.feature.rms(y=__import__('scipy.signal',fromlist=['x']).sosfilt(__import__('scipy.signal',fromlist=['x']).butter(4,[25,60],'bp',fs=sr,output='sos'),M),frame_length=22050,hop_length=22050)[0]
print('sub 25-60 dB per s:',' '.join(f'{int(v)}' for v in 20*np.log10(sb+1e-9)))
# drum decay: kick/snare tail: median decay of drum envelope after onsets
d,_=sf.read(D+'stems_raw/htdemucs/song/drums.wav');d=d.mean(1)
env=librosa.feature.rms(y=d,frame_length=512,hop_length=128)[0];de=20*np.log10(env+1e-9)
on=librosa.onset.onset_detect(y=d,sr=sr,hop_length=128,units='frames',backtrack=False)
dec=[]
for o in on[::3]:
    if o+60<len(de):
        pk=de[o:o+4].max(); seg=de[o+4:o+60]
        k=np.where(seg<pk-20)[0]; dec.append((k[0]+4)*128/sr*1000 if len(k) else np.nan)
print('drum -20dB decay ms median/p10/p90',np.nanpercentile(dec,[50,10,90]))
# onset count & hat density per section
for a,bb in [(15,66),(66,76),(88,109),(134,159),(159,188)]:
    s=d[int(a*sr):int(bb*sr)]
    hf=librosa.effects.preemphasis(s)
    Sx=np.abs(librosa.stft(s,n_fft=2048))**2;ff=librosa.fft_frequencies(sr=sr,n_fft=2048)
    print(a,bb,'drum hi(>6k)/total dB',round(10*np.log10(Sx[ff>6000].sum()/Sx.sum()),1),'low<150',round(10*np.log10(Sx[ff<150].sum()/Sx.sum()),1))
# vocal stem band-limiting + level per section
v,_=sf.read(D+'stems_raw/htdemucs/song/vocals.wav');v=v.mean(1)
lv=json.load(open(D+'music_views/per_second_levels.json'))
vd=np.array([q['vocals'] for q in lv]);act=vd>-40
print('vocal-active seconds',act.sum(),'of',len(vd))
Sv=np.abs(librosa.stft(v,n_fft=4096)).mean(1);fv=librosa.fft_frequencies(sr=sr,n_fft=4096)
for lo,hi in [(0,150),(150,300),(300,1000),(1000,3000),(3000,5000),(5000,8000),(8000,16000)]:
    print(lo,hi,round(20*np.log10(Sv[(fv>=lo)&(fv<hi)].mean()+1e-12),1),end=' | ')
print()
# dynamic: LUFS-like via pyloudnorm?
try:
    import pyloudnorm as pl; m=pl.Meter(sr);print('LUFS',m.integrated_loudness(x))
except Exception as e: print('no pyln')
w=np.array([q['width'] for q in lv]);dbf=np.array([q['dbfs'] for q in lv])
print('corr(width,dbfs)',np.corrcoef(w,dbf)[0,1]);print('dbfs pct',np.percentile(dbf,[5,50,95]))
oth=np.array([q['other'] for q in lv]);dr=np.array([q['drums'] for q in lv]);bs=np.array([q['bass'] for q in lv])
print('median stem dB v/d/b/o',np.median(vd[act]),np.median(dr),np.median(bs),np.median(oth))
print('width vs other-level corr',np.corrcoef(w,oth)[0,1],'width vs bass',np.corrcoef(w,bs)[0,1],'width vs vocals',np.corrcoef(w,vd)[0,1])
