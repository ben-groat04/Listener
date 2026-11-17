import numpy as np, librosa, json, scipy.signal as sg
d='/home/user/Listener/v1/data/t_cshells_cshore/'
sr=22050
mix,_=librosa.load(d+'audio/song.wav',sr=None,mono=False,offset=160,duration=20)
print('peak 160-180 lin',np.abs(mix).max(),'n samples>=0.99',(np.abs(mix)>=0.99).sum())
mm,_=librosa.load(d+'audio/song.wav',sr=sr,offset=160,duration=20)
def band(y,lo,hi):
    b=sg.butter(4,[lo/(sr/2),hi/(sr/2)],'band',output='sos');return sg.sosfiltfilt(b,y)
S={n:librosa.load(d+'stems_raw/htdemucs/song/%s.wav'%n,sr=sr,offset=160,duration=20)[0] for n in['drums','bass','other','vocals']}
S['mix']=mm
for n,y in S.items():
    for lo,hi in[(30,200),(200,2000),(2000,5000),(5000,10000)]:
        z=band(y,lo,hi);r=[20*np.log10(np.sqrt(np.mean(z[i*sr:(i+1)*sr]**2))+1e-9) for i in range(20)]
        print(n,lo,hi,' '.join('%.0f'%v for v in r))
# kick grid: low-band drums, peaks of 10ms envelope
z=band(S['drums'],40,120);e=np.sqrt(np.convolve(z**2,np.ones(220)/220,'same'))
pk,_=sg.find_peaks(e,height=e.max()*0.35,distance=int(0.15*sr))
t=pk/sr+160;print('kicks',np.round(t,2));ioi=np.diff(t);print('ioi med',np.median(ioi),'std',ioi.std())
bt=np.array(json.load(open(d+'audio_features/beat_times.json')));b=bt[(bt>=160)&(bt<180)];print('beat ioi',np.median(np.diff(b)),60/np.median(np.diff(b)))
# kick distance to nearest beat-grid 8th
g=np.median(np.diff(b))/2
dev=[(x-b[0]+g/2)%g-g/2 for x in t];print('dev from 8th grid ms std',np.std(dev)*1000)
# loop regularity: bass-env autocorr
env=librosa.feature.rms(y=S['bass'],frame_length=2048,hop_length=512)[0];
ac=np.correlate(env-env.mean(),env-env.mean(),'full')[len(env)-1:];ac/=ac[0]
fps=sr/512
for bars in[1,2,4]:
    lag=int(round(bars*4*60/123*fps));print('bass env autocorr lag',bars,'bar',ac[lag-2:lag+3].max())
