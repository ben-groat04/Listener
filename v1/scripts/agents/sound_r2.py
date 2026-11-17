import numpy as np, librosa, scipy.signal as ss
D='/home/user/Listener/v1/data/video1/stems_raw/htdemucs/song/'
sr=22050
def L(n): return librosa.load(D+n+'.wav',sr=sr,mono=True)[0]
b,o,d,v=L('bass'),L('other'),L('drums'),L('vocals')
def seg(x,a,b_): return x[int(a*sr):int(b_*sr)]
print('== sub onset/envelope')
for t in [121.1,127.3,133.4,139.6,145.7,151.9]:
    x=seg(b,t-0.3,t+2.0)
    env=np.sqrt(np.convolve(x**2,np.ones(441)/441,'same'))
    pk=np.argmax(env)/sr-0.3
    # onset 10-90 rise
    i0=int(0.3*sr)
    e=env; m=e.max()
    t10=np.argmax(e>0.1*m)/sr-0.3; t90=np.argmax(e>0.9*m)/sr-0.3
    # high-band click: >300Hz energy in first 80ms vs sub
    hp=ss.sosfilt(ss.butter(4,300,'hp',fs=sr,output='sos'),x)
    # inst freq over time via 0.1 s windows
    fr=[]
    for k in range(0,int(1.6*sr),int(0.1*sr)):
        w=x[int(0.3*sr)+k-int(0.05*sr):int(0.3*sr)+k+int(0.15*sr)]
        if len(w)<100: continue
        S=np.abs(np.fft.rfft(w*np.hanning(len(w)),n=len(w)*32)); f=np.fft.rfftfreq(len(w)*32,1/sr)
        mk=(f>30)&(f<60); fr.append(round(f[mk][np.argmax(S[mk])],1))
    print(t,'t10 %.3f t90 %.3f peak %.2f'%(t10,t90,pk),'hp300 rms/total %.3f'%(np.sqrt((hp[:int(.5*sr)]**2).mean())/np.sqrt((x[:int(.5*sr)]**2).mean()+1e-12)),'freq',fr)
print('== other 1:15-1:40 attack (onset strength, flatness)')
x=seg(o,75,100)
oe=librosa.onset.onset_strength(y=x,sr=sr); print('onset str mean/max %.2f %.2f'%(oe.mean(),oe.max()))
rms=librosa.feature.rms(y=x,frame_length=2048,hop_length=512)[0]
print('rms dB range', 20*np.log10(rms.min()+1e-9), 20*np.log10(rms.max()))
fl=librosa.feature.spectral_flatness(y=x)[0]; print('flatness',fl.mean())
for a,bb in [(77,79.5),(79.5,82),(82,84),(84,85)]:
    y=seg(o,a,bb); S=np.abs(librosa.stft(y,n_fft=4096)); f=librosa.fft_frequencies(sr=sr,n_fft=4096)
    p=S.mean(1); print(a,'centroid %.0f'%((p*f).sum()/p.sum()),'rms %.1f'%(20*np.log10(np.sqrt((y**2).mean()))))
    # envelope modulation: rms in 50ms frames, std of dB
    r=librosa.feature.rms(y=y,frame_length=1102,hop_length=551)[0]; print('  dB std %.2f'%np.std(20*np.log10(r+1e-9)))
print('== wall centroid/rolloff')
for a,bb in [(30,60),(90,109),(109.5,119),(121,133),(135,153),(170,180),(150,165)]:
    y=seg(o,a,bb); S=np.abs(librosa.stft(y,n_fft=2048))**2; f=librosa.fft_frequencies(sr=sr,n_fft=2048); p=S.mean(1)
    c=np.cumsum(p)/p.sum(); print(a,bb,'cent %.0f roll85 %.0f flat %.3f'%((p*f).sum()/p.sum(),f[np.argmax(c>.85)],librosa.feature.spectral_flatness(S=S).mean()))
print('== drum character')
y=d; on=librosa.onset.onset_detect(y=y,sr=sr,units='time',backtrack=False)
st=librosa.onset.onset_strength(y=y,sr=sr)
fr=librosa.times_like(st,sr=sr)
# kick vs hat velocity variability: low band onsets
for nm,(lo,hi) in {'kick':(40,120),'hat':(6000,10000),'snare':(1500,4000)}.items():
    sos=ss.butter(4,[lo,hi],'bp',fs=sr,output='sos'); z=ss.sosfilt(sos,seg(d,20,60))
    e=np.abs(ss.hilbert(z)); pk,_=ss.find_peaks(e,distance=int(0.12*sr),height=0.3*e.max())
    h=e[pk]; print(nm,'n',len(pk),'peak-amp CV %.2f'%(h.std()/h.mean()))
# hat velocity: time-grid at 16ths
bt=60/78.3/4
sos=ss.butter(4,[6000,10000],'bp',fs=sr,output='sos'); z=np.abs(ss.hilbert(ss.sosfilt(sos,seg(d,20,60))))
n=int(40/bt); vals=np.array([z[int(k*bt*sr):int((k*bt+0.05)*sr)].max() for k in range(n)])
print('hat 16th slots CV %.2f'%(vals.std()/vals.mean()))
print('== drums after 2:48 vs before')
for a,bb in [(160,166),(169,175),(176,186),(190,187)]:
    pass
for a,bb in [(150,165),(170,180),(180,188)]:
    y=seg(d,a,bb); S=np.abs(librosa.stft(y,n_fft=2048))**2; f=librosa.fft_frequencies(sr=sr,n_fft=2048);p=S.mean(1)
    print(a,bb,'drum cent %.0f hi(>5k) share %.3f'%((p*f).sum()/p.sum(),p[f>5000].sum()/p.sum()))
print('== swell start')
y=seg(o+d+b+v,0,1.2); r=librosa.feature.rms(y=y,frame_length=441,hop_length=221)[0]; print(np.round(20*np.log10(r[::5]+1e-9),0))
print('== voice hiss in other / voice-gap noise')
# other stem content in speech bursts vs gaps >5k
for a,bb in [(19,24),(28,32),(144,156),(164,168)]:
    for nm,x in [('vocals',v),('other',o)]:
        y=seg(x,a,bb); S=np.abs(librosa.stft(y,n_fft=2048))**2; f=librosa.fft_frequencies(sr=sr,n_fft=2048);p=S.mean(1)
        print(a,bb,nm,'>5k share %.3f  <300 %.3f'%(p[f>5000].sum()/p.sum(),p[f<300].sum()/p.sum()))
