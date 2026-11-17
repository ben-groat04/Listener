import numpy as np, soundfile as sf
D='/home/user/Listener/v1/data/t_birdwalk/'
names=['mix','drums','bass','vocals','other']
paths={'mix':D+'audio/song.wav'}
for s in names[1:]: paths[s]=D+f'stems_raw/htdemucs/song/{s}.wav'
sr=44100; env={}
h=int(0.25*sr)
for n,p in paths.items():
    x,_=sf.read(p); x=x.mean(1); k=len(x)//h
    env[n]=20*np.log10(np.sqrt((x[:k*h].reshape(k,h)**2).mean(1))+1e-9)
# jumps: mean of 1s after vs 1s before (4 frames)
for n in names:
    e=env[n]; out=[]
    for i in range(4,len(e)-4):
        d=e[i:i+4].mean()-e[i-4:i].mean()
        out.append((i*0.25,d))
    # pick local extrema above threshold
    thr=8 if n!='mix' else 4
    res=[]; 
    arr=np.array([o[1] for o in out])
    for j in range(len(arr)):
        if abs(arr[j])>=thr and abs(arr[j])==np.max(np.abs(arr[max(0,j-12):j+13])):
            res.append((out[j][0],round(arr[j],1)))
    print(n,[(f'{int(t//60)}:{t%60:05.2f}',d) for t,d in res])
print('mix 1s levels 2:52-3:08')
e=env['mix']
for t in range(172,188): print(f'{t//60}:{t%60:02d}',*[f'{env[n][t*4:t*4+4].mean():6.1f}' for n in names])
