import numpy as np, soundfile as sf
d='data/t_cshells_cshore/'
def env(p):
    x,sr=sf.read(p); x=x.mean(1) if x.ndim>1 else x
    h=int(sr*.01); n=len(x)//h
    return 20*np.log10(np.sqrt((x[:n*h].reshape(n,h)**2).mean(1))+1e-10),sr,len(x)/sr
e,sr,dur=env(d+'audio/song.wav')
print('dur',dur,'peak dBFS',20*np.log10(abs(sf.read(d+'audio/song.wav')[0]).max()))
last=np.where(e>-90)[0][-1]; print('last env>-90 at',last*.01, e[last])
t=e[-300:]; print('last3s peaks>-60:',sum(1 for i in range(1,299) if t[i]>t[i-1] and t[i]>=t[i+1] and t[i]>-60))
for a,b in [(3,3.1),(5.35,5.4),(5.41,5.425)]: pass
# mix level (1s RMS dB) around boundaries
for t0 in [187,200,205,224,251,276,286,287,317,330,340,342]:
    s=e[int(t0*100):int((t0+1)*100)]; print(t0, round(10*np.log10((10**(s/10)).mean()),1))
dr,_,_=env('stems_raw/htdemucs/song/drums.wav') if False else (None,0,0)
