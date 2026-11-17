import librosa, numpy as np, json
D='/home/user/Listener/v1/data/video1/stems_raw/htdemucs/song/'
sr=22050;hop=128
dr,_=librosa.load(D+'drums.wav',sr=sr)
S=np.abs(librosa.stft(dr,n_fft=1024,hop_length=hop));f=librosa.fft_frequencies(sr=sr,n_fft=1024);fr=sr/hop
def env(lo,hi):
    e=S[(f>=lo)&(f<hi)].sum(0);return np.maximum(0,np.diff(np.log1p(e*10),prepend=0))
E={'low':env(30,150),'mid':env(150,2500),'high':env(5000,10000)}
# global fit: period T, phase, using autocorr-proof: fold at beat period 4*0.19227
T=0.76906
oe=sum(E.values())
def fold(e,t0,t1,nb=32,per=T):
    idx=np.arange(int(t0*fr),min(int(t1*fr),len(e)));ph=((idx/fr)%per)/per
    h=np.zeros(nb);c=np.zeros(nb)
    np.add.at(h,(ph*nb).astype(int),e[idx]);np.add.at(c,(ph*nb).astype(int),1);return h/np.maximum(c,1)
for name,e in E.items():
    h=fold(e,10,180);print(name,np.round(h/h.max(),2))
# check tempo stability: fit period per 30s
for t0 in range(0,180,30):
    best=max(((fold(oe,t0,t0+30,32,p).max()/fold(oe,t0,t0+30,32,p).mean()),p) for p in np.arange(0.755,0.785,0.0005))
    print(t0,'best beat period',round(best[1],4),'bpm',round(60/best[1],2))
print('--- bar folds (16 steps, step0 = first strong slot at beat-phase 6.8/32)')
def barfold(e,t0,t1,off):
    idx=np.arange(int(t0*fr),min(int(t1*fr),len(e)));P=4*T;t=idx/fr
    ph=((t-off)%P)/P
    st=np.round(ph*16).astype(int)%16   # nearest step
    # use max over +-1 frame? use mean energy within +-15ms of step centre
    d=np.abs(((ph*16)-np.round(ph*16)))*P/16
    m=d<0.02
    h=np.zeros(16);c=np.zeros(16);np.add.at(h,st[m],e[idx][m]);np.add.at(c,st[m],1);return h/np.maximum(c,1)
off0=6.8/32*T
np.set_printoptions(linewidth=200)
for name in E:
    for (a,b) in [(10,75),(90,120),(130,165),(170,185)]:
        h=barfold(E[name],a,b,off0);print(name,a,b,np.round(h/h.max(),2))
