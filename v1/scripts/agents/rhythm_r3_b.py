import numpy as np, librosa
D='/home/user/Listener/v1/data/t_dl_mirror/stems_raw/htdemucs/song/'
sr=22050
d,_=librosa.load(D+'drums.wav',sr=sr,mono=True)
de=librosa.feature.rms(y=d,frame_length=441,hop_length=221)[0]
db=librosa.amplitude_to_db(de+1e-6)
# high-passed flux of dB env for sharper alignment
def seg(a,n): 
    x=db[int(a*100):int((a+n)*100)]; return x-x.mean()
def lag(a,b,n=18.0,rng=1.5):
    x=seg(a,n); best=(-2,0)
    for s in range(-int(rng*100),int(rng*100)+1):
        y=seg(b+s/100,n)
        if len(y)!=len(x):continue
        c=np.corrcoef(x,y)[0,1]
        if c>best[0]:best=(c,s/100)
    return best
H=[10.4,71.3,132.0,193.1]
for i in range(1,4):
    c,s=lag(H[0],H[i]); print('hook1->hook',i+1,'start diff',H[i]-H[0],'refined offset',round(s,2),'lag',round(H[i]-H[0]+s,2),'r',round(c,2))
# verses: verse1 core 40-60 vs verse3 core 2:45-3:05
for a,b in ((40,40+61.3*2),(40,40+61.3),(101.3,101.3+61.3)):
    c,s=lag(a,b,18,3); print('verse',a,b,'lag',round(b-a+s,2),'r',round(c,2))
# lag in 4-bar loops (10.2s): consecutive 4-bar windows inside verse 1 autocorr
x=db[int(35*100):int(70*100)];x=x-x.mean()
ac=np.correlate(x,x,'full')[len(x)-1:];ac/=ac[0]
for lo,hi,nm in ((250,260,'1bar'),(500,520,'2bar'),(1000,1040,'4bar')):
    i=lo+np.argmax(ac[lo:hi]);print(nm,i/100,round(ac[i],2))
