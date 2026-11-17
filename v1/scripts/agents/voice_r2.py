import numpy as np, librosa, sys
D='/home/user/Listener/v1/data/t_birdwalk/stems_raw/htdemucs/song/'
v,sr=librosa.load(D+'vocals.wav',sr=22050,mono=False)
m=v.mean(0); d=librosa.load(D+'drums.wav',sr=22050)[0]
hop=256
def ons(x,delta=0.07):
    e=librosa.onset.onset_strength(y=x,sr=sr,hop_length=hop)
    return librosa.onset.onset_detect(onset_envelope=e,sr=sr,hop_length=hop,units='time',delta=delta,backtrack=False)
vo=ons(m); do=ons(d,0.15)
rms=librosa.feature.rms(y=m,hop_length=hop)[0]; t=librosa.times_like(rms,sr=sr,hop_length=hop)
db=20*np.log10(rms+1e-9)
# vocal activity edges per 0.5s around verse bounds
def act(a,b):
    s=(t>=a)&(t<b); return db[s].mean()
for a,b in [(22,26),(44,50),(68,73),(56,62),(1*60+55,2*60+2),(2*60+45,2*60+50)]:
    print('win',a,b,[round(act(x,x+0.5),0) for x in np.arange(a,b,0.5)])
# lag of vocal onsets vs nearest drum hit, per section
def lag(a,b):
    vv=vo[(vo>=a)&(vo<b)]; dd=do[(do>=a-1)&(do<b+1)]
    if len(vv)==0 or len(dd)==0: return None
    l=[(x-dd[np.argmin(abs(dd-x))]) for x in vv]; l=np.array(l)
    return len(vv),np.round(np.median(l),3),np.round(np.mean(l<-0.03),2),np.round(np.mean(abs(l)<0.05),2)
for a,b in [(0,12),(24,47),(47,59),(70,118),(120,131),(143,155)]:
    print('lag',a,b,lag(a,b))
# phase of vocal onsets on 0.19 grid anchored to loop start 47.2 (hat step 0.1875?)
for step in [0.1875,0.19,0.1936]:
  for a,b in [(24,47),(70,118),(131,143)]:
    vv=vo[(vo>=a)&(vo<b)]
    ph=((vv-47.2)/step)%1; ang=np.angle(np.mean(np.exp(2j*np.pi*ph))); R=abs(np.mean(np.exp(2j*np.pi*ph)))
    print('phase',step,a,b,len(vv),'R',round(R,2),'mean phase in step',round(ang/(2*np.pi)%1,2))
# side/mid in hook vs verse
L,R_=v[0],v[1]
for a,b in [(24,47),(48,58),(75,115),(125,140)]:
    s=slice(int(a*sr),int(b*sr)); mid=(L[s]+R_[s])/2; side=(L[s]-R_[s])/2
    print('S/M',a,b,round(np.sqrt((side**2).mean()/(mid**2).mean()),3))
# pitch of hook: pYIN on 2:00-2:11 and 2:35-2:46, cents vs A440
for a,b in [(48,58),(120,131),(155,166),(24,45),(72,115)]:
    y=m[int(a*sr):int(b*sr)]
    f0,vf,_=librosa.pyin(y,fmin=80,fmax=700,sr=sr,frame_length=2048,hop_length=512)
    f=f0[vf&~np.isnan(f0)]; mid=12*np.log2(f/440)+69
    pc=np.round(mid).astype(int)%12; cents=(mid-np.round(mid))*100
    names='C C# D D# E F F# G G# A A# B'.split()
    h=np.bincount(pc,minlength=12)/len(pc)
    print('pitch',a,b,len(f),{names[i]:round(h[i],2) for i in np.argsort(-h)[:5]},'median offset cents',round(np.median(cents),0))
    # C3 vs C#3 specifically, between 125-145 Hz
    c3=np.sum((f>127)&(f<134)); cs=np.sum((f>135)&(f<142)); a2=np.sum((f>106)&(f<114))
    print('   A2',a2,'C3',c3,'C#3',cs)
