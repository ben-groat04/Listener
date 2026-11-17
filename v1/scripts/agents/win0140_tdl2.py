import numpy as np, soundfile as sf, json, librosa, scipy.signal as ss
D='/home/user/Listener/v1/data/t_dl_mirror/'
st={}
for n in ['vocals','drums','bass','other']:
    x,sr=sf.read(D+f'stems_raw/htdemucs/song/{n}.wav',always_2d=True); st[n]=x.mean(1)
mix,_=sf.read(D+'audio/song.wav',always_2d=True); st['mix']=mix.mean(1)
def env(x,hop=0.01):
    h=int(sr*hop); n=len(x)//h
    return 20*np.log10(np.sqrt((x[:n*h].reshape(n,h)**2).mean(1))+1e-9)
E={n:env(st[n]) for n in st}
def m(n,a,b): return round(float(np.mean(E[n][int(a*100):int(b*100)])),1)
print('--- boundaries (dB mean 0.5s before | 0.5s after)')
for tb in [143.0,143.98,145.6,146.8,149.3,149.95,152.5,153.5,154.6,155.2,156.2,156.9,158.1,160.9,161.5,162,163,164]:
    print(tb,{n:(m(n,tb-.5,tb),m(n,tb,tb+.5)) for n in E})
# when does bass return after 158
b=E['bass']; i=int(158.1*100)
while i<len(b) and b[i]<-45: i+=1
print('bass returns',i/100)
# hi band onset density, other hf
for n in ['drums','other','vocals']:
    S=np.abs(librosa.stft(st[n][int(130*sr):int(170*sr)],n_fft=2048,hop_length=1024))**2
    f=librosa.fft_frequencies(sr=sr,n_fft=2048)
    hf=10*np.log10(S[(f>4000)&(f<10000)].sum(0)+1e-12); lf=10*np.log10(S[(f<200)].sum(0)+1e-12)
    t=np.arange(S.shape[1])*1024/sr+130
    out=[]
    for a in range(130,170,2):
        k=(t>=a)&(t<a+2); out.append((a,round(float(hf[k].mean()),1)))
    print(n,'4-10k dB per 2s',out)
# kicks: 35-90 Hz band envelope peaks in drum stem
dr=st['drums']; lo=ss.sosfilt(ss.butter(4,[35,100],'band',fs=sr,output='sos'),dr)
e=np.abs(ss.hilbert(lo)); e=ss.sosfilt(ss.butter(2,40,'low',fs=sr,output='sos'),e)
pk,_=ss.find_peaks(e[:],height=np.percentile(e,80),distance=int(0.08*sr))
tt=pk/sr; tt=tt[(tt>=140)&(tt<160)]
print('kick peaks',len(tt)); ioi=np.diff(tt)
print('IOI percentiles',np.round(np.percentile(ioi,[10,25,50,75,90]),3))
bt=np.array(json.load(open(D+'audio_features/beat_times.json')) if isinstance(json.load(open(D+'audio_features/beat_times.json')),list) else json.load(open(D+'audio_features/beat_times.json'))['beats'])
bi=bt[(bt>=140)&(bt<160)]; bp=np.median(np.diff(bi)); print('beat period',bp,60/bp,'n beats',len(bi))
for name,g in [('beat',bp),('8th',bp/2),('16th',bp/4)]:
    best=min(((np.sqrt((((tt-ph+g/2)%g-g/2)**2).mean()),ph) for ph in np.linspace(0,g,300)))
    print(name,'grid dev ms',round(best[0]*1000,1),'uniform-random expectation ms',round(g/np.sqrt(12)*1000,1))
# kicks distance to nearest tracker beat
d=np.array([np.min(np.abs(bi-x)) for x in tt]); print('kick to nearest tracker beat: median ms',np.median(d)*1000,'frac within 40ms',(d<.04).mean())
print('tracker beat times 140-160',np.round(bi,2).tolist())
# loop check: 2-bar and 4-bar lag at beat period
for n in ['drums','bass','other']:
    e1=E[n][13000:17000]; 
    seg=E[n][14000:16000]-E[n][14000:16000].mean()
    res={}
    for lagb in [4,8,16]:
        lag=int(round(lagb*bp*100))
        a=E[n][14000:16000]; b2=E[n][14000-lag:16000-lag]; res[lagb]=round(float(np.corrcoef(a,b2)[0,1]),2)
    print(n,'corr at lag beats(4,8,16)',res)
# vocal-stem pitch context
print('pk mix over window', 20*np.log10(np.abs(mix[140*sr:160*sr]).max()))
# stem peak
for n in st: print(n,'peak dB 140-160',round(20*np.log10(np.abs(st[n][140*sr:160*sr]).max()),1))
# 10 ms mix dips (min per 0.5 s)
