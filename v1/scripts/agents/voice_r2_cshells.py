import numpy as np, librosa, json
D='/home/user/Listener/v1/data/t_cshells_cshore/'
sr=22050
v,_=librosa.load(D+'stems_raw/htdemucs/song/vocals.wav',sr=sr,mono=True)
o,_=librosa.load(D+'stems_raw/htdemucs/song/other.wav',sr=sr,mono=True)
m,_=librosa.load(D+'audio/song.wav',sr=sr,mono=True)
ev={'2:21.5-2:26':(141.5,146),'3:44-3:49.2':(224,229.2),'4:27-4:31':(267,271),'4:56-4:58':(296,298),'5:12':(312,313),'5:30.5-5:42.8':(330.5,342.8),'5:20-5:28 (music ref)':(320,328),'2:30-2:40 (music ref)':(150,160)}
def st(x,a,b):
    s=x[int(a*sr):int(b*sr)]
    S=np.abs(librosa.stft(s,n_fft=2048,hop_length=512))
    f=librosa.fft_frequencies(sr=sr,n_fft=2048)
    p=S.mean(1); c=np.cumsum(p**2)/np.sum(p**2)
    r85=f[np.searchsorted(c,.85)];r95=f[np.searchsorted(c,.95)]
    cen=(f*p).sum()/p.sum()
    e=np.sqrt((S**2).mean(0)); 
    env=librosa.feature.rms(y=s,frame_length=1024,hop_length=256)[0]
    en=env-env.mean()
    ac=np.fft.rfft(en,2048);fr=np.fft.rfftfreq(2048,256/sr);pw=np.abs(ac)**2
    sel=(fr>1)&(fr<12); mod=fr[sel][pw[sel].argmax()]
    band=lambda lo,hi: 10*np.log10((p[(f>=lo)&(f<hi)]**2).sum()+1e-12)
    tot=10*np.log10((p**2).sum()+1e-12)
    return dict(cen=round(cen),r85=round(r85),r95=round(r95),rms_db=round(20*np.log10(np.sqrt((s**2).mean())+1e-9),1),mod_hz=round(mod,1),
      b300_3k_frac=round(10**((band(300,3400)-tot)/10),2),above5k_frac=round(10**((band(5000,11000)-tot)/10),3))
for k,(a,b) in ev.items():
    print(k,'V',st(v,a,b)); print('   O',st(o,a,b)); print('   M',st(m,a,b))
# LTAS correlation between events on vocal stem
f=librosa.fft_frequencies(sr=sr,n_fft=2048)
def ltas(x,a,b):
    S=np.abs(librosa.stft(x[int(a*sr):int(b*sr)],n_fft=2048,hop_length=512)).mean(1)
    edges=np.geomspace(100,8000,25);L=[]
    for i in range(24):
        L.append(20*np.log10(S[(f>=edges[i])&(f<edges[i+1])].mean()+1e-9))
    L=np.array(L);return L-L.mean()
keys=['2:21.5-2:26','3:44-3:49.2','4:27-4:31','4:56-4:58','5:12','5:30.5-5:42.8']
Ls={k:ltas(v,*ev[k]) for k in keys}
print('LTAS corr (vocals stem, 24 log bands 100-8k)')
for a in keys: print(a.ljust(14),[round(float(np.corrcoef(Ls[a],Ls[b])[0,1]),2) for b in keys])
# 4:27-4:31 fine: per 0.25 s vocal & mix level
for t in np.arange(267,271,0.5):
    s=v[int(t*sr):int((t+.5)*sr)];ms=m[int(t*sr):int((t+.5)*sr)]
    print(round(t,1),round(20*np.log10(np.sqrt((s**2).mean())+1e-9),1),round(20*np.log10(np.sqrt((ms**2).mean())+1e-9),1))
# whisper words 4:28
j=json.load(open(D+'lyrics/whisper_medium_mix_auto_transcribe.json'))
for s in j['segments']:
    if 265<s['start']<272 : print({k:s[k] for k in ('start','end','text','no_speech_prob','avg_logprob','compression_ratio') if k in s})
