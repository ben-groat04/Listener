import librosa,numpy as np,sys
D='/home/user/Listener/v1/data/video2/stems_raw/htdemucs/song/'
N=['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
def chroma(y,sr,a,b,fmin=None):
    s=y[int(a*sr):int(b*sr)]
    c=librosa.feature.chroma_cqt(y=s,sr=sr,fmin=fmin or 32.7).mean(1);return c/c.max()
def show(c):return ' '.join('%s%.2f'%(N[i],c[i]) for i in np.argsort(-c)[:5])
bass,sr=librosa.load(D+'bass.wav',sr=22050,mono=True)
oth,_=librosa.load(D+'other.wav',sr=22050,mono=True)
print('BASS root per 4s (chroma top) / OTHER chroma top')
for a in list(range(0,300,4)):
    print('%d:%02d'%(a//60,a%60),'bass:',show(chroma(bass,sr,a,a+4))[:30],'| other:',show(chroma(oth,sr,a,a+4)))
