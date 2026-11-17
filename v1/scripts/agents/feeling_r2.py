import json,numpy as np,librosa
d=json.load(open('/home/user/Listener/v1/data/video1/music_views/per_second_levels.json'))
db=np.array([x['dbfs'] for x in d]);w=np.array([x['width'] for x in d])
i=np.argsort(db)[::-1][:8];print('loudest s',[(int(d[k]['t']),db[k]) for k in i])
for a,b in [(0,9),(9,32),(32,50),(50,75),(75,87),(87,100),(100,115),(115,121),(121,133),(133,158),(158,168),(168,188)]:
    print(a,b,'mix %.1f width %.2f'%(db[a:b].mean(),w[a:b].mean()))
# spectral: hiss >8k fraction & hf per window; mix mono
y,sr=librosa.load('/home/user/Listener/v1/data/video1/audio/song.wav',sr=22050,mono=True)
S=np.abs(librosa.stft(y,n_fft=2048))**2;f=librosa.fft_frequencies(sr=sr,n_fft=2048)
for a,b in [(20,30),(60,70),(88,98),(125,135),(150,160),(170,180),(185,188)]:
    s=S[:,int(a*sr/512):int(b*sr/512)].sum(1)
    print(a,'frac>5k %.4f >8k %.5f centroid %.0f'%(s[f>5000].sum()/s.sum(),s[f>8000].sum()/s.sum(),(s*f).sum()/s.sum()))
