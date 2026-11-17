import numpy as np, soundfile as sf, librosa, sys
D='data/t_cshells_cshore/'
names=['mix','drums','bass','other','vocals']
def load(n):
    p=D+('audio/song.wav' if n=='mix' else f'stems_raw/htdemucs/song/{n}.wav')
    y,sr=sf.read(p); y=y.mean(1) if y.ndim>1 else y
    return y.astype(np.float32),sr
S={}
for n in names:
    y,sr=load(n)
    S[n]=np.abs(librosa.stft(y,n_fft=4096,hop_length=sr//4))**2  # 4 fps
mel=librosa.filters.mel(sr=sr,n_fft=4096,n_mels=40,fmax=12000)
M={n:10*np.log10(mel@S[n]+1e-12) for n in names}
fps=4
def nov(n,t,w=2.4):
    a=M[n][:,int((t-w)*fps):int(t*fps)].mean(1); b=M[n][:,int(t*fps):int((t+w)*fps)].mean(1)
    return np.sqrt(np.mean((a-b)**2)), (b-a).mean()
cands=[24.4,47.4,64.8,104.5,109.3,113.4,127.5,141,187,193,208,224,251.5,276.5,286.5,307.1,322.5,329,222,248,240,160,200,290]
cands=sorted(set([24.4,47.4,64.8,80.8,89,109.3,113.4,127.5,141,163,187,193,208,224,248,251.5,276.5,286.5,307.1,322.5,329]))
print('t  | novelty (rms dB mel diff) mix drums bass other | mean dB change')
for t in cands:
    r=[nov(n,t) for n in ['mix','drums','bass','other']]
    print(f"{int(t//60)}:{t%60:04.1f} | "+' '.join(f"{x[0]:5.1f}" for x in r)+' | '+' '.join(f"{x[1]:+5.1f}" for x in r))
# top novelty across whole mix
T=M['mix'].shape[1]/fps
sc=[]
for t in np.arange(10,T-10,0.5):
    sc.append((nov('mix',t,4.0)[0],t))
# peaks
sc=np.array(sc); from scipy.signal import find_peaks
pk,_=find_peaks(sc[:,0],distance=16,height=4)
top=sorted(pk,key=lambda i:-sc[i,0])[:20]
print('top mix-spectrum novelty peaks (4 s windows)')
for i in sorted(top,key=lambda i:sc[i,1]): print(f"{int(sc[i,1]//60)}:{sc[i,1]%60:04.1f} {sc[i,0]:.1f}")
