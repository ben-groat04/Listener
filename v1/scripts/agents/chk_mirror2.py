import numpy as np, soundfile as sf, json
d='/home/user/Listener/v1/data/t_dl_mirror/'
x,sr=sf.read(d+'audio/song.wav')
L,R=x[:,0],x[:,1]
print('corr',np.corrcoef(L,R)[0,1],'ndiff',(L!=R).sum(), 'max',np.abs(L-R).max())
i=np.where(L!=R)[0]; print(i[:10]/sr, i[-10:]/sr)
for c,a in [('L',L),('R',R)]:
  print(c,'peak',np.abs(a).max(),(np.abs(a)>=.999).sum(),'rms',20*np.log10(np.sqrt((a**2).mean())))
h=441
def env(a): n=len(a)//h; return 20*np.log10(np.sqrt((a[:n*h].reshape(n,h)**2).mean(1))+1e-10)
e=env(L)
print([round(v,1) for v in e[23640:23675]])
# clipped run
c=np.where(np.abs(L)>=.999)[0]; 
print('clip run near 177.4',[ (v/sr) for v in c if 177<v/sr<178][:3],sum(1 for v in c if 177.4<v/sr<177.6))
# mutes near 10.62 and 177.54
for t in [10.62,177.54]:
  seg=L[int((t-.1)*sr):int((t+.1)*sr)]; e1=20*np.log10(np.abs(seg).reshape(-1,44).max(1)+1e-9)
  k=np.where(e1<-50)[0]; print(t,'mute ms',k[:3]*1.0,k[-3:], len(k))
# per-second levels
j=json.load(open(d+'music_views/per_second_levels.json')); print(type(j), list(j)[:5] if isinstance(j,dict) else j[:2])
