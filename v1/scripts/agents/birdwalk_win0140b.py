import numpy as np, librosa, scipy.signal as sg, json
D='/home/user/Listener/v1/data/t_birdwalk/';S=D+'stems_raw/htdemucs/song/'
sr=22050
L=lambda p:librosa.load(p,sr=sr,mono=True)[0]
st={k:L(S+k+'.wav') for k in['drums','bass','vocals','other']}
mix=L(D+'audio/song.wav')
hop=int(.01*sr)
def env(y):
    n=len(y)//hop; return 20*np.log10(np.sqrt((y[:n*hop].reshape(n,hop)**2).mean(1))+1e-9)
E={k:env(v) for k,v in st.items()}; E['mix']=env(mix)
def last_above(k,a,b,th):
    e=E[k][int(a*100):int(b*100)]; i=np.where(e>th)[0]; return a+i[-1]/100 if len(i) else None
def first_above(k,a,b,th):
    e=E[k][int(a*100):int(b*100)]; i=np.where(e>th)[0]; return a+i[0]/100 if len(i) else None
print('bass last >-40 before 146',last_above('bass',140,146,-40))
print('drums last >-45 before 146',last_above('drums',140,146,-45))
print('bass first >-40 after 150',first_above('bass',150,160,-40))
print('drums first >-40 after 150',first_above('drums',150,160,-40))
print('mix 143.0-144.0 per 0.1s',np.round(E['mix'][14300:14400:10],1))
print('mix 155.4-156 per .1',np.round(E['mix'][15540:15600:10],1))
# drum hits in 140-143.5: peak picking on drum env
d=E['drums']; seg=d[14000:14500]
pk,_=sg.find_peaks(seg,height=-35,distance=8,prominence=6)
print('drum env peaks 140-145',[ (round(140+p/100,2),round(seg[p],1)) for p in pk])
seg=d[15500:16100]; pk,_=sg.find_peaks(seg,height=-32,distance=8,prominence=6)
print('drum env peaks 155-161',[ (round(155+p/100,2),round(seg[p],1)) for p in pk])
# kick band
b,a=sg.butter(4,[40/(sr/2),120/(sr/2)],'band'); kb=sg.filtfilt(b,a,st['drums'])
ke=env(kb); 
for a_,b_ in [(139,144),(155,161)]:
    seg=ke[int(a_*100):int(b_*100)]; pk,_=sg.find_peaks(seg,height=seg.max()-12,distance=8,prominence=5)
    print('kickband',[ (round(a_+p/100,2),round(seg[p],1)) for p in pk])
# bass notes in 155-161 via env peaks
seg=E['bass'][15500:16100]; pk,_=sg.find_peaks(seg,height=-25,distance=15,prominence=4)
print('bass env peaks',[ (round(155+p/100,2),round(seg[p],1)) for p in pk])
seg=E['bass'][14000:14400]; pk,_=sg.find_peaks(seg,height=-25,distance=15,prominence=4)
print('bass env peaks 140-144',[ (round(140+p/100,2),round(seg[p],1)) for p in pk])
# streak tracking: vocals stem spectral centroid 2-8k per 0.25 s 150-157
Sg=np.abs(librosa.stft(st['vocals'],n_fft=2048,hop_length=512)); fr=librosa.fft_frequencies(sr=sr,n_fft=2048)
tt=librosa.frames_to_time(np.arange(Sg.shape[1]),sr=sr,hop_length=512)
m=(fr>1500)&(fr<7000)
for t0 in np.arange(151,157,0.5):
    i=(tt>=t0)&(tt<t0+.5); x=Sg[m][:,i].mean(1); print('vocal 1.5-7k peak',t0,round(fr[m][np.argmax(x)]),'centroid',round((fr[m]*x).sum()/x.sum()))
# stereo width of whole mix: side/mid in streak
# vocal onset rate / syllables each region from vocals
# other-stem 10ms spikes
# bar-to-bar similarity of drums for loop regularity 140-143 not enough. Use vocal-stem chroma? skip
# peak true
y,_=librosa.load(D+'audio/song.wav',sr=None,mono=False)
fs=librosa.get_samplerate(D+'audio/song.wav')
a=y[:,int(140*fs):int(160*fs)]; print('fs',fs,'sample peak',20*np.log10(np.abs(a).max()))
up=sg.resample_poly(a,4,1,axis=1); print('4x true peak',20*np.log10(np.abs(up).max()))
print('whole song sample peak',20*np.log10(np.abs(y).max()))
print('frac of samples within 0.5 dB of peak 140-160',(np.abs(a)>0.94).mean())
