import numpy as np, librosa, sys
D='/home/user/Listener/v1/data/video2/'
sr=22050
def L(p,mono=True):
    y,_=librosa.load(p,sr=sr,mono=mono); return y
oth=L(D+'stems_raw/htdemucs/song/other.wav',False)
bas=L(D+'stems_raw/htdemucs/song/bass.wav')
dr=L(D+'stems_raw/htdemucs/song/drums.wav')
mix=L(D+'audio/song.wav',False)
def seg(y,a,b): return y[...,int(a*sr):int(b*sr)]
def db(x): return 20*np.log10(np.sqrt(np.mean(x**2))+1e-9)
# 1. other stem spectral bands and width over time
def bands(y,a,b):
    m=seg(y,a,b); m=m.mean(0) if m.ndim>1 else m
    S=np.abs(np.fft.rfft(m*np.hanning(len(m))))**2; f=np.fft.rfftfreq(len(m),1/sr)
    out=[]
    for lo,hi in [(60,250),(250,1000),(1000,4000),(4000,10000)]:
        out.append(10*np.log10(S[(f>=lo)&(f<hi)].sum()+1e-12))
    return out,m
print('other stem band dB (60-250,250-1k,1-4k,4-10k)')
for a in [2*60+10,2*60+40,2*60+44,2*60+52,3*60,3*60+30,3*60+50,4*60+10]:
    b,_=bands(oth,a,a+6); print(a,[round(x,1) for x in b])
# side/mid of other & mix
for a in [60+20,60+26,60+28,60+31,60+40,2*60+30,3*60+40]:
    for nm,y in [('oth',oth),('mix',mix)]:
        s=seg(y,a,a+4); M=(s[0]+s[1])/2; S=(s[0]-s[1])/2
        print(a,nm,'S/M dB',round(db(S)-db(M),1),'corr',round(np.corrcoef(s[0],s[1])[0,1],2))
# 2. 2:46-2:52 jump
rms=lambda y,a,b: db(seg(y.mean(0) if y.ndim>1 else y,a,b))
print('other 0.5s rms 2:44-2:52',[round(rms(oth,t,t+.5),1) for t in np.arange(164,172,.5)])
# 3. odd/even harmonic: spectral flatness and HF noise at onsets for other stem
for a in [100,200,260]:
    m=seg(oth,a,a+10).mean(0)
    print(a,'flatness',round(float(np.mean(librosa.feature.spectral_flatness(y=m))),4),'centroid',round(float(np.mean(librosa.feature.spectral_centroid(y=m,sr=sr))),0), 'onset str mean',round(float(np.mean(librosa.onset.onset_strength(y=m,sr=sr))),2))
# other onset spacing 3:00-3:40
m=seg(oth,180,220).mean(0)
oe=librosa.onset.onset_strength(y=m,sr=sr,hop_length=128)
ac=librosa.autocorrelate(oe-oe.mean()); ac/=ac[0]
lag=np.arange(len(ac))*128/sr
for t in [0.125,0.25,0.375,0.5,1.0,2.0]:
    i=np.argmin(abs(lag-t)); print('other onset ac lag',t,round(ac[max(0,i-2):i+3].max(),2))
# bass onsets 3:00-3:40
m=seg(bas,180,220)
oe=librosa.onset.onset_strength(y=m,sr=sr,hop_length=128); ac=librosa.autocorrelate(oe-oe.mean()); ac/=ac[0]
for t in [0.125,0.25,0.375,0.5,1.0,2.0]:
    i=np.argmin(abs(lag[:len(ac)]-t)); print('bass onset ac lag',t,round(ac[max(0,i-2):i+3].max(),2))
# bass harmonic: ratio of 2nd/3rd harmonic energy above fundamental
m=seg(bas,200,206); S=np.abs(np.fft.rfft(m*np.hanning(len(m)))); f=np.fft.rfftfreq(len(m),1/sr)
print('bass 200-206: <150 Hz vs 150-1k vs 1k-4k dB',[round(20*np.log10(S[(f>=lo)&(f<hi)].sum()+1e-9),1) for lo,hi in [(30,150),(150,1000),(1000,4000)]])
# 4. ending
e=mix.mean(0)
print('mix 0.1s rms 5:00-5:06')
print([round(db(seg(e,t,t+.1)),0) for t in np.arange(300,306,.2)])
fin=seg(e,302.2,302.8)
print('final hit peak sample', float(np.abs(seg(e,302,303)).max()))
# onset sharpness of final hit: rise time
env=np.abs(seg(e,302.0,303.2)); 
i=np.argmax(env>0.5*env.max()); print('time of 50% peak',302+i/sr)
