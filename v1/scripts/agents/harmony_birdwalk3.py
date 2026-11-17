import librosa, numpy as np
D='/home/user/Listener/v1/data/t_birdwalk/stems_raw/htdemucs/song/'
names=['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
t,m=np.load('/tmp/bass_midi.npy')
# glide check: voiced runs; compare first 3 frames vs rest
runs=[];i=0
ok=np.isfinite(m)
while i<len(m):
    if ok[i]:
        j=i
        while j<len(m) and ok[j]: j+=1
        if j-i>=12 and 31<np.nanmedian(m[i:j])<36: runs.append((i,j))
        i=j
    else: i+=1
st=np.array([np.mean(m[a:a+3]) for a,b in runs]); en=np.array([np.median(m[a+4:b]) for a,b in runs])
print('runs',len(runs),'start-mean',st.mean(),'sustain median',np.median(en),'frac start>+0.5st',np.mean(st-en>0.5))
print('median run length s',np.median([(b-a)*512/22050 for a,b in runs]))
# C vs C# in other and in mix, by section with CQT energy at A-relative bins (all octaves)
for nm in ['other','vocals']:
    y,sr=librosa.load(D+nm+'.wav',sr=22050,mono=True)
    ch=librosa.feature.chroma_cqt(y=y,sr=sr,hop_length=512); tt=librosa.times_like(ch,sr=sr,hop_length=512)
    print(nm,'C/C# ratio, E, G, G# per section')
    for a,b in [(12,47),(47,60),(60,83),(92,100),(100,131),(144,155),(155,168)]:
        s=(tt>=a)&(tt<b); v=ch[:,s].mean(1)
        print(' ',a,b,'C %.2f C# %.2f E %.2f G %.2f G# %.2f F# %.2f D %.2f'%(v[0],v[1],v[4],v[7],v[8],v[6],v[2]))
# mix chroma at stab window 1:20-1:23 and 1:33-1:40
y,sr=librosa.load('/home/user/Listener/v1/data/t_birdwalk/audio/song.wav',sr=22050,mono=True)
ch=librosa.feature.chroma_cqt(y=y,sr=sr,hop_length=512); tt=librosa.times_like(ch,sr=sr,hop_length=512)
for a,b in [(80,83),(83,92),(93,100),(106,110),(119,120),(131,144),(167,170),(184,188)]:
    s=(tt>=a)&(tt<b); v=ch[:,s].mean(1); v/=v.max()
    print('mix',a,b,' '.join(f'{names[i]}:{v[i]:.2f}' for i in np.argsort(-v)[:6]))
