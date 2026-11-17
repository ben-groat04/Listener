import librosa, numpy as np, json
P='/home/user/Listener/v1/data/video1/audio/song.wav'
y2,sr=librosa.load(P,sr=22050,mono=False); y=y2.mean(0); L,R=y2
H,Pc=librosa.effects.hpss(y)
S=np.abs(librosa.stft(y,n_fft=4096,hop_length=512)); f=librosa.fft_frequencies(sr=sr,n_fft=4096); t=librosa.times_like(S[0],sr=sr,hop_length=512)
bands={'sub25-80':(25,80),'bass80-250':(80,250),'lowmid250-800':(250,800),'mid0.8-3k':(800,3000),'pres3-6k':(3000,6000),'air6k+':(6000,11000)}
secs=[(0,10),(10,15),(15,40),(40,66),(66,76),(76,88),(88,109),(109,119),(119,134),(134,159),(159,172),(172,189)]
out={}
print('sec | rms dB | perc/harm dB | sub bass lowmid mid pres air (dB) | width corr | onset/s')
on=librosa.onset.onset_strength(y=y,sr=sr,hop_length=512)
for a,b in secs:
    m=(t>=a)&(t<b); s0,s1=int(a*sr),int(b*sr)
    rms=20*np.log10(np.sqrt((y[s0:s1]**2).mean())+1e-9)
    ph=10*np.log10((Pc[s0:s1]**2).sum()/((H[s0:s1]**2).sum()+1e-9))
    bd=[10*np.log10((S[(f>=lo)&(f<hi)][:,m]**2).sum(1).mean()+1e-9) for lo,hi in bands.values()]
    M=(L[s0:s1]+R[s0:s1])/2; Sd=(L[s0:s1]-R[s0:s1])/2
    sw=10*np.log10((Sd**2).mean()/((M**2).mean()+1e-12))
    c=np.corrcoef(L[s0:s1],R[s0:s1])[0,1]
    pk=len(librosa.onset.onset_detect(onset_envelope=on[m],sr=sr,hop_length=512))/(b-a)
    print(f'{a}-{b} | {rms:.1f} | {ph:.1f} | '+' '.join(f'{x:.0f}' for x in bd)+f' | S/M {sw:.1f}dB corr {c:.2f} | {pk:.1f}')
    out[f'{a}-{b}']=dict(rms=rms,perc_harm=ph,bands=bd,side_mid=sw,corr=c,onsets=pk)
json.dump(out,default=float,fp=open('/home/user/Listener/v1/data/video1/audio_features/extra/ears_sections.json','w'),indent=1)
# per-second rms dB, list big changes
r=librosa.feature.rms(y=y,frame_length=2048,hop_length=512)[0]; rd=20*np.log10(r+1e-6)
s1=np.array([rd[(t>=i)&(t<i+1)].mean() for i in range(188)])
print('per-sec dB:',' '.join(f'{i}:{v:.0f}' for i,v in enumerate(s1)))
print('big jumps',[(i+1,round(s1[i+1]-s1[i],1)) for i in range(187) if abs(s1[i+1]-s1[i])>4])
print('min rms windows <-35dB',[(round(float(t[i]),2)) for i in range(len(rd)) if rd[i]<-40][:20])
# tempo
for a,b in [(15,66),(88,109),(134,159),(159,188)]:
    seg=y[int(a*sr):int(b*sr)]; oe=librosa.onset.onset_strength(y=seg,sr=sr)
    tg=librosa.feature.tempogram(onset_envelope=oe,sr=sr); m=tg.mean(1); bpm=librosa.tempo_frequencies(tg.shape[0],sr=sr)
    idx=np.argsort(-m)[:200]; seen=[]
    for i in idx:
        if 50<bpm[i]<220 and all(abs(bpm[i]-s)>6 for s in seen): seen.append(bpm[i])
        if len(seen)>=4: break
    print('tempo cand',a,b,[round(float(x),1) for x in seen])
# beats from file
bt=json.load(open('/home/user/Listener/v1/data/video1/audio_features/beat_times.json'))
bt=bt if isinstance(bt,list) else bt.get('beats',bt)
bt=np.array(bt); ib=np.diff(bt); print('beat IBI median by 20s:',[(a,round(float(np.median(ib[(bt[:-1]>=a)&(bt[:-1]<a+20)])),3) if ((bt[:-1]>=a)&(bt[:-1]<a+20)).any() else None) for a in range(0,188,20)])
# chroma key per section w/ KS profiles
ch=librosa.feature.chroma_cqt(y=H,sr=sr); ct=librosa.times_like(ch,sr=sr)
maj=np.array([6.35,2.23,3.48,2.33,4.38,4.09,2.52,5.19,2.39,3.66,2.29,2.88]);mn=np.array([6.33,2.68,3.52,5.38,2.60,3.53,2.54,4.75,3.98,2.69,3.34,3.17])
N=['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
for a,b in secs:
    c=ch[:,(ct>=a)&(ct<b)].mean(1); sc=[]
    for k in range(12):
        sc.append((np.corrcoef(c,np.roll(maj,k))[0,1],N[k]+' maj'));sc.append((np.corrcoef(c,np.roll(mn,k))[0,1],N[k]+' min'))
    sc.sort(reverse=True); print('key',a,b,[(n,round(float(v),2)) for v,n in sc[:3]],'top pcs',[N[i] for i in np.argsort(-c)[:4]])
