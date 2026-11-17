import numpy as np, soundfile as sf, json
D='/home/user/Listener/v1/data/t_birdwalk/'
names=['mix','drums','bass','vocals','other']
paths={'mix':D+'audio/song.wav'}
for s in names[1:]: paths[s]=D+f'stems_raw/htdemucs/song/{s}.wav'
sig={};sr=None
for n,p in paths.items():
    x,sr=sf.read(p); x=x.mean(1) if x.ndim>1 else x; sig[n]=x
print(sr,len(sig['mix'])/sr)
def db(x): return 20*np.log10(np.sqrt(np.mean(x**2))+1e-9)
def lv(n,a,b): x=sig[n][int(a*sr):int(b*sr)]; return db(x)
# sample peak
m,_=sf.read(paths['mix']); print('mix sample peak dBFS',20*np.log10(np.abs(m).max()), 'rms dBFS',db(m.flatten()))
B=[12.1,24,47.3,59.4,70.4,83.4,93.8,119.5,131.4,143,156.4,120,131.4,143.4,155.7,167.3,176.5,...] if False else [12.1,47.3,59.4,70.4,83.4,93.8,120.0,131.4,143.4,155.7,167.3,176.5]
print('boundary: dB 3s before -> 3s after (mix drums bass vocals other)')
for t in B:
    row=[]
    for n in names:
        row.append(f'{n} {lv(n,t-3.5,t-0.5):6.1f}->{lv(n,t+0.5,t+3.5):6.1f}')
    print(f'{t:6.1f}',' | '.join(row))
# 5s means every 1s step 
print('per-5s levels')
for t in range(0,188,5):
    print(t//60,f'{t%60:02d}',' '.join(f'{lv(n,t,min(t+5,188.1)):6.1f}' for n in names))
# end
print('END 10ms env last 3s')
hop=int(sr*0.01)
for n in names:
    x=sig[n][-int(3*sr):]; k=len(x)//hop
    e=np.sqrt((x[:k*hop].reshape(k,hop)**2).mean(1)); ed=20*np.log10(e+1e-9)
    print(n,'last 3s: 3.0-2.0',ed[:100].mean().round(1),'2-1',ed[100:200].mean().round(1),'1-0',ed[200:].mean().round(1),'min',ed.min().round(1),'last>-60 at', (len(sig[n])/sr-3+ (np.where(ed>-60)[0].max()+1)*0.01) if (ed>-60).any() else None, 'last>-70',(len(sig[n])/sr-3+(np.where(ed>-70)[0].max()+1)*0.01) if (ed>-70).any() else None)
    if n=='mix':
        for i in range(0,300,20): print('  t',round(len(sig[n])/sr-3+i*0.01,2),ed[i:i+20].mean().round(1))
        from scipy.signal import find_peaks
        pk,_=find_peaks(ed,prominence=6); print(' peaks',[(round(len(sig[n])/sr-3+p*0.01,2),round(ed[p],1)) for p in pk])
