import numpy as np, librosa
from scipy.signal import correlate
D='/home/user/Listener/v1/data/t_birdwalk/stems_raw/htdemucs/song/'
v,sr=librosa.load(D+'vocals.wav',sr=22050,mono=False); d=librosa.load(D+'drums.wav',sr=22050)[0]; m=v.mean(0)
hop=256
e=librosa.onset.onset_strength(y=d,sr=sr,hop_length=hop)
do=librosa.onset.onset_detect(onset_envelope=e,sr=sr,hop_length=hop,units='time',delta=0.15)
ev=librosa.onset.onset_strength(y=m,sr=sr,hop_length=hop)
vo=librosa.onset.onset_detect(onset_envelope=ev,sr=sr,hop_length=hop,units='time',delta=0.07)
for a,b in [(0.5,12),(47.2,59),(120,131),(24,47),(72,118)]:
    dd=do[(do>=a)&(do<b)]
    if len(dd)==0: continue
    hit=np.mean([np.min(abs(vo-x))<0.05 for x in dd])
    # chance: random times
    rnd=np.random.uniform(a,b,500); ch=np.mean([np.min(abs(vo-x))<0.05 for x in rnd])
    lag=[vo[np.argmin(abs(vo-x))]-x for x in dd]
    print(a,b,'drumhits',len(dd),'with vocal onset within 50ms',round(hit,2),'chance',round(ch,2),'median voc-drum',round(np.median(lag),3))
rms=librosa.feature.rms(y=m,hop_length=hop)[0]; t=librosa.times_like(rms,sr=sr,hop_length=hop); db=20*np.log10(rms+1e-9)
def quiet(a,b,th=-33):
    s=(t>=a)&(t<b)&(db<th); tt=t[s]
    if len(tt)==0: return []
    runs=[];st=tt[0];p=tt[0]
    for x in tt[1:]:
        if x-p>0.05: runs.append((round(st,2),round(p,2)));st=x
        p=x
    runs.append((round(st,2),round(p,2)));return [r for r in runs if r[1]-r[0]>0.15]
for a,b in [(21,27),(43,49),(66,75),(112,122),(1*60+55,2*60+3),(160,168)]:
    print('quiet runs <-33dB',a,b,quiet(a,b))
# stereo: lag between L and R in hook vs verse, and L/R pitch
L,R=v[0],v[1]
for a,b,nm in [(48,58,'hook'),(125,140,'hook2'),(24,45,'verse1'),(75,110,'verse2')]:
    s=slice(int(a*sr),int(b*sr)); l=L[s];r=R[s]
    c=correlate(l,r,mode='full')[len(l)-1-400:len(l)+400]; k=np.argmax(abs(c))-400
    print(nm,'L/R xcorr peak lag samples',k,'ms',round(k/sr*1000,1),'norm',round(abs(c).max()/np.sqrt((l**2).sum()*(r**2).sum()),2))
    out=[]
    for ch in (l,r):
        f0,vf,_=librosa.pyin(ch,fmin=80,fmax=700,sr=sr,frame_length=2048,hop_length=512); out.append((f0,vf))
    both=out[0][1]&out[1][1]
    if both.sum(): 
        dev=12*np.log2(out[0][0][both]/out[1][0][both]); print('   voiced both',both.sum(),'median |L-R pitch| cents',round(np.median(abs(dev))*100,0))
# loop-twin test: hook 12 s steps, onset pattern coincidence
for a in [47.2+12*k for k in range(0,10)]:
    pass
x=vo[(vo>=47.2)&(vo<59.2)]-47.2
for k in [1,6,7,8,9]:
    y=vo[(vo>=47.2+12*k)&(vo<59.2+12*k)]-47.2-12*k
    mt=np.mean([np.min(abs(y-q))<0.04 for q in x]) if len(y) else None
    print('loop+',k,'onsets',len(y),'matching first loop within 40ms',mt)
