import numpy as np, soundfile as sf, librosa
D='/home/user/Listener/v1/data/t_birdwalk/stems_raw/htdemucs/song/'
def ld(n):
    y,sr=sf.read(D+n+'.wav'); return y.T,sr
V,sr=ld('vocals'); O,_=ld('other'); B,_=ld('bass')
def seg(y,a,b): return y[:,int(a*sr):int(b*sr)]
# Q1 voice: side-channel coupling vocals vs other
print("SIDE correlation vocals vs other (envelope of side RMS, 50ms frames) and sample-level")
for a,b in [(0.50*60+0,58),(135,143),(152,158),(165,170),(14,40),(95,120)]:
    v=seg(V,a,b); o=seg(O,a,b)
    sv=(v[0]-v[1]); so=(o[0]-o[1]); mv=v[0]+v[1]; mo=o[0]+o[1]
    h=int(.05*sr); n=len(sv)//h
    env=lambda x:np.sqrt((x[:n*h].reshape(n,h)**2).mean(1))+1e-12
    c_env=np.corrcoef(np.log(env(sv)),np.log(env(so)))[0,1]
    c_samp=np.corrcoef(sv,so)[0,1]
    c_mid=np.corrcoef(np.log(env(mv)),np.log(env(sv)))[0,1]
    # band-limited spectral shape of vocal side vs other side
    S=lambda x:np.abs(np.fft.rfft(x[:len(x)//4096*4096].reshape(-1,4096)*np.hanning(4096),axis=1)).mean(0)
    f=np.fft.rfftfreq(4096,1/sr)
    cs=np.corrcoef(np.log(S(sv)[(f>100)&(f<5000)]+1e-9),np.log(S(so)[(f>100)&(f<5000)]+1e-9))[0,1]
    print(f"{a:.0f}-{b:.0f}s side env corr V/O {c_env:.2f}; sample corr {c_samp:.2f}; V side-vs-mid env {c_mid:.2f}; side-spectrum corr {cs:.2f}; V side/mid rms {np.sqrt((sv**2).mean()/((mv**2).mean()+1e-12)):.2f}")
# Q harmony: stab patch before/after 0:47 -- harmonic ladder & attack/decay on other (mono)
print("STAB ladder")
m=O.mean(0)
for a,b in [(40,47),(62,80),(120,130),(165,170)]:
    x=m[int(a*sr):int(b*sr)]
    S=np.abs(librosa.stft(x,n_fft=8192,hop_length=512))
    f=librosa.fft_frequencies(sr=sr,n_fft=8192)
    mean=S.mean(1)
    lo,hi=(700,1100) if a==40 else (180,280)
    band=(f>lo)&(f<hi); f0=f[band][np.argmax(mean[band])]
    lad=[]
    for k in range(1,9):
        w=(f>k*f0*0.97)&(f<k*f0*1.03); lad.append(20*np.log10(mean[w].max()/mean[(f>f0*.97)&(f<f0*1.03)].max()+1e-12))
    print(f"{a}-{b} f0={f0:.0f} ladder dB rel f0:",[round(l) for l in lad])
    # onset envelope attack/decay around f0 band
    bs=S[(f>f0*.9)&(f<f0*1.1)].sum(0); db=20*np.log10(bs/bs.max()+1e-9)
    on=librosa.onset.onset_detect(onset_envelope=np.diff(db,prepend=db[0]).clip(0),sr=sr,hop_length=512,units='frames')
    dec=[]
    for o in on[:60]:
        seg_=db[o:o+40]
        pk=seg_.max(); i=seg_.argmax(); t=np.where(seg_[i:]<pk-15)[0]
        if len(t): dec.append(t[0]*512/sr)
    print("   onsets",len(on),"rate/s",round(len(on)/(b-a),2),"15dB decay median s",round(float(np.median(dec)),2) if dec else None, "spectral flatness",round(float(librosa.feature.spectral_flatness(y=x).mean()),4),"centroid",round(float(librosa.feature.spectral_centroid(y=x,sr=sr).mean())))
    # odd/even harmonic: square-like if 3rd strong, even weak
