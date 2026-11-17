import numpy as np, librosa, json
D='/home/user/Listener/v1/data/video1/stems_raw/htdemucs/song/'
sr=22050
def load(n): return librosa.load(D+n+'.wav',sr=sr,mono=True)[0]
dr=load('drums'); mix=librosa.load('/home/user/Listener/v1/data/video1/audio/song.wav',sr=sr,mono=True)[0]
hop=441
def rms(y): return 20*np.log10(librosa.feature.rms(y=y,frame_length=1024,hop_length=hop)[0]+1e-9)
rd=rms(dr); rm=rms(mix); t=np.arange(len(rd)+2)*hop/sr
print('mix dips (below -20 dB, local 10ms):')
low=rm<-20; i=0
while i<len(low):
    if low[i]:
        j=i
        while j<len(low) and low[j]: j+=1
        if (j-i)>=18: print(f'  {t[i]:.2f}-{t[j]:.2f}s ({(j-i)*0.01:.2f}s) mix min {rm[i:j].min():.0f} drums {rd[i:j].mean():.0f}')
        i=j
    else: i+=1
# drum dips lasting >=0.12s below median-12
th=np.median(rd)-14; low=rd<th; i=0; print('drum stem dips (median-14 dB):',np.median(rd))
while i<len(low):
    if low[i]:
        j=i
        while j<len(low) and low[j]: j+=1
        if (j-i)>=8: print(f'  {t[i]:.2f}-{t[j]:.2f}s')
        i=j
    else: i+=1
# 16th-grid regularity: drum onset intervals histogram
o=librosa.onset.onset_detect(y=dr,sr=sr,hop_length=256,units='time',backtrack=False)
ioi=np.diff(o); h,e=np.histogram(ioi,bins=np.arange(0.05,1.0,0.02)); 
print('IOI modes:',[(round(e[k],2),int(h[k])) for k in np.argsort(h)[::-1][:6]])
# local tempo over time: tempogram argmax in 78 vs 156 band per 20s
oenv=librosa.onset.onset_strength(y=dr,sr=sr,hop_length=256)
for a in range(0,180,20):
    seg=oenv[int(a*sr/256):int((a+20)*sr/256)]
    ac=librosa.autocorrelate(seg-seg.mean()); ac/=ac[0]; lag=np.arange(len(ac))*256/sr
    m=(lag>0.3)&(lag<1.7); k=np.argmax(ac[m]); 
    print(a,'strongest periodicity',round(lag[m][k],3),'s =',round(60/lag[m][k],1),'bpm; ac@0.383',round(ac[np.argmin(abs(lag-0.383))],2),'@0.766',round(ac[np.argmin(abs(lag-0.766))],2),'@1.533',round(ac[np.argmin(abs(lag-1.533))],2),'@3.07',round(ac[np.argmin(abs(lag-3.07))],2) if len(ac)>0 else '')
