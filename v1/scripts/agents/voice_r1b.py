import numpy as np, soundfile as sf, librosa, json
D='/home/user/Listener/v1/data/t_dl_mirror/'
S=D+'stems_raw/htdemucs/song/'
v,sr=sf.read(S+'vocals.wav'); v=v.mean(1)
m,_=sf.read(D+'audio/song.wav'); m=m.mean(1)
def rms(x,a,b): 
    s=x[int(a*sr):int(b*sr)]; return round(20*np.log10(np.sqrt(np.mean(s**2))+1e-9),1)
f=lambda t:f"{int(t//60)}:{t%60:04.1f}"
# tail
print('tail mix 0.5s rms 3:30..4:00')
for t in np.arange(210,239.5,2): print(f(t),rms(m,t,t+2),rms(v,t,t+2),end=' | ')
print()
h=int(.01*sr); x=m[-4*sr:]; e=20*np.log10(np.array([np.sqrt(np.mean(x[i:i+h]**2)) for i in range(0,len(x)-h,h)])+1e-9)
t0=len(m)/sr-4
from scipy.signal import find_peaks
p,_=find_peaks(e,height=-50,prominence=6)
print('env peaks (mix last 4s):',[(round(t0+i*.01,2),round(e[i],1)) for i in p])
print('last>-70',round(t0+np.where(e>-70)[0][-1]*.01,2),'last>-50',round(t0+np.where(e>-50)[0][-1]*.01,2))
# hook instances: chroma of vocal stem and envelope similarity
inst={'a':10.2,'b':20.5,'c':72.0,'d':82.0,'e':132.2,'f':142.0,'g':194.0,'h':204.0}
# use onset envelopes of vocals for 10 s windows; correlate
def env(t,L=10):
    s=v[int(t*sr):int((t+L)*sr)]; hop=512
    return librosa.feature.rms(y=s,frame_length=1024,hop_length=hop)[0]
def chrm(t,L=10):
    s=v[int(t*sr):int((t+L)*sr)]; return librosa.feature.chroma_cqt(y=s,sr=sr,hop_length=512)
ks=list(inst)
print('hook envelope corr (10s):')
for k in ks:
    print(k,[round(np.corrcoef(env(inst[k])[:800],env(inst[j])[:800])[0,1],2) for j in ks])
# find exact hook starts: first vocal onset after span start 
# waveform cross-correlation of 2 s of vocal between repeated verse starts? hook c vs e
def xc(t1,t2,L=3,sh=1.0):
    a=v[int(t1*sr):int((t1+L)*sr)]; b=v[int((t2-sh)*sr):int((t2+L+sh)*sr)]
    c=np.correlate(b,a,'valid'); return round(np.max(np.abs(c))/ (np.linalg.norm(a)*np.sqrt(np.max(np.convolve(b**2,np.ones(len(a)),'valid')))+1e-9),3)
for t1,t2 in [(24.8,72.0),(1*60+13,2*60+14),(2*60+14,3*60+15)]:
    print('xcorr',f(t1),f(t2),xc(t1,t2))
# pitch median per section via pyin on vocal
secs=[('hook1',11,24),('v1',30.4,56.4),('hook2',72,89),('v2',91.5,128),('hook3',134,148),('v3',150,180),('hook4',194,208)]
for n,a,b in secs:
    s=v[int(a*sr):int(b*sr)]
    f0,vf,_=librosa.pyin(s,fmin=70,fmax=700,sr=sr,frame_length=2048)
    f0=f0[~np.isnan(f0)]
    print(n,f(a),f(b),'voiced',len(f0),'median Hz',round(np.median(f0),1),'p10',round(np.percentile(f0,10),1),'p90',round(np.percentile(f0,90),1),'level',rms(v,a,b),'mix',rms(m,a,b))
    # onset rate
    o=librosa.onset.onset_detect(y=s,sr=sr,units='time'); print('  onsets/s',round(len(o)/(b-a),2))
