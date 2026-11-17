import librosa, numpy as np
D='/home/user/Listener/v1/data/t_birdwalk/'; S='stems_raw/htdemucs/song/'; sr=22050
L=lambda p,o,d: librosa.load(D+p,sr=sr,offset=o,duration=d)[0]
y=L('audio/song.wav',158,24); st={k:L(S+k+'.wav',158,24) for k in ['vocals','drums','bass','other']}
def env(x,w=0.01):
    h=int(sr*w); n=len(x)//h; return 20*np.log10(np.sqrt((x[:n*h].reshape(n,h)**2).mean(1))+1e-9)
e=env(y); t=158+np.arange(len(e))*0.01
low=e<-30
# gaps in mix
i=0;print('mix gaps (<-30dB 10ms):')
while i<len(e):
    if low[i]:
        j=i
        while j<len(e) and low[j]: j+=1
        if j-i>=5: print(round(t[i],2),round(t[j-1]+.01,2),'dur',(j-i)*.01)
        i=j
    else: i+=1
# 1 s stem levels
for k,x in dict(mix=y,**st).items():
    ee=env(x,1.0); print(k,[round(float(v)) for v in ee[2:22]])
# sweep tracking in vocals 176.3-180 and mix 162-166 
for nm,x,a,b in [('vox',st['vocals'],176.5,180),('mix',y,163,165.5),('mix',y,176.8,180)]:
    seg=x[int((a-158)*sr):int((b-158)*sr)]
    S_=np.abs(librosa.stft(seg,n_fft=2048,hop_length=512)); fr=librosa.fft_frequencies(sr=sr,n_fft=2048)
    m=(fr>400)&(fr<5000)
    pk=fr[m][S_[m].argmax(0)]; print(nm,a,[int(p) for p in pk[::6]])
