import numpy as np, librosa, json
D='/home/user/Listener/v1/data/t_dl_mirror/'
sr=22050; hop=32; fr=sr/hop
dr,_=librosa.load(D+'stems_raw/htdemucs/song/drums.wav',sr=sr,mono=True)
S=np.abs(librosa.stft(dr,n_fft=1024,hop_length=hop)); f=librosa.fft_frequencies(sr=sr,n_fft=1024)
def band(lo,hi):
    m=(f>=lo)&(f<hi); e=np.log1p(30*S[m].sum(0)); return np.maximum(np.diff(e,prepend=e[0]),0)
env={'kick':band(35,110),'snare':band(150,400),'crack':band(1500,5000),'hat':band(6000,10000)}
tot=sum(v/v.std() for v in env.values())
beat=0.6385; step=beat/4
t=np.arange(len(tot))/fr
# phase drift: per 12 s block, circular-mean phase of onset env at beat period
print('phase of pulse (ms from t=0 grid) per block at beat=0.6385')
ph=[]
for a in range(0,228,12):
    m=(t>=a)&(t<a+12)
    z=np.sum(tot[m]*np.exp(-2j*np.pi*t[m]/beat))
    p=(np.angle(z)/(2*np.pi))*beat; ph.append(p)
    print(a,round(p*1000,1),'ms  strength',round(abs(z)/tot[m].sum(),3))
# fold onto 16 steps per bar for 30-215 s using unwrapped phase of whole
m=(t>=30)&(t<215)
z=np.sum(tot[m]*np.exp(-2j*np.pi*t[m]/beat)); p0=np.angle(z)/(2*np.pi)*beat
print('global phase ms',p0*1000)
# 64-bin fold over a beat then 16 over bar; need downbeat: fold at bar period 4*beat into 64 bins per kind
bar=4*beat
for k,v in env.items():
    x=v/v.std(); 
    ph=((t[m]-p0)%bar)/bar
    h,_=np.histogram(ph,bins=64,weights=x[m]); h=h/h.sum()
    # sum into 16 steps (each 4 bins, centred)
    h16=np.roll(h,2).reshape(16,4).sum(1)
    print(k,'bar fold 16 steps (% of band onset energy):',np.round(h16*100,1).tolist())
# pulse-level offsets: for kick, find within-step offset distribution (swing). fold the 8th-note: position of onset energy between beat 0 and 0.5
for k,v in env.items():
    x=v/v.std()
    ph=((t[m]-p0)%beat)/beat
    h,_=np.histogram(ph,bins=48,weights=x[m]); h=h/h.sum()
    print(k,'beat fold 48 bins',np.round(h*100,1).tolist())
