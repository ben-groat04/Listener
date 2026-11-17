import librosa,numpy as np
R='/home/user/Listener/v1/data/t_cshells_cshore/stems_raw/htdemucs/song/'
for s in ['bass','other']:
  for a,b in [(30,32),(65,100),(120,140),(150,180),(240,280),(300,320),(320,340)]:
    y,sr=librosa.load(R+s+'.wav',sr=22050,offset=a,duration=b-a)
    print(s,a,b,'tuning(semitones)',round(float(librosa.estimate_tuning(y=y,sr=sr)),2))
y,sr=librosa.load(R+'bass.wav',sr=22050,offset=150,duration=30)
f=librosa.yin(y,fmin=35,fmax=120,sr=sr); print('bass median f0',np.median(f), np.percentile(f,[10,90]))
y,sr=librosa.load(R+'other.wav',sr=22050,offset=325,duration=17)
S=np.abs(np.fft.rfft(y*np.hanning(len(y))));fr=np.fft.rfftfreq(len(y),1/sr)
i=np.argsort(S)[::-1]; pk=[];
for k in i:
  if all(abs(fr[k]-p)>8 for p in pk) and 50<fr[k]<1500: pk.append(fr[k])
  if len(pk)==8: break
print('other 5:25-5:42 top peaks',[round(p,1) for p in pk])
