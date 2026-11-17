import librosa, numpy as np, json
D='/home/user/Listener/v1/data/t_birdwalk/'
y,sr=librosa.load(D+'audio/song.wav',sr=None,mono=False)
print('sr',sr,y.shape)
L,R=y; m=(L+R)/2; S=(L-R)/2
mono=m
H,P=librosa.effects.hpss(mono)
hop=sr  # 1s
def per_s(x):
    n=len(x)//sr; return np.array([np.sqrt(np.mean(x[i*sr:(i+1)*sr]**2)) for i in range(n)])
Hs,Ps,Ms,Ss=per_s(H),per_s(P),per_s(m),per_s(S)
stft=np.abs(librosa.stft(mono,n_fft=4096,hop_length=sr//2))
fr=librosa.fft_frequencies(sr=sr,n_fft=4096)
bands={'sub<60':(20,60),'bass60-200':(60,200),'lowmid200-800':(200,800),'mid800-3k':(800,3000),'hi3-6k':(3000,6000),'air>6k':(6000,sr/2)}
be={k:np.sqrt((stft[(fr>=a)&(fr<b)]**2).sum(0)) for k,(a,b) in bands.items()}
secs=[(0,12.86),(12.86,47.46),(47.46,59.79),(59.79,83.43),(83.43,93.79),(93.79,119.47),(119.47,131.96),(131.96,143.08),(143.08,156.41),(156.41,188.15)]
out=[]
for a,b in secs:
    i,j=int(a),int(b)
    r={'start':a,'end':b,'perc_over_harm':float(Ps[i:j].mean()/Hs[i:j].mean()),'side_over_mid':float(Ss[i:j].mean()/Ms[i:j].mean()),'rms':float(Ms[i:j].mean())}
    ia,ib=int(a*2),int(b*2)
    tot=sum(be[k][ia:ib].mean() for k in be)
    for k in be: r[k]=round(float(be[k][ia:ib].mean()/tot),3)
    out.append(r); print(r)
# sub-bass presence per second (30-70Hz)
sub=be['sub<60']
# 1-s sub energy
subs=np.array([sub[2*i:2*i+2].mean() for i in range(len(sub)//2)])
on=subs>0.5*subs.max()
ch=[i for i in range(1,len(on)) if on[i]!=on[i-1]]
print('sub-bass on/off changes at s',ch)
# tempo
oenv=librosa.onset.onset_strength(y=mono,sr=sr)
tg=librosa.feature.tempogram(onset_envelope=oenv,sr=sr)
ac=librosa.autocorrelate(oenv); 
tempos=librosa.tempo_frequencies(len(ac),sr=sr)
for lo,hi in [(60,90),(70,80),(140,160)]:
    mk=(tempos>=lo)&(tempos<=hi); print(lo,hi,tempos[mk][np.argmax(ac[mk])])
# drums stem onset rate / beat from drums.mp3
dr,_=librosa.load(D+'stems/drums.mp3',sr=22050)
tp,bt=librosa.beat.beat_track(y=dr,sr=22050); print('drums tempo',tp)
# silences: frames with very low rms
rms=librosa.feature.rms(y=mono,hop_length=512)[0]; t=librosa.times_like(rms,sr=sr,hop_length=512)
q=np.where(rms<0.01)[0]; print('quiet frames sec',t[q][:5],len(q))
# dynamics
db=20*np.log10(Ms+1e-6); print('dynamic range p95-p5 dB',np.percentile(db,95)-np.percentile(db,5))
# chroma per section key
for a,b in secs:
    c=librosa.feature.chroma_cqt(y=m[int(a*sr):int(b*sr)],sr=sr).mean(1)
    print(a,b,np.array(['C','C#','D','D#','E','F','F#','G','G#','A','A#','B'])[np.argsort(c)[::-1][:5]])
# stereo corr
print('LR corr',np.corrcoef(L,R)[0,1])
json.dump(out,open(D+'audio_features/extra/birdwalk_sections_measure.json','w'),indent=1)
np.save(D+'audio_features/extra/sub_per_s.npy',subs)
