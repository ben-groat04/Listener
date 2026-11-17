import librosa, numpy as np, sys
D='/home/user/Listener/v1/data/video2/stems_raw/htdemucs/song/'
names=['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
def load(n): return librosa.load(D+n+'.wav',sr=22050,mono=True)
b,sr=load('bass'); o,_=load('other')
print('tuning other',librosa.estimate_tuning(y=o,sr=sr),'bass',librosa.estimate_tuning(y=b,sr=sr))
hop=512
cb=librosa.feature.chroma_cqt(y=b,sr=sr,hop_length=hop,fmin=librosa.note_to_hz('C1'),n_octaves=4)
co=librosa.feature.chroma_cqt(y=o,sr=sr,hop_length=hop)
fr=lambda t:int(t*sr/hop)
def seg(t0,t1):
    a=cb[:,fr(t0):fr(t1)].mean(1); c=co[:,fr(t0):fr(t1)].mean(1)
    ra=np.argsort(a)[::-1][:2]; rc=np.argsort(c)[::-1][:4]
    return names[ra[0]]+'(%.2f)'%(a[ra[0]]/a.sum()), ' '.join(names[i] for i in rc)
step=float(sys.argv[1]) if len(sys.argv)>1 else 4
t=0
while t<300:
    r,u=seg(t,t+step); print('%d:%02d'%(t//60,t%60),'bassroot',r,'other-top4',u); t+=step
