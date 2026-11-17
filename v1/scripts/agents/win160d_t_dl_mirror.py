import numpy as np, librosa, json, soundfile as sf
D='/home/user/Listener/v1/data/t_dl_mirror/'
T0,T1=160,180
p=json.load(open(D+'music_views/per_second_levels.json'))[T0:T1]
b=np.array([r['bass'] for r in p]);m=np.array([r['dbfs'] for r in p]);v=np.array([r['vocals'] for r in p]);dr=np.array([r['drums'] for r in p]);o=np.array([r['other'] for r in p])
print('bass<-50 secs',[r['t'] for r in p if r['bass']<-50],'mix mean there',m[b<-50].mean().round(2),'with bass',m[b>-30].mean().round(2),'n',(b<-50).sum(),(b>-30).sum())
print('mix dB range',m.min(),m.max(),'mean',m.mean().round(1),'vocals mean',v.mean().round(1),'drums',dr.mean().round(1),'other',o.mean().round(1),'bass(on)',b[b>-30].mean().round(1))
print('vocal-minus-drum', (v-dr).mean().round(1))
ln=[x for x in json.load(open(D+'music_views/lead_notes.json')) if T0<=x['start']<T1]
from collections import Counter
print(len(ln),Counter(x['note'] for x in ln).most_common(8))
mid=[librosa.note_to_midi(x['note'].replace('♯','#')) for x in ln];print('lead midi min/max/median',min(mid),max(mid),np.median(mid))
# vocals pitch: pyin on vocal stem
y,fs=sf.read(D+'stems_raw/htdemucs/song/vocals.wav');y=y.mean(1)[T0*fs:T1*fs]
y=librosa.resample(y,orig_sr=fs,target_sr=22050)
f0,vf,vp=librosa.pyin(y,fmin=80,fmax=500,sr=22050,frame_length=2048,hop_length=512)
print('vocal voiced frac',np.nanmean(vf),'f0 median',np.nanmedian(f0),'p10/p90',np.nanpercentile(f0,[10,90]))
# silences in vocals within window (frames below -40dB)
e=20*np.log10(np.sqrt(np.convolve(y**2,np.ones(2205)/2205,'same'))+1e-9)
q=e<-35;print('vocal frames <-35 dB frac',q.mean().round(3))
ch=np.flatnonzero(np.diff(q.astype(int)))/22050+T0
print('vocal gaps edges',np.round(ch,2).tolist()[:30])
# band-limit: mix and stems rolloff at native
mix,fs=sf.read(D+'audio/song.wav');mix=mix.mean(1)[T0*fs:T1*fs]
S=np.abs(librosa.stft(mix,n_fft=4096))**2;f=librosa.fft_frequencies(sr=fs,n_fft=4096)
c=np.cumsum(S.sum(1))/S.sum();print('mix 95% rolloff',f[np.searchsorted(c,0.95)],'99%',f[np.searchsorted(c,0.99)],'energy>10k dB rel',10*np.log10(S[f>10000].sum()/S.sum()),'>16k',10*np.log10(S[f>16000].sum()/S.sum()))
for k in ['other','vocals','drums']:
    z,_=sf.read(D+f'stems_raw/htdemucs/song/{k}.wav');z=z.mean(1)[T0*fs:T1*fs]
    S=np.abs(librosa.stft(z,n_fft=4096))**2;c=np.cumsum(S.sum(1))/S.sum();print(k,'95%',f[np.searchsorted(c,0.95)],'99%',f[np.searchsorted(c,0.99)],'>10k dB',10*np.log10(S[f>10000].sum()/S.sum()))
# other: chroma dominance
z,_=sf.read(D+'stems_raw/htdemucs/song/other.wav');z=z.mean(1)[T0*fs:T1*fs]
ch_=librosa.feature.chroma_cqt(y=librosa.resample(z,orig_sr=fs,target_sr=22050),sr=22050).mean(1)
print('other chroma C..B',np.round(ch_/ch_.max(),2).tolist())
# 'other' strong partials low
S=np.abs(librosa.stft(z,n_fft=8192)).mean(1);f2=librosa.fft_frequencies(sr=fs,n_fft=8192)
idx=np.argsort(S[(f2>60)&(f2<1200)])[-12:];print('other top low peaks Hz',np.sort(np.round(f2[(f2>60)&(f2<1200)][idx],0)).tolist())
