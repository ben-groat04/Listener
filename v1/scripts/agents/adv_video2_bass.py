import numpy as np,librosa
D='stems_raw/htdemucs/song/'
y,sr=librosa.load(D+'bass.wav',sr=22050)
C=np.abs(librosa.cqt(y,sr=sr,hop_length=512,fmin=librosa.note_to_hz('C1'),n_bins=48,bins_per_octave=12))
names=['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
fr=sr/512
def dom(a,b):
    x=C[:,int(a*fr):int(b*fr)].mean(1);pc=np.array([x[i::12].sum() for i in range(12)]);return names[pc.argmax()],round(pc.max()/pc.sum(),2)
import sys
def seq(a,b,step=2): 
    return [(round(t),)+dom(t,t+step) for t in np.arange(a,b,step)]
print('loopA',[ (t,n) for t,n,_ in seq(28.1,84.1)])
print('post-drop',[ (t,n) for t,n,_ in seq(88.6,156.6)])
print('loopB',[ (t,n) for t,n,_ in seq(156.6,204.6,2)])
# B share
def share(a,b):
    x=C[:,int(a*fr):int(b*fr)].mean(1);pc=np.array([x[i::12].sum() for i in range(12)]);return dict(zip(names,np.round(pc/pc.sum(),2)))
print('A',share(28.1,156.6));print('B',share(156.6,276.6))
print('loopB tail',[ (t,n) for t,n,_ in seq(204.6,300.6,2)])
# bass note change times (onsets of pitch-class change) around 28 and 156
def change(a,b):
    pcs=[]
    for t in np.arange(a,b,0.25):
        pcs.append((round(t,2),)+dom(t,t+0.25)[:1])
    return pcs
print(change(27,30)[:12])
# intro chroma other stem
o,_=librosa.load(D+'other.wav',sr=22050)
ch=librosa.feature.chroma_cqt(y=o[:int(30*sr)],sr=sr,hop_length=2048)
f2=sr/2048
for a in range(0,28,4):
    x=ch[:,int(a*f2):int((a+4)*f2)].mean(1);top=np.argsort(x)[::-1][:4];print(a,[(names[i],round(x[i]/x.max(),2)) for i in top])
