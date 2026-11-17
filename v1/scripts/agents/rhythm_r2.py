import numpy as np, librosa, json
D='/home/user/Listener/v1/data/video1/'
y,sr=librosa.load(D+'stems_raw/htdemucs/song/drums.wav',sr=22050)
P=0.7692; 
# refine grid: fit phase of 16th grid
hop=64
S=np.abs(librosa.stft(y,n_fft=1024,hop_length=hop))
f=librosa.fft_frequencies(sr=sr,n_fft=1024)
bands={'low':(30,150),'mid':(150,2500),'hi':(3000,10000)}
env={k:S[(f>=a)&(f<b)].sum(0) for k,(a,b) in bands.items()}
for k in env:
    e=np.diff(env[k],prepend=0);e[e<0]=0;env[k]=e
t=np.arange(len(env['low']))*hop/sr
g=P/4
# phase fit on total
tot=sum(env.values())
best=None
for ph in np.arange(0,g,0.002):
    idx=np.round((np.arange(0,188,g)+ph)*sr/hop).astype(int)
    idx=idx[idx<len(tot)]
    s=tot[idx].sum()
    if best is None or s>best[0]:best=(s,ph)
ph=best[1];print('phase',ph,'period P',P)
# refine P
bestP=None
for p in np.arange(0.766,0.772,0.0002):
    gg=p/4
    idx=np.round((np.arange(0,188,gg)+ph)*sr/hop).astype(int);idx=idx[idx<len(tot)]
    s=tot[idx].sum()
    if bestP is None or s>bestP[0]:bestP=(s,p)
print('P',bestP[1],'bpm',60/bestP[1]);P=bestP[1];g=P/4
nsteps=int(188/g)
def val(k,i,w=1):
    c=int(round((ph+i*g)*sr/hop));return env[k][max(c-w,0):c+w+1].max()
M={k:np.array([val(k,i) for i in range(nsteps)]) for k in env}
# normalise per band
for k in M:M[k]=M[k]/np.percentile(M[k],95)
# bar position: step0 is phase; determine which step mod 16 is bar start by lowband strongest? print fold per 20-s segments
def fold(k,a,b):
    ia,ib=int(a/g)//16*16,int(b/g)//16*16
    x=M[k][ia:ib].reshape(-1,16);return x.mean(0),x
segs=[(0,32),(33,75),(75,108),(108,115),(120,168),(168,188)]
np.set_printoptions(precision=2,suppress=True,linewidth=200)
for a,b in segs:
    print('---',a,b)
    for k in M:print(k,fold(k,a,b)[0])
# bar to bar variability: correlation of each bar's low+mid+hi vector with segment mean
for a,b in segs:
    m=np.concatenate([fold(k,a,b)[0] for k in M]);cs=[]
    ia,ib=int(a/g)//16*16,int(b/g)//16*16
    for i in range(ia,ib,16):
        v=np.concatenate([M[k][i:i+16] for k in M]);cs.append(np.corrcoef(v,m)[0,1])
    print(a,b,'bar-corr mean %.2f min %.2f'%(np.mean(cs),np.min(cs)))
# beats 1-4 level difference (snare backbeat?) mid band fold by beat position (steps 0,4,8,12) mean over every 4-step offset
for off in range(4):
    print('offset',off,[round(float(M['mid'][off::16][:].mean()),2)])
# section boundaries bar position
for tb in [14.8,32,66.4,75.6,87.9,100,109.4,118.7,134,158.7,167.8,27.9,31.7,2*60+19.5,2*60+25.7,2*60+31.9,2*60+38.3,6.2,9]:
    x=(tb-ph)/P; print('t %.1f beat %.2f bar %.2f (frac beats %.2f)'%(tb,x,x/4,x%4))
# bar-vs-beat: also off-beat 16th mean per position in 4-step
for k in M:
    print(k,'pos in beat mean',[round(float(M[k][j::4].mean()),2) for j in range(4)])
