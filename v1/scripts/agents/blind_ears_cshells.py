import librosa, numpy as np, json, sys
D='/home/user/Listener/v1/data/t_cshells_cshore/'
y,sr=librosa.load(D+'audio/song.wav',sr=22050,mono=False)
L,R=y; m=(L+R)/2; S=(L-R)/2
n=len(m)/sr
out={}
H,P=librosa.effects.hpss(m)
Sx=np.abs(librosa.stft(m,n_fft=2048,hop_length=512))
f=librosa.fft_frequencies(sr=sr,n_fft=2048)
bands={'sub<80':(20,80),'bass80-250':(80,250),'low-mid250-800':(250,800),'mid800-3k':(800,3000),'pres3-6k':(3000,6000),'air>6k':(6000,11000)}
fr=sr/512
T=int(n//10+1)
rows=[]
secs=[(0,24.9),(24.9,40.7),(40.7,67.4),(67.4,113.4),(113.4,189.3),(189.3,245.2),(245.2,330),(330,361)]
# per-10 s windows
for i in range(T):
    a,b=i*10,min((i+1)*10,n)
    sl=slice(int(a*fr),int(b*fr))
    if sl.start>=Sx.shape[1]:break
    e=(Sx[:,sl]**2).sum()+1e-12
    bd={k:round(float(10*np.log10((Sx[(f>=lo)&(f<hi),sl]**2).sum()+1e-12)),1) for k,(lo,hi) in bands.items()}
    hs=slice(int(a*sr),int(b*sr))
    hp=float((P[hs]**2).sum()/((P[hs]**2).sum()+(H[hs]**2).sum()+1e-12))
    ss=float((S[hs]**2).sum()/((m[hs]**2).sum()+(S[hs]**2).sum()+1e-12))
    rms=float(np.sqrt((m[hs]**2).mean()))
    on=librosa.onset.onset_strength(y=m[hs],sr=sr)
    rows.append(dict(t=a,rms=round(rms,4),perc_share=round(hp,2),side_share=round(ss,3),onset_mean=round(float(on.mean()),2),bands_db=bd,
      crest=round(float(np.abs(m[hs]).max()/(rms+1e-9)),1)))
out['windows10s']=rows
# tempo with different priors
oenv=librosa.onset.onset_strength(y=m,sr=sr)
for sec,(a,b) in {'full':(0,n),'80-190':(80,190),'190-330':(190,330)}.items():
    o=oenv[int(a*fr):int(b*fr)]
    tg=librosa.feature.tempogram(onset_envelope=o,sr=sr,hop_length=512)
    ac=tg.mean(1); bpm=librosa.tempo_frequencies(tg.shape[0],sr=sr,hop_length=512)
    idx=np.argsort(ac[1:])[::-1][:30]+1
    cand=[]
    for k in idx:
        if 50<bpm[k]<260 and all(abs(bpm[k]-c[0])>4 for c in cand): cand.append((round(float(bpm[k]),1),round(float(ac[k]),3)))
        if len(cand)>=5:break
    out['tempo_'+sec]=cand
# silences
rm=librosa.feature.rms(y=m,hop_length=512)[0]
db=20*np.log10(rm+1e-6)
sil=[];st=None
for i,v in enumerate(db):
    t=i/fr
    if v<-60 and st is None: st=t
    if v>=-60 and st is not None:
        if t-st>0.5: sil.append((round(st,2),round(t,2)))
        st=None
if st is not None: sil.append((round(st,2),round(n,2)))
out['silences_below_-60dB']=sil
# 1s loudness diffs: biggest jumps
r1=[float(np.sqrt((m[int(t*sr):int((t+1)*sr)]**2).mean())) for t in range(int(n))]
d=np.diff(20*np.log10(np.array(r1)+1e-5))
jumps=sorted([(round(float(d[i]),1),i+1) for i in range(len(d)) if r1[i]>0.003],key=lambda x:-abs(x[0]))[:15]
out['biggest_1s_jumps_db(delta,t)']=jumps
# chroma per section for tonic
ch=librosa.feature.chroma_cqt(y=H,sr=sr)
names=['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
for a,b in secs:
    c=ch[:,int(a*fr):int(b*fr)].mean(1);c/=c.sum()+1e-9
    top=np.argsort(c)[::-1][:5]
    out.setdefault('chroma_top',[]).append(dict(sec=[a,b],top=[(names[k],round(float(c[k]),3)) for k in top]))
# stems share per section
st=json.load(open(D+'stems/stem_rms_per_second.json'))
for a,b in secs:
    sh={k:round(float(np.mean(st[k][int(a):int(b)])),4) for k in st}
    out.setdefault('stem_mean_rms',[]).append(dict(sec=[a,b],**sh))
# kick/low-end periodicity: sub-bass onset
json.dump(out,open(D+'audio_features/extra/blind_ears.json','w'),indent=1)
print(json.dumps(out)[:200])
