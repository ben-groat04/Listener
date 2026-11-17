import numpy as np, soundfile as sf
d='data/t_dl_mirror/stems_raw/htdemucs/song/'
v,sr=sf.read(d+'vocals.wav'); v=v.mean(1) if v.ndim>1 else v
def db(a,b):
    x=v[int(a*sr):int(b*sr)]; return 20*np.log10(np.sqrt((x**2).mean())+1e-9)
for n,(a,b) in {'h1 10.4-30':(10.4,30),'v1 30-71':(30,71),'h2 71.4-91':(71.4,91),'v2 92-132':(92,132),'h3 134-154':(134,154),'v3 155-193':(155,193),'h4 195.1-215':(195.1,215)}.items(): print(n,round(db(a,b),1))
# active-frame level (frames above -40 dB), 0.1s
def act(a,b):
    x=v[int(a*sr):int(b*sr)];f=len(x)//(sr//10);x=x[:f*(sr//10)].reshape(f,-1);l=20*np.log10(np.sqrt((x**2).mean(1))+1e-9);l=l[l>-40];return round(l.mean(),1),round(len(l)/f,2)
for n,(a,b) in {'h1':(10.4,30),'h2':(71.4,91),'h3':(134,154),'h4':(195.1,215)}.items(): print(n,'active mean dB, fraction',act(a,b))
bar=0.627*4
for t in (73.15,134.0,193.8,195.09,72.15,133.3): print(t,'bar phase',round((t-10.4)%bar/bar,2))
