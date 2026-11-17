import numpy as np, soundfile as sf
D='/home/user/Listener/v1/data/t_birdwalk/';sr=44100
S={n:sf.read(D+f'stems_raw/htdemucs/song/{n}.wav')[0].mean(1) for n in ['vocals','drums','bass','other']}
S['mix']=sf.read(D+'audio/song.wav')[0].mean(1)
db=lambda x:round(20*np.log10(np.sqrt(np.mean(x**2))+1e-9),1)
for t in [166.9,167.0,167.3,169.9,176.4,176.5]:
    print(t,{k:(db(v[int((t-.4)*sr):int(t*sr)]),db(v[int(t*sr):int((t+.4)*sr)])) for k,v in S.items()})
for a,b in [(160,167),(167,170),(170,176.4),(176.5,180)]: print(a,b,{k:db(v[int(a*sr):int(b*sr)]) for k,v in S.items()})
