import numpy as np,librosa
d='data/t_birdwalk/stems_raw/htdemucs/song';sr=22050;hop=512/sr
V,_=librosa.load(f'{d}/vocals.wav',sr=sr)
M=librosa.power_to_db(librosa.feature.melspectrogram(y=V,sr=sr,n_fft=2048,hop_length=512,n_mels=64))
def seg(t,L=12.0): return M[:,int(t/hop):int((t+L)/hop)].ravel()
ref=seg(131.3);n=len(ref)
res=[]
for t in np.arange(0,176,0.25):
    s=seg(t)
    if len(s)==n: res.append((t,np.corrcoef(ref,s)[0,1]))
# local maxima >0.7
for i,(t,r) in enumerate(res):
    if r>0.7 and all(r>=res[j][1] for j in range(max(0,i-8),min(len(res),i+9))): print(f"{int(t//60)}:{t%60:05.2f} r={r:.2f}")
