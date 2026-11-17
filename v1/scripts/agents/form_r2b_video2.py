import numpy as np, librosa, json
P='data/video2/stems_raw/htdemucs/song/'
# bar lattice test: grid 0.5 s beats; 2 s bars. Use drum-stem kick onsets to find absolute bar phase per stretch
d,sr=librosa.load(P+'drums.wav',sr=22050,mono=True)
S=np.abs(librosa.stft(d,n_fft=1024,hop_length=256))
f=librosa.fft_frequencies(sr=sr,n_fft=1024); fr=sr/256
k=S[(f>=30)&(f<150)].sum(0); k=np.maximum(np.diff(k,prepend=k[0]),0)
def phase(t0,t1,P_=2.0):
    i0,i1=int(t0*fr),int(t1*fr); t=np.arange(i0,i1)/fr
    z=(k[i0:i1]*np.exp(2j*np.pi*t/P_)).sum(); return (np.angle(z)/(2*np.pi)*P_)%P_, abs(z)/k[i0:i1].sum()
for a,b in [(30,60),(90,150),(160,215),(220,275),(280,298)]:
    ph,c=phase(a,b,0.5); print('beat phase',a,b,round(ph,3),round(c,2))
# bar phase (2 s) using kick+snare weighting: report 2s phase
for a,b in [(90,150),(160,215),(220,275),(282,298)]:
    ph,c=phase(a,b,2.0); print('bar phase 2s',a,b,round(ph,3),round(c,2))
ev={'0:28.1':28.14,'0:42.7':42.7,'1:10.0':70.0,'1:16.5':76.5,'1:24.5':84.5,'1:28.6':88.61,'1:40':100.0,'1:56.5':116.5,'2:08':128.0,'2:24':144,'2:36.5':156.5,'2:48':168.0,'3:28.7':208.7,'3:37':217.0,'4:37':277.0,'4:48.4':288.4,'5:00.86':300.86,'5:02.34':302.34}
print('event, secs from 0:00.14, bars, from 1:28.61 bars')
for n,t in ev.items(): print(n, round((t-0.14)/2,2), round((t-88.61)/2,2))
# other-stem 4-10k, 1 s resolution 2:50-4:00
o,_=librosa.load(P+'other.wav',sr=22050,mono=True)
So=np.abs(librosa.stft(o,n_fft=2048,hop_length=512))**2
fo=librosa.fft_frequencies(sr=sr,n_fft=2048); fro=sr/512
hb=10*np.log10(So[(fo>=4000)&(fo<10000)].sum(0)+1e-12)
print('other 4-10k per 4 s from 2:50')
for t in range(170,250,4): print(f'{t//60}:{t%60:02d}',round(hb[int(t*fro):int((t+4)*fro)].mean(),1))
# vocals onset first >-45 dB after 3:15 and rms around 2:30-3:40
v,_=librosa.load(P+'vocals.wav',sr=22050,mono=True)
db=20*np.log10(librosa.feature.rms(y=v,frame_length=1024,hop_length=256)[0]+1e-9)
print('vocal mean dB per 8 s 3:20-4:00')
for t in range(200,248,8): print(f'{t//60}:{t%60:02d}',round(db[int(t*fr):int((t+8)*fr)].mean(),1))
