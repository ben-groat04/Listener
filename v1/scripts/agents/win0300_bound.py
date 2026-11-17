import numpy as np, librosa
D='/home/user/Listener/v1/data/t_cshells_cshore/'
sr=22050
ks=['drums','bass','vocals','other']
S={k:librosa.load(D+f'stems_raw/htdemucs/song/{k}.wav',sr=sr,mono=True,offset=296,duration=30)[0] for k in ks}
M=librosa.load(D+'audio/song.wav',sr=sr,mono=True,offset=296,duration=30)[0]
def r(y,a,b): s=y[int((a-296)*sr):int((b-296)*sr)]; return 20*np.log10(np.sqrt((s**2).mean())+1e-9)
for name,t in [('bass dip',300.0),('bass return',304.0),('other drop',307.0),('other back',310.0),('voice1',312.3),('voice2',316.8),('drum stop',318.0),('bass 12.5-13',312.5)]:
    print(name,t)
    for k in ks+['mix']:
        y=M if k=='mix' else S[k]
        print('  ',k,[round(r(y,t+d,t+d+0.5),1) for d in (-2,-1.5,-1,-0.5,0,0.5,1,1.5,2)])
# centroid of other per 2 s
for a in range(298,322,2):
    s=S['other'][int((a-296)*sr):int((a+2-296)*sr)]
    print(a,'other centroid',round(float(librosa.feature.spectral_centroid(y=s,sr=sr).mean())),'mix',round(float(librosa.feature.spectral_centroid(y=M[int((a-296)*sr):int((a+2-296)*sr)],sr=sr).mean())))
# end of drums: 10ms env 316.5-320
d=S['drums'];e=np.sqrt(np.convolve(d**2,np.ones(220)/220,'same'))
for a in np.arange(317.0,319.6,0.1): print(round(a,1),round(20*np.log10(e[int((a-296)*sr):int((a+.1-296)*sr)].max()+1e-9),1),end=' | ')
print()
# loop regularity: autocorr of drum onset env at bar lag
env=librosa.onset.onset_strength(y=d[int(4*sr):int(24*sr)],sr=sr,hop_length=256)
env=env-env.mean();ac=np.correlate(env,env,'full')[len(env)-1:];ac/=ac[0]
lag=256/sr
for L in [0.488,0.976,1.95,3.9,7.8]:
    i=int(round(L/lag));print('lag',L,'ac',round(float(ac[i-3:i+4].max()),2))
# a/b windows corr
a=env[:int(len(env)/2)];print('half corr',np.corrcoef(env[:len(env)//2],env[len(env)//2:2*(len(env)//2)])[0,1])
