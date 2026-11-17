import librosa, numpy as np, sys
D='/home/user/Listener/v1/data/video2/stems_raw/htdemucs/song/'
names=['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
a,d=float(sys.argv[1]),float(sys.argv[2])
y,sr=librosa.load(D+'other.wav',sr=22050,offset=a,duration=d)
hop=256
C=np.abs(librosa.cqt(y,sr=sr,hop_length=hop,fmin=librosa.note_to_hz('C3'),n_bins=48,bins_per_octave=12))
# top note each 0.125s
step=int(0.125*sr/hop)
out=[]
for i in range(0,C.shape[1]-step,step):
    v=C[:,i:i+step].mean(1); k=v.argmax(); out.append(names[k%12]+str(3+k//12)+('' if v[k]>0.3*C.max() else '.'))
print(a,' '.join(out))
# onset times of other
oe=librosa.onset.onset_strength(y=y,sr=sr,hop_length=hop)
ac=librosa.autocorrelate(oe-oe.mean());ac/=ac[0];lags=np.arange(len(ac))*hop/sr
pk=[i for i in range(1,len(ac)-1) if 0.1<lags[i]<8 and ac[i]>ac[i-1] and ac[i]>ac[i+1]]
pk=sorted(pk,key=lambda i:-ac[i])[:5];print('other ac',[(round(lags[i],2),round(ac[i],2)) for i in pk])
