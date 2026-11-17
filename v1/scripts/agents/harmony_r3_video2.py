import librosa,numpy as np,sys
y,sr=librosa.load('data/video2/stems_raw/htdemucs/song/bass.wav',sr=11025,mono=True)
n=['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
def root(a,b):
    s=y[int(a*sr):int(b*sr)]
    if len(s)<2048: return None
    c=librosa.feature.chroma_cqt(y=s,sr=sr,fmin=32.7,n_octaves=3).mean(1)
    i=int(np.argmax(c)); return n[i],round(float(c[i]/c.sum()),2)
for a,b in [(float(x),float(x)+0.5) for x in np.arange(1070/10,1300/10,0.5)] if False else []: pass
for t in np.arange(72,92,0.75): print(round(t,2),root(t,t+0.75))
print('--- loop B cycle starts, 2s slices late')
for t in [4676,4680,4684,4688,4690,4692]: 
    t/=1; print(t/1 if False else t, end=' ')
print()
for t in np.arange(280,292,1.0): print(t,root(t,t+1.0))
