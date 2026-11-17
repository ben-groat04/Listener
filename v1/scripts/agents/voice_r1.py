import numpy as np, librosa, sys
y,sr=librosa.load('/home/user/Listener/v1/data/video1/stems_raw/htdemucs/song/vocals.wav',sr=16000)
m,_=librosa.load('/home/user/Listener/v1/data/video1/audio/song_16k_mono.wav',sr=16000)
hop=1600
r=librosa.feature.rms(y=y,frame_length=3200,hop_length=hop)[0]
rm=librosa.feature.rms(y=m,frame_length=3200,hop_length=hop)[0]
db=20*np.log10(r+1e-9); dm=20*np.log10(rm+1e-9)
# segments where vocal stem > -40 dB, 0.1s resolution
on=db>-42
seg=[];s=None
for i,o in enumerate(on):
    if o and s is None:s=i
    if not o and s is not None:
        seg.append((s,i));s=None
if s is not None: seg.append((s,len(on)))
mg=[]
for a,b in seg:
    if mg and a-mg[-1][1]<=3: mg[-1]=(mg[-1][0],b)
    else: mg.append((a,b))
for a,b in mg:
    if b-a>=3: print('%d:%04.1f-%d:%04.1f  vocdB max %.1f  mix %.1f  voc-mix %.1f'%(a//600,(a%600)/10,b//600,(b%600)/10,db[a:b].max(),dm[a:b].mean(),db[a:b].max()-dm[a:b].mean()))
