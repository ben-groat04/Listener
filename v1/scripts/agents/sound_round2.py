import numpy as np, librosa
D='/home/user/Listener/v1/data/video1/stems_raw/htdemucs/song/'
def load(n): 
    y,sr=librosa.load(D+n+'.wav',sr=None,mono=True); return y,sr
def spec(y,sr,t0,t1):
    s=y[int(t0*sr):int(t1*sr)]
    S=np.abs(librosa.stft(s,n_fft=4096))**2; return S.mean(1),librosa.fft_frequencies(sr=sr,n_fft=4096)
def bands(y,sr,t0,t1,edges):
    p,f=spec(y,sr,t0,t1); tot=p.sum()+1e-20
    return [round(10*np.log10(p[(f>=a)&(f<b)].sum()+1e-20),1) for a,b in edges]
E=[(100,500),(500,2000),(2000,5000),(5000,8000),(8000,12000),(12000,20000)]
o,sr=load('other')
print('other band dB (100-500,500-2k,2-5k,5-8k,8-12k,12-20k)')
for a,b in [(20,30),(60,75),(80,86),(95,100),(135,145),(150,160),(170,180),(185,195)]:
    print(a,b,bands(o,sr,a,b,E))
# rolloff over time
for t in range(0,188,15):
    s=o[int(t*sr):int((t+15)*sr)]
    print(t,'rolloff99',round(float(np.mean(librosa.feature.spectral_rolloff(y=s,sr=sr,roll_percent=0.99))),0),'odd/even harm proxy n/a')
# voice segments
v,sr=load('vocals')
print('voice bands (100-500,500-2k,2-5k,5-8k,8-12k,12-20k)')
for a,b in [(10,16),(20,26),(27.9,31.7),(100,104),(135,141),(164,166)]:
    print(a,b,bands(v,sr,a,b,E))
# mix hf after 2:48 vs before
m,sr=load('drums'); 
y,sr=librosa.load('/home/user/Listener/v1/data/video1/audio/song.wav',sr=None,mono=True)
print('mix hf')
for a,b in [(100,110),(160,167),(169,178),(180,187)]:
    print(a,b,bands(y,sr,a,b,[(5000,8000),(8000,12000),(12000,16000),(16000,20000)]))
# sub glide + harmonic structure of sub
bs,sr=load('bass')
for t in [121.5,127.5,133.7,139.9]:
    s=bs[int((t)*sr):int((t+0.8)*sr)]
    f=np.fft.rfftfreq(len(s)*8,1/sr);P=np.abs(np.fft.rfft(s*np.hanning(len(s)),len(s)*8))
    k=(f>30)&(f<60); print('sub',t,round(f[k][P[k].argmax()],2))
# other 1:27 vs 1:20 by band
print('1:20-1:26',bands(o,sr,80,86,E)); print('1:28-1:34',bands(o,sr,88,94,E)); print('2:07-2:12',bands(o,sr,127,132,E)); print('2:14-2:20',bands(o,sr,134,140,E))
