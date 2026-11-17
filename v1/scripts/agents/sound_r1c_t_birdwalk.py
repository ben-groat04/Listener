import numpy as np, soundfile as sf, scipy.signal as ss
D='data/t_birdwalk/'; S=D+'stems_raw/htdemucs/song/'
sr=44100
def load(n): 
    s,_=sf.read(S+n+'.wav'); return s
dr=load('drums'); dm=dr.mean(1)
def corr_hits(ts,sig,pre=0.01,L=0.25):
    seg=[sig[int((t-pre)*sr):int((t-pre+L)*sr)] for t in ts]
    out=[]
    for i in range(len(seg)):
        for j in range(i+1,len(seg)):
            a,b=seg[i],seg[j]
            c=ss.correlate(a,b,'full'); c/= (np.linalg.norm(a)*np.linalg.norm(b)+1e-12)
            out.append(c.max())
    return np.round(np.mean(out),3),np.round(np.min(out),3)
intro=[0.81,2.28,3.81,5.36,6.94,8.54,10.12]
mid=[47.83,49.32,50.86,52.50,53.98,55.55,57.14,58.71]
late=[120+1.29-0.0, 121.29+1.57]  # not used
a=[2*60+1.29,2*60+2.86,2*60+4.46,2*60+5.93,2*60+7.54,2*60+9.06,2*60+10.64]
# refine peak positions
def refine(ts,sig):
    o=[]
    for t in ts:
        w=np.abs(sig[int((t-.05)*sr):int((t+.1)*sr)]); o.append(t-.05+w.argmax()/sr)
    return o
for name,ts in [('intro',intro),('0:47-0:59',mid),('2:01-2:11',a)]:
    r=refine(ts,dm); print(name,'refined',np.round(r,3),'IOI',np.round(np.diff(r),3),'sd ms',round(np.diff(r).std()*1000,1))
    print('  waveform corr mean/min',corr_hits(r,dm), 'drum stem peak levels',[round(20*np.log10(np.abs(dm[int((t-.02)*sr):int((t+.1)*sr)]).max()),1) for t in r])
    print('  centroid',[round(float((np.abs(np.fft.rfft(dm[int(t*sr):int((t+.1)*sr)]))*np.fft.rfftfreq(int(.1*sr)+0,1/sr)[:len(np.fft.rfft(dm[int(t*sr):int((t+.1)*sr)]))]).sum()/np.abs(np.fft.rfft(dm[int(t*sr):int((t+.1)*sr)])).sum())) for t in r])
# bass note decay
b=load('bass').mean(1)
env=np.sqrt(np.convolve(b**2,np.ones(441)/441,'same'))
for t in [59.4+0.0,60.0,61.5,100.0, 2*60+12.33,2*60+13.07, 2*60+14.27]:
    i=int(t*sr); w=env[i-2000:i+int(1.5*sr)]; k=w.argmax(); pk=w[k]
    dec=np.where(w[k:]<pk*10**(-20/20))[0]; print('bass note near',t,'peak dB',round(20*np.log10(pk),1),'-20 dB decay s',round(dec[0]/sr,2) if len(dec) else '>1.5')
# bass spectral content: fraction of energy above 120 Hz, harmonics
f,P=ss.welch(b[int(60*sr):int(100*sr)],sr,nperseg=16384); 
print('bass stem welch peaks',[round(f[i],1) for i in ss.find_peaks(10*np.log10(P+1e-20),prominence=10)[0][:8]])
# distortion proxy: H2/H1 etc around 55 Hz
for h in [1,2,3,4]:
    j=np.searchsorted(f,55*h); print(' harmonic',h*55,round(10*np.log10(P[j-3:j+4].max()),1))
# stereo by stem per section
for n in ['vocals','drums','bass','other']:
    s=load(n); 
    row=[]
    for a0,a1 in [(1,11),(13,23),(25,40),(48,58),(62,72),(1*60+25,1*60+32),(2*60,2*60+10),(2*60+25,2*60+35),(2*60+51,2*60+55)]:
        L=s[int(a0*sr):int(a1*sr),0];R=s[int(a0*sr):int(a1*sr),1]
        row.append(round(10*np.log10(((L-R)**2).sum()/(((L+R)**2).sum()+1e-12)+1e-12),1))
    print(n,'S/M dB',row)
# mix loudness approx per section (K-weight skipped) 
x,_=sf.read(D+'audio/song.wav'); m=x.mean(1)
for a0,a1,l in [(1,11.9,'intro'),(13,47,'groove A'),(48,59,'stripped'),(60,119,'groove B'),(120,131,'sparse'),(132,143,'groove D'),(144,155,'stop 2:24-2:35'),(156,187,'finale')]:
    s=m[int(a0*sr):int(a1*sr)]; print(l,'RMS dBFS',round(20*np.log10(np.sqrt((s**2).mean())),1),'peak',round(20*np.log10(np.abs(s).max()),1))
# end peaks in 10ms envelope last 3s
E=np.sqrt(np.convolve(m**2,np.ones(441)/441,'same'))[-3*sr:]
pk=ss.find_peaks(20*np.log10(E+1e-9),prominence=3)[0]; print('end env peaks (prominence 3dB)',[(round(188.15-3+p/sr,2),round(20*np.log10(E[p]),1)) for p in pk])
