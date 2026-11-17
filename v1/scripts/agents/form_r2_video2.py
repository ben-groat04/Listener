import numpy as np, librosa, json
P='data/video2/stems_raw/htdemucs/song/'
# bar counts on 2.0 s bars: old lattice 0:28+2n, new lattice 88.6+2n
ev={'0:28':28.0,'0:42.7':42.7,'1:04':64,'1:28.6':88.6,'1:41':100.6,'2:36.8':156.8,'3:24.8':204.8,'3:36.8':216.8,'4:36.8':276.8,'4:48.8':288.8,'5:00.6':300.6}
for k,v in ev.items():
    print(k, 'bars from 0:28:',round((v-28)/2,2),' bars from 1:28.6:',round((v-88.6)/2,2))
print('2:36.8->3:24.8 bars',(204.8-156.8)/2, ' 3:24.8->3:36.8',6, ' 3:36.8->4:36.8',(276.8-216.8)/2, ' 4:36.8->5:00.6',(300.6-276.8)/2)
print('1:28.6->2:36.8 bars',(156.8-88.6)/2,' 0:28->1:28.6',(88.6-28)/2)
# other-stem top band (3-10k) and 250-1k at 1 s res, 3:10-3:50
y,sr=librosa.load(P+'other.wav',sr=22050,mono=True)
S=np.abs(librosa.stft(y,n_fft=2048,hop_length=512))**2
f=librosa.fft_frequencies(sr=sr,n_fft=2048); fr=sr/512
def band(lo,hi):
    return 10*np.log10(S[(f>=lo)&(f<hi)].sum(0)+1e-12)
hb=band(3000,10000); mb=band(250,1000)
def at(t0,t1,b): return b[int(t0*fr):int(t1*fr)].mean()
print('t  top3-10k  mid250-1k (other, 2 s means)')
for t in range(196,226,2): print(f'{t//60}:{t%60:02d}',round(at(t,t+2,hb),1),round(at(t,t+2,mb),1))
# cycle-start steps: mean in 12 s cycles
print('cycle means (top band)')
for s in np.arange(156.8,300,12): print(f'{int(s)//60}:{s%60:04.1f}',round(at(s,s+12,hb),1),round(at(s,s+12,mb),1))
# voice onset 3:15-3:35
v,_=librosa.load(P+'vocals.wav',sr=22050,mono=True)
rms=librosa.feature.rms(y=v,frame_length=1024,hop_length=256)[0]; db=20*np.log10(rms+1e-9); fr2=sr/256
for i in range(int(200*fr2),int(212*fr2)):
    if db[i]>-45 and db[i-1]<=-45: print('voice on',round(i/fr2,2), round(db[i],1))
