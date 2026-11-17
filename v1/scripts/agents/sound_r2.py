import numpy as np, librosa, sys
D='/home/user/Listener/v1/data/t_birdwalk/stems_raw/htdemucs/song/'
def ld(n): return librosa.load(D+n+'.wav',sr=22050,mono=False)[0]
st={n:ld(n) for n in ['vocals','drums','bass','other']}
mix=sum(st.values())
def corr(x,a,b):
    s=x[:,int(a*22050):int(b*22050)]; 
    if s.std()==0: return None
    return np.corrcoef(s[0],s[1])[0,1], np.sqrt((((s[0]-s[1])/2)**2).mean())/ (np.sqrt((((s[0]+s[1])/2)**2).mean())+1e-9)
segs=[(2,9),(14,40),(50,58),(62,80),(84,92),(95,120),(135,143),(152,158),(165,170),(178,186)]
for a,b in segs:
    print(a,b,' '.join(f"{n}:{(lambda r: 'na' if r is None else '%.2f/%.2f'%r)(corr(x,a,b))}" for n,x in list(st.items())+[('mix',mix)]))
# other-stem loop test: correlate mel patterns of 1:23-1:33 vs 1:35..; vocal hook repetition: 2:11-2:23 vs 2:23-2:35 etc.
def mel(x,a,b):
    m=x.mean(0)[int(a*22050):int(b*22050)]
    return librosa.power_to_db(librosa.feature.melspectrogram(y=m,sr=22050,n_mels=64,hop_length=512)).flatten()
def sim(n,a,b,c,d):
    L=min(int((b-a)*22050/512),int((d-c)*22050/512))*64
    x=mel(st[n],a,b)[:L];y=mel(st[n],c,d)[:L]
    return np.corrcoef(x,y)[0,1]
for n,a,b,c,d in [('vocals',48,58,120,130),('vocals',48,58,60,70),('other',48,58,120,130),('drums',48,58,120,130),('vocals',131,143,143,155),('vocals',131,143,155,167),('other',62,74,74,86),('vocals',62,74,74,86)]:
    print('sim',n,a,c,'%.2f'%sim(n,a,b,c,d))
# bass note analysis: onset, pitch glide
b=st['bass'].mean(0); sr=22050
f0,vf,vp=librosa.pyin(b[int(62*sr):int(80*sr)],fmin=30,fmax=120,sr=sr,frame_length=4096,hop_length=256)
on=librosa.onset.onset_detect(y=b[int(62*sr):int(80*sr)],sr=sr,hop_length=256,units='frames',backtrack=False)
print('onsets',len(on))
gl=[]
for o in on[:40]:
    seg=f0[o:o+12]
    if np.sum(~np.isnan(seg))>=6:
        v=seg[~np.isnan(seg)]; gl.append((v[0],v[-1]))
g=np.array(gl); print('glide first/last Hz median',np.median(g,0),'n',len(g),'frac falling',np.mean(g[:,0]>g[:,1]+0.5))
# decay length and 2nd harmonic ratio
S=np.abs(librosa.stft(b[int(62*sr):int(80*sr)],n_fft=4096,hop_length=256))
fr=librosa.fft_frequencies(sr=sr,n_fft=4096)
i1=(fr>45)&(fr<70); i2=(fr>100)&(fr<125); i3=(fr>150)&(fr<190)
print('H2/H1 dB',20*np.log10(S[i2].max(0).mean()/S[i1].max(0).mean()),'H3/H1',20*np.log10(S[i3].max(0).mean()/S[i1].max(0).mean()))
# other stem: spectral peaks 600-1500 Hz in 0:40-0:47 and 1:02-1:20
o=st['other'].mean(0)
for a,bb in [(40,47),(62,80),(100,120)]:
    seg=o[int(a*sr):int(bb*sr)]
    S=np.abs(librosa.stft(seg,n_fft=8192)).mean(1);fr=librosa.fft_frequencies(sr=sr,n_fft=8192)
    m=(fr>150)&(fr<3000); idx=np.argsort(S[m])[::-1]
    pk=[];
    for i in idx:
        f=fr[m][i]
        if all(abs(f-p)>20 for p in pk): pk.append(f)
        if len(pk)==8: break
    print('other peaks',a,bb,[round(p) for p in pk])
# chirps: harmonic ratio via hpss on vocals 9-12
seg=st['vocals'].mean(0)[int(9*sr):int(12*sr)]
fl=librosa.feature.spectral_flatness(y=seg)[0]; print('chirp flatness',fl.mean())
seg2=st['vocals'].mean(0)[int(24*sr):int(34*sr)]; print('speech flatness',librosa.feature.spectral_flatness(y=seg2)[0].mean())
