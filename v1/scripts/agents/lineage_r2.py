import numpy as np, librosa, scipy.signal as ss
D='/home/user/Listener/v1/data/t_cshells_cshore/'
def ld(p): return librosa.load(p,sr=22050,mono=True)
v,sr=ld(D+'stems_raw/htdemucs/song/vocals.wav')
m,_=ld(D+'audio/song.wav')
d,_=ld(D+'stems_raw/htdemucs/song/drums.wav')
def band(x,a,b):
    S=np.abs(np.fft.rfft(x*np.hanning(len(x))))**2;f=np.fft.rfftfreq(len(x),1/sr)
    c=np.cumsum(S);return f[np.searchsorted(c,.85*c[-1])],f[np.searchsorted(c,.95*c[-1])],10*np.log10(S.sum()/len(x)**2+1e-20)
for nm,(a,b) in {'4:27-4:32':(267,272),'2:21-2:27':(141,147),'5:30-5:42':(330,342),'3:44-3:49':(224,229)}.items():
    for s,x in (('vocals',v),('mix',m)):
        print(nm,s,'roll85/95 Hz, dB',band(x[int(a*sr):int(b*sr)],0,0))
# kick onsets 40-120Hz drum stem, IOI histogram, 2:20-5:17
sos=ss.butter(4,[40,120],'bp',fs=sr,output='sos');k=ss.sosfilt(sos,d)
for a,b in [(80,120),(140,200),(200,260),(260,317)]:
    e=librosa.onset.onset_strength(y=k[int(a*sr):int(b*sr)],sr=sr,hop_length=110)
    on=librosa.onset.onset_detect(onset_envelope=e,sr=sr,hop_length=110,units='time',delta=0.3)
    i=np.diff(on);h,_=np.histogram(i,bins=[0,.15,.3,.42,.55,.7,1.0,2]);print(a,b,len(on),'IOI hist',h)
